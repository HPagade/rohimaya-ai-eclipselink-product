"""
Reward Model
Represents Phoenix & Peacock Honors™ rewards points
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Reward(Base):
    __tablename__ = "rewards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    facility_id = Column(Integer, nullable=True)

    # Points
    points_earned = Column(Integer, default=0)
    points_type = Column(String(50), nullable=False)  # handoff_baseline, handoff_update, critical_alert, etc.

    # Reference
    reference_type = Column(String(50), nullable=True)  # handoff, patient, etc.
    reference_id = Column(Integer, nullable=True)

    # Description
    description = Column(Text, nullable=True)

    # Timestamps
    earned_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="rewards")
