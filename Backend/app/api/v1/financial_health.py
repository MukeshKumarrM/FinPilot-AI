"""Financial health API routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.analytics import FinancialHealthScore
from app.services.financial_health_service import FinancialHealthService

router = APIRouter(prefix="/financial-health", tags=["financial-health"])


@router.get("/score", response_model=FinancialHealthScore)
def financial_health_score(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> FinancialHealthScore:
    return FinancialHealthService(db).calculate_score(current_user)
