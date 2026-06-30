"""Report schemas."""

from datetime import date, datetime

from app.models.enums import ReportType
from app.schemas.common import BaseSchema


class ReportCreate(BaseSchema):
    report_type: ReportType
    title: str
    start_date: date
    end_date: date


class ReportResponse(BaseSchema):
    id: int
    user_id: int
    report_type: ReportType
    title: str
    start_date: date
    end_date: date
    summary: str | None
    data_json: str | None
    created_at: datetime
