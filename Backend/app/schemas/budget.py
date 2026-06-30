"""Budget schemas."""

from datetime import date, datetime

from pydantic import Field

from app.models.enums import BudgetPeriod, ExpenseCategory
from app.schemas.common import BaseSchema


class BudgetCreate(BaseSchema):
    category: ExpenseCategory
    amount: float = Field(gt=0)
    period: BudgetPeriod
    start_date: date
    end_date: date | None = None
    name: str | None = None
    alert_threshold: float | None = Field(default=None, ge=0, le=100)


class BudgetUpdate(BaseSchema):
    category: ExpenseCategory | None = None
    amount: float | None = Field(default=None, gt=0)
    period: BudgetPeriod | None = None
    start_date: date | None = None
    end_date: date | None = None
    name: str | None = None
    alert_threshold: float | None = Field(default=None, ge=0, le=100)


class BudgetResponse(BaseSchema):
    id: int
    user_id: int
    category: ExpenseCategory
    amount: float
    period: BudgetPeriod
    start_date: date
    end_date: date | None
    name: str | None
    alert_threshold: float | None
    created_at: datetime
    updated_at: datetime


class BudgetStatusResponse(BaseSchema):
    budget: BudgetResponse
    spent: float
    remaining: float
    utilization_percent: float
    is_over_budget: bool
