"""Trip repository."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import TripStatus
from app.models.trip import Trip
from app.repositories.base import BaseRepository


class TripRepository(BaseRepository[Trip]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Trip)

    def list_by_status(self, user_id: int, status: TripStatus | None = None) -> list[Trip]:
        stmt = select(Trip).where(Trip.user_id == user_id)
        if status:
            stmt = stmt.where(Trip.status == status)
        return list(self.db.scalars(stmt.order_by(Trip.start_date.desc())).all())
