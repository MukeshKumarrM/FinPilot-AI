"""Goal repository."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import GoalStatus
from app.models.goal import Goal
from app.repositories.base import BaseRepository


class GoalRepository(BaseRepository[Goal]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Goal)

    def list_by_status(self, user_id: int, status: GoalStatus | None = None) -> list[Goal]:
        stmt = select(Goal).where(Goal.user_id == user_id)
        if status:
            stmt = stmt.where(Goal.status == status)
        return list(self.db.scalars(stmt.order_by(Goal.created_at.desc())).all())
