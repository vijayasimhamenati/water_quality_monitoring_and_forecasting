from pydantic import BaseModel, ConfigDict, Field
from typing import Dict


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

    model_config = ConfigDict(populate_by_name=True)


class ClassificationResult(BaseModel):
    status_code: int
    message: str
    confidence_safe_percent: float
    confidence_toxic_percent: float


class AnalyzeResponse(BaseModel):
    status: str
    classification: ClassificationResult
    treated_water_predictions: Dict[str, float]
