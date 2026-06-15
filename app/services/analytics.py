from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional

from app.database.models import Transaction
from app.schemas.analytics import AnalyticsSummary, CategorySpending, MonthlySpending, TopCategory, CategoryPercentage, MonthlyInsight, AdvancedAnalytics

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

def get_top_category(
    db: Session,
    user_id: int
) -> Optional[TopCategory]:
    result = (
    db.query(
        Transaction.category,
        func.sum(Transaction.amount).label("total_spending")
    )
    .filter(Transaction.user_id == user_id)
    .group_by(Transaction.category)
    .order_by(func.sum(Transaction.amount).desc())
    .first()
)   
    if not result:
        return None
    return TopCategory(
    category=result.category,
    total_spending=result.total_spending
)

def get_highest_spending_month(
        db: Session,
        user_id: int
) -> Optional[MonthlyInsight]:
    month_expr = func.to_char(
    Transaction.transaction_date,
    "YYYY-MM"
)
    result = (
    db.query(
        month_expr.label("month"),
        func.sum(Transaction.amount).label("total_spending")
    )
    .filter(Transaction.user_id == user_id)
    .group_by(month_expr)
    .order_by(func.sum(Transaction.amount).desc())
    .first()
)
    if not result:
        return None
    return MonthlyInsight(
    month=result.month,
    total_spending=result.total_spending
)

def get_lowest_spending_month(
        db: Session,
        user_id: int
) -> Optional[MonthlyInsight]:
    month_expr = func.to_char(
    Transaction.transaction_date,
    "YYYY-MM"
)
    result = (
    db.query(
        month_expr.label("month"),
        func.sum(Transaction.amount).label("total_spending")
    )
    .filter(Transaction.user_id == user_id)
    .group_by(month_expr)
    .order_by(func.sum(Transaction.amount).asc())
    .first()
)
    if not result:
        return None
    return MonthlyInsight(
    month=result.month,
    total_spending=result.total_spending
)


def get_category_percentages(
    db: Session,
    user_id: int
) -> list[CategoryPercentage]:
    summary = get_summary(
    db=db,
    user_id=user_id
)
    if summary.total_spending == 0:
        return []
    breakdown = get_category_breakdown(
        db=db,
        user_id=user_id
    )
    percentages = []

    for item in breakdown:

        percentage = (
            float(item.total_spending)
            / float(summary.total_spending)
        ) * 100

        percentages.append(
            CategoryPercentage(
                category=item.category,
                total_spending=item.total_spending,
                percentage=round(percentage, 2)
            )
        )
    return percentages

def get_advanced_analytics(
    db: Session,
    user_id: int
) -> AdvancedAnalytics:
    top_category=get_top_category(
        db=db,
        user_id=user_id
    )
    highest_spending_month=get_highest_spending_month(
        db=db,
        user_id=user_id
    )
    lowest_spending_month=get_lowest_spending_month(
        db=db,
        user_id=user_id
    )
    category_percentages=get_category_percentages(
        db=db,
        user_id=user_id
    )
    return AdvancedAnalytics(
        top_category=top_category,
        highest_spending_month=highest_spending_month,
        lowest_spending_month=lowest_spending_month,
        category_percentages=category_percentages
    )