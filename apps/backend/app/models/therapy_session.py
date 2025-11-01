"""
WingStrength AI™ - PT/OT Optimization Models
AI-powered therapy tracking with outcome predictions
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class TherapySession(Base):
    """
    Therapy Sessions - PT/OT/Speech therapy sessions
    """
    __tablename__ = "therapy_sessions"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    therapist_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Session details
    therapy_type = Column(String(50), nullable=False)  # PT, OT, Speech
    session_date = Column(DateTime(timezone=True), nullable=False)
    duration_minutes = Column(Integer, nullable=False)

    # Focus areas
    treatment_focus = Column(JSON, nullable=True)  # ["balance", "strength", "ROM"]
    body_parts_treated = Column(JSON, nullable=True)  # ["left_knee", "right_shoulder"]

    # Activities performed
    exercises_completed = Column(JSON, nullable=True)
    modalities_used = Column(JSON, nullable=True)  # ["heat", "ice", "ultrasound", "electrical_stim"]

    # Patient performance
    patient_tolerance = Column(String(50), nullable=True)  # excellent, good, fair, poor
    pain_level_before = Column(Integer, nullable=True)  # 0-10
    pain_level_after = Column(Integer, nullable=True)  # 0-10
    fatigue_level = Column(String(50), nullable=True)

    # Progress
    progress_rating = Column(String(50), nullable=True)  # significant, moderate, minimal, none, decline
    functional_improvements = Column(JSON, nullable=True)

    # Goals addressed
    goals_addressed = Column(JSON, nullable=True)  # Which goals worked on

    # AI insights
    ai_progress_prediction = Column(Float, nullable=True)  # Predicted outcome 0-100
    ai_discharge_readiness = Column(Float, nullable=True)  # 0-100
    ai_recommendations = Column(JSON, nullable=True)

    # Documentation
    notes = Column(Text, nullable=True)
    plan_for_next_session = Column(Text, nullable=True)

    # Status
    status = Column(String(50), nullable=False, default="completed")  # scheduled, completed, cancelled, missed

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    facility = relationship("Facility")
    patient = relationship("Patient", back_populates="therapy_sessions")
    therapist = relationship("User")


class ExercisePlan(Base):
    """
    Exercise Plans - Home exercise programs and facility exercises
    """
    __tablename__ = "exercise_plans"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Plan details
    plan_name = Column(String(255), nullable=False)
    plan_type = Column(String(50), nullable=False)  # home_program, facility_program
    therapy_type = Column(String(50), nullable=False)  # PT, OT, Speech

    # Exercises
    exercises = Column(JSON, nullable=False)  # List of exercises with details
    frequency = Column(String(255), nullable=True)  # "3 times daily", "every other day"
    duration_weeks = Column(Integer, nullable=True)

    # Instructions
    precautions = Column(JSON, nullable=True)
    special_instructions = Column(Text, nullable=True)

    # Status
    status = Column(String(50), nullable=False, default="active")  # active, completed, discontinued
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=True)

    # Compliance tracking
    expected_completions = Column(Integer, nullable=True)
    actual_completions = Column(Integer, default=0)
    compliance_rate = Column(Float, nullable=True)  # Percentage

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    facility = relationship("Facility")
    patient = relationship("Patient")
    created_by = relationship("User")


class TherapyGoal(Base):
    """
    Therapy Goals - Patient-specific rehabilitation goals
    """
    __tablename__ = "therapy_goals"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Goal details
    goal_category = Column(String(100), nullable=False)  # mobility, ADL, strength, balance, pain
    goal_description = Column(Text, nullable=False)
    measurable_objective = Column(Text, nullable=False)  # "Walk 100 feet with walker independently"

    # Timeline
    target_date = Column(DateTime(timezone=True), nullable=True)
    estimated_weeks = Column(Integer, nullable=True)

    # Baseline
    baseline_status = Column(Text, nullable=True)
    baseline_measurement = Column(String(255), nullable=True)

    # Current status
    current_status = Column(Text, nullable=True)
    current_measurement = Column(String(255), nullable=True)
    progress_percentage = Column(Float, nullable=True)  # 0-100

    # Status
    status = Column(String(50), nullable=False, default="active")  # active, met, modified, discontinued
    met_date = Column(DateTime(timezone=True), nullable=True)

    # AI insights
    ai_predicted_achievement_date = Column(DateTime(timezone=True), nullable=True)
    ai_confidence = Column(Float, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    facility = relationship("Facility")
    patient = relationship("Patient")
    created_by = relationship("User")


class MobilityAssessment(Base):
    """
    Mobility Assessments - Standardized assessments (Timed Up and Go, Berg Balance, etc.)
    """
    __tablename__ = "mobility_assessments"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    assessed_by_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Assessment type
    assessment_type = Column(String(100), nullable=False)  # timed_up_and_go, berg_balance, 6_minute_walk, gait_speed

    # Results
    score = Column(Float, nullable=True)
    interpretation = Column(String(255), nullable=True)
    fall_risk_level = Column(String(50), nullable=True)  # low, moderate, high

    # Details
    assessment_data = Column(JSON, nullable=True)  # Specific test details
    notes = Column(Text, nullable=True)

    # AI analysis
    ai_comparison_to_norms = Column(Text, nullable=True)
    ai_improvement_areas = Column(JSON, nullable=True)

    # Timestamp
    assessment_date = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    facility = relationship("Facility")
    patient = relationship("Patient")
    assessed_by = relationship("User")
