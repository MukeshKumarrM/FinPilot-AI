"""Analytics and financial health schemas."""

from app.schemas.common import BaseSchema


class MonthlyTrend(BaseSchema):
    month: str
    income: float
    expenses: float
    savings: float


class AnalyticsOverview(BaseSchema):
    total_expenses: float
    total_income: float
    savings_rate: float
    top_categories: dict[str, float]
    monthly_trends: list[MonthlyTrend]
    active_budgets: int
    active_goals: int
    total_emi: float


class FinancialHealthScore(BaseSchema):
    score: int
    grade: str
    factors: dict[str, float]
    recommendations: list[str]
    disclaimer: str


class EMICalculationRequest(BaseSchema):
    principal: float
    annual_interest_rate: float
    tenure_months: int


class EMICalculationResponse(BaseSchema):
    emi: float
    total_payment: float
    total_interest: float
    amortization_schedule: list[dict[str, float]]


class ScenarioRequest(BaseSchema):
    name: str
    monthly_income: float
    monthly_expenses: float
    savings_goal: float | None = None
    additional_emi: float | None = None
    expense_reduction_percent: float | None = None


class ScenarioResult(BaseSchema):
    name: str
    projected_savings: float
    months_to_goal: int | None
    disposable_income: float
    analysis: str
    disclaimer: str


class AdvisorRequest(BaseSchema):
    budget: float
    preferences: str | None = None
    fuel_type: str | None = None
    usage_type: str | None = None


class AdvisorRecommendation(BaseSchema):
    recommendations: list[dict[str, str | float]]
    analysis: str
    disclaimer: str
