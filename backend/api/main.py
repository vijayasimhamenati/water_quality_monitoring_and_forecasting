from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.api.routers.predict import router as predict_router
from backend.services.model_service import model_service
from backend.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load models on startup
    model_service.load()
    yield
    # Cleanup on shutdown (if needed)
    pass


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Modern API for water quality digital twin predictions",
    lifespan=lifespan
)


app.include_router(predict_router)
