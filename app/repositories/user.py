import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.users import Users


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(
        self,
        email: str,
    ) -> Users | None:
        statement = select(Users).where(
            Users.email == email
        )

        return self.db.scalar(statement)

    def get_by_id(
        self,
        user_id: uuid.UUID,
    ) -> Users | None:
        return self.db.get(Users, user_id)

    def create(
        self,
        *,
        email: str,
        password_hash: str,
        name: str | None = None,
    ) -> Users:
        user = Users(
            email=email,
            password_hash=password_hash,
            name=name,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user