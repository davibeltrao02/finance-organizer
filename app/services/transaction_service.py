import json
import re

from sqlalchemy.orm import Session

from typing import Optional, Tuple
from datetime import date
from dotenv import load_dotenv
from app.schemas.transaction import TransactionExtracted
from app.services.ai import call_groq
from app.models.transaction import Transaction
from app.services.chat_service import load_history
from app.constants.categories import EXPENSE_CATEGORIES, INCOME_CATEGORIES

load_dotenv()

SYSTEM_PROMPT = f"""
Você é um assistente de gestão financeira pessoal.
A data de hoje é {date.today().isoformat()}.

Quando o usuário enviar uma mensagem descrevendo uma transação financeira, extraia as informações e responda APENAS com um JSON válido no seguinte formato:

{{
  "description": "descrição curta da transação",
  "amount": 0.0,
  "type": "expense" ou "income",
  "category": "categoria",
  "transaction_date": "YYYY-MM-DD"
}}

Toda resposta deve seguir estritamente esse formato JSON, sem texto adicional.
Como preciso parsar a resposta da IA, é fundamental que o formato seja sempre o mesmo, sem variações.

Para transaction_date:
- Se o usuário mencionar "hoje", use a data de hoje
- Se mencionar "ontem", use a data de ontem
- Se mencionar um dia específico, calcule a data correta
- Se não mencionar data, use a data de hoje

Categorias possíveis para expense: {", ".join(EXPENSE_CATEGORIES)}
Categorias possíveis para income: {", ".join(INCOME_CATEGORIES)}

Se a mensagem NÃO for sobre uma transação financeira, responda com o JSON:
{{"not_a_transaction": true, "reply": "sua resposta amigável aqui"}}

Exemplos:
- "gastei 45 reais no almoço ontem" → {{"description": "Almoço", "amount": 45.0, "type": "expense", "category": "alimentação", "transaction_date": "2026-04-10"}}
- "recebi meu salário de 3000 reais" → {{"description": "Salário", "amount": 3000.0, "type": "income", "category": "salário", "transaction_date": "{date.today().isoformat()}"}}
- "como estão meus gastos?" → {{"not_a_transaction": true, "reply": "Para ver seus gastos, acesse o dashboard!"}}
"""


def parse_transaction(
    chat_id: int,
    message: str,
    db: Session
) -> Tuple[str, Optional[TransactionExtracted]]:
    """
    Envia a mensagem do usuário para o Groq com o histórico da conversa e retorna:
    - reply: resposta em texto para o usuário
    - transaction: dados extraídos da transação (ou None se não for transação)

    O histórico é convertido de formato Gemini para Groq.
    """
    groq_message = []
    groq_message.append({"role": "system", "content": SYSTEM_PROMPT})
    groq_message.append({"role": "user", "content": message})

    history_messages = load_history(chat_id, db)  # Carrega histórico do chat (ajuste conforme necessário)
    groq_message = history_messages + groq_message  

    response = call_groq(groq_message)

    print("Resposta bruta do Groq:", response)

    # Extrai JSON da resposta — o modelo às vezes adiciona texto antes/depois
    match = re.search(r'\{.*\}', response, re.DOTALL)
    if not match:
        return "Não entendi. Pode tentar novamente?", None

    data = json.loads(match.group())

    if "not_a_transaction" in data and data["not_a_transaction"]:
        return data.get("reply", "Entendi, mas não é uma transação."), None

    transaction = TransactionExtracted(**data)
    amount_fmt = f"R$ {transaction.amount:.2f}"
    type_label = "receita" if transaction.type == "income" else "despesa"
    reply = (
        f"Registrei uma {type_label} de {amount_fmt} "
        f"em {transaction.category}: {transaction.description}."
    )
    return reply, transaction

def save_transaction(db, transaction: TransactionExtracted, raw_message: str):
    db_transaction = Transaction(
        description=transaction.description,
        amount=transaction.amount,
        type=transaction.type,
        category=transaction.category,
        transaction_date=transaction.transaction_date,
        raw_message=raw_message,
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction