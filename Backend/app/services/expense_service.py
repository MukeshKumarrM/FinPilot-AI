"""Expense business logic."""

from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.enums import ExpenseCategory
from app.models.expense import Expense
from app.models.user import User
from app.repositories.expense_repository import ExpenseRepository
from app.schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseSummary, ExpenseUpdate


class ExpenseService:
    def __init__(self, db: Session) -> None:
        self.repo = ExpenseRepository(db)

    def create(self, user: User, data: ExpenseCreate) -> ExpenseResponse:
        expense = Expense(user_id=user.id, **data.model_dump())
        created = self.repo.create(expense)
        return ExpenseResponse.model_validate(created)

    def get(self, user: User, expense_id: int) -> ExpenseResponse:
        expense = self._get_owned(user, expense_id)
        return ExpenseResponse.model_validate(expense)

    def list_expenses(
        self,
        user: User,
        *,
        skip: int = 0,
        limit: int = 100,
        start_date: date | None = None,
        end_date: date | None = None,
        category: ExpenseCategory | None = None,
    ) -> list[ExpenseResponse]:
        items = self.repo.list_by_user(
            user.id,
            skip=skip,
            limit=limit,
            start_date=start_date,
            end_date=end_date,
            category=category,
        )
        return [ExpenseResponse.model_validate(e) for e in items]

    def update(self, user: User, expense_id: int, data: ExpenseUpdate) -> ExpenseResponse:
        expense = self._get_owned(user, expense_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(expense, field, value)
        updated = self.repo.update(expense)
        return ExpenseResponse.model_validate(updated)

    def delete(self, user: User, expense_id: int) -> None:
        expense = self._get_owned(user, expense_id)
        self.repo.delete(expense)

    def get_summary(
        self,
        user: User,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> ExpenseSummary:
        by_category = self.repo.sum_by_category(user.id, start_date, end_date)
        total = sum(by_category.values())
        count = len(self.repo.list_by_user(user.id, start_date=start_date, end_date=end_date, limit=10000))
        return ExpenseSummary(total=total, count=count, by_category=by_category)

    def _get_owned(self, user: User, expense_id: int) -> Expense:
        expense = self.repo.get_by_id(expense_id)
        if not expense or expense.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
        return expense
