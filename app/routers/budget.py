from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.budget import BudgetCreate, BudgetResponse, BudgetStatus
from app.services.budget import create_budget, get_budgets, get_budget_status

router = APIRouter(
    prefix="/budget",
    tags=["Budget"]
)

@router.post("/", response_model=BudgetResponse)
def create_budget_route(
    budget: BudgetCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return create_budget(
    db=db,
    user_id=current_user.id,
    budget=budget
    )

@router.get("/", response_model=list[BudgetResponse])
def get_budgets_route(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_budgets(
        db=db,
        user_id=current_user.id
    )

@router.get(
    "/status",
    response_model=list[BudgetStatus]
)
def get_budget_status_route(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_budget_status(
        db=db,
        user_id=current_user.id
    )