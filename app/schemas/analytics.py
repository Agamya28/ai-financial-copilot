from decimal import Decimal
from pydantic import BaseModel
from typing import Optional

class AnalyticsSummary(BaseModel):
    total_spending: Decimal
    transaction_count: int
    average_transaction: Decimal
    largest_expense: Decimal

class CategorySpending(BaseModel):
    category: str
    total_spending: Decimal

class MonthlySpending(BaseModel):
    month: str
    total_spending: Decimal

class TopCategory(BaseModel):
    category: str
    total_spending: Decimal

class CategoryPercentage(BaseModel):
    category: str
    total_spending: Decimal
    percentage: float

class MonthlyInsight(BaseModel):
    month: str
    total_spending: Decimal

class AdvancedAnalytics(BaseModel):
    top_category: Optional[TopCategory]
    highest_spending_month: Optional[MonthlyInsight]
    lowest_spending_month: Optional[MonthlyInsight]
    category_percentages: list[CategoryPercentage]

class SpendingForecast(BaseModel):
    current_spending: Decimal
    forecast: Decimal

class BudgetRecommendation(BaseModel):
    category: str
    message: str