"""
Database models for Rohimaya Health AI - All Products
"""
# Core models
from .facility import Facility
from .user import User
from .patient import Patient
from .audit import AuditLog

# EclipseLink AI - Clinical Handoffs
from .handoff import Handoff

# PlumeDose AI - Medication Management
from .medication import Medication, MedicationOrder, MedicationAdministration, DrugInteraction, MedicationAlert

# RiseGuard AI - Fall Prevention
from .fall_assessment import FallAssessment, FallIncident, FallAlert, EnvironmentalRisk, PatientMobility

# LunarBridge AI - Clinical Trials
from .clinical_trial import ClinicalTrial, TrialMatch, TrialEnrollment, TrialVisit, TrialCriteria

# FeatherSight AI - Lab Intelligence
from .lab_result import LabResult, LabPanel, CriticalValue

# PhoenixBreath AI - Respiratory Monitoring
from .respiratory_vital import RespiratoryVital, VentilatorSetting, ABGResult

# WingStrength AI - PT/OT Optimization
from .therapy_session import TherapySession, ExercisePlan, TherapyGoal, MobilityAssessment

# Phoenix & Peacock Honors - Universal Rewards System
from .reward import (
    Reward,  # Legacy
    RewardTransaction,
    RewardCatalogItem,
    RewardBalance,
    RewardAchievement,
    Leaderboard
)

__all__ = [
    # Core
    "Facility",
    "User",
    "Patient",
    "AuditLog",
    # EclipseLink AI
    "Handoff",
    # PlumeDose AI
    "Medication",
    "MedicationOrder",
    "MedicationAdministration",
    "DrugInteraction",
    "MedicationAlert",
    # RiseGuard AI
    "FallAssessment",
    "FallIncident",
    "FallAlert",
    "EnvironmentalRisk",
    "PatientMobility",
    # LunarBridge AI
    "ClinicalTrial",
    "TrialMatch",
    "TrialEnrollment",
    "TrialVisit",
    "TrialCriteria",
    # FeatherSight AI
    "LabResult",
    "LabPanel",
    "CriticalValue",
    # PhoenixBreath AI
    "RespiratoryVital",
    "VentilatorSetting",
    "ABGResult",
    # WingStrength AI
    "TherapySession",
    "ExercisePlan",
    "TherapyGoal",
    "MobilityAssessment",
    # Phoenix & Peacock Honors
    "Reward",
    "RewardTransaction",
    "RewardCatalogItem",
    "RewardBalance",
    "RewardAchievement",
    "Leaderboard",
]
