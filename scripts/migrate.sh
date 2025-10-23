#!/bin/bash

# Database Migration Script
# Runs all pending migrations in the database/migrations directory

set -e

echo "🗄️  Running database migrations..."

if [ -z "$DATABASE_URL" ]; then
    echo "❌ DATABASE_URL environment variable is not set"
    exit 1
fi

echo "📋 Found database: $DATABASE_URL"

# Run migrations
for file in database/migrations/*.sql; do
    if [ -f "$file" ]; then
        echo "Running migration: $(basename $file)"
        psql $DATABASE_URL -f "$file"
    fi
done

echo "✅ All migrations completed successfully"
