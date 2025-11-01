"""
Patient Model
Represents a patient receiving care
"""
from sqlalchemy import Column, Integer, String, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)
    mrn = Column(String(50), nullable=False)  # Medical Record Number
    ehr_patient_id = Column(String(100), nullable=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(20), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(50), nullable=True)
    zip_code = Column(String(20), nullable=True)
    emergency_contact_name = Column(String(200), nullable=True)
    emergency_contact_phone = Column(String(20), nullable=True)
    emergency_contact_relation = Column(String(50), nullable=True)
    room_number = Column(String(20), nullable=True)
    admission_date = Column(Date, nullable=True)
    discharge_date = Column(Date, nullable=True)
    primary_diagnosis = Column(Text, nullable=True)
    allergies = Column(Text, nullable=True)
    code_status = Column(String(50), nullable=True)
    status = Column(String(50), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    facility = relationship("Facility", back_populates="patients")

    # EclipseLink AI - Handoffs
    handoffs = relationship("Handoff", back_populates="patient")

    # PlumeDose AI - Medications
    medication_orders = relationship("MedicationOrder", back_populates="patient", cascade="all, delete-orphan")
    medication_administrations = relationship("MedicationAdministration", back_populates="patient", cascade="all, delete-orphan")

    # RiseGuard AI - Fall Prevention
    fall_assessments = relationship("FallAssessment", back_populates="patient", cascade="all, delete-orphan")
    fall_incidents = relationship("FallIncident", back_populates="patient", cascade="all, delete-orphan")
    mobility_observations = relationship("PatientMobility", back_populates="patient", cascade="all, delete-orphan")

    # LunarBridge AI - Clinical Trials
    trial_matches = relationship("TrialMatch", back_populates="patient", cascade="all, delete-orphan")
    trial_enrollments = relationship("TrialEnrollment", back_populates="patient", cascade="all, delete-orphan")

    # FeatherSight AI - Lab Results
    lab_results = relationship("LabResult", back_populates="patient", cascade="all, delete-orphan")

    # PhoenixBreath AI - Respiratory
    respiratory_vitals = relationship("RespiratoryVital", back_populates="patient", cascade="all, delete-orphan")

    # WingStrength AI - PT/OT
    therapy_sessions = relationship("TherapySession", back_populates="patient", cascade="all, delete-orphan")
