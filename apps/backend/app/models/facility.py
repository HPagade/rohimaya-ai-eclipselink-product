"""
Facility Model
Represents a healthcare facility (hospital, clinic, etc.)
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.orm import relationship
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
    features = Column(JSON, default={"ehr_integration": False})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    users = relationship("User", back_populates="facility")
    patients = relationship("Patient", back_populates="facility")

    # EclipseLink AI - Handoffs
    handoffs = relationship("Handoff", back_populates="facility")

    # PlumeDose AI - Medications
    medications = relationship("Medication", back_populates="facility", cascade="all, delete-orphan")
