from datetime import date
from sqlalchemy.orm import Session
from app.handlers.base import BaseHandler
from app.services.summary_service import get_monthly_summary


class SummaryHandler(BaseHandler):

    def handle(self, text: str, chat_id: int, db: Session) -> str:
        today = date.today()
        summary = get_monthly_summary(today.year, today.month, db)
        return (
            f"Seu resumo para {today.strftime('%B/%Y')}:\n"
            f"Receitas: R$ {summary['total_income']}\n"
            f"Despesas: R$ {summary['total_expense']}\n"
            f"Saldo: R$ {summary['balance']}"
        )
