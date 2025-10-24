#!/bin/bash

# =============================================
# EclipseLink AI - Database Setup Script
# =============================================

set -e  # Exit on error

echo "🚀 EclipseLink AI Database Setup"
echo "=================================="
echo ""

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
  echo "❌ Error: DATABASE_URL environment variable is not set"
  echo ""
  echo "Please set it with:"
  echo "  export DATABASE_URL=\"postgresql://postgres:[PASSWORD]@db.[PROJECT].supabase.co:5432/postgres\""
  exit 1
fi

echo "✅ Database URL configured"
echo ""

# Check if psql is installed
if ! command -v psql &> /dev/null; then
  echo "❌ Error: psql is not installed"
  echo "Please install PostgreSQL client tools"
  exit 1
fi

echo "✅ psql found"
echo ""

# Test database connection
echo "📡 Testing database connection..."
if ! psql "$DATABASE_URL" -c "SELECT version();" > /dev/null 2>&1; then
  echo "❌ Error: Could not connect to database"
  echo "Please check your DATABASE_URL"
  exit 1
fi

echo "✅ Database connection successful"
echo ""

# Run migrations in order
echo "📊 Running database migrations..."
echo ""

echo "  [1/4] Running complete schema (enums + core tables)..."
if [ -f "database/schema.sql" ]; then
  psql "$DATABASE_URL" -f database/schema.sql > /dev/null 2>&1 || {
    echo "    Using migrations instead..."
    psql "$DATABASE_URL" -f database/migrations/001_core_tables.sql > /dev/null 2>&1
  }
  echo "  ✅ Core tables created"
else
  psql "$DATABASE_URL" -f database/migrations/001_core_tables.sql > /dev/null 2>&1
  echo "  ✅ Core tables created (from migration)"
fi

echo "  [2/4] Creating audit and notification tables..."
if [ -f "database/migrations/002_audit_and_notifications.sql" ]; then
  psql "$DATABASE_URL" -f database/migrations/002_audit_and_notifications.sql > /dev/null 2>&1
  echo "  ✅ Audit and notification tables created"
else
  echo "  ⚠️  002_audit_and_notifications.sql not found, skipping"
fi

echo "  [3/4] Creating functions and triggers..."
if [ -f "database/functions/triggers.sql" ]; then
  psql "$DATABASE_URL" -f database/functions/triggers.sql > /dev/null 2>&1
  echo "  ✅ Functions and triggers created"
else
  echo "  ⚠️  triggers.sql not found, skipping"
fi

echo "  [4/4] Enabling Row-Level Security..."
psql "$DATABASE_URL" << 'SQL' > /dev/null 2>&1
-- Ensure RLS is enabled on all tables
ALTER TABLE facilities ENABLE ROW LEVEL SECURITY;
ALTER TABLE staff ENABLE ROW LEVEL SECURITY;
ALTER TABLE patients ENABLE ROW LEVEL SECURITY;
ALTER TABLE handoffs ENABLE ROW LEVEL SECURITY;
SQL
echo "  ✅ RLS enabled"

echo ""
echo "🎉 Database setup complete!"
echo ""

# Show table count
TABLE_COUNT=$(psql "$DATABASE_URL" -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';" | tr -d ' ')
echo "📊 Database Statistics:"
echo "  - Tables created: $TABLE_COUNT"

# Show tables
echo ""
echo "📋 Tables:"
psql "$DATABASE_URL" -c "\dt" | grep "public" || echo "  No tables found"

echo ""
echo "✅ Setup complete! Your database is ready to use."
echo ""
echo "Next steps:"
echo "  1. Update your .env file with DATABASE_URL"
echo "  2. Run 'npm run dev:backend' to start the API server"
echo "  3. Visit http://localhost:4000/api/docs for API documentation"
echo ""
