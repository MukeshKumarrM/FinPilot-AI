"""Admin API routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_active_admin, get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserResponse
from app.schemas.common import MessageResponse

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=list[UserResponse])
def list_users(
    skip: int = 0,
    limit: int = 100,
    _: User = Depends(get_current_active_admin),
    db: Session = Depends(get_db),
) -> list[UserResponse]:
    users = UserRepository(db).list_all(skip=skip, limit=limit)
    return [UserResponse.model_validate(u) for u in users]


@router.patch("/users/{user_id}/deactivate", response_model=MessageResponse)
def deactivate_user(
    user_id: int,
    admin: User = Depends(get_current_active_admin),
    db: Session = Depends(get_db),
) -> MessageResponse:
    repo = UserRepository(db)
    user = repo.get_by_id(user_id)
    if not user:
        from fastapi import HTTPException, status

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.id == admin.id:
        from fastapi import HTTPException, status

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate your own account",
        )
    user.is_active = False
    repo.update(user)
    return MessageResponse(message="User deactivated")


@router.patch("/users/{user_id}/activate", response_model=MessageResponse)
def activate_user(
    user_id: int,
    _: User = Depends(get_current_active_admin),
    db: Session = Depends(get_db),
) -> MessageResponse:
    repo = UserRepository(db)
    user = repo.get_by_id(user_id)
    if not user:
        from fastapi import HTTPException, status

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.is_active = True
    repo.update(user)
    return MessageResponse(message="User activated")
