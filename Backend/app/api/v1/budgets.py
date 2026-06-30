"""Budget API routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.enums import ExpenseCategory
from app.models.user import User
from app.schemas.budget import BudgetCreate, BudgetResponse, BudgetStatusResponse, BudgetUpdate
from app.schemas.common import MessageResponse
from app.services.budget_service import BudgetService

router = APIRouter(prefix="/budgets", tags=["budgets"])


@router.post("", response_model=BudgetResponse, status_code=201)
def create_budget(
    data: BudgetCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> BudgetResponse:
    return BudgetService(db).create(current_user, data)


@router.get("", response_model=list[BudgetResponse])
def list_budgets(
    active_only: bool = True,
    category: ExpenseCategory | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[BudgetResponse]:
    return BudgetService(db).list_budgets(current_user, active_only=active_only, category=category)


@router.get("/{budget_id}", response_model=BudgetResponse)
def get_budget(
    budget_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> BudgetResponse:
    return BudgetService(db).get(current_user, budget_id)


@router.get("/{budget_id}/status", response_model=BudgetStatusResponse)
def budget_status(
    budget_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> BudgetStatusResponse:
    return BudgetService(db).get_status(current_user, budget_id)


@router.patch("/{budget_id}", response_model=BudgetResponse)
def update_budget(
    budget_id: int,
    data: BudgetUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> BudgetResponse:
    return BudgetService(db).update(current_user, budget_id, data)


@router.delete("/{budget_id}", response_model=MessageResponse)
def delete_budget(
    budget_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MessageResponse:
    BudgetService(db).delete(current_user, budget_id)
    return MessageResponse(message="Budget deleted")
