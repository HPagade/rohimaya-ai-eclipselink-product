#!/bin/bash

# =============================================
# EclipseLink AI - Complete Setup Script
# =============================================

set -e  # Exit on error

echo "🚀 EclipseLink AI - Complete Setup"
echo "===================================="
echo ""

# Check Node.js version
echo "📦 Checking Node.js version..."
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
  echo "❌ Error: Node.js 18+ is required. Current version: $(node -v)"
  exit 1
fi
echo "✅ Node.js version: $(node -v)"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
npm install
echo "✅ Dependencies installed"
echo ""

# Setup database
if [ -z "$DATABASE_URL" ]; then
  echo "⚠️  DATABASE_URL not set. Skipping database setup."
  echo "   To set up the database later, run:"
  echo "   export DATABASE_URL=\"your-connection-string\""
  echo "   bash database/setup.sh"
else
  echo "🗄️  Setting up database..."
  bash database/setup.sh
  echo "✅ Database setup complete"
fi
echo ""

# Create .env files if they don't exist
echo "🔐 Setting up environment files..."
if [ ! -f "apps/backend/.env" ]; then
  cp apps/backend/.env.example apps/backend/.env
  echo "✅ Created apps/backend/.env from template"
  echo "   ⚠️  Please update with your actual credentials"
else
  echo "✅ apps/backend/.env already exists"
fi

if [ ! -f "apps/frontend/.env.local" ]; then
  if [ -f "apps/frontend/.env.local.example" ]; then
    cp apps/frontend/.env.local.example apps/frontend/.env.local
    echo "✅ Created apps/frontend/.env.local from template"
  fi
else
  echo "✅ apps/frontend/.env.local already exists"
fi
echo ""

# Build shared packages
echo "🔨 Building shared packages..."
npm run build --workspace=packages/types --workspace=packages/config --workspace=packages/utils 2>/dev/null || echo "  ⚠️  Some packages failed to build (expected if not all created yet)"
echo ""

echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Update environment variables in apps/backend/.env"
echo "  2. Update environment variables in apps/frontend/.env.local (if applicable)"
echo "  3. Run 'npm run dev' to start development servers"
echo "  4. Frontend: http://localhost:3000"
echo "  5. Backend: http://localhost:4000"
echo ""
echo "For more information, see README.md"
