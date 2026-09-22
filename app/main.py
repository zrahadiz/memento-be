from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings

from app.db.base import Base
import app.models

print(Base.metadata.tables.keys())

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

app.include_router(
    api_router,
    prefix="/api/v1",
)


@app.get("/")
def root():
    return {
        "message": f"{settings.app_name} API"
    }