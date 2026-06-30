"""AI coach API routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.ai import AIChatRequest, AIChatResponse, AIConversationResponse
from app.services.ai_coach_service import AICoachService

router = APIRouter(prefix="/ai-coach", tags=["ai-coach"])


@router.post("/chat", response_model=AIChatResponse)
def chat(
    data: AIChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AIChatResponse:
    return AICoachService(db).chat(current_user, data)


@router.get("/conversations", response_model=list[AIConversationResponse])
def list_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[AIConversationResponse]:
    return AICoachService(db).list_conversations(current_user)


@router.get("/conversations/{conversation_id}", response_model=AIConversationResponse)
def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> AIConversationResponse:
    return AICoachService(db).get_conversation(current_user, conversation_id)
