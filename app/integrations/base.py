from abc import ABC, abstractmethod
from typing import Any

class MessagingPlatform(ABC):

    @abstractmethod
    def parse_message(self, payload: dict) -> str:
        """Extrai o texto da mensagem recebida do webhook"""
        ...

    @abstractmethod
    def send_message(self, to: Any, text: str) -> None:
        """Envia uma resposta para o usuário"""
        ...