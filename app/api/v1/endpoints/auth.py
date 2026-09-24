from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
    Cookie
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
    MessageResponse,
    RegisterRequest,
)
from app.api.dependencies.auth import get_current_user
from app.models.users import Users

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
    response_model=MessageResponse,
)
def login(
    data: LoginRequest,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
) -> MessageResponse:
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

    return MessageResponse(
        message="Login successful"
    )

@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: Users = Depends(get_current_user),
) -> UserResponse:
    return current_user

@router.post(
    "/logout",
    response_model=MessageResponse,
)
def logout(
    response: Response,
    session_token: str | None = Cookie(
        default=None,
        alias=settings.session_cookie_name,
    ),
    auth_service: AuthService = Depends(get_auth_service),
) -> MessageResponse:
    if session_token is not None:
        auth_service.logout(session_token)

    response.delete_cookie(
        key=settings.session_cookie_name,
        path="/",
        httponly=True,
        secure=settings.session_cookie_secure,
        samesite="lax",
    )

    return MessageResponse(
        message="Logout successful"
    )