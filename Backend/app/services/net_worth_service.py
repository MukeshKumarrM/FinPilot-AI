"""Net worth tracking business logic."""

from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.net_worth import NetWorthEntry
from app.models.user import User
from app.repositories.net_worth_repository import NetWorthRepository
from app.schemas.net_worth import NetWorthEntryCreate, NetWorthEntryResponse, NetWorthEntryUpdate, NetWorthSummary


class NetWorthService:
    def __init__(self, db: Session) -> None:
        self.repo = NetWorthRepository(db)

    def create(self, user: User, data: NetWorthEntryCreate) -> NetWorthEntryResponse:
        if data.entry_type == "asset" and not data.asset_type:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="asset_type required")
        if data.entry_type == "liability" and not data.liability_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="liability_type required",
            )
        entry = NetWorthEntry(user_id=user.id, **data.model_dump())
        created = self.repo.create(entry)
        return NetWorthEntryResponse.model_validate(created)

    def get(self, user: User, entry_id: int) -> NetWorthEntryResponse:
        return NetWorthEntryResponse.model_validate(self._get_owned(user, entry_id))

    def list_entries(self, user: User, as_of: date | None = None) -> list[NetWorthEntryResponse]:
        items = self.repo.list_by_date(user.id, as_of)
        return [NetWorthEntryResponse.model_validate(e) for e in items]

    def update(self, user: User, entry_id: int, data: NetWorthEntryUpdate) -> NetWorthEntryResponse:
        entry = self._get_owned(user, entry_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(entry, field, value)
        updated = self.repo.update(entry)
        return NetWorthEntryResponse.model_validate(updated)

    def delete(self, user: User, entry_id: int) -> None:
        self.repo.delete(self._get_owned(user, entry_id))

    def get_summary(self, user: User) -> NetWorthSummary:
        entries = self.repo.get_all(user_id=user.id, limit=1000)
        assets_by_type: dict[str, float] = {}
        liabilities_by_type: dict[str, float] = {}
        total_assets = 0.0
        total_liabilities = 0.0

        for entry in entries:
            amount = float(entry.amount)
            if entry.entry_type == "asset":
                total_assets += amount
                key = entry.asset_type.value if entry.asset_type else "other"
                assets_by_type[key] = assets_by_type.get(key, 0) + amount
            else:
                total_liabilities += amount
                key = entry.liability_type.value if entry.liability_type else "other"
                liabilities_by_type[key] = liabilities_by_type.get(key, 0) + amount

        return NetWorthSummary(
            total_assets=round(total_assets, 2),
            total_liabilities=round(total_liabilities, 2),
            net_worth=round(total_assets - total_liabilities, 2),
            assets_by_type=assets_by_type,
            liabilities_by_type=liabilities_by_type,
        )

    def _get_owned(self, user: User, entry_id: int) -> NetWorthEntry:
        entry = self.repo.get_by_id(entry_id)
        if not entry or entry.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Net worth entry not found",
            )
        return entry
