"""
Audit Log Model
HIPAA-compliant audit logging (7-year retention)
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    facility_id = Column(Integer, nullable=True, index=True)

    # Event details
    event_type = Column(String(100), nullable=False, index=True)  # login, logout, view_patient, etc.
    event_category = Column(String(50), nullable=False)  # authentication, data_access, data_modification

    # Resource accessed
    resource_type = Column(String(50), nullable=True)  # patient, handoff, user
    resource_id = Column(Integer, nullable=True)

    # Request details
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    request_method = Column(String(10), nullable=True)
    request_path = Column(String(500), nullable=True)

    # Response details
    response_status = Column(Integer, nullable=True)

    # Change tracking
    old_values = Column(JSON, nullable=True)
    new_values = Column(JSON, nullable=True)

    # Additional metadata
    extra_metadata = Column("metadata", JSON, nullable=True)
    notes = Column(Text, nullable=True)

    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationships
    user = relationship("User", back_populates="audit_logs")
