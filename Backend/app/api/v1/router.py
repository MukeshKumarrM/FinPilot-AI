"""Aggregate all v1 API routers."""

from fastapi import APIRouter

from app.api.v1 import (
    admin,
    ai_coach,
    analytics,
    auth,
    bike_advisor,
    budgets,
    car_advisor,
    emi,
    expenses,
    financial_health,
    goals,
    loans,
    net_worth,
    receipts,
    reports,
    scenarios,
    statements,
    subscriptions,
    trips,
)

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(expenses.router)
api_router.include_router(budgets.router)
api_router.include_router(goals.router)
api_router.include_router(receipts.router)
api_router.include_router(statements.router)
api_router.include_router(emi.router)
api_router.include_router(loans.router)
api_router.include_router(trips.router)
api_router.include_router(subscriptions.router)
api_router.include_router(net_worth.router)
api_router.include_router(analytics.router)
api_router.include_router(reports.router)
api_router.include_router(ai_coach.router)
api_router.include_router(admin.router)
api_router.include_router(financial_health.router)
api_router.include_router(scenarios.router)
api_router.include_router(car_advisor.router)
api_router.include_router(bike_advisor.router)
