"""Receipt API routes."""

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.receipt import ReceiptProcessResponse, ReceiptResponse
from app.services.receipt_service import ReceiptService

router = APIRouter(prefix="/receipts", tags=["receipts"])


@router.post("/upload", response_model=ReceiptResponse, status_code=201)
async def upload_receipt(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ReceiptResponse:
    return await ReceiptService(db).upload(current_user, file)


@router.get("", response_model=list[ReceiptResponse])
def list_receipts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[ReceiptResponse]:
    return ReceiptService(db).list_receipts(current_user)


@router.post("/{receipt_id}/process", response_model=ReceiptProcessResponse)
def process_receipt(
    receipt_id: int,
    create_expense: bool = True,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ReceiptProcessResponse:
    return ReceiptService(db).process(current_user, receipt_id, create_expense)
