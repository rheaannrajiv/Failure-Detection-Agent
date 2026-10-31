from pydantic import BaseModel, Field
from typing import Literal

class DiagnosisRequest(BaseModel):
    description: str = Field(default="", max_length=10000)
    symptoms: list[str] = Field(default_factory=list, max_length=100)
    inspection_results: dict[str, Literal["Finding observed", "Finding not observed", "Inconclusive"]] = Field(default_factory=dict)

class DiagnosisResponse(BaseModel):
    extracted_symptoms: list[str]
    symptoms_used: list[str]
    ranked_failures: list[dict]
    next_check: str | None
    scoring_note: str

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str

class SensorAnalysisResponse(BaseModel):
    features: list[dict]
    inferred_symptoms: list[str]
    evidence_notes: list[str]
    method_note: str
