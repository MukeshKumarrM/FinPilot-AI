"""Car purchase advisor API routes."""

from fastapi import APIRouter

from app.schemas.analytics import AdvisorRecommendation, AdvisorRequest
from app.services.car_advisor_service import CarAdvisorService

router = APIRouter(prefix="/car-advisor", tags=["car-advisor"])


@router.post("/recommend", response_model=AdvisorRecommendation)
def car_recommendations(data: AdvisorRequest) -> AdvisorRecommendation:
    return CarAdvisorService().recommend(data)
