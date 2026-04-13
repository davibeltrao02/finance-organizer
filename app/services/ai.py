import json
import os
from typing import Optional, Tuple, List
from datetime import date
from dotenv import load_dotenv
from groq import Groq
from app.schemas.transaction import TransactionExtracted

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

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

Toda resposta deve seguir estritamente esse formato JSON, sem texto adicional. Se a mensagem do usuário não for sobre uma transação financeira, responda com um JSON indicando que não é uma transação.
Como preciso parsar a resposta da IA, é fundamental que o formato seja sempre o mesmo, sem variações.

Para transaction_date:
- Se o usuário mencionar "hoje", use a data de hoje
- Se mencionar "ontem", use a data de ontem
- Se mencionar um dia específico, calcule a data correta
- Se não mencionar data, use a data de hoje

Categorias possíveis para expense: alimentação, transporte, moradia, saúde, lazer, educação, vestuário, outros
Categorias possíveis para income: salário, freelance, investimentos, presente, outros

Se a mensagem NÃO for sobre uma transação financeira, responda com o JSON:
{{"not_a_transaction": true, "reply": "sua resposta amigável aqui"}}

Exemplos:
- "gastei 45 reais no almoço ontem" → {{"description": "Almoço", "amount": 45.0, "type": "expense", "category": "alimentação", "transaction_date": "2026-04-10"}}
- "recebi meu salário de 3000 reais" → {{"description": "Salário", "amount": 3000.0, "type": "income", "category": "salário", "transaction_date": "{date.today().isoformat()}"}}
- "como estão meus gastos?" → {{"not_a_transaction": true, "reply": "Para ver seus gastos, acesse o dashboard!"}}
"""


def process_message(
    message: str,
    history: List[dict],
) -> Tuple[str, Optional[TransactionExtracted]]:
    """
    Envia a mensagem do usuário para o Groq com o histórico da conversa e retorna:
    - reply: resposta em texto para o usuário
    - transaction: dados extraídos da transação (ou None se não for transação)

    O histórico é convertido de formato Gemini para Groq.
    """
    # Converte histórico de formato Gemini (com "parts") para Groq (com "content")
    groq_history = []
    for msg in history:
        role = msg.get("role")
        # Se é formato Gemini (tem "parts"), pega o primeiro elemento
        content = msg.get("parts", [None])[0] if "parts" in msg else msg.get("content", "")
        # Mapeia "model" para "assistant" (Groq usa "assistant" em vez de "model")
        if role == "model":
            role = "assistant"
        groq_history.append({"role": role, "content": content})

    # Adiciona a mensagem atual
    groq_history.append({"role": "user", "content": message})

    # Envia para Groq
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=groq_history,
        temperature=0.7,
    )

    print("Resposta bruta do Groq:", response)

    # Limpa o texto da resposta (remove markdown code blocks se houver)
    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    data = json.loads(raw.strip())

    if data.get("not_a_transaction"):
        return data.get("reply", "Entendido!"), None

    transaction = TransactionExtracted(**data)
    amount_fmt = f"R$ {transaction.amount:.2f}"
    type_label = "receita" if transaction.type == "income" else "despesa"
    reply = (
        f"Registrei uma {type_label} de {amount_fmt} "
        f"em {transaction.category}: {transaction.description}."
    )
    return reply, transaction
