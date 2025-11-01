"""
Initialize database tables
Creates all tables defined in SQLAlchemy models
"""
import sys
sys.path.insert(0, '/home/user/rohimaya-ai-eclipselink-product/apps/backend')

from app.database import Base, engine
from app.models import Facility, User, Patient, Handoff, Reward, AuditLog

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✅ Database tables created successfully!")
print("\nTables created:")
for table in Base.metadata.tables:
    print(f"  - {table}")
