from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.transaction import (
    TransactionCreate,
    TransactionResponse
)
from app.crud.transaction import (
    create_transaction,
    get_transactions,
    delete_transaction
)

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)

@router.post("/", response_model=TransactionResponse)
def create_transaction_route(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):
    return create_transaction(db, transaction)

@router.get("/", response_model=list[TransactionResponse])
def get_transactions_route(
    db: Session = Depends(get_db)
):
    return get_transactions(db)

@router.delete("/{transaction_id}")
def delete_transaction_route(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    transaction = delete_transaction(db, transaction_id)

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return {"message": "Transaction deleted"}