"""Expense tracking AI agent."""

from app.ai.agents.base_agent import BaseAgent


class ExpenseAgent(BaseAgent):
    system_prompt = (
        "You are FinPilot's expense tracking coach. Help users categorize expenses, "
        "identify spending patterns, and suggest practical ways to reduce unnecessary costs."
    )

    def _run_fallback(self, message: str, context: dict[str, object]) -> str:
        expenses = context.get("monthly_expenses", 0)
        income = context.get("monthly_income", 0)
        currency = context.get("currency", "INR")
        return (
            f"I see your monthly expenses are {currency} {expenses:,.2f} against an income of "
            f"{currency} {income:,.2f}. Review your top spending categories and look for "
            f"subscriptions or dining expenses you can trim. Regarding your question: {message}"
        )
