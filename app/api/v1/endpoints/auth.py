from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.repositories.session import SessionRepository
from app.repositories.user import UserRepository
from app.schemas.user import UserResponse
from app.services.auth import AuthService
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
)

router = APIRouter()

def get_auth_service(
    db: Session = Depends(get_db),
) -> AuthService:
    return AuthService(
        user_repository=UserRepository(db),
        session_repository=SessionRepository(db),
    )

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    data: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    return auth_service.register(data)

@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(
    data: LoginRequest,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
) -> LoginResponse:
    session_token = auth_service.login(data)

    response.set_cookie(
        key=settings.session_cookie_name,
        value=session_token,
        httponly=True,
        secure=settings.session_cookie_secure,
        samesite="lax",
        max_age=settings.session_expire_days * 24 * 60 * 60,
        path="/",
    )

    return LoginResponse(
        message="Login successful"
    )