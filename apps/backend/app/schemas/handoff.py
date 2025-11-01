"""
Handoff Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime


class HandoffCreate(BaseModel):
    patient_id: int
    assigned_to_id: Optional[int] = None
    handoff_type: str = "baseline"  # baseline, update
    baseline_handoff_id: Optional[int] = None
    voice_recording_url: Optional[str] = None
    voice_recording_duration: Optional[int] = None
    transcription_text: Optional[str] = None
    sbar_situation: Optional[str] = None
    sbar_background: Optional[str] = None
    sbar_assessment: Optional[str] = None
    sbar_recommendation: Optional[str] = None
    priority: str = "normal"  # routine, urgent, critical
    shift: Optional[str] = None


class HandoffUpdate(BaseModel):
    assigned_to_id: Optional[int] = None
    transcription_text: Optional[str] = None
    sbar_situation: Optional[str] = None
    sbar_background: Optional[str] = None
    sbar_assessment: Optional[str] = None
    sbar_recommendation: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None


class HandoffResponse(BaseModel):
    id: int
    facility_id: int
    patient_id: int
    created_by_id: int
    assigned_to_id: Optional[int]
    handoff_type: str
    baseline_handoff_id: Optional[int]
    voice_recording_url: Optional[str]
    voice_recording_duration: Optional[int]
    transcription_text: Optional[str]
    sbar_situation: Optional[str]
    sbar_background: Optional[str]
    sbar_assessment: Optional[str]
    sbar_recommendation: Optional[str]
    status: str
    priority: str
    shift: Optional[str]
    has_critical_alerts: bool
    critical_alerts: Optional[Dict]
    ai_confidence_score: Optional[int]
    ai_processing_time: Optional[int]
    submitted_at: Optional[datetime]
    received_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    # Related data
    patient_name: Optional[str] = None
    created_by_name: Optional[str] = None
    assigned_to_name: Optional[str] = None

    class Config:
        from_attributes = True


class HandoffList(BaseModel):
    handoffs: List[HandoffResponse]
    total: int
    page: int
    page_size: int
