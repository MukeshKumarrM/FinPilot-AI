"""Bike purchase advisor API routes."""

from fastapi import APIRouter

from app.schemas.analytics import AdvisorRecommendation, AdvisorRequest
from app.services.bike_advisor_service import BikeAdvisorService

router = APIRouter(prefix="/bike-advisor", tags=["bike-advisor"])


@router.post("/recommend", response_model=AdvisorRecommendation)
def bike_recommendations(data: AdvisorRequest) -> AdvisorRecommendation:
    return BikeAdvisorService().recommend(data)
