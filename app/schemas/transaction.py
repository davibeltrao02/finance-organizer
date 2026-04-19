from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional
from app.models.transaction import TransactionType


# Schema que a IA retorna após processar a mensagem
class TransactionExtracted(BaseModel):
    description: str
    amount: float
    type: TransactionType
    category: str
    transaction_date: date


# Schema para criar uma transação via API diretamente
class TransactionCreate(TransactionExtracted):
    raw_message: Optional[str] = None


# Schema de resposta da API (inclui id e data)
class TransactionResponse(TransactionCreate):
    id: int
    transaction_date: date
    created_at: datetime

    class Config:
        from_attributes = True


class TransactionUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None
    type: Optional[TransactionType] = None
    category: Optional[str] = None
    transaction_date: Optional[date] = None


# Schema para receber a mensagem do chat
class ChatMessage(BaseModel):
    message: str


# Schema de resposta do chat
class ChatResponse(BaseModel):
    reply: str
    transaction: Optional[TransactionResponse] = None
