from sqlalchemy.orm import Session
from app.handlers.base import BaseHandler
from app.services.chat_service import save_message
from app.services.transaction_service import parse_transaction, save_transaction


class TransactionHandler(BaseHandler):

    def handle(self, text: str, chat_id: int, db: Session) -> str:
        reply, extracted = parse_transaction(chat_id, text, db)
        if extracted is not None:
            save_transaction(db, extracted, text)
        save_message(db, role="user", content=text, chat_id=chat_id)
        save_message(db, role="assistant", content=reply, chat_id=chat_id)
        return reply
