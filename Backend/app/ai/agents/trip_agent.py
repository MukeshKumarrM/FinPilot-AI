"""Trip budgeting AI agent."""

from app.ai.agents.base_agent import BaseAgent


class TripAgent(BaseAgent):
    system_prompt = (
        "You are FinPilot's travel budgeting coach. Help users plan trip budgets covering "
        "transport, accommodation, food, and activities with realistic cost estimates."
    )

    def _run_fallback(self, message: str, context: dict[str, object]) -> str:
        income = float(context.get("monthly_income", 0) or 0)
        currency = context.get("currency", "INR")
        trip_budget = income * 0.15
        return (
            f"A common guideline is allocating 10-20% of monthly income for travel. "
            f"With {currency} {income:,.2f} income, a reasonable trip budget might be "
            f"{currency} {trip_budget:,.0f}. Book flights early and track daily spending. "
            f"Question: {message}"
        )
