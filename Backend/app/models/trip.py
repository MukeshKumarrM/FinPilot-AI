"""Trip ORM model."""

from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Index, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import TripStatus


class Trip(Base):
    """User travel plan with budget tracking."""

    __tablename__ = "trips"
    __table_args__ = (
        Index("ix_trips_user_status", "user_id", "status"),
        Index("ix_trips_user_dates", "user_id", "start_date", "end_date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    destination: Mapped[str] = mapped_column(String(255), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    budget: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    spent_amount: Mapped[float] = mapped_column(Numeric(14, 2), default=0, nullable=False)
    status: Mapped[TripStatus] = mapped_column(
        Enum(TripStatus, name="trip_status"),
        default=TripStatus.PLANNED,
        nullable=False,
    )
    travelers_count: Mapped[int] = mapped_column(default=1, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    itinerary: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user = relationship("User", back_populates="trips")
