from fastapi import APIRouter

from app.api.v1.endpoints import health, auth, ebook


api_router = APIRouter()

api_router.include_router(
    health.router,
    prefix="/health",
    tags=["Health"],
)

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"],
)

api_router.include_router(
    ebook.router,
    prefix="/ebooks",
    tags=["Ebooks"],
)