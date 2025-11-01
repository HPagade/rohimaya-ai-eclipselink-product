"""
PhoenixBreath AI™ - Respiratory Monitoring Models
AI-powered respiratory monitoring with predictive alerts
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class RespiratoryVital(Base):
    """
    Respiratory Vitals - Tracking oxygen saturation, respiratory rate, etc.
    """
    __tablename__ = "respiratory_vitals"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    recorded_by_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Vital signs
    spo2 = Column(Float, nullable=True)  # Oxygen saturation %
    respiratory_rate = Column(Integer, nullable=True)  # Breaths per minute
    oxygen_device = Column(String(100), nullable=True)  # room_air, nasal_cannula, simple_mask, non_rebreather, bipap, ventilator
    oxygen_flow_rate = Column(Float, nullable=True)  # Liters per minute
    fio2 = Column(Float, nullable=True)  # Fraction of inspired oxygen %

    # Assessment
    breath_sounds = Column(String(100), nullable=True)  # clear, crackles, wheezes, diminished
    respiratory_effort = Column(String(50), nullable=True)  # normal, labored, shallow
    use_of_accessory_muscles = Column(Boolean, default=False)
    cough = Column(Boolean, default=False)
    cough_type = Column(String(50), nullable=True)  # productive, nonproductive

    # Symptoms
    shortness_of_breath = Column(Boolean, default=False)
    dyspnea_scale = Column(Integer, nullable=True)  # 0-10
    chest_pain = Column(Boolean, default=False)
    cyanosis = Column(Boolean, default=False)

    # AI analysis
    ai_respiratory_distress_score = Column(Float, nullable=True)  # 0-100
    ai_trend_analysis = Column(JSON, nullable=True)
    ai_alerts = Column(JSON, nullable=True)
    ai_intervention_suggested = Column(JSON, nullable=True)

    # Timestamp
    recorded_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    facility = relationship("Facility")
    patient = relationship("Patient", back_populates="respiratory_vitals")
    recorded_by = relationship("User")


class VentilatorSetting(Base):
    """
    Ventilator Settings - For intubated patients
    """
    __tablename__ = "ventilator_settings"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    recorded_by_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Vent mode
    mode = Column(String(100), nullable=False)  # AC, SIMV, PSV, CPAP

    # Settings
    tidal_volume = Column(Float, nullable=True)  # mL
    respiratory_rate_set = Column(Integer, nullable=True)
    peep = Column(Float, nullable=True)  # Positive end-expiratory pressure
    fio2_set = Column(Float, nullable=True)
    pressure_support = Column(Float, nullable=True)
    peak_inspiratory_pressure = Column(Float, nullable=True)

    # Measured values
    minute_ventilation = Column(Float, nullable=True)
    peak_pressure = Column(Float, nullable=True)
    plateau_pressure = Column(Float, nullable=True)

    # Timestamp
    recorded_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    facility = relationship("Facility")
    patient = relationship("Patient")
    recorded_by = relationship("User")


class ABGResult(Base):
    """
    Arterial Blood Gas Results
    """
    __tablename__ = "abg_results"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)

    # ABG values
    ph = Column(Float, nullable=True)
    paco2 = Column(Float, nullable=True)  # mmHg
    pao2 = Column(Float, nullable=True)  # mmHg
    hco3 = Column(Float, nullable=True)  # mEq/L
    base_excess = Column(Float, nullable=True)
    sao2 = Column(Float, nullable=True)  # %

    # Calculated
    pao2_fio2_ratio = Column(Float, nullable=True)  # P/F ratio

    # Interpretation
    acid_base_status = Column(String(100), nullable=True)  # normal, acidosis, alkalosis
    oxygenation_status = Column(String(100), nullable=True)

    # AI analysis
    ai_interpretation = Column(Text, nullable=True)
    ai_clinical_significance = Column(Text, nullable=True)

    # Timing
    collection_date = Column(DateTime(timezone=True), nullable=False)
    result_date = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    facility = relationship("Facility")
    patient = relationship("Patient")
