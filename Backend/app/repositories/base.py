"""Generic repository base class."""

from typing import Generic, TypeVar

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import Base

ModelT = TypeVar("ModelT", bound=Base)


class BaseRepository(Generic[ModelT]):
    """CRUD operations for a SQLAlchemy model."""

    def __init__(self, db: Session, model: type[ModelT]) -> None:
        self.db = db
        self.model = model

    def get_by_id(self, entity_id: int) -> ModelT | None:
        return self.db.get(self.model, entity_id)

    def get_all(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        user_id: int | None = None,
    ) -> list[ModelT]:
        stmt = select(self.model)
        if user_id is not None and hasattr(self.model, "user_id"):
            stmt = stmt.where(self.model.user_id == user_id)
        stmt = stmt.offset(skip).limit(limit)
        return list(self.db.scalars(stmt).all())

    def count(self, user_id: int | None = None) -> int:
        stmt = select(func.count()).select_from(self.model)
        if user_id is not None and hasattr(self.model, "user_id"):
            stmt = stmt.where(self.model.user_id == user_id)
        return self.db.scalar(stmt) or 0

    def create(self, entity: ModelT) -> ModelT:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def update(self, entity: ModelT) -> ModelT:
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete(self, entity: ModelT) -> None:
        self.db.delete(entity)
        self.db.commit()
