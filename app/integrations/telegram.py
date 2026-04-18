import requests
from app.integrations.base import MessagingPlatform

class TelegramMessager(MessagingPlatform):

    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

    def parse_message(self, payload: dict) -> str:
        return payload.get("message", {}).get("text", "")

    def send_message(self, to: int, text: str) -> None:
        requests.post(self.url, json={"chat_id": to, "text": text})