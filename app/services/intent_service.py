from sqlalchemy.orm import Session

from app.services.ai import call_groq
from app.services.chat_service import load_history

INTENT_PROMPT = """
    Você é um assistente de gestão financeira pessoal. Analise a mensagem do usuário e responda APENAS com a intenção detectada, sem texto adicional. As intenções possíveis são:
    - "transaction"
        - Responsável por mensagens que descrevem uma transação financeira (ex: "gastei 50 reais no almoço ontem", "recebi meu salário de 3000 reais")
    - "summary"
        - Para mensagens que solicitam um resumo financeiro, balanço ou análise de gastos (ex: "como estão meus gastos?", "qual meu saldo atual?", "me mostre um resumo do mês")
    - "unknown"
        - Para mensagens que não se encaixam nas categorias acima ou são irrelevantes para gestão financeira (ex: "qual é a capital da França?", "me conte uma piada")
"""

def get_chat_intent(chat_id: int, message: str, db: Session) -> str:
    intent = __get_chat_intent_rules(message)
    if intent != "unknown":
        return intent
    return __get_chat_intent_groq(chat_id, message, db)

def __get_chat_intent_groq(
    chat_id: int,
    message: str,
    db: Session
) -> str:
    """
    Analisa a mensagem do usuário usando o Groq e retorna a intenção detectada.
    Exemplo de intenções: "transaction", "summary", "unknown"
    """

    history_messages = load_history(chat_id, db)

    groq_message = [{"role": "system", "content": INTENT_PROMPT}] + [{"role": "user", "content": message}]
    groq_message = history_messages + groq_message
    response = call_groq(groq_message)
    return response.strip().lower()

def __get_chat_intent_rules(
    message: str,
) -> str:
    
    text = message.lower()
    if any(word in text for word in ["adicionar", "registrar", "inserir"]):
        return "transaction"
    elif any(word in text for word in ["resumo", "balanço", "saldo"]):
        return "summary"
    else:
        return "unknown"