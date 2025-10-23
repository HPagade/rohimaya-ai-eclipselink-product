#!/bin/bash

# Database Seeding Script
# Seeds the database with initial data

set -e

echo "🌱 Seeding database..."

if [ -z "$DATABASE_URL" ]; then
    echo "❌ DATABASE_URL environment variable is not set"
    exit 1
fi

echo "📋 Found database: $DATABASE_URL"

# Run seed files
for file in database/seeds/*.sql; do
    if [ -f "$file" ]; then
        echo "Seeding: $(basename $file)"
        psql $DATABASE_URL -f "$file"
    fi
done

echo "✅ Database seeded successfully"
