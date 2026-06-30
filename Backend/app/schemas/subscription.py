"""Subscription schemas."""

from datetime import date, datetime

from pydantic import Field

from app.models.enums import ExpenseCategory, SubscriptionFrequency, SubscriptionStatus
from app.schemas.common import BaseSchema


class SubscriptionCreate(BaseSchema):
    name: str = Field(min_length=1, max_length=255)
    amount: float = Field(gt=0)
    frequency: SubscriptionFrequency
    category: ExpenseCategory = ExpenseCategory.SUBSCRIPTION
    start_date: date
    next_billing_date: date | None = None
    provider: str | None = None


class SubscriptionUpdate(BaseSchema):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    amount: float | None = Field(default=None, gt=0)
    frequency: SubscriptionFrequency | None = None
    category: ExpenseCategory | None = None
    status: SubscriptionStatus | None = None
    next_billing_date: date | None = None
    provider: str | None = None


class SubscriptionResponse(BaseSchema):
    id: int
    user_id: int
    name: str
    amount: float
    frequency: SubscriptionFrequency
    category: ExpenseCategory
    status: SubscriptionStatus
    start_date: date
    next_billing_date: date | None
    provider: str | None
    monthly_equivalent: float = 0
    created_at: datetime
    updated_at: datetime
