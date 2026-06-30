"""Base LangChain agent with OpenAI fallback."""

from abc import ABC, abstractmethod

from app.core.config import settings


class BaseAgent(ABC):
    """Base class for FinPilot AI agents."""

    system_prompt: str = "You are a helpful financial assistant."

    def __init__(self) -> None:
        self.disclaimer = settings.AI_DISCLAIMER

    def run(self, message: str, context: dict[str, object] | None = None) -> str:
        context = context or {}
        try:
            return self._run_llm(message, context)
        except Exception:
            return self._run_fallback(message, context)

    def _run_llm(self, message: str, context: dict[str, object]) -> str:
        if not settings.OPENAI_API_KEY:
            return self._run_fallback(message, context)

        from langchain_core.messages import HumanMessage, SystemMessage
        from langchain_openai import ChatOpenAI

        llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            api_key=settings.OPENAI_API_KEY,
            temperature=0.3,
        )
        context_str = "\n".join(f"- {k}: {v}" for k, v in context.items())
        system = (
            f"{self.system_prompt}\n\n"
            f"User financial context:\n{context_str}\n\n"
            f"Always include educational guidance only. {self.disclaimer}"
        )
        response = llm.invoke([SystemMessage(content=system), HumanMessage(content=message)])
        return str(response.content)

    @abstractmethod
    def _run_fallback(self, message: str, context: dict[str, object]) -> str:
        """Rule-based fallback when LLM is unavailable."""
