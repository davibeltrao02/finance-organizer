from abc import ABC, abstractmethod
from sqlalchemy.orm import Session


class BaseHandler(ABC):

    @abstractmethod
    def handle(self, text: str, chat_id: int, db: Session) -> str:
        """Processa a mensagem e retorna a resposta para o usuário."""
        ...
