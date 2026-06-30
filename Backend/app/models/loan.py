"""Loan ORM model."""

from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Index, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import LoanStatus, LoanType


class Loan(Base):
    """User loan with EMI tracking."""

    __tablename__ = "loans"
    __table_args__ = (
        Index("ix_loans_user_status", "user_id", "status"),
        Index("ix_loans_user_type", "user_id", "loan_type"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    loan_type: Mapped[LoanType] = mapped_column(
        Enum(LoanType, name="loan_type"),
        nullable=False,
    )
    principal_amount: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    outstanding_balance: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    interest_rate: Mapped[float] = mapped_column(Numeric(6, 3), nullable=False)
    tenure_months: Mapped[int] = mapped_column(Integer, nullable=False)
    emi_amount: Mapped[float] = mapped_column(Numeric(14, 2), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    lender: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[LoanStatus] = mapped_column(
        Enum(LoanStatus, name="loan_status"),
        default=LoanStatus.ACTIVE,
        nullable=False,
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
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

    user = relationship("User", back_populates="loans")
