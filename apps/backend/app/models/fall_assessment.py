"""
RiseGuard AI™ - Fall Prevention Models
AI-powered fall prevention with predictive analytics and real-time monitoring
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class FallAssessment(Base):
    """
    Fall Risk Assessments - Morse Fall Scale and AI-enhanced predictions
    """
    __tablename__ = "fall_assessments"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    assessed_by_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Morse Fall Scale Scoring (Standard)
    history_of_falling = Column(Integer, nullable=False, default=0)  # 0 or 25 points
    secondary_diagnosis = Column(Integer, nullable=False, default=0)  # 0 or 15 points
    ambulatory_aid = Column(Integer, nullable=False, default=0)  # 0, 15, or 30 points
    iv_heparin_lock = Column(Integer, nullable=False, default=0)  # 0 or 20 points
    gait_transfer = Column(Integer, nullable=False, default=0)  # 0, 10, or 20 points
    mental_status = Column(Integer, nullable=False, default=0)  # 0 or 15 points

    # Total Morse score
    morse_score = Column(Integer, nullable=False, default=0)  # Sum of above
    morse_risk_level = Column(String(50), nullable=False)  # low (0-24), moderate (25-50), high (51+)

    # AI-Enhanced Scoring (Revolutionary!)
    ai_risk_score = Column(Float, nullable=True)  # 0-100, AI-calculated using ALL patient data
    ai_risk_factors = Column(JSON, nullable=True)  # AI-identified risk factors
    ai_confidence = Column(Float, nullable=True)  # How confident AI is in assessment

    # Additional risk factors
    age = Column(Integer, nullable=True)
    medications_increasing_risk = Column(JSON, nullable=True)  # Sedatives, antihypertensives, etc.
    environmental_risks = Column(JSON, nullable=True)  # From environmental assessment
    recent_lab_abnormalities = Column(JSON, nullable=True)  # Low BP, anemia, etc.

    # Patient-specific factors
    vision_impairment = Column(Boolean, default=False)
    hearing_impairment = Column(Boolean, default=False)
    incontinence = Column(Boolean, default=False)
    orthostatic_hypotension = Column(Boolean, default=False)
    confusion = Column(Boolean, default=False)

    # Interventions in place
    interventions = Column(JSON, nullable=True)  # ["bed alarm", "fall mat", "hourly rounding"]
    bed_alarm_active = Column(Boolean, default=False)
    fall_mat_in_use = Column(Boolean, default=False)
    call_light_in_reach = Column(Boolean, default=True)

    # Assessment details
    assessment_type = Column(String(50), nullable=False, default="initial")  # initial, reassessment, post-fall
    notes = Column(Text, nullable=True)

    # Timestamps
    assessment_date = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    facility = relationship("Facility")
    patient = relationship("Patient", back_populates="fall_assessments")
    assessed_by = relationship("User")


class FallIncident(Base):
    """
    Fall Incident Reports - Track actual falls and near-misses
    """
    __tablename__ = "fall_incidents"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    reported_by_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Incident details
    incident_type = Column(String(50), nullable=False)  # fall, near_miss, found_on_floor
    incident_date = Column(DateTime(timezone=True), nullable=False)
    location = Column(String(255), nullable=False)  # "Room 301", "Bathroom", "Hallway"

    # Circumstances
    witnessed = Column(Boolean, default=False)
    activity_at_time = Column(String(255), nullable=True)  # "walking to bathroom", "getting out of bed"
    use_of_assistive_device = Column(Boolean, default=False)
    device_type = Column(String(100), nullable=True)  # "walker", "cane"

    # Patient status at time
    alert_oriented = Column(Boolean, default=True)
    recent_medications = Column(JSON, nullable=True)  # Medications given in last 4 hours
    call_light_within_reach = Column(Boolean, default=True)
    bed_alarm_was_on = Column(Boolean, default=False)
    bed_alarm_responded_to = Column(Boolean, default=False)

    # Injury assessment
    injury_occurred = Column(Boolean, default=False)
    injury_type = Column(String(100), nullable=True)  # "none", "minor", "moderate", "severe"
    injury_description = Column(Text, nullable=True)
    body_parts_affected = Column(JSON, nullable=True)  # ["head", "hip", "arm"]

    # Medical response
    physician_notified = Column(Boolean, default=False)
    physician_notified_at = Column(DateTime(timezone=True), nullable=True)
    family_notified = Column(Boolean, default=False)
    family_notified_at = Column(DateTime(timezone=True), nullable=True)
    xray_ordered = Column(Boolean, default=False)
    ct_scan_ordered = Column(Boolean, default=False)
    neuro_checks_ordered = Column(Boolean, default=False)

    # Environmental factors
    lighting_adequate = Column(Boolean, default=True)
    floor_wet_or_slippery = Column(Boolean, default=False)
    obstacles_present = Column(Boolean, default=False)
    footwear_appropriate = Column(Boolean, default=True)

    # AI analysis
    ai_predicted_fall = Column(Boolean, default=False)  # Did AI predict this?
    ai_warning_issued = Column(Boolean, default=False)  # Was warning given before fall?
    ai_contributing_factors = Column(JSON, nullable=True)  # AI-identified factors
    ai_prevention_recommendations = Column(JSON, nullable=True)  # What AI recommends to prevent recurrence

    # Follow-up actions
    interventions_added = Column(JSON, nullable=True)  # New interventions after fall
    reassessment_completed = Column(Boolean, default=False)
    reassessment_id = Column(Integer, ForeignKey("fall_assessments.id"), nullable=True)

    # Incident report
    incident_report_number = Column(String(50), nullable=True, unique=True)
    description = Column(Text, nullable=False)
    root_cause_analysis_completed = Column(Boolean, default=False)
    root_cause_findings = Column(Text, nullable=True)

    # Status
    status = Column(String(50), nullable=False, default="open")  # open, under_review, closed
    reviewed_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    facility = relationship("Facility")
    patient = relationship("Patient", back_populates="fall_incidents")
    reported_by = relationship("User", foreign_keys=[reported_by_id])
    reviewed_by = relationship("User", foreign_keys=[reviewed_by_id])
    reassessment = relationship("FallAssessment", foreign_keys=[reassessment_id])


class FallAlert(Base):
    """
    Active Fall Alerts - Real-time alerts for high-risk patients
    """
    __tablename__ = "fall_alerts"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    assessment_id = Column(Integer, ForeignKey("fall_assessments.id", ondelete="CASCADE"), nullable=True, index=True)

    # Alert details
    alert_type = Column(String(100), nullable=False)  # high_risk, new_medication, bed_alarm, mobility_change
    severity = Column(String(50), nullable=False)  # low, medium, high, critical
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)

    # Risk details
    current_risk_score = Column(Float, nullable=False)
    previous_risk_score = Column(Float, nullable=True)
    risk_change = Column(Float, nullable=True)  # How much risk increased

    # Trigger
    trigger_event = Column(String(255), nullable=True)  # What caused the alert
    trigger_data = Column(JSON, nullable=True)  # Additional context

    # Recommendations
    recommended_interventions = Column(JSON, nullable=True)
    immediate_actions = Column(JSON, nullable=True)

    # Status
    status = Column(String(50), nullable=False, default="active", index=True)  # active, acknowledged, resolved, escalated
    acknowledged_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)
    resolution_notes = Column(Text, nullable=True)

    # AI generated
    ai_generated = Column(Boolean, default=False)
    ai_confidence = Column(Float, nullable=True)
    ai_prediction_horizon = Column(String(50), nullable=True)  # "next_4_hours", "next_24_hours"

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    resolved_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    facility = relationship("Facility")
    patient = relationship("Patient")
    assessment = relationship("FallAssessment")
    acknowledged_by = relationship("User")


class EnvironmentalRisk(Base):
    """
    Environmental Risk Assessments - Room/area safety checks
    """
    __tablename__ = "environmental_risks"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)
    location = Column(String(255), nullable=False, index=True)  # "Room 301", "Hallway 3B"
    assessed_by_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Room/area hazards
    lighting_adequate = Column(Boolean, default=True)
    floor_clear_of_obstacles = Column(Boolean, default=True)
    floor_dry_and_clean = Column(Boolean, default=True)
    handrails_present = Column(Boolean, default=True)
    grab_bars_in_bathroom = Column(Boolean, default=True)
    non_slip_mats_present = Column(Boolean, default=True)
    furniture_stable = Column(Boolean, default=True)
    electrical_cords_secured = Column(Boolean, default=True)

    # Patient-specific
    bed_at_lowest_position = Column(Boolean, default=True)
    bed_locked = Column(Boolean, default=True)
    call_light_within_reach = Column(Boolean, default=True)
    bedside_table_within_reach = Column(Boolean, default=True)
    personal_items_accessible = Column(Boolean, default=True)

    # Safety equipment
    bed_alarm_functional = Column(Boolean, default=True)
    fall_mat_in_place = Column(Boolean, default=False)
    walker_or_cane_available = Column(Boolean, default=False)
    proper_footwear_available = Column(Boolean, default=True)

    # Hazards identified
    hazards_found = Column(JSON, nullable=True)  # List of specific hazards
    corrective_actions_taken = Column(JSON, nullable=True)
    corrective_actions_needed = Column(JSON, nullable=True)

    # Overall risk
    overall_risk_level = Column(String(50), nullable=False)  # low, moderate, high

    # Notes
    notes = Column(Text, nullable=True)

    # Timestamps
    assessment_date = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    facility = relationship("Facility")
    assessed_by = relationship("User")


class PatientMobility(Base):
    """
    Patient Mobility Tracking - Track mobility changes over time (AI uses this for predictions!)
    """
    __tablename__ = "patient_mobility"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    observed_by_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Mobility assessment
    mobility_level = Column(String(50), nullable=False)  # independent, supervision, minimal_assist, moderate_assist, max_assist, dependent

    # Specific abilities
    can_stand_independently = Column(Boolean, default=True)
    can_walk_independently = Column(Boolean, default=True)
    requires_assistive_device = Column(Boolean, default=False)
    device_type = Column(String(100), nullable=True)

    # Transfer ability
    bed_to_chair_transfer = Column(String(50), nullable=True)  # independent, supervision, assist_of_1, assist_of_2
    toilet_transfer = Column(String(50), nullable=True)

    # Balance
    steady_gait = Column(Boolean, default=True)
    balance_impaired = Column(Boolean, default=False)
    uses_furniture_for_support = Column(Boolean, default=False)

    # Changes
    mobility_changed = Column(Boolean, default=False)
    change_description = Column(Text, nullable=True)
    decline_noted = Column(Boolean, default=False)

    # AI tracking
    ai_trend_analysis = Column(JSON, nullable=True)  # AI-detected trends over time
    ai_decline_predicted = Column(Boolean, default=False)
    ai_intervention_suggested = Column(JSON, nullable=True)

    # Context
    observation_time = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    notes = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    facility = relationship("Facility")
    patient = relationship("Patient", back_populates="mobility_observations")
    observed_by = relationship("User")
