"""Net worth API routes."""

from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.common import MessageResponse
from app.schemas.net_worth import NetWorthEntryCreate, NetWorthEntryResponse, NetWorthEntryUpdate, NetWorthSummary
from app.services.net_worth_service import NetWorthService

router = APIRouter(prefix="/net-worth", tags=["net-worth"])


@router.post("", response_model=NetWorthEntryResponse, status_code=201)
def create_entry(
    data: NetWorthEntryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> NetWorthEntryResponse:
    return NetWorthService(db).create(current_user, data)


@router.get("", response_model=list[NetWorthEntryResponse])
def list_entries(
    as_of: date | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[NetWorthEntryResponse]:
    return NetWorthService(db).list_entries(current_user, as_of)


@router.get("/summary", response_model=NetWorthSummary)
def net_worth_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> NetWorthSummary:
    return NetWorthService(db).get_summary(current_user)


@router.get("/{entry_id}", response_model=NetWorthEntryResponse)
def get_entry(
    entry_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> NetWorthEntryResponse:
    return NetWorthService(db).get(current_user, entry_id)


@router.patch("/{entry_id}", response_model=NetWorthEntryResponse)
def update_entry(
    entry_id: int,
    data: NetWorthEntryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> NetWorthEntryResponse:
    return NetWorthService(db).update(current_user, entry_id, data)


@router.delete("/{entry_id}", response_model=MessageResponse)
def delete_entry(
    entry_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MessageResponse:
    NetWorthService(db).delete(current_user, entry_id)
    return MessageResponse(message="Net worth entry deleted")
