from sqlalchemy.orm import Session

from app.database.models import Transaction
from app.schemas.transaction import TransactionCreate


def create_transaction(db: Session, transaction: TransactionCreate, user_id: int):
    db_transaction = Transaction(
        amount=transaction.amount,
        category=transaction.category,
        merchant=transaction.merchant,
        description=transaction.description,
        transaction_date=transaction.transaction_date,
        user_id=user_id
    )

    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    return db_transaction

def get_transactions(db: Session, user_id: int)-> list[Transaction]:
    return db.query(Transaction).filter(Transaction.user_id==user_id).all()

def delete_transaction(db: Session, transaction_id: int, user_id: int):
    transaction = (
        db.query(Transaction)
        .filter(
            Transaction.id == transaction_id , 
            Transaction.user_id ==user_id
            )
        .first()
    )

    if transaction is None:
        return None

    db.delete(transaction)
    db.commit()

    return transaction