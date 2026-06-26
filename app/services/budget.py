from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from fastapi import HTTPException

from app.database.models import Budget, Transaction
from app.schemas.budget import BudgetCreate, BudgetStatus


def create_budget(
    db: Session,
    user_id: int,
    budget: BudgetCreate
):

    existing_budget = (
        db.query(Budget)
        .filter(
            Budget.user_id == user_id,
            func.lower(Budget.category)
            == budget.category.lower()
        )
        .first()
    )

    if existing_budget:
        raise HTTPException(
            status_code=400,
            detail=(
                "A budget already exists "
                "for this category."
            )
        )

    new_budget = Budget(
        user_id=user_id,
        category=budget.category.lower(),
        monthly_limit=budget.monthly_limit
    )

    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)

    return new_budget

def get_budgets(
    db: Session,
    user_id: int
):
    return (
        db.query(Budget)
        .filter(Budget.user_id == user_id)
        .all()
    )

def get_budget_status(
    db: Session,
    user_id: int
) -> list[BudgetStatus]:

    budgets = (
        db.query(Budget)
        .filter(Budget.user_id == user_id)
        .all()
    )

    results = []

    today = date.today()

    for budget in budgets:

        spent = (
            db.query(func.sum(Transaction.amount))
            .filter(
                Transaction.user_id == user_id,
                func.lower(Transaction.category)
                == budget.category,
                func.extract(
                    "month",
                    Transaction.transaction_date
                ) == today.month,
                func.extract(
                    "year",
                    Transaction.transaction_date
                ) == today.year
            )
            .scalar()
        ) or 0

        remaining = budget.monthly_limit - spent
        if budget.monthly_limit>0:
            percentage_used = (
                float(spent)
                / float(budget.monthly_limit)
            ) * 100
        else:
            percentage_used=0
        results.append(
            BudgetStatus(
                category=budget.category,
                monthly_limit=budget.monthly_limit,
                spent=spent,
                remaining=remaining,
                percentage_used=round(
                    percentage_used,
                    2
                )
            )
        )

    return results
