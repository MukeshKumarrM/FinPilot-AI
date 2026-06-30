"""EMI calculator API routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.repositories.loan_repository import LoanRepository
from app.schemas.analytics import EMICalculationRequest, EMICalculationResponse
from app.services.emi_service import EMIService

router = APIRouter(prefix="/emi", tags=["emi"])


@router.post("/calculate", response_model=EMICalculationResponse)
def calculate_emi(data: EMICalculationRequest) -> EMICalculationResponse:
    return EMIService.calculate(data)


@router.get("/affordability")
def emi_affordability(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, float | str]:
    total_emi = LoanRepository(db).total_emi(current_user.id)
    income = float(current_user.monthly_income or 0)
    return EMIService.affordability_check(income, total_emi)
