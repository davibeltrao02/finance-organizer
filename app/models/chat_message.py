from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, nullable=False)   # "user" ou "model"
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
