import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ebooks import Ebooks

class EbookRepository:
    def __init__(self, db: Session):
            self.db = db

    def create(
        self,
        *,
        user_id: uuid.UUID,
        title: str,
        description: str | None = None,
        subject: str | None = None,
        topic: str | None = None,
    ) -> Ebooks:
        ebook = Ebooks(
            user_id=user_id,
            title=title,
            description=description,
            subject=subject,
            topic=topic,
        )

        self.db.add(ebook)
        self.db.commit()
        self.db.refresh(ebook)

        return ebook

    def get_all_by_user(
        self,
        user_id: uuid.UUID,
    ) -> list[Ebooks]:
        statement = (
            select(Ebooks)
            .where(Ebooks.user_id == user_id)
            .order_by(Ebooks.updated_at.desc())
        )

        return list(
            self.db.scalars(statement).all()
        )

    def get_by_id_and_user(
        self,
        ebook_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> Ebooks | None:
        statement = select(Ebooks).where(
            Ebooks.id == ebook_id,
            Ebooks.user_id == user_id,
        )

        return self.db.scalar(statement)

    def update(
        self,
        ebook: Ebooks,
        data: dict,
    ) -> Ebooks:
        for field, value in data.items():
            setattr(ebook, field, value)

        self.db.commit()
        self.db.refresh(ebook)

        return ebook

    def delete(
        self,
        ebook: Ebooks,
    ) -> None:
        self.db.delete(ebook)
        self.db.commit()