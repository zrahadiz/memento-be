from fastapi import HTTPException, status

from app.core.security import hash_password
from app.models.users import Users
from app.repositories.user import UserRepository
from app.schemas.auth import RegisterRequest


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
    ):
        self.user_repository = user_repository

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