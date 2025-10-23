#!/bin/bash

# EclipseLink AI - Complete Setup Script
# This script sets up the entire development environment

set -e  # Exit on error

echo "🦚 EclipseLink AI - Initial Setup"
echo "=================================="

# Check prerequisites
echo "📋 Checking prerequisites..."

command -v node >/dev/null 2>&1 || { echo "❌ Node.js is required but not installed. Please install Node.js 18+"; exit 1; }
command -v git >/dev/null 2>&1 || { echo "❌ Git is required but not installed."; exit 1; }

echo "✅ Prerequisites met"

# Install root dependencies
echo ""
echo "📦 Installing root dependencies..."
npm install

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd apps/frontend
npm install
cd ../..

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd apps/backend
npm install
cd ../..

# Create environment files
echo ""
echo "⚙️  Setting up environment files..."

if [ ! -f apps/frontend/.env.local ]; then
    cp apps/frontend/.env.local.example apps/frontend/.env.local
    echo "✅ Created apps/frontend/.env.local (please update with your values)"
else
    echo "⏭️  apps/frontend/.env.local already exists"
fi

if [ ! -f apps/backend/.env ]; then
    cp apps/backend/.env.example apps/backend/.env
    echo "✅ Created apps/backend/.env (please update with your values)"
else
    echo "⏭️  apps/backend/.env already exists"
fi

# Initialize Supabase (if installed)
if command -v supabase >/dev/null 2>&1; then
    echo ""
    echo "🗄️  Initializing Supabase..."
    supabase init
    echo "✅ Supabase initialized"
else
    echo "⏭️  Supabase CLI not installed (optional for local development)"
fi

# Build packages
echo ""
echo "🔨 Building shared packages..."
cd packages/types && npm run build && cd ../..
cd packages/config && npm run build && cd ../..
cd packages/utils && npm run build && cd ../..
echo "✅ Packages built"

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Update environment variables in:"
echo "   - apps/frontend/.env.local"
echo "   - apps/backend/.env"
echo "2. Run 'npm run dev:frontend' to start the frontend"
echo "3. Run 'npm run dev:backend' to start the backend"
echo "4. Visit http://localhost:3000"
echo ""
echo "🦚 Happy coding with EclipseLink AI!"
