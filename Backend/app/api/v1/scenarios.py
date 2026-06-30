"""Financial scenario API routes."""

from fastapi import APIRouter

from app.schemas.analytics import ScenarioRequest, ScenarioResult
from app.services.scenario_service import ScenarioService

router = APIRouter(prefix="/scenarios", tags=["scenarios"])


@router.post("/simulate", response_model=ScenarioResult)
def simulate_scenario(data: ScenarioRequest) -> ScenarioResult:
    return ScenarioService().simulate(data)
