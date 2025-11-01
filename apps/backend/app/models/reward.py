"""
Phoenix & Peacock Honors™ - Universal Rewards System Models
Earn points across all Rohimaya products, redeem for PTO, meals, spa, education & more
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class RewardTransaction(Base):
    """
    Reward Transactions - Points earned or redeemed
    """
    __tablename__ = "reward_transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)

    # Transaction details
    transaction_type = Column(String(50), nullable=False, index=True)  # earned, redeemed, bonus, expired
    points = Column(Integer, nullable=False)  # Positive for earned, negative for redeemed
    balance_after = Column(Integer, nullable=False)  # Running balance

    # Source (what action earned/spent points)
    source_product = Column(String(50), nullable=False)  # eclipselink, plumedose, riseguard, etc.
    source_action = Column(String(100), nullable=False)  # handoff_created, medication_verified, fall_prevented, etc.
    reference_type = Column(String(50), nullable=True)  # handoff, medication_order, fall_assessment, etc.
    reference_id = Column(Integer, nullable=True)

    # Description
    description = Column(Text, nullable=True)

    # Redemption details (if redeemed)
    reward_item_id = Column(Integer, ForeignKey("reward_catalog.id"), nullable=True)
    redemption_status = Column(String(50), nullable=True)  # pending, approved, fulfilled, cancelled

    # Expiration
    expires_at = Column(DateTime(timezone=True), nullable=True)
    is_expired = Column(Boolean, default=False)

    # Timestamps
    transaction_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="reward_transactions")
    facility = relationship("Facility")
    reward_item = relationship("RewardCatalogItem", back_populates="redemptions")


class RewardCatalogItem(Base):
    """
    Reward Catalog - Items available for redemption
    """
    __tablename__ = "reward_catalog"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=True, index=True)

    # Item details
    category = Column(String(100), nullable=False, index=True)  # pto, meals, spa, education, gift_cards, merchandise
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)

    # Points cost
    points_cost = Column(Integer, nullable=False)

    # Availability
    is_active = Column(Boolean, default=True)
    is_facility_specific = Column(Boolean, default=False)
    available_quantity = Column(Integer, nullable=True)  # Null = unlimited
    remaining_quantity = Column(Integer, nullable=True)

    # Details
    terms_and_conditions = Column(Text, nullable=True)
    redemption_instructions = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    facility = relationship("Facility")
    redemptions = relationship("RewardTransaction", back_populates="reward_item")


class RewardBalance(Base):
    """
    Reward Balances - Current point balance per user (for quick lookup)
    """
    __tablename__ = "reward_balances"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=False, index=True)

    # Balance
    current_balance = Column(Integer, default=0, nullable=False)
    lifetime_earned = Column(Integer, default=0, nullable=False)
    lifetime_redeemed = Column(Integer, default=0, nullable=False)

    # Breakdown by product
    eclipselink_points = Column(Integer, default=0)
    plumedose_points = Column(Integer, default=0)
    riseguard_points = Column(Integer, default=0)
    lunarbridge_points = Column(Integer, default=0)
    feathersight_points = Column(Integer, default=0)
    phoenixbreath_points = Column(Integer, default=0)
    wingstrength_points = Column(Integer, default=0)

    # Tier status
    tier = Column(String(50), default="bronze")  # bronze, silver, gold, platinum
    tier_multiplier = Column(Float, default=1.0)  # Points multiplier based on tier

    # Timestamps
    last_earned_at = Column(DateTime(timezone=True), nullable=True)
    last_redeemed_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="reward_balance", uselist=False)
    facility = relationship("Facility")


class RewardAchievement(Base):
    """
    Achievements - Badges and milestones
    """
    __tablename__ = "reward_achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Achievement details
    achievement_type = Column(String(100), nullable=False)  # handoff_streak, perfect_week, safety_champion, etc.
    achievement_name = Column(String(255), nullable=False)
    achievement_description = Column(Text, nullable=True)
    badge_icon_url = Column(String(500), nullable=True)

    # Requirements met
    criteria_met = Column(JSON, nullable=True)
    bonus_points = Column(Integer, default=0)

    # Timestamps
    earned_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="achievements")


class Leaderboard(Base):
    """
    Leaderboards - Rankings by facility, product, or global
    """
    __tablename__ = "leaderboards"

    id = Column(Integer, primary_key=True, index=True)
    facility_id = Column(Integer, ForeignKey("facilities.id", ondelete="CASCADE"), nullable=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Leaderboard details
    leaderboard_type = Column(String(50), nullable=False)  # facility, role, product, global
    period = Column(String(50), nullable=False)  # week, month, quarter, year, all_time
    product = Column(String(50), nullable=True)  # Specific product or "all"

    # Rankings
    rank = Column(Integer, nullable=False)
    points = Column(Integer, nullable=False)
    percentile = Column(Float, nullable=True)

    # Period dates
    period_start = Column(DateTime(timezone=True), nullable=False)
    period_end = Column(DateTime(timezone=True), nullable=False)

    # Timestamps
    calculated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    facility = relationship("Facility")
    user = relationship("User")


# Legacy Reward model for backward compatibility
class Reward(Base):
    """Legacy rewards table - keeping for backward compatibility"""
    __tablename__ = "rewards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    facility_id = Column(Integer, nullable=True)

    # Points
    points_earned = Column(Integer, default=0)
    points_type = Column(String(50), nullable=False)

    # Reference
    reference_type = Column(String(50), nullable=True)
    reference_id = Column(Integer, nullable=True)

    # Description
    description = Column(Text, nullable=True)

    # Timestamps
    earned_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="rewards")
