from decimal import Decimal
from pydantic import BaseModel

class BudgetCreate(BaseModel):
    category: str
    monthly_limit: Decimal

class BudgetResponse(BudgetCreate):
    id: int

    class Config:
        from_attributes = True

class BudgetStatus(BaseModel):
    category: str
    monthly_limit: Decimal
    spent: Decimal
    remaining: Decimal
    percentage_used: float