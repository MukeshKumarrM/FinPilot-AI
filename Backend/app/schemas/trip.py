"""Trip schemas."""

from datetime import date, datetime

from pydantic import Field

from app.models.enums import TripStatus
from app.schemas.common import BaseSchema


class TripCreate(BaseSchema):
    name: str = Field(min_length=1, max_length=255)
    destination: str = Field(min_length=1, max_length=255)
    start_date: date
    end_date: date
    budget: float = Field(gt=0)
    travelers_count: int = Field(default=1, ge=1)
    notes: str | None = None
    itinerary: str | None = None


class TripUpdate(BaseSchema):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    destination: str | None = Field(default=None, min_length=1, max_length=255)
    start_date: date | None = None
    end_date: date | None = None
    budget: float | None = Field(default=None, gt=0)
    spent_amount: float | None = Field(default=None, ge=0)
    status: TripStatus | None = None
    travelers_count: int | None = Field(default=None, ge=1)
    notes: str | None = None
    itinerary: str | None = None


class TripResponse(BaseSchema):
    id: int
    user_id: int
    name: str
    destination: str
    start_date: date
    end_date: date
    budget: float
    spent_amount: float
    status: TripStatus
    travelers_count: int
    notes: str | None
    itinerary: str | None
    remaining_budget: float = 0
    created_at: datetime
    updated_at: datetime
