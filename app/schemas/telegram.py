from pydantic import BaseModel
from typing import Optional

class TelegramChat(BaseModel):
    id: int

class TelegramMessage(BaseModel):
    chat: TelegramChat
    text: str

class TelegramPayload(BaseModel):
    message: TelegramMessage