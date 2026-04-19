from sqlalchemy.orm import Session
from app.models.chat_message import ChatMessage

HISTORY_LIMIT = 20


def load_history(chat_id: int, db: Session) -> list:
    """
    Busca as últimas mensagens do banco e converte para o formato
    que o Groq espera: lista de dicts com "role" e "content".
    """
    messages = (
        db.query(ChatMessage)
        .filter(ChatMessage.chat_id == chat_id)
        .order_by(ChatMessage.created_at.desc())
        .limit(HISTORY_LIMIT)
        .all()
    )
    history = [{"role": msg.role, "content": msg.content} for msg in reversed(messages)]
    return history


def save_message(db: Session, role: str, content: str, chat_id: int):
    db.add(ChatMessage(role=role, content=content, chat_id=chat_id))
    delete_old_messages(db, chat_id)
    db.commit()


def delete_old_messages(db: Session, chat_id: int):
    subquery = (
        db.query(ChatMessage.id)
        .filter(ChatMessage.chat_id == chat_id)
        .order_by(ChatMessage.created_at.desc())
        .offset(HISTORY_LIMIT)
        .subquery()
        .as_scalar()
    )
    db.query(ChatMessage).filter(ChatMessage.id.in_(subquery)).delete(
        synchronize_session=False
    )
