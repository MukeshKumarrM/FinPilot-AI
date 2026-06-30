"""Shared Pydantic schema utilities."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base schema with ORM mode enabled."""

    model_config = ConfigDict(from_attributes=True)


class TimestampSchema(BaseSchema):
    """Mixin for created/updated timestamps."""

    created_at: datetime
    updated_at: datetime | None = None


class MessageResponse(BaseSchema):
    """Generic message response."""

    message: str


class PaginatedResponse(BaseSchema):
    """Generic paginated list wrapper."""

    items: list
    total: int
    page: int
    page_size: int
    pages: int
