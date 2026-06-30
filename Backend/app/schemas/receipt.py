"""Receipt schemas."""

from datetime import datetime

from app.models.enums import ExpenseCategory, ReceiptStatus
from app.schemas.common import BaseSchema


class ReceiptResponse(BaseSchema):
    id: int
    user_id: int
    file_path: str
    original_filename: str
    status: ReceiptStatus
    extracted_amount: float | None
    extracted_merchant: str | None
    extracted_date: str | None
    extracted_category: ExpenseCategory | None
    created_at: datetime
    updated_at: datetime


class ReceiptProcessResponse(BaseSchema):
    receipt: ReceiptResponse
    expense_created: bool
    message: str
