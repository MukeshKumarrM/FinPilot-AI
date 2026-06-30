"""Analytics API routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.analytics import AnalyticsOverview
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/overview", response_model=AnalyticsOverview)
def analytics_overview(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AnalyticsOverview:
    return AnalyticsService(db).get_overview(current_user)
