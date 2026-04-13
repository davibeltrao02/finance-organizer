from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from app.database import get_db
from app.models.transaction import Transaction, TransactionType

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
def get_by_category(db: Session = Depends(get_db)):
    """Retorna o total gasto por categoria (apenas despesas)."""
    rows = (
        db.query(Transaction.category, func.sum(Transaction.amount).label("total"))
        .filter(Transaction.type == TransactionType.expense)
        .group_by(Transaction.category)
        .order_by(func.sum(Transaction.amount).desc())
        .all()
    )
    return [{"category": row.category, "total": round(row.total, 2)} for row in rows]


@router.get("/monthly")
def get_monthly(year: int, month: int, db: Session = Depends(get_db)):
    """
    Retorna receitas, despesas e saldo de um mês específico.
    Exemplo: /summary/monthly?year=2026&month=4
    """
    start = date(year, month, 1)
    # Calcula o primeiro dia do mês seguinte para usar como limite
    if month == 12:
        end = date(year + 1, 1, 1)
    else:
        end = date(year, month + 1, 1)

    base_query = db.query(func.sum(Transaction.amount)).filter(
        Transaction.transaction_date >= start,
        Transaction.transaction_date < end,
    )

    total_income = base_query.filter(
        Transaction.type == TransactionType.income
    ).scalar() or 0.0

    total_expense = base_query.filter(
        Transaction.type == TransactionType.expense
    ).scalar() or 0.0

    return {
        "year": year,
        "month": month,
        "total_income": round(total_income, 2),
        "total_expense": round(total_expense, 2),
        "balance": round(total_income - total_expense, 2),
    }
