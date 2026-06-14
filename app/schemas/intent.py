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
    UNKNOWN = "unknown"


class IntentResult(BaseModel):
    intent: Intent
    parameters: dict[str, Any] = Field(default_factory=dict)