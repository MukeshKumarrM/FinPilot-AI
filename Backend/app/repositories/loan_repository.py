"""Loan repository."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.enums import LoanStatus
from app.models.loan import Loan
from app.repositories.base import BaseRepository


class LoanRepository(BaseRepository[Loan]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Loan)

    def list_active(self, user_id: int) -> list[Loan]:
        stmt = select(Loan).where(
            Loan.user_id == user_id,
            Loan.status == LoanStatus.ACTIVE,
        )
        return list(self.db.scalars(stmt).all())

    def total_emi(self, user_id: int) -> float:
        stmt = select(func.coalesce(func.sum(Loan.emi_amount), 0)).where(
            Loan.user_id == user_id,
            Loan.status == LoanStatus.ACTIVE,
        )
        return float(self.db.scalar(stmt) or 0)
