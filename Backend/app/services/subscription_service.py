"""Subscription business logic."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.subscription import Subscription
from app.models.user import User
from app.repositories.subscription_repository import SubscriptionRepository
from app.schemas.subscription import SubscriptionCreate, SubscriptionResponse, SubscriptionUpdate


class SubscriptionService:
    def __init__(self, db: Session) -> None:
        self.repo = SubscriptionRepository(db)

    def create(self, user: User, data: SubscriptionCreate) -> SubscriptionResponse:
        sub = Subscription(user_id=user.id, **data.model_dump())
        created = self.repo.create(sub)
        return self._to_response(created)

    def get(self, user: User, subscription_id: int) -> SubscriptionResponse:
        return self._to_response(self._get_owned(user, subscription_id))

    def list_subscriptions(self, user: User) -> list[SubscriptionResponse]:
        items = self.repo.get_all(user_id=user.id, limit=500)
        return [self._to_response(s) for s in items]

    def update(self, user: User, subscription_id: int, data: SubscriptionUpdate) -> SubscriptionResponse:
        sub = self._get_owned(user, subscription_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(sub, field, value)
        updated = self.repo.update(sub)
        return self._to_response(updated)

    def delete(self, user: User, subscription_id: int) -> None:
        self.repo.delete(self._get_owned(user, subscription_id))

    def monthly_total(self, user: User) -> float:
        return self.repo.monthly_total(user.id)

    def _get_owned(self, user: User, subscription_id: int) -> Subscription:
        sub = self.repo.get_by_id(subscription_id)
        if not sub or sub.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subscription not found",
            )
        return sub

    def _to_response(self, sub: Subscription) -> SubscriptionResponse:
        monthly = self._monthly_equivalent(sub)
        response = SubscriptionResponse.model_validate(sub)
        response.monthly_equivalent = monthly
        return response

    @staticmethod
    def _monthly_equivalent(sub: Subscription) -> float:
        amount = float(sub.amount)
        freq = sub.frequency.value
        if freq == "weekly":
            return round(amount * 4.33, 2)
        if freq == "quarterly":
            return round(amount / 3, 2)
        if freq == "yearly":
            return round(amount / 12, 2)
        return amount
