import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

class UserResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: uuid.UUID
    name: str | None
    email: EmailStr
    email_verified: bool
    image: str | None
    created_at: datetime
    updated_at: datetime