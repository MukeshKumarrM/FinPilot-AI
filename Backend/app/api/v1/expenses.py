"""Expense API routes."""

from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.enums import ExpenseCategory
from app.models.user import User
from app.schemas.common import MessageResponse
from app.schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseSummary, ExpenseUpdate
from app.services.expense_service import ExpenseService

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("", response_model=ExpenseResponse, status_code=201)
def create_expense(
    data: ExpenseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ExpenseResponse:
    return ExpenseService(db).create(current_user, data)


@router.get("", response_model=list[ExpenseResponse])
def list_expenses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    start_date: date | None = None,
    end_date: date | None = None,
    category: ExpenseCategory | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[ExpenseResponse]:
    return ExpenseService(db).list_expenses(
        current_user,
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
        category=category,
    )


@router.get("/summary", response_model=ExpenseSummary)
def expense_summary(
    start_date: date | None = None,
    end_date: date | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ExpenseSummary:
    return ExpenseService(db).get_summary(current_user, start_date, end_date)


@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ExpenseResponse:
    return ExpenseService(db).get(current_user, expense_id)


@router.patch("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    data: ExpenseUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ExpenseResponse:
    return ExpenseService(db).update(current_user, expense_id, data)


@router.delete("/{expense_id}", response_model=MessageResponse)
def delete_expense(
    expense_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MessageResponse:
    ExpenseService(db).delete(current_user, expense_id)
    return MessageResponse(message="Expense deleted")
