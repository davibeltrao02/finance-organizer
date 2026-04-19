from sqlalchemy.orm import Session
from app.handlers.base import BaseHandler


class UnknownHandler(BaseHandler):

    def handle(self, text: str, chat_id: int, db: Session) -> str:
        return "Desculpe, não consegui entender. Tente descrever uma transação ou perguntar sobre seu saldo."
