from fastapi import APIRouter, HTTPException
from backend.models.schemas import RawWaterInput, AnalyzeResponse
from backend.services.model_service import model_service

router = APIRouter(prefix="/api/v1", tags=["prediction"])


@router.get("/health")
def health_check():
    return {"status": "online", "message": "Water Quality API is running"}


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_water(payload: RawWaterInput):
    try:
        return model_service.predict(payload)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Processing error: {exc}")
