from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionResponse, TransactionUpdate
from fastapi import HTTPException
from fastapi import Response, status

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
        raise HTTPException(status_code=404, detail="Transação não encontrada")

    db.delete(transaction)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{transaction_id}")
def update_transaction(transaction_id: int, transaction_data: TransactionUpdate, db: Session = Depends(get_db)):
    """Atualiza uma transação pelo ID."""
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transação não encontrada")

    for key, value in transaction_data.model_dump(exclude_unset=True).items():
        setattr(transaction, key, value)

    db.commit()
    db.refresh(transaction)
    return {"message": "Transação atualizada com sucesso"}
