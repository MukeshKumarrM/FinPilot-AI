"""Bank statement import and parsing service."""

import io
from datetime import date, datetime

import pandas as pd
from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.models.enums import ExpenseCategory
from app.models.expense import Expense
from app.models.user import User
from app.repositories.expense_repository import ExpenseRepository


class StatementService:
    COLUMN_ALIASES = {
        "date": ["date", "transaction date", "txn date", "value date"],
        "amount": ["amount", "debit", "withdrawal", "transaction amount"],
        "description": ["description", "narration", "particulars", "remarks"],
    }

    def __init__(self, db: Session) -> None:
        self.expense_repo = ExpenseRepository(db)

    async def import_statement(
        self,
        user: User,
        file: UploadFile,
        *,
        default_category: ExpenseCategory = ExpenseCategory.OTHER,
    ) -> dict[str, int | str]:
        if not file.filename:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No filename provided")

        content = await file.read()
        ext = file.filename.rsplit(".", 1)[-1].lower()

        try:
            if ext in ("xlsx", "xls"):
                df = pd.read_excel(io.BytesIO(content))
            elif ext == "csv":
                df = pd.read_csv(io.BytesIO(content))
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Supported formats: csv, xlsx, xls",
                )
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to parse file: {exc}",
            ) from exc

        col_map = self._map_columns(df.columns.tolist())
        if "amount" not in col_map:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not find amount column in statement",
            )

        imported = 0
        skipped = 0

        for _, row in df.iterrows():
            try:
                amount = abs(float(row[col_map["amount"]]))
                if amount <= 0:
                    skipped += 1
                    continue

                expense_date = date.today()
                if "date" in col_map and pd.notna(row[col_map["date"]]):
                    expense_date = self._parse_date(row[col_map["date"]])

                description = None
                if "description" in col_map and pd.notna(row[col_map["description"]]):
                    description = str(row[col_map["description"]])[:500]

                expense = Expense(
                    user_id=user.id,
                    amount=amount,
                    category=default_category,
                    description=description,
                    expense_date=expense_date,
                    payment_method="bank_transfer",
                )
                self.expense_repo.create(expense)
                imported += 1
            except (ValueError, TypeError):
                skipped += 1

        return {
            "imported": imported,
            "skipped": skipped,
            "message": f"Imported {imported} transactions, skipped {skipped}",
        }

    def _map_columns(self, columns: list[str]) -> dict[str, str]:
        col_map: dict[str, str] = {}
        normalized = {c: c.lower().strip() for c in columns}
        for field, aliases in self.COLUMN_ALIASES.items():
            for col, norm in normalized.items():
                if norm in aliases:
                    col_map[field] = col
                    break
        return col_map

    @staticmethod
    def _parse_date(value: object) -> date:
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        parsed = pd.to_datetime(str(value), errors="coerce")
        if pd.isna(parsed):
            return date.today()
        return parsed.date()
