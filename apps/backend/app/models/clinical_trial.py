"""
LunarBridge AI™ - Clinical Trial Matching Models
AI-powered clinical trial matching with automated eligibility screening
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class ClinicalTrial(Base):
    """
    Clinical Trials Database - All available trials
    """
    __tablename__ = "clinical_trials"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=True, index=True)

    # Trial identification
    nct_number = Column(String(50), nullable=True, unique=True, index=True)  # ClinicalTrials.gov NCT number
    trial_title = Column(String(500), nullable=False)
    short_title = Column(String(255), nullable=True)
    acronym = Column(String(50), nullable=True)

    # Study details
    phase = Column(String(50), nullable=True)  # Phase 1, Phase 2, Phase 3, Phase 4
    study_type = Column(String(100), nullable=True)  # Interventional, Observational, Expanded Access
    condition_or_disease = Column(JSON, nullable=True)  # ["Diabetes Type 2", "Cardiovascular Disease"]
    intervention_type = Column(JSON, nullable=True)  # ["Drug", "Device", "Behavioral"]
    intervention_name = Column(String(255), nullable=True)

    # Sponsor information
    sponsor = Column(String(255), nullable=True)
    principal_investigator = Column(String(255), nullable=True)
    pi_contact_email = Column(String(255), nullable=True)
    pi_contact_phone = Column(String(50), nullable=True)

    # Status
    overall_status = Column(String(100), nullable=False, default="recruiting", index=True)  # recruiting, active_not_recruiting, completed, suspended, terminated
    enrollment_start_date = Column(Date, nullable=True)
    enrollment_end_date = Column(Date, nullable=True)
    estimated_enrollment = Column(Integer, nullable=True)
    current_enrollment = Column(Integer, default=0)

    # Description
    brief_summary = Column(Text, nullable=True)
    detailed_description = Column(Text, nullable=True)
    study_design = Column(Text, nullable=True)
    primary_outcome = Column(Text, nullable=True)
    secondary_outcomes = Column(JSON, nullable=True)

    # Eligibility criteria (structured for AI matching!)
    min_age = Column(Integer, nullable=True)
    max_age = Column(Integer, nullable=True)
    accepts_healthy_volunteers = Column(Boolean, default=False)
    gender = Column(String(20), nullable=True)  # all, male, female

    # Requirements (AI extracts these from criteria)
    required_diagnoses = Column(JSON, nullable=True)  # ["diabetes", "hypertension"]
    excluded_diagnoses = Column(JSON, nullable=True)  # ["pregnancy", "liver disease"]
    required_lab_values = Column(JSON, nullable=True)  # {"hba1c": {"min": 7.0, "max": 10.0}}
    excluded_medications = Column(JSON, nullable=True)
    required_biomarkers = Column(JSON, nullable=True)

    # Full criteria text
    inclusion_criteria = Column(Text, nullable=True)
    exclusion_criteria = Column(Text, nullable=True)

    # Location
    is_multisite = Column(Boolean, default=False)
    sites = Column(JSON, nullable=True)  # List of participating sites
    available_at_facility = Column(Boolean, default=False)

    # Compensation
    compensation_offered = Column(Boolean, default=False)
    compensation_details = Column(Text, nullable=True)

    # URLs and documents
    clinicaltrials_gov_url = Column(String(500), nullable=True)
    study_protocol_url = Column(String(500), nullable=True)
    consent_form_url = Column(String(500), nullable=True)

    # AI matching optimization
    ai_keywords = Column(JSON, nullable=True)  # AI-extracted keywords for matching
    ai_matching_criteria = Column(JSON, nullable=True)  # Structured criteria for AI
    ai_complexity_score = Column(Float, nullable=True)  # How complex are eligibility criteria

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_updated_from_registry = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    facility = relationship("Facility")
    enrollments = relationship("TrialEnrollment", back_populates="trial", cascade="all, delete-orphan")
    matches = relationship("TrialMatch", back_populates="trial", cascade="all, delete-orphan")


class TrialMatch(Base):
    """
    AI-Generated Trial Matches - Patients matched to trials
    """
    __tablename__ = "trial_matches"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    trial_id = Column(Integer, ForeignKey("clinical_trials.id", ondelete="CASCADE"), nullable=False, index=True)

    # Matching details
    match_score = Column(Float, nullable=False)  # 0-100, how well patient matches
    ai_confidence = Column(Float, nullable=False)  # How confident AI is in match

    # Eligibility analysis
    eligibility_status = Column(String(50), nullable=False, default="potential")  # potential, eligible, ineligible, needs_review
    matched_criteria = Column(JSON, nullable=True)  # Which criteria patient meets
    unmatched_criteria = Column(JSON, nullable=True)  # Which criteria patient doesn't meet
    unknown_criteria = Column(JSON, nullable=True)  # Criteria that need verification

    # Detailed reasoning
    ai_reasoning = Column(Text, nullable=True)  # Why AI thinks this is a match
    key_strengths = Column(JSON, nullable=True)  # Strong matches
    key_concerns = Column(JSON, nullable=True)  # Potential issues

    # Patient data used for matching
    patient_age_at_match = Column(Integer, nullable=True)
    patient_diagnoses_at_match = Column(JSON, nullable=True)
    patient_medications_at_match = Column(JSON, nullable=True)
    patient_labs_at_match = Column(JSON, nullable=True)

    # Review status
    reviewed = Column(Boolean, default=False)
    reviewed_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    reviewer_notes = Column(Text, nullable=True)
    reviewer_decision = Column(String(50), nullable=True)  # approved, rejected, needs_discussion

    # Patient notification
    patient_notified = Column(Boolean, default=False)
    notification_sent_at = Column(DateTime(timezone=True), nullable=True)
    notification_method = Column(String(50), nullable=True)  # email, phone, in_person

    # Interest tracking
    patient_interested = Column(Boolean, nullable=True)
    patient_response_date = Column(DateTime(timezone=True), nullable=True)
    patient_questions = Column(Text, nullable=True)

    # Status
    status = Column(String(50), nullable=False, default="pending", index=True)  # pending, presented, interested, not_interested, enrolled, ineligible
    status_updated_at = Column(DateTime(timezone=True), nullable=True)

    # Timestamps
    matched_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    facility = relationship("Facility")
    patient = relationship("Patient", back_populates="trial_matches")
    trial = relationship("ClinicalTrial", back_populates="matches")
    reviewed_by = relationship("User")


class TrialEnrollment(Base):
    """
    Trial Enrollments - Patients enrolled in trials
    """
    __tablename__ = "trial_enrollments"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    trial_id = Column(Integer, ForeignKey("clinical_trials.id", ondelete="CASCADE"), nullable=False, index=True)
    match_id = Column(Integer, ForeignKey("trial_matches.id", ondelete="CASCADE"), nullable=True, index=True)

    # Enrollment details
    enrollment_number = Column(String(100), nullable=True, unique=True)  # Trial-specific patient ID
    enrollment_date = Column(Date, nullable=False)
    enrollment_status = Column(String(50), nullable=False, default="active", index=True)  # active, completed, withdrawn, terminated

    # Randomization (for RCTs)
    randomized = Column(Boolean, default=False)
    randomization_date = Column(Date, nullable=True)
    treatment_arm = Column(String(255), nullable=True)
    blinded = Column(Boolean, default=False)

    # Consent
    consent_obtained = Column(Boolean, default=False)
    consent_date = Column(Date, nullable=True)
    consent_version = Column(String(50), nullable=True)
    consented_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    consent_document_url = Column(String(500), nullable=True)

    # Pre-enrollment screening
    screening_date = Column(Date, nullable=True)
    screening_passed = Column(Boolean, default=True)
    screening_notes = Column(Text, nullable=True)

    # Baseline assessments
    baseline_completed = Column(Boolean, default=False)
    baseline_date = Column(Date, nullable=True)
    baseline_data = Column(JSON, nullable=True)

    # Visit tracking
    expected_visits = Column(Integer, nullable=True)
    completed_visits = Column(Integer, default=0)
    missed_visits = Column(Integer, default=0)
    next_visit_date = Column(Date, nullable=True)

    # Adverse events
    adverse_events_reported = Column(Integer, default=0)
    serious_adverse_events = Column(Integer, default=0)

    # Completion
    completion_date = Column(Date, nullable=True)
    completion_reason = Column(String(255), nullable=True)
    early_termination = Column(Boolean, default=False)
    termination_reason = Column(Text, nullable=True)

    # Outcomes (if study completed)
    primary_outcome_met = Column(Boolean, nullable=True)
    outcome_summary = Column(Text, nullable=True)

    # Coordinator
    study_coordinator_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    primary_contact_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Compliance
    protocol_deviations = Column(Integer, default=0)
    compliance_rate = Column(Float, nullable=True)  # Percentage

    # Notes
    notes = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    facility = relationship("Facility")
    patient = relationship("Patient", back_populates="trial_enrollments")
    trial = relationship("ClinicalTrial", back_populates="enrollments")
    match = relationship("TrialMatch")
    consented_by = relationship("User", foreign_keys=[consented_by_id])
    study_coordinator = relationship("User", foreign_keys=[study_coordinator_id])
    primary_contact = relationship("User", foreign_keys=[primary_contact_id])
    visits = relationship("TrialVisit", back_populates="enrollment", cascade="all, delete-orphan")


class TrialVisit(Base):
    """
    Trial Visits - Track study visits and assessments
    """
    __tablename__ = "trial_visits"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)
    enrollment_id = Column(Integer, ForeignKey("trial_enrollments.id", ondelete="CASCADE"), nullable=False, index=True)

    # Visit details
    visit_number = Column(Integer, nullable=False)
    visit_type = Column(String(100), nullable=False)  # screening, baseline, follow_up, final
    visit_name = Column(String(255), nullable=True)  # "Week 4 Visit", "Month 6 Assessment"

    # Scheduling
    scheduled_date = Column(Date, nullable=False)
    scheduled_time = Column(String(50), nullable=True)
    actual_date = Column(Date, nullable=True)
    actual_time = Column(String(50), nullable=True)

    # Visit window
    window_before_days = Column(Integer, nullable=True)
    window_after_days = Column(Integer, nullable=True)
    within_window = Column(Boolean, nullable=True)

    # Status
    status = Column(String(50), nullable=False, default="scheduled", index=True)  # scheduled, completed, missed, rescheduled, cancelled
    completion_status = Column(String(50), nullable=True)  # complete, partial, not_done

    # Assessments performed
    assessments_required = Column(JSON, nullable=True)  # List of required assessments
    assessments_completed = Column(JSON, nullable=True)  # List of completed assessments
    assessments_missed = Column(JSON, nullable=True)  # List of missed assessments

    # Labs
    labs_ordered = Column(Boolean, default=False)
    labs_completed = Column(Boolean, default=False)
    lab_results = Column(JSON, nullable=True)

    # Study drug/intervention
    study_drug_dispensed = Column(Boolean, default=False)
    study_drug_returned = Column(Boolean, default=False)
    compliance_assessment = Column(String(50), nullable=True)  # excellent, good, fair, poor

    # Adverse events
    adverse_events_assessed = Column(Boolean, default=False)
    adverse_events_reported = Column(Integer, default=0)

    # Staff
    conducted_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Notes
    notes = Column(Text, nullable=True)
    protocol_deviations = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    facility = relationship("Facility")
    enrollment = relationship("TrialEnrollment", back_populates="visits")
    conducted_by = relationship("User")


class TrialCriteria(Base):
    """
    Structured Trial Criteria - Machine-readable eligibility criteria for AI matching
    """
    __tablename__ = "trial_criteria"

    id = Column(Integer, primary_key=True, index=True)
    trial_id = Column(Integer, ForeignKey("clinical_trials.id", ondelete="CASCADE"), nullable=False, index=True)

    # Criterion details
    criterion_type = Column(String(50), nullable=False)  # inclusion, exclusion
    criterion_category = Column(String(100), nullable=False)  # age, diagnosis, lab, medication, biomarker
    criterion_text = Column(Text, nullable=False)  # Original text

    # Structured data (for AI matching)
    field_name = Column(String(255), nullable=True)  # "age", "hba1c", "diagnosis"
    operator = Column(String(50), nullable=True)  # ">", "<", "=", "between", "contains"
    value = Column(String(255), nullable=True)
    value_min = Column(Float, nullable=True)
    value_max = Column(Float, nullable=True)
    unit = Column(String(50), nullable=True)

    # Priority
    is_critical = Column(Boolean, default=False)  # Must meet vs nice to have
    weight = Column(Float, default=1.0)  # Importance for matching algorithm

    # AI extracted
    ai_extracted = Column(Boolean, default=False)
    ai_confidence = Column(Float, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    trial = relationship("ClinicalTrial")
