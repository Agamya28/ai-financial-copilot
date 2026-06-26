from sqlalchemy.orm import Session

from app.services.analytics import (
    get_summary,
    get_category_breakdown,
    get_monthly_breakdown,
    get_top_category,
    get_highest_spending_month,
    get_lowest_spending_month,
)

from app.services.budget import get_budget_status


def build_financial_context(db: Session, user_id: int):

    try:
        summary = get_summary(db, user_id)
    except Exception:
        summary = None

    try:
        categories = get_category_breakdown(db, user_id)
    except Exception:
        categories = []

    try:
        monthly = get_monthly_breakdown(db, user_id)
    except Exception:
        monthly = []

    try:
        budgets = get_budget_status(db, user_id)
    except Exception:
        budgets = []

    try:
        top_category = get_top_category(db, user_id)
    except Exception:
        top_category = None

    try:
        highest_month = get_highest_spending_month(
            db,
            user_id
        )
    except Exception:
        highest_month = None

    try:
        lowest_month = get_lowest_spending_month(
            db,
            user_id
        )
    except Exception:
        lowest_month = None

    category_text = "\n".join(
        [
            f"{item.category}: ₹{item.total_spending}"
            for item in categories
        ]
    )

    monthly_text = "\n".join(
        [
            f"{item.month}: ₹{item.total_spending}"
            for item in monthly
        ]
    )

    budget_text = "\n".join(
        [
            f"""
Category: {item.category}
Budget: ₹{item.monthly_limit}
Spent: ₹{item.spent}
Remaining: ₹{item.remaining}
Usage: {item.percentage_used}%
"""
            for item in budgets
        ]
    )

    return {
        "summary": f"""
Total Spending: ₹{summary.total_spending if summary else 0}
Transaction Count: {summary.transaction_count if summary else 0}
Average Transaction: ₹{summary.average_transaction if summary else 0}
Largest Expense: ₹{summary.largest_expense if summary else 0}
""",

        "category_breakdown": category_text,

        "monthly_spending": monthly_text,

        "budget_status": budget_text,

        "insights": f"""
Top Category:
{top_category.category if top_category else "N/A"}

Highest Spending Month:
{highest_month.month if highest_month else "N/A"}

Lowest Spending Month:
{lowest_month.month if lowest_month else "N/A"}
"""
    }