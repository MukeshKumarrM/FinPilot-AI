"""Bank statement import API routes."""

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.enums import ExpenseCategory
from app.models.user import User
from app.services.statement_service import StatementService

router = APIRouter(prefix="/statements", tags=["statements"])


@router.post("/import")
async def import_statement(
    file: UploadFile = File(...),
    default_category: ExpenseCategory = ExpenseCategory.OTHER,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, int | str]:
    return await StatementService(db).import_statement(
        current_user,
        file,
        default_category=default_category,
    )
