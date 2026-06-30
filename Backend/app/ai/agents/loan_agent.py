"""Loan and EMI AI agent."""

from app.ai.agents.base_agent import BaseAgent


class LoanAgent(BaseAgent):
    system_prompt = (
        "You are FinPilot's loan and EMI coach. Explain EMI calculations, debt payoff strategies, "
        "and help users understand affordability. Never recommend specific lenders."
    )

    def _run_fallback(self, message: str, context: dict[str, object]) -> str:
        income = float(context.get("monthly_income", 0) or 0)
        emi = float(context.get("total_emi", 0) or 0)
        currency = context.get("currency", "INR")
        ratio = (emi / income * 100) if income else 0
        return (
            f"Your total EMI obligations are {currency} {emi:,.2f}, which is {ratio:.1f}% of income. "
            f"Financial planners often suggest keeping EMIs below 40% of gross income. "
            f"Consider the avalanche method (highest interest first) for faster debt reduction. "
            f"Question: {message}"
        )
