"""
PlumeDose AI™ - Medication Management Models
Revolutionary medication safety with AI-powered verification and alerts
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON, Date, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Medication(Base):
    """
    Medication Master List - All medications available in the facility
    """
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)

    # Medication details
    name = Column(String(255), nullable=False, index=True)
    generic_name = Column(String(255), nullable=True)
    brand_name = Column(String(255), nullable=True)
    drug_class = Column(String(100), nullable=True)  # antibiotic, analgesic, etc.
    controlled_substance_schedule = Column(String(10), nullable=True)  # I, II, III, IV, V

    # Dosage information
    default_dose = Column(Float, nullable=True)
    default_unit = Column(String(50), nullable=True)  # mg, mL, units, etc.
    available_routes = Column(JSON, nullable=True)  # ["oral", "IV", "IM", "SubQ"]
    available_forms = Column(JSON, nullable=True)  # ["tablet", "capsule", "injection"]

    # Safety information
    black_box_warning = Column(Boolean, default=False)
    high_alert_medication = Column(Boolean, default=False)
    requires_double_check = Column(Boolean, default=False)

    # Barcode for scanning
    barcode = Column(String(100), nullable=True, unique=True, index=True)
    ndc_code = Column(String(50), nullable=True)  # National Drug Code

    # AI-enhanced data
    common_interactions = Column(JSON, nullable=True)  # Most common drug interactions
    ai_risk_score = Column(Float, nullable=True)  # 0-100, AI-calculated risk

    # Status
    is_active = Column(Boolean, default=True, index=True)
    is_formulary = Column(Boolean, default=True)  # On facility formulary

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    facility = relationship("Facility", back_populates="medications")
    orders = relationship("MedicationOrder", back_populates="medication", cascade="all, delete-orphan")


class MedicationOrder(Base):
    """
    Medication Orders - Prescribed medications for patients
    """
    __tablename__ = "medication_orders"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    medication_id = Column(Integer, ForeignKey("medications.id", ondelete="CASCADE"), nullable=False, index=True)
    ordered_by_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Order details
    order_type = Column(String(50), nullable=False, default="routine")  # routine, stat, prn, one-time
    dose = Column(Float, nullable=False)
    dose_unit = Column(String(50), nullable=False)  # mg, mL, units
    route = Column(String(50), nullable=False)  # oral, IV, IM, SubQ, topical
    frequency = Column(String(100), nullable=False)  # q4h, BID, TID, QID, daily, PRN

    # Schedule
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=True)
    scheduled_times = Column(JSON, nullable=True)  # ["08:00", "12:00", "16:00", "20:00"]

    # PRN (as-needed) details
    is_prn = Column(Boolean, default=False)
    prn_indication = Column(Text, nullable=True)  # "for pain", "for nausea"
    prn_max_dose_24h = Column(Float, nullable=True)
    prn_min_interval_hours = Column(Float, nullable=True)

    # Special instructions
    instructions = Column(Text, nullable=True)
    food_instructions = Column(String(255), nullable=True)  # "take with food", "empty stomach"

    # Status tracking
    status = Column(String(50), nullable=False, default="active", index=True)  # active, completed, discontinued, held
    discontinue_reason = Column(Text, nullable=True)
    discontinued_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    discontinued_at = Column(DateTime(timezone=True), nullable=True)

    # AI enhancements
    ai_interaction_warnings = Column(JSON, nullable=True)  # AI-detected interactions
    ai_duplicates_detected = Column(JSON, nullable=True)  # Similar medications already prescribed
    ai_confidence_score = Column(Float, nullable=True)  # How confident AI is in safety

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    facility = relationship("Facility")
    patient = relationship("Patient", back_populates="medication_orders")
    medication = relationship("Medication", back_populates="orders")
    ordered_by = relationship("User", foreign_keys=[ordered_by_id])
    discontinued_by = relationship("User", foreign_keys=[discontinued_by_id])
    administrations = relationship("MedicationAdministration", back_populates="order", cascade="all, delete-orphan")


class MedicationAdministration(Base):
    """
    Medication Administration Records (MAR) - Track when medications are given
    """
    __tablename__ = "medication_administrations"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    order_id = Column(Integer, ForeignKey("medication_orders.id", ondelete="CASCADE"), nullable=False, index=True)
    administered_by_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Administration details
    scheduled_time = Column(DateTime(timezone=True), nullable=True)
    actual_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(50), nullable=False, default="given")  # given, refused, held, omitted

    # Dosage administered
    dose_given = Column(Float, nullable=False)
    dose_unit = Column(String(50), nullable=False)
    route_used = Column(String(50), nullable=False)

    # Verification (barcode scanning)
    barcode_scanned = Column(Boolean, default=False)
    scanned_barcode = Column(String(100), nullable=True)
    verification_method = Column(String(50), nullable=True)  # barcode, manual, override

    # Double-check for high-alert meds
    double_checked = Column(Boolean, default=False)
    double_checked_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    double_check_time = Column(DateTime(timezone=True), nullable=True)

    # Patient response
    patient_response = Column(Text, nullable=True)
    side_effects = Column(Text, nullable=True)

    # Notes
    notes = Column(Text, nullable=True)
    refusal_reason = Column(Text, nullable=True)
    hold_reason = Column(Text, nullable=True)

    # Site for injections
    injection_site = Column(String(100), nullable=True)  # "left deltoid", "right thigh"

    # AI tracking
    ai_flagged = Column(Boolean, default=False)
    ai_flag_reason = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    facility = relationship("Facility")
    patient = relationship("Patient", back_populates="medication_administrations")
    order = relationship("MedicationOrder", back_populates="administrations")
    administered_by = relationship("User", foreign_keys=[administered_by_id])
    double_checked_by = relationship("User", foreign_keys=[double_checked_by_id])


class DrugInteraction(Base):
    """
    Drug Interaction Database - Known interactions between medications
    """
    __tablename__ = "drug_interactions"

    id = Column(Integer, primary_key=True, index=True)

    # Medications involved
    medication_1_id = Column(Integer, ForeignKey("medications.id", ondelete="CASCADE"), nullable=False, index=True)
    medication_2_id = Column(Integer, ForeignKey("medications.id", ondelete="CASCADE"), nullable=False, index=True)

    # Interaction details
    severity = Column(String(50), nullable=False)  # minor, moderate, major, contraindicated
    description = Column(Text, nullable=False)
    clinical_effects = Column(Text, nullable=True)
    management = Column(Text, nullable=True)  # How to manage the interaction

    # Evidence
    evidence_level = Column(String(50), nullable=True)  # excellent, good, fair, poor
    references = Column(JSON, nullable=True)  # Literature references

    # AI enhancements
    frequency_encountered = Column(Integer, default=0)  # How often seen in practice
    ai_risk_score = Column(Float, nullable=True)  # AI-calculated risk

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


class MedicationAlert(Base):
    """
    Active Medication Alerts - Real-time alerts for medication issues
    """
    __tablename__ = "medication_alerts"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    order_id = Column(Integer, ForeignKey("medication_orders.id", ondelete="CASCADE"), nullable=True, index=True)

    # Alert details
    alert_type = Column(String(100), nullable=False)  # interaction, allergy, duplicate, overdose, missed_dose
    severity = Column(String(50), nullable=False)  # low, medium, high, critical
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)

    # Recommendation
    recommended_action = Column(Text, nullable=True)

    # Status
    status = Column(String(50), nullable=False, default="active", index=True)  # active, acknowledged, resolved, overridden
    acknowledged_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)
    resolution_notes = Column(Text, nullable=True)

    # AI generated
    ai_generated = Column(Boolean, default=False)
    ai_confidence = Column(Float, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    resolved_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    facility = relationship("Facility")
    patient = relationship("Patient")
    order = relationship("MedicationOrder")
    acknowledged_by = relationship("User")
