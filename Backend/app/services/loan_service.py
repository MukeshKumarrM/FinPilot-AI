"""Loan business logic."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.loan import Loan
from app.models.user import User
from app.repositories.loan_repository import LoanRepository
from app.schemas.loan import LoanCreate, LoanResponse, LoanUpdate


class LoanService:
    def __init__(self, db: Session) -> None:
        self.repo = LoanRepository(db)

    def create(self, user: User, data: LoanCreate) -> LoanResponse:
        loan = Loan(user_id=user.id, **data.model_dump())
        created = self.repo.create(loan)
        return LoanResponse.model_validate(created)

    def get(self, user: User, loan_id: int) -> LoanResponse:
        return LoanResponse.model_validate(self._get_owned(user, loan_id))

    def list_loans(self, user: User, active_only: bool = False) -> list[LoanResponse]:
        items = self.repo.list_active(user.id) if active_only else self.repo.get_all(user_id=user.id)
        return [LoanResponse.model_validate(l) for l in items]

    def update(self, user: User, loan_id: int, data: LoanUpdate) -> LoanResponse:
        loan = self._get_owned(user, loan_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(loan, field, value)
        updated = self.repo.update(loan)
        return LoanResponse.model_validate(updated)

    def delete(self, user: User, loan_id: int) -> None:
        self.repo.delete(self._get_owned(user, loan_id))

    def total_emi(self, user: User) -> float:
        return self.repo.total_emi(user.id)

    def _get_owned(self, user: User, loan_id: int) -> Loan:
        loan = self.repo.get_by_id(loan_id)
        if not loan or loan.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan not found")
        return loan
