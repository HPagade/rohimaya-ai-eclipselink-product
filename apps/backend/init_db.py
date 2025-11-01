"""
Initialize database tables for Rohimaya Health AI - All Products
Creates all tables defined in SQLAlchemy models
"""
import sys
sys.path.insert(0, '/home/user/rohimaya-ai-eclipselink-product/apps/backend')

from app.database import Base, engine

# Import all models to ensure they're registered with SQLAlchemy
from app.models import (
    # Core
    Facility, User, Patient, AuditLog,
    # EclipseLink AI
    Handoff,
    # PlumeDose AI
    Medication, MedicationOrder, MedicationAdministration, DrugInteraction, MedicationAlert,
    # RiseGuard AI
    FallAssessment, FallIncident, FallAlert, EnvironmentalRisk, PatientMobility,
    # LunarBridge AI
    ClinicalTrial, TrialMatch, TrialEnrollment, TrialVisit, TrialCriteria,
    # FeatherSight AI
    LabResult, LabPanel, CriticalValue,
    # PhoenixBreath AI
    RespiratoryVital, VentilatorSetting, ABGResult,
    # WingStrength AI
    TherapySession, ExercisePlan, TherapyGoal, MobilityAssessment,
    # Phoenix & Peacock Honors
    Reward, RewardTransaction, RewardCatalogItem, RewardBalance, RewardAchievement, Leaderboard
)

print("🏗️  Rohimaya Health AI - Database Initialization")
print("=" * 60)
print("\nCreating database tables for all 8 products...")
print("  🔗 EclipseLink AI - Clinical Handoffs")
print("  💊 PlumeDose AI - Medication Management")
print("  🛡️  RiseGuard AI - Fall Prevention")
print("  🧪 LunarBridge AI - Clinical Trials")
print("  🔬 FeatherSight AI - Lab Intelligence")
print("  🫁 PhoenixBreath AI - Respiratory Monitoring")
print("  💪 WingStrength AI - PT/OT Optimization")
print("  🏆 Phoenix & Peacock Honors - Universal Rewards")
print("\n" + "=" * 60)

Base.metadata.create_all(bind=engine)

print("\n✅ Database tables created successfully!")
print(f"\n📊 Total tables created: {len(Base.metadata.tables)}")
print("\nTables by product:")

# Group tables by product
tables = sorted(Base.metadata.tables.keys())

core_tables = [t for t in tables if t in ['facilities', 'users', 'patients', 'audit_logs']]
eclipselink_tables = [t for t in tables if 'handoff' in t]
plumedose_tables = [t for t in tables if 'medication' in t or 'drug' in t]
riseguard_tables = [t for t in tables if 'fall' in t or 'mobility' in t or 'environmental' in t]
lunarbridge_tables = [t for t in tables if 'trial' in t or 'clinical_trial' in t]
feathersight_tables = [t for t in tables if 'lab' in t or 'critical_value' in t]
phoenixbreath_tables = [t for t in tables if 'respiratory' in t or 'ventilator' in t or 'abg' in t]
wingstrength_tables = [t for t in tables if 'therapy' in t or 'exercise' in t or 'mobility_assessment' in t]
rewards_tables = [t for t in tables if 'reward' in t or 'leaderboard' in t]

if core_tables:
    print("\n📦 Core Tables:")
    for t in core_tables:
        print(f"    - {t}")

if eclipselink_tables:
    print("\n🔗 EclipseLink AI:")
    for t in eclipselink_tables:
        print(f"    - {t}")

if plumedose_tables:
    print("\n💊 PlumeDose AI:")
    for t in plumedose_tables:
        print(f"    - {t}")

if riseguard_tables:
    print("\n🛡️  RiseGuard AI:")
    for t in riseguard_tables:
        print(f"    - {t}")

if lunarbridge_tables:
    print("\n🧪 LunarBridge AI:")
    for t in lunarbridge_tables:
        print(f"    - {t}")

if feathersight_tables:
    print("\n🔬 FeatherSight AI:")
    for t in feathersight_tables:
        print(f"    - {t}")

if phoenixbreath_tables:
    print("\n🫁 PhoenixBreath AI:")
    for t in phoenixbreath_tables:
        print(f"    - {t}")

if wingstrength_tables:
    print("\n💪 WingStrength AI:")
    for t in wingstrength_tables:
        print(f"    - {t}")

if rewards_tables:
    print("\n🏆 Phoenix & Peacock Honors:")
    for t in rewards_tables:
        print(f"    - {t}")

print("\n" + "=" * 60)
print("🎉 Rohimaya Health AI platform is ready!")
print("=" * 60)
