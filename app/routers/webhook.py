from datetime import date
import os
import logging
from fastapi import APIRouter, Depends

logger = logging.getLogger(__name__)
from sqlalchemy.orm import Session
from app.database import get_db
from app.integrations.telegram import TelegramMessager
from app.schemas.telegram import TelegramPayload

from app.services.intent_service import get_chat_intent
from app.services.transaction_service import parse_transaction, save_transaction
from app.services.summary_service import get_monthly_summary

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

    intent = get_chat_intent(text)
    
    logger.info(f"Intent: {intent}")

    if intent == "transaction":
        reply, extracted = parse_transaction(text)
        if extracted is not None:
            save_transaction(db, extracted, text)
    elif intent == "summary":
        today = date.today()
        summary = get_monthly_summary(today.year, today.month, db)
        reply = f"Seu resumo para {today.strftime('%B/%Y')}: Receitas: {summary['total_income']} reais, Despesas: {summary['total_expense']} reais, Saldo: {summary['balance']} reais."
    else:
        reply = "Desculpe, não consegui entender sua mensagem. Por favor, tente reformular ou seja mais específico sobre o que deseja."
        
    bot.send_message(to=chat_id, text=reply)
    return {"ok": True}
