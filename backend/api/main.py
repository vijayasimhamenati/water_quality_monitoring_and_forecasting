from fastapi import FastAPI
from backend.api.routers.predict import router as predict_router
from backend.services.model_service import model_service
from backend.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Modern API for water quality digital twin predictions"
)


@app.on_event("startup")
def startup_event():
    model_service.load()


@app.on_event("shutdown")
def shutdown_event():
    # Add cleanup actions if models or external resources are used.
    pass


app.include_router(predict_router)
