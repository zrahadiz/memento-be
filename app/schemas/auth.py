from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    name: str | None = Field(
        default=None,
        max_length=255,
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
    )

class LoginRequest(BaseModel):
    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
    )

class LoginResponse(BaseModel):
    message: str