"""Analytics and reporting business logic."""

import json
from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.models.enums import GoalStatus, ReportType
from app.models.report import Report
from app.models.user import User
from app.repositories.budget_repository import BudgetRepository
from app.repositories.expense_repository import ExpenseRepository
from app.repositories.goal_repository import GoalRepository
from app.repositories.loan_repository import LoanRepository
from app.repositories.report_repository import ReportRepository
from app.schemas.analytics import AnalyticsOverview, MonthlyTrend
from app.schemas.report import ReportCreate, ReportResponse


class AnalyticsService:
    def __init__(self, db: Session) -> None:
        self.expense_repo = ExpenseRepository(db)
        self.budget_repo = BudgetRepository(db)
        self.goal_repo = GoalRepository(db)
        self.loan_repo = LoanRepository(db)
        self.report_repo = ReportRepository(db)

    def get_overview(self, user: User) -> AnalyticsOverview:
        today = date.today()
        month_start = today.replace(day=1)
        total_expenses = self.expense_repo.total_spent(user.id, start_date=month_start)
        total_income = float(user.monthly_income or 0)
        savings_rate = (
            ((total_income - total_expenses) / total_income * 100) if total_income else 0
        )
        top_categories = self.expense_repo.sum_by_category(user.id, month_start, today)
        monthly_trends = self._build_monthly_trends(user)
        active_budgets = len(self.budget_repo.list_active(user.id))
        active_goals = len(self.goal_repo.list_by_status(user.id, GoalStatus.ACTIVE))
        total_emi = self.loan_repo.total_emi(user.id)

        return AnalyticsOverview(
            total_expenses=round(total_expenses, 2),
            total_income=total_income,
            savings_rate=round(savings_rate, 2),
            top_categories=top_categories,
            monthly_trends=monthly_trends,
            active_budgets=active_budgets,
            active_goals=active_goals,
            total_emi=total_emi,
        )

    def generate_report(self, user: User, data: ReportCreate) -> ReportResponse:
        expenses = self.expense_repo.sum_by_category(user.id, data.start_date, data.end_date)
        total = sum(expenses.values())
        summary_data = {
            "total_expenses": total,
            "by_category": expenses,
            "period": f"{data.start_date} to {data.end_date}",
        }
        report = Report(
            user_id=user.id,
            report_type=data.report_type,
            title=data.title,
            start_date=data.start_date,
            end_date=data.end_date,
            summary=f"Total expenses: ₹{total:,.2f} over the period.",
            data_json=json.dumps(summary_data),
        )
        created = self.report_repo.create(report)
        return ReportResponse.model_validate(created)

    def list_reports(self, user: User) -> list[ReportResponse]:
        items = self.report_repo.get_all(user_id=user.id, limit=100)
        return [ReportResponse.model_validate(r) for r in items]

    def _build_monthly_trends(self, user: User, months: int = 6) -> list[MonthlyTrend]:
        trends: list[MonthlyTrend] = []
        today = date.today()
        income = float(user.monthly_income or 0)

        for i in range(months - 1, -1, -1):
            ref = today.replace(day=1) - timedelta(days=i * 30)
            month_start = ref.replace(day=1)
            if month_start.month == 12:
                month_end = month_start.replace(year=month_start.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                month_end = month_start.replace(month=month_start.month + 1, day=1) - timedelta(days=1)

            expenses = self.expense_repo.total_spent(user.id, month_start, month_end)
            trends.append(
                MonthlyTrend(
                    month=month_start.strftime("%Y-%m"),
                    income=income,
                    expenses=round(expenses, 2),
                    savings=round(income - expenses, 2),
                )
            )
        return trends
