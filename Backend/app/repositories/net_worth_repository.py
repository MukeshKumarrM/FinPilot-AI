"""Net worth repository."""

from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.net_worth import NetWorthEntry
from app.repositories.base import BaseRepository


class NetWorthRepository(BaseRepository[NetWorthEntry]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, NetWorthEntry)

    def list_by_date(self, user_id: int, as_of: date | None = None) -> list[NetWorthEntry]:
        ref_date = as_of or date.today()
        stmt = (
            select(NetWorthEntry)
            .where(NetWorthEntry.user_id == user_id, NetWorthEntry.entry_date <= ref_date)
            .order_by(NetWorthEntry.entry_date.desc())
        )
        return list(self.db.scalars(stmt).all())

    def sum_by_type(self, user_id: int, entry_type: str) -> float:
        stmt = select(func.coalesce(func.sum(NetWorthEntry.amount), 0)).where(
            NetWorthEntry.user_id == user_id,
            NetWorthEntry.entry_type == entry_type,
        )
        return float(self.db.scalar(stmt) or 0)
