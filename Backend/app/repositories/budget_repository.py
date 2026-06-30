"""Budget repository."""

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.budget import Budget
from app.models.enums import ExpenseCategory
from app.repositories.base import BaseRepository


class BudgetRepository(BaseRepository[Budget]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Budget)

    def list_active(
        self,
        user_id: int,
        *,
        as_of: date | None = None,
        category: ExpenseCategory | None = None,
    ) -> list[Budget]:
        ref_date = as_of or date.today()
        stmt = select(Budget).where(
            Budget.user_id == user_id,
            Budget.start_date <= ref_date,
        )
        stmt = stmt.where((Budget.end_date.is_(None)) | (Budget.end_date >= ref_date))
        if category:
            stmt = stmt.where(Budget.category == category)
        return list(self.db.scalars(stmt.order_by(Budget.start_date.desc())).all())
