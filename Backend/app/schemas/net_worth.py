"""Net worth schemas."""

from datetime import date, datetime
from typing import Literal

from pydantic import Field

from app.models.enums import NetWorthAssetType, NetWorthLiabilityType
from app.schemas.common import BaseSchema


class NetWorthEntryCreate(BaseSchema):
    name: str = Field(min_length=1, max_length=255)
    entry_type: Literal["asset", "liability"]
    asset_type: NetWorthAssetType | None = None
    liability_type: NetWorthLiabilityType | None = None
    amount: float = Field(gt=0)
    entry_date: date
    notes: str | None = None


class NetWorthEntryUpdate(BaseSchema):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    amount: float | None = Field(default=None, gt=0)
    entry_date: date | None = None
    notes: str | None = None


class NetWorthEntryResponse(BaseSchema):
    id: int
    user_id: int
    name: str
    entry_type: str
    asset_type: NetWorthAssetType | None
    liability_type: NetWorthLiabilityType | None
    amount: float
    entry_date: date
    notes: str | None
    created_at: datetime
    updated_at: datetime


class NetWorthSummary(BaseSchema):
    total_assets: float
    total_liabilities: float
    net_worth: float
    assets_by_type: dict[str, float]
    liabilities_by_type: dict[str, float]
