from decimal import Decimal
from pydantic import BaseModel

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