from pathlib import Path
import pandas as pd
import joblib
from typing import Dict, List
import datetime
import random

from backend.config import settings
from backend.models.schemas import RawWaterInput, ClassificationResult, AnalyzeResponse, LiveSensorData, LiveDashboardResponse


class ModelService:
    def __init__(self):
        self.rw_scaler = None
        self.rw_classifier = None
        self.tw_scaler = None
        self.tw_predictor = None
        self.rw_data = None
        self.current_index = 0
        self.recent_readings: List[LiveSensorData] = []

    def load(self):
        base = Path(settings.model_base_path)
        self.rw_scaler = joblib.load(base / settings.rw_scaler_file)
        self.rw_classifier = joblib.load(base / settings.rw_classifier_file)
        self.tw_scaler = joblib.load(base / settings.tw_scaler_file)
        self.tw_predictor = joblib.load(base / settings.tw_predictor_file)

        # Load RW classification data for live simulation
        data_base = Path(__file__).parent.parent.parent / settings.data_base_path
        data_path = data_base / "rw_classification_data.csv"
        self.rw_data = pd.read_csv(data_path)

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

    def get_live_sensor_reading(self) -> LiveSensorData:
        """Get next sensor reading from RW classification data in loop"""
        if self.rw_data is None:
            raise RuntimeError("RW classification data not loaded")

        # Get current row, loop back to start if at end
        if self.current_index >= len(self.rw_data):
            self.current_index = 0

        row = self.rw_data.iloc[self.current_index]
        self.current_index += 1

        # Extract RW metrics
        rw_metrics = {
            "RW pH": float(row["RW pH"]),
            "RW Tur": float(row["RW Tur"]),
            "RW Colour": float(row["RW Colour"]),
            "RW TDS": float(row["RW TDS"]),
            "RW Iron": float(row["RW Iron"]),
            "RW Hardness": float(row["RW Hardness"]),
            "RW S Solids": float(row["RW S Solids"]),
            "RW Aluminium": float(row["RW Aluminium"]),
            "RW Chloride": float(row["RW Chloride"]),
            "RW Manganese": float(row["RW Manganese"]),
            "RW Conductivity": float(row["RW Conductivity"]),
            "RW Calcium": float(row["RW Calcium"]),
            "RW Magnesium": float(row["RW Magnesium"]),
            "RW Alkalinity": float(row["RW Alkalinity"]),
            "RW Ammonia as N": float(row["RW Ammonia as N"])
        }

        # Create RawWaterInput from the metrics
        input_data = RawWaterInput(**rw_metrics)

        # Get prediction
        prediction = self.predict(input_data)

        # Create LiveSensorData
        live_data = LiveSensorData(
            timestamp=datetime.datetime.now(),
            raw_water_metrics=rw_metrics,
            classification=prediction.classification,
            treated_water_predictions=prediction.treated_water_predictions
        )

        # Store in recent readings (keep last 60 readings for 1 hour of data)
        self.recent_readings.append(live_data)
        if len(self.recent_readings) > 60:
            self.recent_readings.pop(0)

        return live_data

    def get_live_dashboard_data(self) -> LiveDashboardResponse:
        """Get current reading and recent readings for live dashboard"""
        current_reading = self.get_live_sensor_reading()

        return LiveDashboardResponse(
            status="success",
            current_reading=current_reading,
            recent_readings=self.recent_readings[-10:]  # Last 10 readings
        )


model_service = ModelService()
