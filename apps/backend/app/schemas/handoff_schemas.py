"""
Pydantic schemas for handoff API requests/responses
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class HandoffCreateRequest(BaseModel):
    """Request to create a new handoff"""
    patient_id: int = Field(..., description="Patient ID")
    is_baseline: bool = Field(True, description="Is this a baseline handoff or update?")


class SBARResponse(BaseModel):
    """SBAR structured response"""
    situation: str
    background: str
    assessment: str
    recommendation: str


class CriticalAlertResponse(BaseModel):
    """Critical alert detected"""
    alert_type: str
    severity: str
    confidence: float
    message: str
    recommended_actions: str


class HandoffResponse(BaseModel):
    """Handoff response"""
    id: int
    patient_id: int
    created_by_user_id: int
    is_baseline: bool
    baseline_handoff_id: Optional[int]

    # Audio
    audio_duration_seconds: Optional[int]

    # Transcription
    transcript_text: Optional[str]
    transcript_confidence: Optional[float]

    # SBAR
    sbar: Optional[SBARResponse]

    # Critical alert
    critical_alert: Optional[CriticalAlertResponse]

    # Status
    status: str
    points_earned: int

    # Timestamps
    created_at: datetime
    ai_processed_at: Optional[datetime]

    class Config:
        from_attributes = True
