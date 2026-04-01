from fastapi import APIRouter, HTTPException
from backend.models.schemas import RawWaterInput, AnalyzeResponse, LiveDashboardResponse, LiveSensorData
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


@router.get("/live-dashboard", response_model=LiveDashboardResponse)
def get_live_dashboard_data():
    """Get live sensor data for dashboard display"""
    try:
        return model_service.get_live_dashboard_data()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Live data error: {exc}")


@router.get("/live-sensor", response_model=LiveSensorData)
def get_live_sensor_reading():
    """Get one live sensor reading (looping through RW dataset)"""
    try:
        return model_service.get_live_sensor_reading()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Live sensor error: {exc}")
