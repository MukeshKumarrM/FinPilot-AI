"""AI conversation ORM models."""

from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import AIMessageRole


class AIConversation(Base):
    """AI coach conversation session."""

    __tablename__ = "ai_conversations"
    __table_args__ = (Index("ix_ai_conversations_user", "user_id"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    agent_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
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

    user = relationship("User", back_populates="ai_conversations")
    messages = relationship(
        "AIConversationMessage",
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="AIConversationMessage.created_at",
    )


class AIConversationMessage(Base):
    """Individual message within an AI conversation."""

    __tablename__ = "ai_conversation_messages"
    __table_args__ = (Index("ix_ai_messages_conversation", "conversation_id"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("ai_conversations.id", ondelete="CASCADE"),
        nullable=False,
    )
    role: Mapped[AIMessageRole] = mapped_column(
        Enum(AIMessageRole, name="ai_message_role"),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    conversation = relationship("AIConversation", back_populates="messages")
