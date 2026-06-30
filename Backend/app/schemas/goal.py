"""Goal schemas."""

from datetime import date, datetime

from pydantic import Field

from app.models.enums import GoalStatus, GoalType
from app.schemas.common import BaseSchema


class GoalCreate(BaseSchema):
    name: str = Field(min_length=1, max_length=255)
    goal_type: GoalType
    target_amount: float = Field(gt=0)
    current_amount: float = Field(default=0, ge=0)
    target_date: date | None = None
    description: str | None = None
    monthly_contribution: float | None = Field(default=None, ge=0)


class GoalUpdate(BaseSchema):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    goal_type: GoalType | None = None
    target_amount: float | None = Field(default=None, gt=0)
    current_amount: float | None = Field(default=None, ge=0)
    target_date: date | None = None
    status: GoalStatus | None = None
    description: str | None = None
    monthly_contribution: float | None = Field(default=None, ge=0)


class GoalResponse(BaseSchema):
    id: int
    user_id: int
    name: str
    goal_type: GoalType
    target_amount: float
    current_amount: float
    target_date: date | None
    status: GoalStatus
    description: str | None
    monthly_contribution: float | None
    progress_percent: float = 0
    created_at: datetime
    updated_at: datetime
