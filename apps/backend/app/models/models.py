"""
SQLAlchemy models for EclipseLink AI
Maps to the PostgreSQL schema created in database/schema.sql
"""
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, Text, ForeignKey, DECIMAL, ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.database import Base


class Facility(Base):
    __tablename__ = "facilities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(50))
    zip_code = Column(String(20))
    phone = Column(String(20))
    email = Column(String(255))
    license_number = Column(String(100), unique=True, index=True)

    subscription_tier = Column(String(50), default="trial")
    subscription_status = Column(String(50), default="active", index=True)
    subscription_expires_at = Column(DateTime(timezone=True))

    features = Column(JSONB, default={"ehr_integration": False})

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)

    # Authentication
    email = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    email_verified = Column(Boolean, default=False)
    email_verification_token = Column(String(255))
    email_verification_expires_at = Column(DateTime(timezone=True))

    # Password reset
    reset_password_token = Column(String(255))
    reset_password_expires_at = Column(DateTime(timezone=True))

    # Profile
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    profile_photo_url = Column(Text)

    # Clinical role (15 roles)
    role = Column(String(50), nullable=False, index=True)  # RN, LPN, CNA, NP, MD, DO, PA, MA, PT, OT, RT, SLP, SW, Case Manager, Dietitian
    department = Column(String(100))
    license_number = Column(String(100))

    # Permissions
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True, index=True)

    # Last login
    last_login_at = Column(DateTime(timezone=True))
    last_login_ip = Column(String(45))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)

    # Patient identifiers
    mrn = Column(String(50), nullable=False, index=True)
    ehr_patient_id = Column(String(100))

    # Demographics
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(20))

    # Contact
    phone = Column(String(20))
    email = Column(String(255))
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(50))
    zip_code = Column(String(20))

    # Emergency contact
    emergency_contact_name = Column(String(200))
    emergency_contact_phone = Column(String(20))
    emergency_contact_relation = Column(String(50))

    # Clinical
    room_number = Column(String(20), index=True)
    admission_date = Column(Date)
    discharge_date = Column(Date)
    primary_diagnosis = Column(Text)
    allergies = Column(Text)
    code_status = Column(String(50))

    # Status
    status = Column(String(50), default="active", index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))


class Handoff(Base):
    __tablename__ = "handoffs"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    created_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Update-Only Model™
    is_baseline = Column(Boolean, default=False, index=True)
    baseline_handoff_id = Column(Integer, ForeignKey("handoffs.id"), index=True)

    # Voice recording
    audio_file_url = Column(Text, nullable=False)
    audio_duration_seconds = Column(Integer)
    audio_file_size_bytes = Column(Integer)

    # Transcription (Whisper)
    transcript_text = Column(Text)
    transcript_confidence = Column(DECIMAL(3, 2))  # 0.00 to 1.00
    transcribed_at = Column(DateTime(timezone=True))

    # AI-generated SBAR (Claude)
    sbar_situation = Column(Text)
    sbar_background = Column(Text)
    sbar_assessment = Column(Text)
    sbar_recommendation = Column(Text)
    ai_processing_time_ms = Column(Integer)
    ai_processed_at = Column(DateTime(timezone=True))

    # Change detection (for updates)
    changes_detected = Column(JSONB)  # [{ field: 'vital_signs', old: '...', new: '...', severity: 'medium' }]
    changes_summary = Column(Text)

    # Critical alerts
    has_critical_alert = Column(Boolean, default=False, index=True)
    critical_alert_type = Column(String(100))
    critical_alert_confidence = Column(DECIMAL(3, 2))
    critical_alert_notified_at = Column(DateTime(timezone=True))

    # Status
    status = Column(String(50), default="draft", index=True)
    reviewed_by_user_id = Column(Integer, ForeignKey("users.id"))
    reviewed_at = Column(DateTime(timezone=True))

    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))


class RewardPoints(Base):
    __tablename__ = "rewards_points"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)

    # Points
    points_earned = Column(Integer, nullable=False)
    action_type = Column(String(100), nullable=False)  # baseline_handoff, update_handoff, critical_alert, perfect_sbar
    description = Column(Text)

    # Associated handoff
    handoff_id = Column(Integer, ForeignKey("handoffs.id", ondelete="SET NULL"))

    earned_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), index=True)

    # Action details
    action = Column(String(100), nullable=False, index=True)  # login, logout, view_patient, create_handoff, etc.
    resource_type = Column(String(50))  # user, patient, handoff, etc.
    resource_id = Column(Integer)

    # Context
    ip_address = Column(String(45))
    user_agent = Column(Text)
    request_method = Column(String(10))
    request_path = Column(Text)

    # Changes (for data modifications)
    old_values = Column(JSONB)
    new_values = Column(JSONB)

    # Security
    is_suspicious = Column(Boolean, default=False)
    suspicious_reason = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
