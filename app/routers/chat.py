from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.transaction import ChatMessage, ChatResponse, TransactionResponse
from app.models.transaction import Transaction
from app.models.chat_message import ChatMessage as ChatMessageModel
from app.services.ai import process_message, SYSTEM_PROMPT

router = APIRouter(prefix="/chat", tags=["chat"])

# Quantas mensagens anteriores enviar ao Gemini como contexto
HISTORY_LIMIT = 10


def _load_history(db: Session) -> list:
    """
    Busca as últimas mensagens do banco e converte para o formato
    que o Gemini espera: lista de dicts com "role" e "parts".
    """
    messages = (
        db.query(ChatMessageModel)
        .order_by(ChatMessageModel.created_at.desc())
        .limit(HISTORY_LIMIT)
        .all()
    )
    # Reverte para ordem cronológica e monta o formato do Gemini
    history = [
        {"role": msg.role, "parts": [msg.content]}
        for msg in reversed(messages)
    ]
    # Injeta o system prompt como primeira mensagem do modelo
    system_turn = [
        {"role": "user", "parts": ["Instruções do sistema: " + SYSTEM_PROMPT]},
        {"role": "model", "parts": ["Entendido! Estou pronto para registrar suas transações financeiras."]},
    ]
    return system_turn + history


def _save_message(db: Session, role: str, content: str):
    """Salva uma mensagem no histórico do banco."""
    db.add(ChatMessageModel(role=role, content=content))
    db.commit()


@router.post("/", response_model=ChatResponse)
def chat(message: ChatMessage, db: Session = Depends(get_db)):
    """
    Recebe uma mensagem em linguagem natural, processa com IA (com histórico)
    e salva a transação no banco se identificada.
    """
    history = _load_history(db)

    reply, extracted = process_message(message.message, history)

    # Salva a troca no histórico
    _save_message(db, "user", message.message)
    _save_message(db, "model", reply)

    if extracted is None:
        return ChatResponse(reply=reply)

    # Salva a transação no banco
    transaction = Transaction(
        description=extracted.description,
        amount=extracted.amount,
        type=extracted.type,
        category=extracted.category,
        transaction_date=extracted.transaction_date,
        raw_message=message.message,
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return ChatResponse(
        reply=reply,
        transaction=TransactionResponse.model_validate(transaction),
    )


@router.get("/history", response_model=list)
def get_history(db: Session = Depends(get_db)):
    """Retorna o histórico completo de mensagens."""
    messages = (
        db.query(ChatMessageModel)
        .order_by(ChatMessageModel.created_at.asc())
        .all()
    )
    return [{"role": m.role, "content": m.content, "created_at": m.created_at} for m in messages]
