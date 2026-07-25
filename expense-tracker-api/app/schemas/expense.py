import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.category import CategoryRead


class ExpenseCreate(BaseModel):
    description: str = Field(min_length=1, max_length=255)
    amount: Decimal = Field(gt=0, decimal_places=2)
    expense_date: date
    category_id: uuid.UUID | None = None


class ExpenseUpdate(BaseModel):
    description: str | None = Field(default=None, min_length=1, max_length=255)
    amount: Decimal | None = Field(default=None, gt=0, decimal_places=2)
    expense_date: date | None = None
    category_id: uuid.UUID | None = None


class ExpenseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    description: str
    amount: Decimal
    expense_date: date
    category: CategoryRead | None = None
    created_at: datetime


class MonthlySummary(BaseModel):
    year: int
    month: int
    total: Decimal
    by_category: dict[str, Decimal]
