from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database.models import Transaction


def get_transactions(
    db: Session,
    user_id: int
):
    return (
        db.query(Transaction)
        .filter(Transaction.user_id == user_id)
        .order_by(
            Transaction.transaction_date.desc(),
            Transaction.created_at.desc()
        )
        .all()
    )