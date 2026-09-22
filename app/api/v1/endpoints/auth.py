from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.user import UserRepository
from app.schemas.auth import RegisterRequest
from app.schemas.user import UserResponse
from app.services.auth import AuthService

router = APIRouter()

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db),
) -> UserResponse:
    user_repository = UserRepository(db)

    auth_service = AuthService(
        user_repository=user_repository,
    )

    return auth_service.register(data)