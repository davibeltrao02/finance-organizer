from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from app.models.transaction import Transaction, TransactionType

def get_monthly_summary(year: int, month:int, db: Session):
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


def get_category_monthly_expenses(year: int, month: int, db: Session):
    start = date(year, month, 1)
    # Calcula o primeiro dia do mês seguinte para usar como limite
    if month == 12:
        end = date(year + 1, 1, 1)
    else:
        end = date(year, month + 1, 1)

    rows = (
        db.query(Transaction.category, func.sum(Transaction.amount).label("total"))
        .filter(Transaction.transaction_date >= start, Transaction.transaction_date < end)
        .filter(Transaction.type == TransactionType.expense)
        .group_by(Transaction.category)
        .order_by(func.sum(Transaction.amount).desc())
        .all()
    )
    return [{"category": row.category, "total": round(row.total, 2)} for row in rows]