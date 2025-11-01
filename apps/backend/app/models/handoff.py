"""
Handoff Model
Represents a clinical handoff with SBAR report
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Handoff(Base):
    __tablename__ = "handoffs"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    assigned_to_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)

    # Handoff type
    handoff_type = Column(String(50), default="baseline")  # baseline, update
    baseline_handoff_id = Column(Integer, ForeignKey("handoffs.id"), nullable=True)

    # Voice recording
    voice_recording_url = Column(String(500), nullable=True)
    voice_recording_duration = Column(Integer, nullable=True)  # seconds
    transcription_text = Column(Text, nullable=True)

    # SBAR Report
    sbar_situation = Column(Text, nullable=True)
    sbar_background = Column(Text, nullable=True)
    sbar_assessment = Column(Text, nullable=True)
    sbar_recommendation = Column(Text, nullable=True)

    # Metadata
    status = Column(String(50), default="draft")  # draft, submitted, received, archived
    priority = Column(String(20), default="normal")  # routine, urgent, critical
    shift = Column(String(20), nullable=True)  # day, evening, night
    has_critical_alerts = Column(Boolean, default=False)
    critical_alerts = Column(JSON, nullable=True)

    # AI metadata
    ai_confidence_score = Column(Integer, nullable=True)  # 0-100
    ai_processing_time = Column(Integer, nullable=True)  # milliseconds

    # Timestamps
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    received_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    facility = relationship("Facility", back_populates="handoffs")
    patient = relationship("Patient", back_populates="handoffs")
    created_by = relationship("User", foreign_keys=[created_by_id], back_populates="handoffs_created")
    assigned_to = relationship("User", foreign_keys=[assigned_to_id], back_populates="handoffs_assigned")
    baseline_handoff = relationship("Handoff", remote_side=[id], backref="updates")
