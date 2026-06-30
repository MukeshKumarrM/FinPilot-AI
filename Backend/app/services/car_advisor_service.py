"""Car purchase advisor service."""

from app.core.config import settings
from app.schemas.analytics import AdvisorRecommendation, AdvisorRequest


class CarAdvisorService:
    DISCLAIMER = settings.AI_DISCLAIMER

    CAR_OPTIONS = [
        {"model": "Maruti Swift", "price": 650000, "fuel": "petrol", "type": "hatchback"},
        {"model": "Hyundai Creta", "price": 1200000, "fuel": "diesel", "type": "suv"},
        {"model": "Tata Nexon EV", "price": 1500000, "fuel": "electric", "type": "suv"},
        {"model": "Honda City", "price": 1300000, "fuel": "petrol", "type": "sedan"},
        {"model": "Mahindra XUV700", "price": 1800000, "fuel": "diesel", "type": "suv"},
    ]

    def recommend(self, data: AdvisorRequest) -> AdvisorRecommendation:
        budget = data.budget
        fuel_pref = (data.fuel_type or "").lower()
        usage = (data.usage_type or "city").lower()

        candidates = [
            car
            for car in self.CAR_OPTIONS
            if car["price"] <= budget * 1.1
            and (not fuel_pref or car["fuel"] == fuel_pref)
        ]
        if not candidates:
            candidates = sorted(self.CAR_OPTIONS, key=lambda c: abs(c["price"] - budget))[:3]

        recommendations: list[dict[str, str | float]] = []
        for car in candidates[:5]:
            emi_estimate = round(car["price"] * 0.015, 0)
            score = 100 - abs(car["price"] - budget) / budget * 50
            if usage == "highway" and car["type"] == "suv":
                score += 10
            if usage == "city" and car["type"] == "hatchback":
                score += 10
            recommendations.append(
                {
                    "model": car["model"],
                    "estimated_price": car["price"],
                    "fuel_type": car["fuel"],
                    "estimated_emi": emi_estimate,
                    "fit_score": round(min(score, 100), 1),
                }
            )

        recommendations.sort(key=lambda r: float(r["fit_score"]), reverse=True)
        analysis = (
            f"Based on your budget of ₹{budget:,.0f}, we found {len(recommendations)} suitable options. "
            f"Consider total cost of ownership including insurance, maintenance, and fuel."
        )
        return AdvisorRecommendation(
            recommendations=recommendations,
            analysis=analysis,
            disclaimer=self.DISCLAIMER,
        )
