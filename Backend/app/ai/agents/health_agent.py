"""Financial health AI agent."""

from app.ai.agents.base_agent import BaseAgent


class HealthAgent(BaseAgent):
    system_prompt = (
        "You are FinPilot's financial health coach. Assess overall financial wellness "
        "across savings, debt, budgeting, and goal progress with actionable recommendations."
    )

    def _run_fallback(self, message: str, context: dict[str, object]) -> str:
        income = float(context.get("monthly_income", 0) or 0)
        expenses = float(context.get("monthly_expenses", 0) or 0)
        emi = float(context.get("total_emi", 0) or 0)
        currency = context.get("currency", "INR")
        savings_rate = ((income - expenses) / income * 100) if income else 0
        return (
            f"Financial snapshot: income {currency} {income:,.2f}, expenses {currency} {expenses:,.2f}, "
            f"EMI {currency} {emi:,.2f}, savings rate {savings_rate:.1f}%. "
            f"Focus on increasing savings rate above 20% and reducing high-interest debt. "
            f"Question: {message}"
        )
