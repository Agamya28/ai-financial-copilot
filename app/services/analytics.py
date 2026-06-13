from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.models import Transaction
from app.schemas.analytics import AnalyticsSummary, CategorySpending, MonthlySpending

def get_summary(
    db: Session,
    user_id: int
) -> AnalyticsSummary:

    result = (
        db.query(
            func.sum(Transaction.amount),
            func.count(Transaction.id),
            func.avg(Transaction.amount),
            func.max(Transaction.amount)
        )
        .filter(Transaction.user_id == user_id)
        .first()
    )

    total_spending, transaction_count, average_transaction, largest_expense = result

    return AnalyticsSummary(
        total_spending=total_spending or Decimal("0"),
        transaction_count=transaction_count or 0,
        average_transaction=average_transaction or Decimal("0"),
        largest_expense=largest_expense or Decimal("0")
    )

def get_category_breakdown(
    db: Session,
    user_id: int
) -> list[CategorySpending]:
    result = (
        db.query(
            Transaction.category,
            func.sum(Transaction.amount)
        )
        .filter(Transaction.user_id == user_id).group_by(Transaction.category)
        .all()
    )
    breakdown = []

    for category, total_spending in result:
        breakdown.append(
            CategorySpending(
                category=category,
                total_spending=total_spending
            )
        )

    return breakdown

def get_monthly_breakdown(
        db: Session,
        user_id: int
) -> list[MonthlySpending]:
    month_expr = func.to_char(
    Transaction.transaction_date,
    "YYYY-MM"
)
    result = (
    db.query(
        month_expr,
        func.sum(Transaction.amount)
    )
    .filter(Transaction.user_id == user_id)
    .group_by(month_expr)
    .order_by(month_expr)
    .all()
)
    return [
    MonthlySpending(
        month=month,
        total_spending=total_spending
    )
    for month, total_spending in result
]