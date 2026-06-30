"""Subscription API routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.common import MessageResponse
from app.schemas.subscription import SubscriptionCreate, SubscriptionResponse, SubscriptionUpdate
from app.services.subscription_service import SubscriptionService

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


@router.post("", response_model=SubscriptionResponse, status_code=201)
def create_subscription(
    data: SubscriptionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SubscriptionResponse:
    return SubscriptionService(db).create(current_user, data)


@router.get("", response_model=list[SubscriptionResponse])
def list_subscriptions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[SubscriptionResponse]:
    return SubscriptionService(db).list_subscriptions(current_user)


@router.get("/monthly-total")
def monthly_total(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, float]:
    return {"monthly_total": SubscriptionService(db).monthly_total(current_user)}


@router.get("/{subscription_id}", response_model=SubscriptionResponse)
def get_subscription(
    subscription_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SubscriptionResponse:
    return SubscriptionService(db).get(current_user, subscription_id)


@router.patch("/{subscription_id}", response_model=SubscriptionResponse)
def update_subscription(
    subscription_id: int,
    data: SubscriptionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> SubscriptionResponse:
    return SubscriptionService(db).update(current_user, subscription_id, data)


@router.delete("/{subscription_id}", response_model=MessageResponse)
def delete_subscription(
    subscription_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MessageResponse:
    SubscriptionService(db).delete(current_user, subscription_id)
    return MessageResponse(message="Subscription deleted")
