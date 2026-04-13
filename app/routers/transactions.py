from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionResponse

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("/", response_model=list[TransactionResponse])
def list_transactions(db: Session = Depends(get_db)):
    """Retorna todas as transações salvas."""
    return db.query(Transaction).order_by(Transaction.created_at.desc()).all()  # type: ignore


@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Remove uma transação pelo ID."""
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        return {"error": "Transação não encontrada"}
    db.delete(transaction)
    db.commit()
    return {"message": "Transação removida com sucesso"}
