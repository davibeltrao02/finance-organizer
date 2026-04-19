from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from app.database import get_db
from app.models.transaction import Transaction, TransactionType
from app.services.summary_service import get_monthly_summary, get_category_monthly_expenses

router = APIRouter(prefix="/summary", tags=["summary"])


@router.get("/balance")
def get_balance(db: Session = Depends(get_db)):
    """Retorna o saldo atual: total de receitas menos total de despesas."""
    total_income = db.query(func.sum(Transaction.amount)).filter(
        Transaction.type == TransactionType.income
    ).scalar() or 0.0

    total_expense = db.query(func.sum(Transaction.amount)).filter(
        Transaction.type == TransactionType.expense
    ).scalar() or 0.0

    return {
        "total_income": round(total_income, 2),
        "total_expense": round(total_expense, 2),
        "balance": round(total_income - total_expense, 2),
    }


@router.get("/by-category")
def get_by_category(year: int, month: int, db: Session = Depends(get_db)):
    return get_category_monthly_expenses(year, month, db)


@router.get("/monthly")
def get_monthly(year: int, month: int, db: Session = Depends(get_db)):
    """
    Retorna receitas, despesas e saldo de um mês específico.
    Exemplo: /summary/monthly?year=2026&month=4
    """
    return get_monthly_summary(year, month, db)
    