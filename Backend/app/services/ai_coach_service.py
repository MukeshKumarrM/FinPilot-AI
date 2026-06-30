"""AI financial coach service."""

from sqlalchemy.orm import Session

from app.ai.agents.budget_agent import BudgetAgent
from app.ai.agents.expense_agent import ExpenseAgent
from app.ai.agents.health_agent import HealthAgent
from app.ai.agents.loan_agent import LoanAgent
from app.ai.agents.savings_agent import SavingsAgent
from app.ai.agents.trip_agent import TripAgent
from app.core.config import settings
from app.models.ai_conversation import AIConversation
from app.models.enums import AIMessageRole
from app.models.user import User
from app.repositories.ai_conversation_repository import AIConversationRepository
from app.repositories.budget_repository import BudgetRepository
from app.repositories.expense_repository import ExpenseRepository
from app.repositories.goal_repository import GoalRepository
from app.repositories.loan_repository import LoanRepository
from app.schemas.ai import AIChatRequest, AIChatResponse, AIConversationResponse, AIMessageResponse


class AICoachService:
    AGENT_MAP = {
        "expense": ExpenseAgent,
        "budget": BudgetAgent,
        "savings": SavingsAgent,
        "loan": LoanAgent,
        "trip": TripAgent,
        "health": HealthAgent,
        "general": ExpenseAgent,
    }

    def __init__(self, db: Session) -> None:
        self.db = db
        self.conversation_repo = AIConversationRepository(db)
        self.expense_repo = ExpenseRepository(db)
        self.budget_repo = BudgetRepository(db)
        self.goal_repo = GoalRepository(db)
        self.loan_repo = LoanRepository(db)

    def chat(self, user: User, data: AIChatRequest) -> AIChatResponse:
        agent_type = data.agent_type or "general"
        agent_cls = self.AGENT_MAP.get(agent_type, ExpenseAgent)
        agent = agent_cls()

        context = self._build_context(user)
        conversation = self._get_or_create_conversation(user, data.conversation_id, agent_type)

        self.conversation_repo.add_message(
            conversation.id,
            AIMessageRole.USER,
            data.message,
        )

        reply = agent.run(data.message, context)
        reply_with_disclaimer = f"{reply}\n\n---\n*{settings.AI_DISCLAIMER}*"

        self.conversation_repo.add_message(
            conversation.id,
            AIMessageRole.ASSISTANT,
            reply_with_disclaimer,
        )

        return AIChatResponse(
            conversation_id=conversation.id,
            reply=reply_with_disclaimer,
            disclaimer=settings.AI_DISCLAIMER,
            agent_type=agent_type,
        )

    def list_conversations(self, user: User) -> list[AIConversationResponse]:
        conversations = self.conversation_repo.list_by_user(user.id)
        return [self._to_conversation_response(c) for c in conversations]

    def get_conversation(self, user: User, conversation_id: int) -> AIConversationResponse:
        conversation = self.conversation_repo.get_with_messages(conversation_id, user.id)
        if not conversation:
            from fastapi import HTTPException, status

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found",
            )
        return self._to_conversation_response(conversation)

    def _get_or_create_conversation(
        self,
        user: User,
        conversation_id: int | None,
        agent_type: str,
    ) -> AIConversation:
        if conversation_id:
            conversation = self.conversation_repo.get_with_messages(conversation_id, user.id)
            if conversation:
                return conversation

        conversation = AIConversation(
            user_id=user.id,
            title=f"{agent_type.title()} Coach",
            agent_type=agent_type,
        )
        return self.conversation_repo.create(conversation)

    def _build_context(self, user: User) -> dict[str, object]:
        from datetime import date

        month_start = date.today().replace(day=1)
        return {
            "user_name": user.full_name or user.email,
            "monthly_income": float(user.monthly_income or 0),
            "currency": user.currency,
            "monthly_expenses": self.expense_repo.total_spent(user.id, month_start),
            "active_budgets": len(self.budget_repo.list_active(user.id)),
            "active_goals": len(self.goal_repo.get_all(user_id=user.id)),
            "total_emi": self.loan_repo.total_emi(user.id),
        }

    def _to_conversation_response(self, conversation: AIConversation) -> AIConversationResponse:
        messages = [
            AIMessageResponse.model_validate(m)
            for m in getattr(conversation, "messages", [])
        ]
        return AIConversationResponse(
            id=conversation.id,
            user_id=conversation.user_id,
            title=conversation.title,
            agent_type=conversation.agent_type,
            messages=messages,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
        )
