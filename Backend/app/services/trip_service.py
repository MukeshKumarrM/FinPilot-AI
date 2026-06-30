"""Trip planning business logic."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.enums import TripStatus
from app.models.trip import Trip
from app.models.user import User
from app.repositories.trip_repository import TripRepository
from app.schemas.trip import TripCreate, TripResponse, TripUpdate


class TripService:
    def __init__(self, db: Session) -> None:
        self.repo = TripRepository(db)

    def create(self, user: User, data: TripCreate) -> TripResponse:
        if data.end_date < data.start_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="End date must be after start date",
            )
        trip = Trip(user_id=user.id, **data.model_dump())
        created = self.repo.create(trip)
        return self._to_response(created)

    def get(self, user: User, trip_id: int) -> TripResponse:
        return self._to_response(self._get_owned(user, trip_id))

    def list_trips(self, user: User, status: TripStatus | None = None) -> list[TripResponse]:
        items = self.repo.list_by_status(user.id, status)
        return [self._to_response(t) for t in items]

    def update(self, user: User, trip_id: int, data: TripUpdate) -> TripResponse:
        trip = self._get_owned(user, trip_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(trip, field, value)
        if trip.end_date < trip.start_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="End date must be after start date",
            )
        updated = self.repo.update(trip)
        return self._to_response(updated)

    def delete(self, user: User, trip_id: int) -> None:
        self.repo.delete(self._get_owned(user, trip_id))

    def add_expense(self, user: User, trip_id: int, amount: float) -> TripResponse:
        if amount <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Amount must be positive")
        trip = self._get_owned(user, trip_id)
        trip.spent_amount = float(trip.spent_amount) + amount
        updated = self.repo.update(trip)
        return self._to_response(updated)

    def _get_owned(self, user: User, trip_id: int) -> Trip:
        trip = self.repo.get_by_id(trip_id)
        if not trip or trip.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
        return trip

    def _to_response(self, trip: Trip) -> TripResponse:
        response = TripResponse.model_validate(trip)
        response.remaining_budget = max(float(trip.budget) - float(trip.spent_amount), 0)
        return response
