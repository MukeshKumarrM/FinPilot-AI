"""Authentication and user schemas."""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.schemas.common import BaseSchema


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = None
    currency: str = "INR"
    timezone: str = "Asia/Kolkata"
    monthly_income: float | None = None


class UserUpdate(BaseModel):
    full_name: str | None = None
    currency: str | None = None
    timezone: str | None = None
    monthly_income: float | None = None


class UserResponse(BaseSchema):
    id: int
    email: str
    full_name: str | None
    currency: str
    timezone: str
    monthly_income: float | None
    is_active: bool
    is_admin: bool
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str
