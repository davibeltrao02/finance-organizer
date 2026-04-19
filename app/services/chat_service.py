from sqlalchemy.orm import Session
from app.models.chat_message import ChatMessage
# from app.services.ai import SYSTEM_PROMPT

from app.models.transaction import Transaction
from datetime import date, datetime
    

HISTORY_LIMIT = 10


# def load_history(db: Session) -> list:
#     """
#     Busca as últimas mensagens do banco e converte para o formato
#     que o Groq espera: lista de dicts com "role" e "content".
#     """
#     messages = (
#         db.query(ChatMessage)
#         .order_by(ChatMessage.created_at.desc())
#         .limit(HISTORY_LIMIT)
#         .all()
#     )
#     history = [
#         {"role": msg.role, "content": msg.content}
#         for msg in reversed(messages)
#     ]
#     system_turn = [
#         {"role": "user", "content": "Instruções do sistema: " + SYSTEM_PROMPT},
#         {"role": "assistant", "content": "Entendido! Estou pronto para registrar suas transações financeiras."},
#     ]
#     return system_turn + history


def save_message(db: Session, role: str, content: str):
    """Salva uma mensagem no histórico do banco."""
    db.add(ChatMessage(role=role, content=content))
    db.commit()
