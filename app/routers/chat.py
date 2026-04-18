from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.transaction import ChatMessage, ChatResponse, TransactionResponse
from app.models.transaction import Transaction
from app.models.chat_message import ChatMessage as ChatMessageModel
from app.services.ai import process_message
from app.services.chat_service import load_history, save_message

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
def chat(message: ChatMessage, db: Session = Depends(get_db)):
    """
    Recebe uma mensagem em linguagem natural, processa com IA (com histórico)
    e salva a transação no banco se identificada.
    """
    history = load_history(db)

    reply, extracted = process_message(message.message, history)

    # Salva a troca no histórico
    save_message(db, "user", message.message)
    save_message(db, "assistant", reply)

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
