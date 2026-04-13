from sqlalchemy import Column, Integer, String, Float, DateTime, Date, Enum
from sqlalchemy.sql import func
import enum
from app.database import Base


class TransactionType(str, enum.Enum):
    income = "income"    # receita
    expense = "expense"  # despesa


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    category = Column(String, nullable=False)
    raw_message = Column(String)                          # mensagem original do usuário
    transaction_date = Column(Date, nullable=False, server_default=func.current_date())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
