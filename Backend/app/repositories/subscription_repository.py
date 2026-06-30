"""Subscription repository."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.enums import SubscriptionStatus
from app.models.subscription import Subscription
from app.repositories.base import BaseRepository


class SubscriptionRepository(BaseRepository[Subscription]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, Subscription)

    def list_active(self, user_id: int) -> list[Subscription]:
        stmt = select(Subscription).where(
            Subscription.user_id == user_id,
            Subscription.status == SubscriptionStatus.ACTIVE,
        )
        return list(self.db.scalars(stmt).all())

    def monthly_total(self, user_id: int) -> float:
        subs = self.list_active(user_id)
        total = 0.0
        for sub in subs:
            if sub.frequency.value == "weekly":
                total += float(sub.amount) * 4.33
            elif sub.frequency.value == "monthly":
                total += float(sub.amount)
            elif sub.frequency.value == "quarterly":
                total += float(sub.amount) / 3
            elif sub.frequency.value == "yearly":
                total += float(sub.amount) / 12
        return round(total, 2)
