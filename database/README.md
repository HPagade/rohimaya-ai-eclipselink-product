# EclipseLink AI™ Database

This directory contains all database-related files for EclipseLink AI.

## 📁 Directory Structure

```
database/
├── schema.sql                    # Complete database schema with enums and core tables
├── migrations/                   # Migration scripts
│   ├── 001_core_tables.sql      # Handoffs, voice recordings, SBAR tables
│   └── 002_audit_and_notifications.sql  # Audit, notifications, EHR tables
├── functions/                    # Database functions and triggers
│   └── triggers.sql             # Triggers and RLS policies
├── seeds/                        # Seed data (empty - to be populated)
├── setup.sh                      # Database setup script
└── README.md                     # This file
```

## 🚀 Quick Setup

### Prerequisites
- PostgreSQL 15+ (via Supabase recommended)
- `psql` command-line tool installed

### Setup Instructions

1. **Set your database URL:**
   ```bash
   export DATABASE_URL="postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT].supabase.co:5432/postgres"
   ```

2. **Run the setup script:**
   ```bash
   bash database/setup.sh
   ```

3. **Verify setup:**
   ```bash
   psql $DATABASE_URL -c "\dt"
   ```

## 📊 Database Schema

### 15 Core Tables

**Core Tables:**
- `facilities` - Healthcare facilities (6,000+ nationwide)
- `staff` - Healthcare professionals (9M+ users)
- `patients` - Patient records (50M+ patients)
- `handoffs` - Clinical handoffs (100M+ handoffs/year)

**Processing Tables:**
- `voice_recordings` - Audio file metadata
- `ai_generations` - AI processing records
- `sbar_reports` - Generated SBAR reports

**Assignment Tables:**
- `handoff_assignments` - Staff-to-handoff mapping (N:N)

**Audit & Compliance:**
- `audit_logs` - HIPAA-compliant audit trail (7-year retention)
- `notifications` - Real-time notifications

**EHR Integration:**
- `ehr_connections` - EHR system configurations
- `ehr_sync_logs` - Synchronization history

**System Tables:**
- `user_sessions` - Active user sessions
- `feature_flags` - Feature toggles
- `system_settings` - Application configuration

### Custom Types (Enums)

The schema defines 15+ custom PostgreSQL enums:
- `facility_type` - Hospital, clinic, nursing home, etc.
- `user_role` - RN, MD, NP, PA, etc.
- `handoff_status` - Draft, recording, ready, completed, etc.
- `recording_status` - Uploading, transcribed, failed, etc.
- `generation_status` - Queued, processing, completed, failed
- And more...

## 🔐 Security Features

### Row-Level Security (RLS)
All tables have RLS enabled with facility-level isolation:
- Staff can only see data from their facility
- Admins have full access to their facility's data
- Super admins have cross-facility access

### Audit Logging
PHI access is tracked automatically:
- Every INSERT, UPDATE, DELETE on patient data is logged
- User information captured (who, what, when, where)
- 7-year retention for HIPAA compliance

### Encryption
- Passwords: Bcrypt hashed
- SSN: AES-256 encrypted
- EHR credentials: Facility-specific encryption
- All connections: SSL/TLS required

## 🔧 Database Functions

### Triggers

**1. Updated Timestamp Trigger**
```sql
update_updated_at_column()
```
Automatically updates `updated_at` column on record modification

**2. Audit Logging Trigger**
```sql
log_table_changes()
```
Logs all changes to PHI tables for HIPAA compliance

### Helper Functions

See `functions/triggers.sql` for all database functions.

## 📈 Performance Optimizations

### Indexes
- **Full-text search** indexes on names and content
- **B-tree indexes** on foreign keys and frequently filtered columns
- **Partial indexes** on active records only
- **GIN indexes** for JSONB columns

### Partitioning (Future)
Large tables can be partitioned by:
- `handoffs` - Partition by month
- `audit_logs` - Partition by month
- `voice_recordings` - Partition by month

## 🗄️ Migrations

Migrations are run in order:
1. `schema.sql` - Base schema with enums and core tables
2. `migrations/001_core_tables.sql` - Handoff-related tables
3. `migrations/002_audit_and_notifications.sql` - Audit and system tables
4. `functions/triggers.sql` - Functions, triggers, and RLS

### Running Migrations Manually

```bash
# Connect to database
psql $DATABASE_URL

# Run individual migration
\i database/migrations/001_core_tables.sql

# Or run all at once
\i database/schema.sql
\i database/migrations/001_core_tables.sql
\i database/migrations/002_audit_and_notifications.sql
\i database/functions/triggers.sql
```

## 🌱 Seed Data

To populate the database with test data:

```bash
# Create seed scripts in database/seeds/
# Then run:
psql $DATABASE_URL -f database/seeds/facilities.sql
psql $DATABASE_URL -f database/seeds/staff.sql
```

## 📊 Useful Queries

### Check all tables
```sql
SELECT tablename FROM pg_tables WHERE schemaname = 'public';
```

### Check table sizes
```sql
SELECT
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Check RLS policies
```sql
SELECT tablename, rowsecurity FROM pg_tables WHERE schemaname = 'public';
```

### View recent audit logs
```sql
SELECT
  created_at,
  user_email,
  action,
  resource,
  phi_accessed
FROM audit_logs
ORDER BY created_at DESC
LIMIT 10;
```

### Active user sessions
```sql
SELECT
  u.email,
  s.device_type,
  s.last_activity_at,
  s.expires_at
FROM user_sessions s
JOIN staff u ON s.user_id = u.id
WHERE s.is_active = true
ORDER BY s.last_activity_at DESC;
```

## 🔍 Troubleshooting

### Connection Issues
```bash
# Test connection
psql $DATABASE_URL -c "SELECT version();"

# Check if tables exist
psql $DATABASE_URL -c "\dt"
```

### Permission Issues
```sql
-- Grant permissions to user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO your_user;
```

### RLS Issues
```sql
-- Temporarily disable RLS for testing (NOT for production!)
ALTER TABLE patients DISABLE ROW LEVEL SECURITY;

-- Re-enable RLS
ALTER TABLE patients ENABLE ROW LEVEL SECURITY;
```

## 📚 Additional Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Supabase Documentation](https://supabase.com/docs)
- [Row-Level Security Guide](https://supabase.com/docs/guides/auth/row-level-security)
- [HIPAA Compliance Guide](https://supabase.com/docs/guides/platform/hipaa)

## 🔄 Backup & Recovery

### Backup
```bash
# Backup entire database
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Backup specific table
pg_dump $DATABASE_URL -t patients > patients_backup.sql
```

### Restore
```bash
# Restore from backup
psql $DATABASE_URL < backup_20250123.sql

# Restore specific table
psql $DATABASE_URL < patients_backup.sql
```

## 📞 Support

For database-related questions:
- Check the main [README.md](../README.md)
- Review [Part 3: Database Schema Documentation](../eclipse-ai-part3-database-schema.md)
- Contact: support@rohimaya.ai

---

© 2025 Rohimaya Health AI. All rights reserved.
