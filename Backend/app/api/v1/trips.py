"""Trip API routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.enums import TripStatus
from app.models.user import User
from app.schemas.common import MessageResponse
from app.schemas.trip import TripCreate, TripResponse, TripUpdate
from app.services.trip_service import TripService

router = APIRouter(prefix="/trips", tags=["trips"])


@router.post("", response_model=TripResponse, status_code=201)
def create_trip(
    data: TripCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TripResponse:
    return TripService(db).create(current_user, data)


@router.get("", response_model=list[TripResponse])
def list_trips(
    status: TripStatus | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[TripResponse]:
    return TripService(db).list_trips(current_user, status)


@router.get("/{trip_id}", response_model=TripResponse)
def get_trip(
    trip_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TripResponse:
    return TripService(db).get(current_user, trip_id)


@router.patch("/{trip_id}", response_model=TripResponse)
def update_trip(
    trip_id: int,
    data: TripUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TripResponse:
    return TripService(db).update(current_user, trip_id, data)


@router.post("/{trip_id}/expense", response_model=TripResponse)
def add_trip_expense(
    trip_id: int,
    amount: float,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TripResponse:
    return TripService(db).add_expense(current_user, trip_id, amount)


@router.delete("/{trip_id}", response_model=MessageResponse)
def delete_trip(
    trip_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MessageResponse:
    TripService(db).delete(current_user, trip_id)
    return MessageResponse(message="Trip deleted")
