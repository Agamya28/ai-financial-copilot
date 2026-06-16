from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.models import User
from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.analytics import AnalyticsSummary, CategorySpending, MonthlySpending, AdvancedAnalytics
from app.services.analytics import get_summary, get_category_breakdown, get_monthly_breakdown, get_advanced_analytics
from app.services.insights import generate_insights

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

@router.get("/summary", response_model=AnalyticsSummary)
def get_analytics_summary(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_summary(
        db=db,
        user_id=current_user.id
    )

@router.get("/category_breakdown", response_model=list[CategorySpending])
def get_category_breakdown_route(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_category_breakdown(
        db=db,
        user_id=current_user.id
    )

@router.get(
    "/monthly-spending",
    response_model=list[MonthlySpending]
)
def get_monthly_spending_route(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_monthly_breakdown(
        db=db,
        user_id=current_user.id
    )

@router.get(
    "/advanced",
    response_model=AdvancedAnalytics
)
def get_advanced_analytics_route(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_advanced_analytics(
        db=db,
        user_id=current_user.id
    )

@router.get("/insights")
def get_insights(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return generate_insights(
        db=db,
        user_id=current_user.id
    )