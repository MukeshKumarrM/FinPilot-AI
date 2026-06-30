"""Financial scenario modeling service."""

from app.core.config import settings
from app.schemas.analytics import ScenarioRequest, ScenarioResult


class ScenarioService:
    DISCLAIMER = settings.AI_DISCLAIMER

    def simulate(self, data: ScenarioRequest) -> ScenarioResult:
        income = data.monthly_income
        expenses = data.monthly_expenses

        if data.expense_reduction_percent:
            expenses *= 1 - data.expense_reduction_percent / 100

        additional_emi = data.additional_emi or 0
        disposable = income - expenses - additional_emi
        projected_savings = disposable * 12

        months_to_goal: int | None = None
        if data.savings_goal and disposable > 0:
            months_to_goal = int(data.savings_goal / disposable) + (
                1 if data.savings_goal % disposable else 0
            )

        analysis_parts = [
            f"Monthly disposable income: ₹{disposable:,.2f}.",
            f"Annual projected savings: ₹{projected_savings:,.2f}.",
        ]
        if months_to_goal:
            analysis_parts.append(f"Estimated {months_to_goal} months to reach savings goal.")
        if disposable < 0:
            analysis_parts.append("Warning: expenses and EMIs exceed income in this scenario.")

        return ScenarioResult(
            name=data.name,
            projected_savings=round(projected_savings, 2),
            months_to_goal=months_to_goal,
            disposable_income=round(disposable, 2),
            analysis=" ".join(analysis_parts),
            disclaimer=self.DISCLAIMER,
        )
