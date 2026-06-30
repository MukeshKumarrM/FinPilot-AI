"""Budget business logic."""

from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.budget import Budget
from app.models.enums import ExpenseCategory
from app.models.user import User
from app.repositories.budget_repository import BudgetRepository
from app.repositories.expense_repository import ExpenseRepository
from app.schemas.budget import BudgetCreate, BudgetResponse, BudgetStatusResponse, BudgetUpdate


class BudgetService:
    def __init__(self, db: Session) -> None:
        self.repo = BudgetRepository(db)
        self.expense_repo = ExpenseRepository(db)

    def create(self, user: User, data: BudgetCreate) -> BudgetResponse:
        budget = Budget(user_id=user.id, **data.model_dump())
        created = self.repo.create(budget)
        return BudgetResponse.model_validate(created)

    def get(self, user: User, budget_id: int) -> BudgetResponse:
        budget = self._get_owned(user, budget_id)
        return BudgetResponse.model_validate(budget)

    def list_budgets(
        self,
        user: User,
        *,
        active_only: bool = True,
        category: ExpenseCategory | None = None,
    ) -> list[BudgetResponse]:
        if active_only:
            items = self.repo.list_active(user.id, category=category)
        else:
            items = self.repo.get_all(user_id=user.id, limit=500)
        return [BudgetResponse.model_validate(b) for b in items]

    def update(self, user: User, budget_id: int, data: BudgetUpdate) -> BudgetResponse:
        budget = self._get_owned(user, budget_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(budget, field, value)
        updated = self.repo.update(budget)
        return BudgetResponse.model_validate(updated)

    def delete(self, user: User, budget_id: int) -> None:
        budget = self._get_owned(user, budget_id)
        self.repo.delete(budget)

    def get_status(self, user: User, budget_id: int) -> BudgetStatusResponse:
        budget = self._get_owned(user, budget_id)
        end = budget.end_date or date.today()
        spent = self.expense_repo.total_spent(
            user.id,
            start_date=budget.start_date,
            end_date=end,
            category=budget.category,
        )
        remaining = max(float(budget.amount) - spent, 0)
        utilization = (spent / float(budget.amount) * 100) if budget.amount else 0
        return BudgetStatusResponse(
            budget=BudgetResponse.model_validate(budget),
            spent=spent,
            remaining=remaining,
            utilization_percent=round(utilization, 2),
            is_over_budget=spent > float(budget.amount),
        )

    def _get_owned(self, user: User, budget_id: int) -> Budget:
        budget = self.repo.get_by_id(budget_id)
        if not budget or budget.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
        return budget
