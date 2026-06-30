"""Expense repository."""

from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.enums import ExpenseCategory
from app.models.expense import Expense
from app.repositories.base import BaseRepository


class ExpenseRepository(BaseRepository[Expense]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Expense)

    def list_by_user(
        self,
        user_id: int,
        *,
        skip: int = 0,
        limit: int = 100,
        start_date: date | None = None,
        end_date: date | None = None,
        category: ExpenseCategory | None = None,
    ) -> list[Expense]:
        stmt = select(Expense).where(Expense.user_id == user_id)
        if start_date:
            stmt = stmt.where(Expense.expense_date >= start_date)
        if end_date:
            stmt = stmt.where(Expense.expense_date <= end_date)
        if category:
            stmt = stmt.where(Expense.category == category)
        stmt = stmt.order_by(Expense.expense_date.desc()).offset(skip).limit(limit)
        return list(self.db.scalars(stmt).all())

    def sum_by_category(
        self,
        user_id: int,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> dict[str, float]:
        stmt = (
            select(Expense.category, func.sum(Expense.amount))
            .where(Expense.user_id == user_id)
            .group_by(Expense.category)
        )
        if start_date:
            stmt = stmt.where(Expense.expense_date >= start_date)
        if end_date:
            stmt = stmt.where(Expense.expense_date <= end_date)
        rows = self.db.execute(stmt).all()
        return {cat.value: float(total) for cat, total in rows}

    def total_spent(
        self,
        user_id: int,
        start_date: date | None = None,
        end_date: date | None = None,
        category: ExpenseCategory | None = None,
    ) -> float:
        stmt = select(func.coalesce(func.sum(Expense.amount), 0)).where(
            Expense.user_id == user_id
        )
        if start_date:
            stmt = stmt.where(Expense.expense_date >= start_date)
        if end_date:
            stmt = stmt.where(Expense.expense_date <= end_date)
        if category:
            stmt = stmt.where(Expense.category == category)
        return float(self.db.scalar(stmt) or 0)
