"""Loan API routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.common import MessageResponse
from app.schemas.loan import LoanCreate, LoanResponse, LoanUpdate
from app.services.loan_service import LoanService

router = APIRouter(prefix="/loans", tags=["loans"])


@router.post("", response_model=LoanResponse, status_code=201)
def create_loan(
    data: LoanCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> LoanResponse:
    return LoanService(db).create(current_user, data)


@router.get("", response_model=list[LoanResponse])
def list_loans(
    active_only: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[LoanResponse]:
    return LoanService(db).list_loans(current_user, active_only=active_only)


@router.get("/total-emi")
def total_emi(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, float]:
    return {"total_emi": LoanService(db).total_emi(current_user)}


@router.get("/{loan_id}", response_model=LoanResponse)
def get_loan(
    loan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> LoanResponse:
    return LoanService(db).get(current_user, loan_id)


@router.patch("/{loan_id}", response_model=LoanResponse)
def update_loan(
    loan_id: int,
    data: LoanUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> LoanResponse:
    return LoanService(db).update(current_user, loan_id, data)


@router.delete("/{loan_id}", response_model=MessageResponse)
def delete_loan(
    loan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MessageResponse:
    LoanService(db).delete(current_user, loan_id)
    return MessageResponse(message="Loan deleted")
