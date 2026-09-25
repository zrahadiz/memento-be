import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.ebooks import EbookStatus


class EbookCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255,
    )

    description: str | None = None

    subject: str | None = Field(
        default=None,
        max_length=255,
    )

    topic: str | None = Field(
        default=None,
        max_length=255,
    )


class EbookUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    description: str | None = None

    subject: str | None = Field(
        default=None,
        max_length=255,
    )

    topic: str | None = Field(
        default=None,
        max_length=255,
    )


class EbookResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: uuid.UUID
    title: str
    description: str | None
    subject: str | None
    topic: str | None
    cover_image_url: str | None
    status: EbookStatus
    created_at: datetime
    updated_at: datetime