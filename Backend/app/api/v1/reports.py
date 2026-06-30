"""Report API routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.report import ReportCreate, ReportResponse
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("", response_model=ReportResponse, status_code=201)
def generate_report(
    data: ReportCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ReportResponse:
    return AnalyticsService(db).generate_report(current_user, data)


@router.get("", response_model=list[ReportResponse])
def list_reports(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[ReportResponse]:
    return AnalyticsService(db).list_reports(current_user)
