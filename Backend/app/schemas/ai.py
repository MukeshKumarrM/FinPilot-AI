"""AI coach schemas."""

from datetime import datetime

from pydantic import Field

from app.models.enums import AIMessageRole
from app.schemas.common import BaseSchema


class AIChatRequest(BaseSchema):
    message: str = Field(min_length=1, max_length=4000)
    conversation_id: int | None = None
    agent_type: str | None = "general"


class AIMessageResponse(BaseSchema):
    id: int
    role: AIMessageRole
    content: str
    created_at: datetime


class AIConversationResponse(BaseSchema):
    id: int
    user_id: int
    title: str | None
    agent_type: str | None
    messages: list[AIMessageResponse]
    created_at: datetime
    updated_at: datetime


class AIChatResponse(BaseSchema):
    conversation_id: int
    reply: str
    disclaimer: str
    agent_type: str
