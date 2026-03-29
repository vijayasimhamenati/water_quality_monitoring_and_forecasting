from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
import pandas as pd
import joblib
import os

# ==========================================
# 1. LIFESPAN MANAGEMENT (Memory-Safe Loading)
# ==========================================
# This dictionary will hold our AI brains in memory while the server runs
ml_components = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # We use ../models/ because main.py is inside the backend/ folder
        # Load Regression Components (Treated Water Predictor)
        ml_components["tw_scaler"] = joblib.load("../models/tw_scaler.pkl")
        ml_components["tw_predictor"] = joblib.load("../models/tw_predictor.pkl")
        
        # Load Classification Components (Zero-Fail Early Warning)
        ml_components["rw_scaler"] = joblib.load("../models/rw_classifier_scaler.pkl")
        ml_components["rw_classifier"] = joblib.load("../models/rw_classifier.pkl")
        
        print("✅ All AI Models & Scalers loaded into memory successfully.")
    except Exception as e:
        print(f"❌ ERROR LOADING MODELS: {e}")
        print("Make sure your 4 .pkl files are safely inside a 'models' folder located one level above the 'backend' folder.")
        
    yield
    # Clean up memory when the server shuts down
    ml_components.clear()
    print("🛑 Server shutting down, memory cleared.")

# Backward-compatibility shim: redirect to new structured API package
from backend.api.main import app

# ==========================================
# 2. DATA VALIDATION (Pydantic Schema)
# ==========================================
# We use aliases so the JSON keys map directly to your exact dataset column names
class RawWaterInput(BaseModel):
    rw_ph: float = Field(..., alias="RW pH")
    rw_tur: float = Field(..., alias="RW Tur")
    rw_colour: float = Field(..., alias="RW Colour")
    rw_tds: float = Field(..., alias="RW TDS")
    rw_iron: float = Field(..., alias="RW Iron")
    rw_hardness: float = Field(..., alias="RW Hardness")
    rw_s_solids: float = Field(..., alias="RW S Solids")
    rw_aluminium: float = Field(..., alias="RW Aluminium")
    rw_chloride: float = Field(..., alias="RW Chloride")
    rw_manganese: float = Field(..., alias="RW Manganese")
    rw_conductivity: float = Field(..., alias="RW Conductivity")
    rw_calcium: float = Field(..., alias="RW Calcium")
    rw_magnesium: float = Field(..., alias="RW Magnesium")
    rw_alkalinity: float = Field(..., alias="RW Alkalinity")
    rw_ammonia: float = Field(..., alias="RW Ammonia as N")

# ==========================================
# 3. ENDPOINTS
# ==========================================
@app.get("/")
def health_check():
    return {"status": "online", "message": "Digital Twin API is running."}

@app.post("/analyze")
def analyze_water(payload: RawWaterInput):
    try:
        # 1. Convert incoming validated JSON into a Dictionary
        input_data = payload.model_dump(by_alias=True)
        
        # 2. Convert to Pandas DataFrame
        df_input = pd.DataFrame([input_data])
        
        # ---------------------------------------------------------
        # TASK A: CLASSIFICATION (Is it Toxic?)
        # ---------------------------------------------------------
        rw_scaler = ml_components.get("rw_scaler")
        rw_classifier = ml_components.get("rw_classifier")
        
        if not rw_scaler or not rw_classifier:
             raise Exception("Classification models are not loaded in memory.")
        
        # Scale the data
        df_class_scaled = rw_scaler.transform(df_input)
        
        # Get the hard prediction (0 or 1)
        safety_prediction = rw_classifier.predict(df_class_scaled)[0]
        safety_status = "SAFE" if safety_prediction == 1 else "TOXIC (ACTION REQUIRED)"
        
        # NEW: Get the exact percentage of confidence!
        # predict_proba returns an array like [[Probability of 0, Probability of 1]]
        probabilities = rw_classifier.predict_proba(df_class_scaled)[0]
        prob_toxic = round(probabilities[0] * 100, 2)
        prob_safe = round(probabilities[1] * 100, 2)
        
        # ---------------------------------------------------------
        # TASK B: REGRESSION (Predicting Treated Water Metrics)
        # ---------------------------------------------------------
        tw_scaler = ml_components.get("tw_scaler")
        tw_predictor = ml_components.get("tw_predictor")
        
        if not tw_scaler or not tw_predictor:
             raise Exception("Regression models are not loaded in memory.")
        
        # Scale and Predict
        df_reg_scaled = tw_scaler.transform(df_input)
        tw_predictions = tw_predictor.predict(df_reg_scaled)[0]
        
        # Map the 16 output array values back to their specific TW names
        tw_columns = [
            "TW pH", "TW Tur", "TW FRC", "TW Colour", "TW TDS", "TW Iron", 
            "TW Hardness", "TW S Solids", "TW Aluminium", "TW Chloride", 
            "TW Manganese", "TW Conductivity", "TW Calcium", "TW Magnesium", 
            "TW Alkalinity", "TW Ammonia as N"
        ]
        
        predicted_metrics = {col: round(float(val), 4) for col, val in zip(tw_columns, tw_predictions)}

        # ---------------------------------------------------------
        # RETURN MASTER DASHBOARD RESPONSE
        # ---------------------------------------------------------
        return {
            "status": "success",
            "classification": {
                "status_code": int(safety_prediction),
                "message": safety_status,
                "confidence_safe_percent": prob_safe,
                "confidence_toxic_percent": prob_toxic
            },
            "treated_water_predictions": predicted_metrics
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Processing Error: {str(e)}")