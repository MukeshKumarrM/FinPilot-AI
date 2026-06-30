"""Budget planning AI agent."""

from app.ai.agents.base_agent import BaseAgent


class BudgetAgent(BaseAgent):
    system_prompt = (
        "You are FinPilot's budget planning coach. Help users allocate income across categories "
        "using the 50/30/20 rule as a starting point and adjust based on their goals."
    )

    def _run_fallback(self, message: str, context: dict[str, object]) -> str:
        income = float(context.get("monthly_income", 0) or 0)
        budgets = context.get("active_budgets", 0)
        currency = context.get("currency", "INR")
        needs = income * 0.5
        wants = income * 0.3
        savings = income * 0.2
        return (
            f"With {budgets} active budgets and {currency} {income:,.2f} monthly income, "
            f"consider allocating ~{currency} {needs:,.0f} for needs, {currency} {wants:,.0f} "
            f"for wants, and {currency} {savings:,.0f} for savings. "
            f"Your question: {message}"
        )
