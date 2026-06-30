"""Bike purchase advisor service."""

from app.core.config import settings
from app.schemas.analytics import AdvisorRecommendation, AdvisorRequest


class BikeAdvisorService:
    DISCLAIMER = settings.AI_DISCLAIMER

    BIKE_OPTIONS = [
        {"model": "Hero Splendor", "price": 75000, "fuel": "petrol", "type": "commuter"},
        {"model": "Honda Activa", "price": 85000, "fuel": "petrol", "type": "scooter"},
        {"model": "TVS Apache RTR", "price": 140000, "fuel": "petrol", "type": "sport"},
        {"model": "Royal Enfield Classic", "price": 200000, "fuel": "petrol", "type": "cruiser"},
        {"model": "Ather 450X", "price": 150000, "fuel": "electric", "type": "scooter"},
    ]

    def recommend(self, data: AdvisorRequest) -> AdvisorRecommendation:
        budget = data.budget
        fuel_pref = (data.fuel_type or "").lower()
        usage = (data.usage_type or "commute").lower()

        candidates = [
            bike
            for bike in self.BIKE_OPTIONS
            if bike["price"] <= budget * 1.1
            and (not fuel_pref or bike["fuel"] == fuel_pref)
        ]
        if not candidates:
            candidates = sorted(self.BIKE_OPTIONS, key=lambda b: abs(b["price"] - budget))[:3]

        recommendations: list[dict[str, str | float]] = []
        for bike in candidates[:5]:
            emi_estimate = round(bike["price"] * 0.02, 0)
            score = 100 - abs(bike["price"] - budget) / budget * 50
            if usage == "commute" and bike["type"] in ("commuter", "scooter"):
                score += 15
            if usage == "leisure" and bike["type"] in ("cruiser", "sport"):
                score += 15
            recommendations.append(
                {
                    "model": bike["model"],
                    "estimated_price": bike["price"],
                    "fuel_type": bike["fuel"],
                    "estimated_emi": emi_estimate,
                    "fit_score": round(min(score, 100), 1),
                }
            )

        recommendations.sort(key=lambda r: float(r["fit_score"]), reverse=True)
        analysis = (
            f"For a budget of ₹{budget:,.0f}, consider fuel efficiency, maintenance costs, "
            f"and insurance alongside the purchase price."
        )
        return AdvisorRecommendation(
            recommendations=recommendations,
            analysis=analysis,
            disclaimer=self.DISCLAIMER,
        )
