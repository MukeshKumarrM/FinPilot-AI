"""Receipt ORM model."""

from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, Index, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import ExpenseCategory, ReceiptStatus


class Receipt(Base):
    """Uploaded receipt with OCR extraction metadata."""

    __tablename__ = "receipts"
    __table_args__ = (Index("ix_receipts_user_status", "user_id", "status"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[ReceiptStatus] = mapped_column(
        Enum(ReceiptStatus, name="receipt_status"),
        default=ReceiptStatus.PENDING,
        nullable=False,
    )
    extracted_amount: Mapped[float | None] = mapped_column(Numeric(14, 2), nullable=True)
    extracted_merchant: Mapped[str | None] = mapped_column(String(255), nullable=True)
    extracted_date: Mapped[str | None] = mapped_column(String(50), nullable=True)
    extracted_category: Mapped[ExpenseCategory | None] = mapped_column(
        Enum(ExpenseCategory, name="expense_category", create_type=False),
        nullable=True,
    )
    raw_text: Mapped[str | None] = mapped_column(Text, nullable=True)
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

    user = relationship("User", back_populates="receipts")
    expense = relationship("Expense", back_populates="receipt", uselist=False)
