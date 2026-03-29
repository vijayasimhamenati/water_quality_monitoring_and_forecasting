from fastapi.testclient import TestClient
from backend.api.main import app

client = TestClient(app)


def test_health_check():
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    assert r.json()["status"] == "online"


def test_analyze_endpoint(monkeypatch):
    # patch model_service.predict to avoid actual model artifacts
    from backend.services import model_service as service_module

    class FakeResult:
        status = "success"
        classification = type(
            "c",
            (),
            {
                "status_code": 1,
                "message": "SAFE",
                "confidence_safe_percent": 99.0,
                "confidence_toxic_percent": 1.0,
            },
        )
        treated_water_predictions = {"TW pH": 7.5}

    monkeypatch.setattr(service_module.model_service, "predict", lambda _: FakeResult())

    payload = {
        "RW pH": 7.2,
        "RW Tur": 3.4,
        "RW Colour": 15.0,
        "RW TDS": 220.0,
        "RW Iron": 0.07,
        "RW Hardness": 110.0,
        "RW S Solids": 4.2,
        "RW Aluminium": 0.02,
        "RW Chloride": 30.0,
        "RW Manganese": 0.01,
        "RW Conductivity": 420.0,
        "RW Calcium": 38.0,
        "RW Magnesium": 12.0,
        "RW Alkalinity": 95.0,
        "RW Ammonia as N": 0.05,
    }

    r = client.post("/api/v1/analyze", json=payload)
    assert r.status_code == 200
    assert r.json()["status"] == "success"
