from datetime import datetime
import uuid

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.sessions import Sessions as AuthSession

class SessionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        *,
        user_id: uuid.UUID,
        token_hash: str,
        expires_at: datetime,
    ) -> AuthSession:
        auth_session = AuthSession(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )

        self.db.add(auth_session)
        self.db.commit()
        self.db.refresh(auth_session)

        return auth_session

    def get_by_token_hash(
        self,
        token_hash: str,
    ) -> AuthSession | None:
        statement = select(AuthSession).where(
            AuthSession.token_hash == token_hash
        )

        return self.db.scalar(statement)

    def delete_by_token_hash(
        self,
        token_hash: str,
    ) -> None:
        statement = delete(AuthSession).where(
            AuthSession.token_hash == token_hash
        )

        self.db.execute(statement)
        self.db.commit()

