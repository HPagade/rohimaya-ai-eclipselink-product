"""
User Model
Represents healthcare staff (nurses, doctors, etc.)
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    email_verified = Column(Boolean, default=False)
    email_verification_token = Column(String(255), nullable=True)
    email_verification_expires_at = Column(DateTime(timezone=True), nullable=True)
    reset_password_token = Column(String(255), nullable=True)
    reset_password_expires_at = Column(DateTime(timezone=True), nullable=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    profile_photo_url = Column(String(500), nullable=True)
    role = Column(String(50), nullable=False, index=True)  # RN, MD, NP, etc.
    department = Column(String(100), nullable=True)
    license_number = Column(String(100), nullable=True)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True, index=True)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    last_login_ip = Column(String(45), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    facility = relationship("Facility", back_populates="users")
    handoffs_created = relationship("Handoff", foreign_keys="Handoff.created_by_id", back_populates="created_by")
    handoffs_assigned = relationship("Handoff", foreign_keys="Handoff.assigned_to_id", back_populates="assigned_to")
    rewards = relationship("Reward", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")
