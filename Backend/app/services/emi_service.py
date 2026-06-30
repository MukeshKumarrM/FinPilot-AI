"""EMI calculation service."""

import math

from app.schemas.analytics import EMICalculationRequest, EMICalculationResponse


class EMIService:
    @staticmethod
    def calculate(data: EMICalculationRequest) -> EMICalculationResponse:
        principal = data.principal
        monthly_rate = data.annual_interest_rate / 12 / 100
        tenure = data.tenure_months

        if monthly_rate == 0:
            emi = principal / tenure
        else:
            emi = principal * monthly_rate * math.pow(1 + monthly_rate, tenure) / (
                math.pow(1 + monthly_rate, tenure) - 1
            )

        emi = round(emi, 2)
        schedule: list[dict[str, float]] = []
        balance = principal
        total_interest = 0.0

        for month in range(1, tenure + 1):
            interest = balance * monthly_rate
            principal_paid = emi - interest
            balance = max(balance - principal_paid, 0)
            total_interest += interest
            schedule.append(
                {
                    "month": float(month),
                    "emi": emi,
                    "principal": round(principal_paid, 2),
                    "interest": round(interest, 2),
                    "balance": round(balance, 2),
                }
            )

        return EMICalculationResponse(
            emi=emi,
            total_payment=round(emi * tenure, 2),
            total_interest=round(total_interest, 2),
            amortization_schedule=schedule,
        )

    @staticmethod
    def affordability_check(monthly_income: float, total_emi: float) -> dict[str, float | str]:
        ratio = (total_emi / monthly_income * 100) if monthly_income else 0
        status_label = "healthy" if ratio <= 40 else "caution" if ratio <= 50 else "risky"
        return {
            "emi_to_income_ratio": round(ratio, 2),
            "status": status_label,
            "recommended_max_emi": round(monthly_income * 0.4, 2),
        }
