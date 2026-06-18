from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Intent(str, Enum):
    TOTAL_SPENDING = "total_spending"
    LARGEST_EXPENSE = "largest_expense"
    AVERAGE_TRANSACTION = "average_transaction"
    TRANSACTION_COUNT = "transaction_count"
    CATEGORY_SPENDING = "category_spending"
    MONTHLY_SPENDING = "monthly_spending"
    SPENDING_SUMMARY = "spending_summary"
    TOP_CATEGORY = "top_category"
    HIGHEST_SPENDING_MONTH = "highest_spending_month"
    LOWEST_SPENDING_MONTH = "lowest_spending_month"
    CATEGORY_PERCENTAGES = "category_percentages"
    BUDGET_ANALYSIS="budget_analysis"
    UNKNOWN = "unknown"


class IntentResult(BaseModel):
    intent: Intent
    parameters: dict[str, Any] = Field(default_factory=dict)