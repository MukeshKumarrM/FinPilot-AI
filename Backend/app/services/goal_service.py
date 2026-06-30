"""Goal business logic."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.enums import GoalStatus
from app.models.goal import Goal
from app.models.user import User
from app.repositories.goal_repository import GoalRepository
from app.schemas.goal import GoalCreate, GoalResponse, GoalUpdate


class GoalService:
    def __init__(self, db: Session) -> None:
        self.repo = GoalRepository(db)

    def create(self, user: User, data: GoalCreate) -> GoalResponse:
        goal = Goal(user_id=user.id, **data.model_dump())
        created = self.repo.create(goal)
        return self._to_response(created)

    def get(self, user: User, goal_id: int) -> GoalResponse:
        return self._to_response(self._get_owned(user, goal_id))

    def list_goals(self, user: User, status: GoalStatus | None = None) -> list[GoalResponse]:
        items = self.repo.list_by_status(user.id, status)
        return [self._to_response(g) for g in items]

    def update(self, user: User, goal_id: int, data: GoalUpdate) -> GoalResponse:
        goal = self._get_owned(user, goal_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(goal, field, value)
        if float(goal.current_amount) >= float(goal.target_amount):
            goal.status = GoalStatus.COMPLETED
        updated = self.repo.update(goal)
        return self._to_response(updated)

    def delete(self, user: User, goal_id: int) -> None:
        self.repo.delete(self._get_owned(user, goal_id))

    def add_contribution(self, user: User, goal_id: int, amount: float) -> GoalResponse:
        if amount <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Amount must be positive")
        goal = self._get_owned(user, goal_id)
        goal.current_amount = float(goal.current_amount) + amount
        if float(goal.current_amount) >= float(goal.target_amount):
            goal.status = GoalStatus.COMPLETED
        updated = self.repo.update(goal)
        return self._to_response(updated)

    def _get_owned(self, user: User, goal_id: int) -> Goal:
        goal = self.repo.get_by_id(goal_id)
        if not goal or goal.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
        return goal

    def _to_response(self, goal: Goal) -> GoalResponse:
        progress = (
            (float(goal.current_amount) / float(goal.target_amount) * 100)
            if goal.target_amount
            else 0
        )
        data = GoalResponse.model_validate(goal)
        data.progress_percent = round(min(progress, 100), 2)
        return data
