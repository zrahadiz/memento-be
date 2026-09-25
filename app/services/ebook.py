import uuid

from fastapi import HTTPException, status

from app.models.ebooks import Ebooks
from app.models.users import Users
from app.repositories.ebook import EbookRepository
from app.schemas.ebook import EbookCreate, EbookUpdate


class EbookService:
    def __init__(
        self,
        ebook_repository: EbookRepository,
    ):
        self.ebook_repository = ebook_repository

    def create(
        self,
        data: EbookCreate,
        current_user: Users,
    ) -> Ebooks:
        return self.ebook_repository.create(
            user_id=current_user.id,
            title=data.title,
            description=data.description,
            subject=data.subject,
            topic=data.topic,
        )

    def get_all(
        self,
        current_user: Users,
    ) -> list[Ebooks]:
        return self.ebook_repository.get_all_by_user(
            current_user.id
        )

    def get_by_id(
        self,
        current_user: Users,
        ebook_id: uuid.UUID,
    ) -> Ebooks | None:
        ebook = self.ebook_repository.get_by_id_and_user(
            ebook_id=ebook_id,
            user_id=current_user.id
        )

        if ebook is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ebook not found"
            )

        return ebook

    def update(
        self,
        ebook_id: uuid.UUID,
        data: EbookUpdate,
        current_user: Users,
    ) -> Ebooks:
        ebook = self.get_by_id(
            current_user,
            ebook_id
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        return self.ebook_repository.update(
            ebook,
            update_data
        )

    def delete(
        self,
        ebook_id: uuid.UUID,
        current_user: Users,
    ) -> None:
        ebook = self.get_by_id(
            current_user,
            ebook_id
        )

        self.ebook_repository.delete(ebook)

        
