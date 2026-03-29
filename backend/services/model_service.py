from pathlib import Path
import pandas as pd
import joblib
from typing import Dict

from backend.config import settings
from backend.models.schemas import RawWaterInput, ClassificationResult, AnalyzeResponse


class ModelService:
    def __init__(self):
        self.rw_scaler = None
        self.rw_classifier = None
        self.tw_scaler = None
        self.tw_predictor = None

    def load(self):
        base = Path(settings.model_base_path)
        self.rw_scaler = joblib.load(base / settings.rw_scaler_file)
        self.rw_classifier = joblib.load(base / settings.rw_classifier_file)
        self.tw_scaler = joblib.load(base / settings.tw_scaler_file)
        self.tw_predictor = joblib.load(base / settings.tw_predictor_file)

    def predict(self, input_data: RawWaterInput) -> AnalyzeResponse:
        if self.rw_scaler is None or self.rw_classifier is None:
            raise RuntimeError("Classification model components are not loaded")
        if self.tw_scaler is None or self.tw_predictor is None:
            raise RuntimeError("Regression model components are not loaded")

        df_input = pd.DataFrame([input_data.model_dump(by_alias=True)])

        # Classification path
        scaled_rw = self.rw_scaler.transform(df_input)
        rw_pred = self.rw_classifier.predict(scaled_rw)[0]
        proba = self.rw_classifier.predict_proba(scaled_rw)[0]

        classification = ClassificationResult(
            status_code=int(rw_pred),
            message="SAFE" if rw_pred == 1 else "TOXIC (ACTION REQUIRED)",
            confidence_safe_percent=round(float(proba[1] * 100), 2),
            confidence_toxic_percent=round(float(proba[0] * 100), 2),
        )

        # Regression path
        scaled_tw = self.tw_scaler.transform(df_input)
        tw_preds = self.tw_predictor.predict(scaled_tw)[0]

        tw_columns = [
            "TW pH", "TW Tur", "TW FRC", "TW Colour", "TW TDS", "TW Iron",
            "TW Hardness", "TW S Solids", "TW Aluminium", "TW Chloride",
            "TW Manganese", "TW Conductivity", "TW Calcium", "TW Magnesium",
            "TW Alkalinity", "TW Ammonia as N"
        ]

        treated_metrics: Dict[str, float] = {
            col: round(float(val), 4) for col, val in zip(tw_columns, tw_preds)
        }

        return AnalyzeResponse(
            status="success",
            classification=classification,
            treated_water_predictions=treated_metrics
        )


model_service = ModelService()
