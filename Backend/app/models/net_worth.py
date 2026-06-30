"""Net worth entry ORM model."""

from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Index, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import NetWorthAssetType, NetWorthLiabilityType


class NetWorthEntry(Base):
    """Asset or liability entry for net worth tracking."""

    __tablename__ = "net_worth_entries"
    __table_args__ = (
        Index("ix_net_worth_user_date", "user_id", "entry_date"),
        Index("ix_net_worth_user_type", "user_id", "entry_type"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    entry_type: Mapped[str] = mapped_column(String(20), nullable=False)  # asset | liability
    asset_type: Mapped[NetWorthAssetType | None] = mapped_column(
        Enum(NetWorthAssetType, name="net_worth_asset_type"),
        nullable=True,
    )
    liability_type: Mapped[NetWorthLiabilityType | None] = mapped_column(
        Enum(NetWorthLiabilityType, name="net_worth_liability_type"),
        nullable=True,
    )
    amount: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    entry_date: Mapped[date] = mapped_column(Date, nullable=False)
    notes: Mapped[str | None] = mapped_column(String(500), nullable=True)
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

    user = relationship("User", back_populates="net_worth_entries")
