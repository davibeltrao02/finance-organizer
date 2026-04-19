import os
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.integrations.telegram import TelegramMessager
from app.models.transaction import Transaction
from app.schemas.telegram import TelegramPayload

from app.services.ai import process_message
from app.services.chat_service import load_history, save_message

router = APIRouter(prefix="/webhook", tags=["webhook"])

bot = TelegramMessager(bot_token=os.getenv("TELEGRAM_BOT_TOKEN", ""))

@router.post("/telegram", response_model=dict)
def receive_telegram_message(payload: TelegramPayload, db: Session = Depends(get_db)):
    chat_id = payload.message.chat.id
    text = payload.message.text

    if not text:
        return {"ok": True}

    if chat_id not in [int(allowed) for allowed in os.getenv("TELEGRAM_ALLOWED_CHAT_IDS", "0").split(";") if allowed]:
        return {"ok": True}

    history = load_history(db)
    reply, extracted = process_message(text, history)

    # Salva a troca no histórico
    save_message(db, "user", text)
    save_message(db, "assistant", reply)

    if extracted is None:
        bot.send_message(to=chat_id, text=reply)
        return {"ok": True}

    transaction = Transaction(
        description=extracted.description,
        amount=extracted.amount,
        type=extracted.type,
        category=extracted.category,
        transaction_date=extracted.transaction_date,
        raw_message=text,
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    bot.send_message(to=chat_id, text=reply)
    return {"ok": True}
