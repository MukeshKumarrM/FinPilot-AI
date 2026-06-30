"""Shared enumerations for FinPilot AI domain models."""

import enum


class ExpenseCategory(str, enum.Enum):
    FOOD = "food"
    TRANSPORT = "transport"
    HOUSING = "housing"
    UTILITIES = "utilities"
    HEALTHCARE = "healthcare"
    ENTERTAINMENT = "entertainment"
    SHOPPING = "shopping"
    EDUCATION = "education"
    TRAVEL = "travel"
    INVESTMENT = "investment"
    INSURANCE = "insurance"
    SUBSCRIPTION = "subscription"
    EMI = "emi"
    OTHER = "other"


class BudgetPeriod(str, enum.Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


class GoalType(str, enum.Enum):
    SAVINGS = "savings"
    DEBT_PAYOFF = "debt_payoff"
    INVESTMENT = "investment"
    PURCHASE = "purchase"
    EMERGENCY_FUND = "emergency_fund"
    RETIREMENT = "retirement"
    OTHER = "other"


class GoalStatus(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class LoanType(str, enum.Enum):
    HOME = "home"
    CAR = "car"
    BIKE = "bike"
    PERSONAL = "personal"
    EDUCATION = "education"
    BUSINESS = "business"
    OTHER = "other"


class LoanStatus(str, enum.Enum):
    ACTIVE = "active"
    PAID_OFF = "paid_off"
    DEFAULTED = "defaulted"


class TripStatus(str, enum.Enum):
    PLANNED = "planned"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class SubscriptionFrequency(str, enum.Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


class SubscriptionStatus(str, enum.Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    CANCELLED = "cancelled"


class ReportType(str, enum.Enum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"
    CUSTOM = "custom"


class NetWorthAssetType(str, enum.Enum):
    CASH = "cash"
    SAVINGS = "savings"
    INVESTMENT = "investment"
    REAL_ESTATE = "real_estate"
    VEHICLE = "vehicle"
    OTHER = "other"


class NetWorthLiabilityType(str, enum.Enum):
    LOAN = "loan"
    CREDIT_CARD = "credit_card"
    MORTGAGE = "mortgage"
    OTHER = "other"


class AIMessageRole(str, enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ReceiptStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSED = "processed"
    FAILED = "failed"
