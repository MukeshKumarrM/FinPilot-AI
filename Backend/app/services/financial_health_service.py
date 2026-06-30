"""Financial health scoring service."""

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.enums import GoalStatus
from app.models.user import User
from app.repositories.budget_repository import BudgetRepository
from app.repositories.expense_repository import ExpenseRepository
from app.repositories.goal_repository import GoalRepository
from app.repositories.loan_repository import LoanRepository
from app.repositories.net_worth_repository import NetWorthRepository
from app.repositories.subscription_repository import SubscriptionRepository
from app.schemas.analytics import FinancialHealthScore


class FinancialHealthService:
    DISCLAIMER = settings.AI_DISCLAIMER

    def __init__(self, db: Session) -> None:
        self.expense_repo = ExpenseRepository(db)
        self.budget_repo = BudgetRepository(db)
        self.goal_repo = GoalRepository(db)
        self.loan_repo = LoanRepository(db)
        self.net_worth_repo = NetWorthRepository(db)
        self.subscription_repo = SubscriptionRepository(db)

    def calculate_score(self, user: User) -> FinancialHealthScore:
        income = float(user.monthly_income or 0)
        expenses = self.expense_repo.total_spent(user.id)
        total_emi = self.loan_repo.total_emi(user.id)
        subscriptions = self.subscription_repo.monthly_total(user.id)
        net_worth = (
            self.net_worth_repo.sum_by_type(user.id, "asset")
            - self.net_worth_repo.sum_by_type(user.id, "liability")
        )
        active_goals = len(self.goal_repo.list_by_status(user.id, GoalStatus.ACTIVE))
        active_budgets = len(self.budget_repo.list_active(user.id))

        factors: dict[str, float] = {}
        recommendations: list[str] = []

        savings_rate = ((income - expenses) / income * 100) if income else 0
        factors["savings_rate"] = round(max(savings_rate, 0), 2)
        if savings_rate < 20:
            recommendations.append("Aim to save at least 20% of your monthly income.")

        emi_ratio = (total_emi / income * 100) if income else 0
        factors["emi_to_income_ratio"] = round(emi_ratio, 2)
        if emi_ratio > 40:
            recommendations.append("Your EMI burden exceeds 40% of income. Consider debt consolidation.")

        factors["net_worth"] = round(net_worth, 2)
        if net_worth < 0:
            recommendations.append("Focus on reducing liabilities to improve net worth.")

        factors["subscription_load"] = round(subscriptions, 2)
        if subscriptions > income * 0.05:
            recommendations.append("Review recurring subscriptions for potential savings.")

        factors["goal_tracking"] = active_goals * 10
        factors["budget_discipline"] = active_budgets * 10

        score = self._compute_score(factors, income, expenses, emi_ratio, savings_rate)
        grade = self._grade(score)

        if not recommendations:
            recommendations.append("Keep maintaining your current financial habits.")

        return FinancialHealthScore(
            score=score,
            grade=grade,
            factors=factors,
            recommendations=recommendations,
            disclaimer=self.DISCLAIMER,
        )

    @staticmethod
    def _compute_score(
        factors: dict[str, float],
        income: float,
        expenses: float,
        emi_ratio: float,
        savings_rate: float,
    ) -> int:
        score = 50.0
        if savings_rate >= 30:
            score += 20
        elif savings_rate >= 20:
            score += 15
        elif savings_rate >= 10:
            score += 8

        if emi_ratio <= 30:
            score += 15
        elif emi_ratio <= 40:
            score += 8
        elif emi_ratio > 50:
            score -= 15

        if factors["net_worth"] > income * 6:
            score += 10
        elif factors["net_worth"] > 0:
            score += 5

        if income > expenses:
            score += 5

        score += min(factors.get("goal_tracking", 0), 10)
        score += min(factors.get("budget_discipline", 0), 10)
        return max(0, min(100, int(round(score))))

    @staticmethod
    def _grade(score: int) -> str:
        if score >= 80:
            return "A"
        if score >= 65:
            return "B"
        if score >= 50:
            return "C"
        if score >= 35:
            return "D"
        return "F"
