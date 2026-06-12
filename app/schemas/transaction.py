from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel


class TransactionCreate(BaseModel):
    amount: Decimal
    category: str
    merchant: str
    description: str | None = None
    transaction_date: date


class TransactionResponse(BaseModel):
    id: int
    amount: Decimal
    category: str
    merchant: str
    description: str | None = None
    transaction_date: date
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True