"""AI conversation repository."""

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.ai_conversation import AIConversation, AIConversationMessage
from app.models.enums import AIMessageRole
from app.repositories.base import BaseRepository


class AIConversationRepository(BaseRepository[AIConversation]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, AIConversation)

    def get_with_messages(self, conversation_id: int, user_id: int) -> AIConversation | None:
        stmt = (
            select(AIConversation)
            .options(joinedload(AIConversation.messages))
            .where(
                AIConversation.id == conversation_id,
                AIConversation.user_id == user_id,
            )
        )
        return self.db.scalar(stmt)

    def list_by_user(self, user_id: int) -> list[AIConversation]:
        stmt = (
            select(AIConversation)
            .where(AIConversation.user_id == user_id)
            .order_by(AIConversation.updated_at.desc())
        )
        return list(self.db.scalars(stmt).all())

    def add_message(
        self,
        conversation_id: int,
        role: AIMessageRole,
        content: str,
    ) -> AIConversationMessage:
        message = AIConversationMessage(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message
