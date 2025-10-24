#!/bin/bash

# EclipseLink AI™ - Database Setup Script
# This script initializes the PostgreSQL database with all tables, functions, and triggers

set -e  # Exit on error

echo "🦚 EclipseLink AI - Database Setup"
echo "===================================="
echo ""

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo "❌ ERROR: DATABASE_URL environment variable is not set"
    echo "   Please set it to your PostgreSQL connection string"
    echo "   Example: export DATABASE_URL='postgresql://user:password@host:5432/database'"
    exit 1
fi

echo "✅ DATABASE_URL is set"
echo ""

# Function to execute SQL file
execute_sql() {
    local file=$1
    local description=$2
    echo "📝 $description"
    psql "$DATABASE_URL" -f "$file"
    echo "   ✅ Done"
    echo ""
}

# Confirm before proceeding
echo "⚠️  This will create/modify database schema at:"
echo "   $DATABASE_URL"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Aborted"
    exit 1
fi

echo ""
echo "🚀 Starting database setup..."
echo ""

# Execute schema files in order
execute_sql "schema.sql" "Creating enums and core tables (facilities, staff, patients)"
execute_sql "migrations/001_core_tables.sql" "Creating handoff tables and voice processing tables"
execute_sql "migrations/002_audit_and_notifications.sql" "Creating audit logs, notifications, and EHR tables"
execute_sql "functions/triggers.sql" "Creating database functions, triggers, and RLS policies"

echo ""
echo "✅ Database setup complete!"
echo ""
echo "📊 Database Summary:"
echo "   - 15 core tables created"
echo "   - Row-Level Security (RLS) enabled"
echo "   - Audit logging configured"
echo "   - Triggers for updated_at timestamps"
echo ""
echo "🔐 Security Features:"
echo "   - Facility-level data isolation"
echo "   - HIPAA-compliant audit trail"
echo "   - Encrypted credentials storage"
echo "   - PHI access tracking"
echo ""
echo "📝 Next steps:"
echo "   1. Verify tables: psql \$DATABASE_URL -c '\\dt'"
echo "   2. Load seed data (optional): bash database/seeds/load_seeds.sh"
echo "   3. Test RLS policies"
echo "   4. Configure Supabase Auth integration"
echo ""
echo "🦚 EclipseLink AI database is ready!"
