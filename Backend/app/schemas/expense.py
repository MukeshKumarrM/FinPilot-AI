"""Expense schemas."""

from datetime import date, datetime

from pydantic import Field

from app.models.enums import ExpenseCategory
from app.schemas.common import BaseSchema


class ExpenseCreate(BaseSchema):
    amount: float = Field(gt=0)
    category: ExpenseCategory
    description: str | None = None
    merchant: str | None = None
    expense_date: date
    payment_method: str | None = None
    tags: str | None = None
    receipt_id: int | None = None


class ExpenseUpdate(BaseSchema):
    amount: float | None = Field(default=None, gt=0)
    category: ExpenseCategory | None = None
    description: str | None = None
    merchant: str | None = None
    expense_date: date | None = None
    payment_method: str | None = None
    tags: str | None = None


class ExpenseResponse(BaseSchema):
    id: int
    user_id: int
    amount: float
    category: ExpenseCategory
    description: str | None
    merchant: str | None
    expense_date: date
    payment_method: str | None
    tags: str | None
    receipt_id: int | None
    created_at: datetime
    updated_at: datetime


class ExpenseSummary(BaseSchema):
    total: float
    count: int
    by_category: dict[str, float]
