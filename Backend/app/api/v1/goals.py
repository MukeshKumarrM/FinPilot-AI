"""Goal API routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.enums import GoalStatus
from app.models.user import User
from app.schemas.common import MessageResponse
from app.schemas.goal import GoalCreate, GoalResponse, GoalUpdate
from app.services.goal_service import GoalService

router = APIRouter(prefix="/goals", tags=["goals"])


@router.post("", response_model=GoalResponse, status_code=201)
def create_goal(
    data: GoalCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> GoalResponse:
    return GoalService(db).create(current_user, data)


@router.get("", response_model=list[GoalResponse])
def list_goals(
    status: GoalStatus | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[GoalResponse]:
    return GoalService(db).list_goals(current_user, status)


@router.get("/{goal_id}", response_model=GoalResponse)
def get_goal(
    goal_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> GoalResponse:
    return GoalService(db).get(current_user, goal_id)


@router.patch("/{goal_id}", response_model=GoalResponse)
def update_goal(
    goal_id: int,
    data: GoalUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> GoalResponse:
    return GoalService(db).update(current_user, goal_id, data)


@router.post("/{goal_id}/contribute", response_model=GoalResponse)
def contribute_to_goal(
    goal_id: int,
    amount: float,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> GoalResponse:
    return GoalService(db).add_contribution(current_user, goal_id, amount)


@router.delete("/{goal_id}", response_model=MessageResponse)
def delete_goal(
    goal_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MessageResponse:
    GoalService(db).delete(current_user, goal_id)
    return MessageResponse(message="Goal deleted")
