"""Loan schemas."""

from datetime import date, datetime

from pydantic import Field

from app.models.enums import LoanStatus, LoanType
from app.schemas.common import BaseSchema


class LoanCreate(BaseSchema):
    name: str = Field(min_length=1, max_length=255)
    loan_type: LoanType
    principal_amount: float = Field(gt=0)
    outstanding_balance: float = Field(gt=0)
    interest_rate: float = Field(ge=0)
    tenure_months: int = Field(gt=0)
    emi_amount: float = Field(gt=0)
    start_date: date
    lender: str | None = None
    notes: str | None = None


class LoanUpdate(BaseSchema):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    outstanding_balance: float | None = Field(default=None, ge=0)
    interest_rate: float | None = Field(default=None, ge=0)
    tenure_months: int | None = Field(default=None, gt=0)
    emi_amount: float | None = Field(default=None, gt=0)
    status: LoanStatus | None = None
    lender: str | None = None
    notes: str | None = None


class LoanResponse(BaseSchema):
    id: int
    user_id: int
    name: str
    loan_type: LoanType
    principal_amount: float
    outstanding_balance: float
    interest_rate: float
    tenure_months: int
    emi_amount: float
    start_date: date
    lender: str | None
    status: LoanStatus
    notes: str | None
    created_at: datetime
    updated_at: datetime
