"""Savings and goals AI agent."""

from app.ai.agents.base_agent import BaseAgent


class SavingsAgent(BaseAgent):
    system_prompt = (
        "You are FinPilot's savings coach. Help users set realistic savings goals, "
        "build emergency funds, and create actionable plans to reach their targets."
    )

    def _run_fallback(self, message: str, context: dict[str, object]) -> str:
        income = float(context.get("monthly_income", 0) or 0)
        expenses = float(context.get("monthly_expenses", 0) or 0)
        savings = max(income - expenses, 0)
        currency = context.get("currency", "INR")
        emergency_target = expenses * 6
        return (
            f"Your current monthly savings capacity is approximately {currency} {savings:,.2f}. "
            f"An emergency fund target of 6 months expenses would be {currency} {emergency_target:,.2f}. "
            f"Automate transfers on payday to build consistency. Question: {message}"
        )
