"""Receipt upload and OCR processing service."""

import re
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.enums import ExpenseCategory, ReceiptStatus
from app.models.expense import Expense
from app.models.receipt import Receipt
from app.models.user import User
from app.repositories.expense_repository import ExpenseRepository
from app.repositories.receipt_repository import ReceiptRepository
from app.schemas.receipt import ReceiptProcessResponse, ReceiptResponse


class ReceiptService:
    def __init__(self, db: Session) -> None:
        self.repo = ReceiptRepository(db)
        self.expense_repo = ExpenseRepository(db)
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def upload(self, user: User, file: UploadFile) -> ReceiptResponse:
        if not file.filename:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No filename provided")

        ext = Path(file.filename).suffix.lower()
        if ext not in settings.ALLOWED_RECEIPT_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type not allowed. Allowed: {settings.ALLOWED_RECEIPT_EXTENSIONS}",
            )

        content = await file.read()
        max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
        if len(content) > max_bytes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File exceeds {settings.MAX_UPLOAD_SIZE_MB}MB limit",
            )

        filename = f"{uuid.uuid4().hex}{ext}"
        file_path = self.upload_dir / str(user.id) / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(content)

        receipt = Receipt(
            user_id=user.id,
            file_path=str(file_path),
            original_filename=file.filename,
            status=ReceiptStatus.PENDING,
        )
        created = self.repo.create(receipt)
        return ReceiptResponse.model_validate(created)

    def process(self, user: User, receipt_id: int, create_expense: bool = True) -> ReceiptProcessResponse:
        receipt = self._get_owned(user, receipt_id)
        raw_text = self._extract_text(receipt.file_path)
        amount, merchant, expense_date = self._parse_receipt_text(raw_text)

        receipt.raw_text = raw_text
        receipt.extracted_amount = amount
        receipt.extracted_merchant = merchant
        receipt.extracted_date = expense_date
        receipt.extracted_category = ExpenseCategory.OTHER
        receipt.status = ReceiptStatus.PROCESSED if amount else ReceiptStatus.FAILED
        updated = self.repo.update(receipt)

        expense_created = False
        if create_expense and amount:
            from datetime import date as date_cls

            parsed_date = date_cls.today()
            if expense_date:
                try:
                    parts = expense_date.split("-")
                    if len(parts) == 3:
                        parsed_date = date_cls(int(parts[0]), int(parts[1]), int(parts[2]))
                except ValueError:
                    pass

            expense = Expense(
                user_id=user.id,
                amount=amount,
                category=ExpenseCategory.OTHER,
                description=f"Receipt: {merchant or updated.original_filename}",
                merchant=merchant,
                expense_date=parsed_date,
                receipt_id=updated.id,
            )
            self.expense_repo.create(expense)
            expense_created = True

        message = "Receipt processed successfully" if amount else "Could not extract amount from receipt"
        return ReceiptProcessResponse(
            receipt=ReceiptResponse.model_validate(updated),
            expense_created=expense_created,
            message=message,
        )

    def list_receipts(self, user: User) -> list[ReceiptResponse]:
        items = self.repo.get_all(user_id=user.id, limit=200)
        return [ReceiptResponse.model_validate(r) for r in items]

    def _get_owned(self, user: User, receipt_id: int) -> Receipt:
        receipt = self.repo.get_by_id(receipt_id)
        if not receipt or receipt.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found")
        return receipt

    def _extract_text(self, file_path: str) -> str:
        path = Path(file_path)
        if not path.exists():
            return ""
        try:
            import pytesseract
            from PIL import Image

            if path.suffix.lower() == ".pdf":
                return ""
            image = Image.open(path)
            return pytesseract.image_to_string(image)
        except Exception:
            return ""

    def _parse_receipt_text(self, text: str) -> tuple[float | None, str | None, str | None]:
        if not text:
            return None, None, None

        amount = None
        amount_patterns = [
            r"(?:total|amount|grand\s*total)[:\s]*(?:₹|rs\.?|inr)?\s*([\d,]+\.?\d*)",
            r"(?:₹|rs\.?|inr)\s*([\d,]+\.?\d*)",
            r"([\d,]+\.\d{2})\s*$",
        ]
        for pattern in amount_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                try:
                    amount = float(match.group(1).replace(",", ""))
                    break
                except ValueError:
                    continue

        merchant = None
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if lines:
            merchant = lines[0][:255]

        date_match = re.search(r"(\d{4}[-/]\d{2}[-/]\d{2})", text)
        expense_date = None
        if date_match:
            expense_date = date_match.group(1).replace("/", "-")

        return amount, merchant, expense_date
