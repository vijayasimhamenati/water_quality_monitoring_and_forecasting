import pytest

from backend.services.model_service import model_service
from backend.models.schemas import RawWaterInput


class DummyScaler:
    def transform(self, X):
        return X


class DummyClassifier:
    def predict(self, X):
        return [1]

    def predict_proba(self, X):
        return [[0.1, 0.9]]


class DummyRegressor:
    def predict(self, X):
        # 16 outputs to align TW columns
        return [[1.0] * 16]


@pytest.fixture(autouse=True)
def setup_dummy_models(monkeypatch):
    model_service.rw_scaler = DummyScaler()
    model_service.rw_classifier = DummyClassifier()
    model_service.tw_scaler = DummyScaler()
    model_service.tw_predictor = DummyRegressor()
    yield
    # cleanup after test
    model_service.rw_scaler = None
    model_service.rw_classifier = None
    model_service.tw_scaler = None
    model_service.tw_predictor = None


def test_predict_success():
    payload = RawWaterInput(**{
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
        "RW Ammonia as N": 0.05
    })

    response = model_service.predict(payload)

    assert response.status == "success"
    assert response.classification.status_code == 1
    assert response.classification.confidence_safe_percent == 90.0
    assert len(response.treated_water_predictions) == 16
