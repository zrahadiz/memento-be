import uuid

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.db.session import get_db
from app.models.users import Users
from app.repositories.ebook import EbookRepository
from app.schemas.ebook import (
    EbookCreate,
    EbookResponse,
    EbookUpdate,
)
from app.services.ebook import EbookService


router = APIRouter()

def get_ebook_service(
    db: Session = Depends(get_db),
) -> EbookService:
    return EbookService(
        ebook_repository=EbookRepository(db)
    )

@router.post(
    "",
    response_model=EbookResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_ebook(
    data: EbookCreate,
    current_user: Users = Depends(get_current_user),
    ebook_service: EbookService = Depends(get_ebook_service)
) -> EbookResponse:
    return ebook_service.create(
        data,
        current_user
    )

@router.get(
    "",
    response_model=list[EbookResponse],
)
def get_ebook(
    current_user: Users = Depends(get_current_user),
    ebook_service: EbookService = Depends(get_ebook_service)
) -> list[EbookResponse]:
    return ebook_service.get_all(
        current_user
    )

@router.get(
    "/{ebook_id}",
    response_model=EbookResponse,
)
def get_ebook_by_id(
    ebook_id: uuid.UUID,
    current_user: Users = Depends(get_current_user),
    ebook_service: EbookService = Depends(get_ebook_service)
) -> EbookResponse:
    return ebook_service.get_by_id(
        current_user,
        ebook_id
    )

@router.patch(
    "/{ebook_id}",
    response_model=EbookResponse,
)
def update_book(
    ebook_id: uuid.UUID,
    data: EbookUpdate,
    current_user: Users = Depends(get_current_user),
    ebook_service: EbookService = Depends(get_ebook_service)
) -> EbookResponse:
    return ebook_service.update(
        ebook_id,
        data,
        current_user,
    )

@router.delete(
    "/{ebook_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_book(
    ebook_id: uuid.UUID,
    current_user: Users = Depends(get_current_user),
    ebook_service: EbookService = Depends(get_ebook_service)
) -> Response:
    ebook_service.delete(
        ebook_id,
        current_user
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )