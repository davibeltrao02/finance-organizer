import os
import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.integrations.telegram import TelegramMessager
from app.schemas.telegram import TelegramPayload
from app.services.intent_service import get_chat_intent
from app.handlers import INTENT_HANDLERS

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhook", tags=["webhook"])

bot = TelegramMessager(bot_token=os.getenv("TELEGRAM_BOT_TOKEN", ""))

ALLOWED_CHAT_IDS = [
    int(i) for i in os.getenv("TELEGRAM_ALLOWED_CHAT_IDS", "0").split(";") if i
]


@router.post("/telegram", response_model=dict)
def receive_telegram_message(payload: TelegramPayload, db: Session = Depends(get_db)):
    chat_id = payload.message.chat.id
    text = payload.message.text

    if not text or chat_id not in ALLOWED_CHAT_IDS:
        return {"ok": True}

    intent = get_chat_intent(chat_id, text, db)
    logger.info(f"Intent detectado: {intent}")

    handler = INTENT_HANDLERS.get(intent, INTENT_HANDLERS["unknown"])
    reply = handler.handle(text, chat_id, db)

    bot.send_message(to=chat_id, text=reply)
    return {"ok": True}
