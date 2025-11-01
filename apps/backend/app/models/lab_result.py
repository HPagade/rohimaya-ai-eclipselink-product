"""
FeatherSight AI™ - Lab Intelligence Models
AI-powered lab result analysis with trend detection and critical value alerts
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class LabResult(Base):
    """
    Lab Results - Individual test results
    """
    __tablename__ = "lab_results"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)

    # Test identification
    test_name = Column(String(255), nullable=False, index=True)
    test_code = Column(String(100), nullable=True)  # LOINC code
    panel_id = Column(Integer, ForeignKey("lab_panels.id"), nullable=True, index=True)

    # Result
    value = Column(String(255), nullable=False)
    numeric_value = Column(Float, nullable=True)  # For numeric results
    unit = Column(String(50), nullable=True)

    # Reference range
    reference_min = Column(Float, nullable=True)
    reference_max = Column(Float, nullable=True)
    reference_range_text = Column(String(255), nullable=True)

    # Flags
    is_abnormal = Column(Boolean, default=False)
    abnormal_flag = Column(String(50), nullable=True)  # high, low, critical_high, critical_low
    is_critical = Column(Boolean, default=False)
    is_delta_check = Column(Boolean, default=False)  # Significant change from previous

    # Timing
    collection_date = Column(DateTime(timezone=True), nullable=False)
    result_date = Column(DateTime(timezone=True), nullable=False)
    reported_date = Column(DateTime(timezone=True), nullable=True)

    # Ordering
    ordered_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    ordering_provider = Column(String(255), nullable=True)

    # Lab details
    performing_lab = Column(String(255), nullable=True)
    specimen_type = Column(String(100), nullable=True)  # blood, urine, csf, etc.

    # AI analysis
    ai_trend_analysis = Column(JSON, nullable=True)  # Trend over time
    ai_clinical_significance = Column(Text, nullable=True)  # What does this mean?
    ai_recommended_actions = Column(JSON, nullable=True)
    ai_related_diagnoses = Column(JSON, nullable=True)  # Possible conditions

    # Status
    status = Column(String(50), nullable=False, default="final")  # preliminary, final, corrected
    reviewed = Column(Boolean, default=False)
    reviewed_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)

    # Notes
    notes = Column(Text, nullable=True)
    interpretation = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    facility = relationship("Facility")
    patient = relationship("Patient", back_populates="lab_results")
    panel = relationship("LabPanel", back_populates="results")
    ordered_by = relationship("User", foreign_keys=[ordered_by_id])
    reviewed_by = relationship("User", foreign_keys=[reviewed_by_id])


class LabPanel(Base):
    """
    Lab Panels - Groups of related tests (e.g., CBC, BMP, CMP)
    """
    __tablename__ = "lab_panels"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)

    # Panel details
    panel_name = Column(String(255), nullable=False)  # "Complete Blood Count", "Basic Metabolic Panel"
    panel_code = Column(String(100), nullable=True)

    # Timing
    collection_date = Column(DateTime(timezone=True), nullable=False)
    result_date = Column(DateTime(timezone=True), nullable=True)

    # Ordering
    ordered_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Status
    status = Column(String(50), nullable=False, default="pending")  # pending, complete, partial
    all_results_received = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    facility = relationship("Facility")
    patient = relationship("Patient")
    ordered_by = relationship("User")
    results = relationship("LabResult", back_populates="panel")


class CriticalValue(Base):
    """
    Critical Value Alerts - Life-threatening lab results
    """
    __tablename__ = "critical_values"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    lab_result_id = Column(Integer, ForeignKey("lab_results.id", ondelete="CASCADE"), nullable=False, index=True)

    # Alert details
    test_name = Column(String(255), nullable=False)
    critical_value = Column(String(255), nullable=False)
    severity = Column(String(50), nullable=False)  # critical, life_threatening

    # Notification
    provider_notified = Column(Boolean, default=False)
    notified_provider_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    notification_time = Column(DateTime(timezone=True), nullable=True)
    notification_method = Column(String(50), nullable=True)  # phone, page, ehr_alert

    # Read-back verification
    read_back_completed = Column(Boolean, default=False)
    read_back_by = Column(String(255), nullable=True)
    read_back_time = Column(DateTime(timezone=True), nullable=True)

    # Response
    action_taken = Column(Text, nullable=True)
    action_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action_time = Column(DateTime(timezone=True), nullable=True)

    # Status
    status = Column(String(50), nullable=False, default="pending")  # pending, notified, acknowledged, resolved

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    facility = relationship("Facility")
    patient = relationship("Patient")
    lab_result = relationship("LabResult")
    notified_provider = relationship("User", foreign_keys=[notified_provider_id])
    action_by = relationship("User", foreign_keys=[action_by_id])
