from pydantic import BaseModel, Field
from typing import Any

class DiagnosticReportRequest(BaseModel):
    machine: str = Field(min_length=1, max_length=300)
    operating_conditions: dict[str, Any] = Field(default_factory=dict)
    symptoms: list[str] = Field(default_factory=list, max_length=50)
    findings: list[str] = Field(default_factory=list, max_length=100)
    ranked_faults: list[dict[str, Any]] = Field(default_factory=list, max_length=20)
    sensor_findings: list[str] = Field(default_factory=list, max_length=50)
    recommended_actions: list[str] = Field(default_factory=list, max_length=50)
    limitations: list[str] = Field(default_factory=list, max_length=30)
