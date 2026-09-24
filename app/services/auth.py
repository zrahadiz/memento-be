from fastapi import HTTPException, status

from app.models.users import Users
from app.repositories.session import SessionRepository
from app.repositories.user import UserRepository
from app.schemas.auth import RegisterRequest, LoginRequest
from app.core.security import (
    generate_session_token,
    get_session_expiry,
    hash_password,
    hash_session_token,
    verify_password,
)

class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        session_repository: SessionRepository,
    ):
        self.user_repository = user_repository
        self.session_repository = session_repository

    def register(
        self,
        data: RegisterRequest,
    ) -> Users:
        email = data.email.strip().lower()

        existing_user = self.user_repository.get_by_email(
            email
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email is already registered",
            )

        password_hash = hash_password(
            data.password
        )

        user = self.user_repository.create(
            name=data.name,
            email=email,
            password_hash=password_hash,
        )

        return user

    def login(
        self,
        data: LoginRequest,
    ) -> str:
        email = data.email.strip().lower()

        user = self.user_repository.get_by_email(
            email
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not verify_password(
            data.password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        session_token = generate_session_token()

        token_hash = hash_session_token(
            session_token
        )

        expires_at = get_session_expiry()

        self.session_repository.create(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at,
        )

        return session_token