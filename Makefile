# ============================================================================
# EclipseLink AI - Makefile
# Simplified commands for development and deployment
# ============================================================================

.PHONY: help install dev build test clean deploy-prod health logs backup

# Default target - show help
help:
	@echo "EclipseLink AI - Available Commands"
	@echo ""
	@echo "Development:"
	@echo "  make install        Install dependencies"
	@echo "  make dev            Start development servers"
	@echo "  make dev-docker     Start with Docker (development mode)"
	@echo "  make build          Build production artifacts"
	@echo "  make test           Run tests"
	@echo "  make lint           Run linters"
	@echo "  make format         Format code"
	@echo "  make clean          Clean build artifacts"
	@echo ""
	@echo "Production:"
	@echo "  make deploy-prod    Deploy to production (Docker)"
	@echo "  make prod-up        Start production containers"
	@echo "  make prod-down      Stop production containers"
	@echo "  make prod-restart   Restart production containers"
	@echo "  make prod-logs      View production logs"
	@echo "  make prod-status    Check production status"
	@echo ""
	@echo "Database:"
	@echo "  make db-setup       Setup database schema"
	@echo "  make db-migrate     Run database migrations"
	@echo "  make db-backup      Backup database"
	@echo "  make db-restore     Restore database from backup"
	@echo ""
	@echo "Health & Monitoring:"
	@echo "  make health         Check application health"
	@echo "  make health-detail  Detailed health check"
	@echo "  make logs           View all logs"
	@echo "  make logs-backend   View backend logs"
	@echo "  make logs-frontend  View frontend logs"
	@echo ""
	@echo "Utilities:"
	@echo "  make security-scan  Run security audit"
	@echo "  make check-deps     Check for outdated dependencies"
	@echo "  make update-deps    Update dependencies"
	@echo ""

# ============================================================================
# Development Commands
# ============================================================================

install:
	@echo "📦 Installing dependencies..."
	npm install
	cd apps/backend && pip install -r requirements.txt
	@echo "✅ Dependencies installed"

dev:
	@echo "🚀 Starting development servers..."
	npm run dev

dev-docker:
	@echo "🐳 Starting development with Docker..."
	docker-compose up

build:
	@echo "🏗️ Building production artifacts..."
	npm run build
	@echo "✅ Build complete"

test:
	@echo "🧪 Running tests..."
	npm test
	@echo "✅ Tests complete"

lint:
	@echo "🔍 Running linters..."
	npm run lint
	@echo "✅ Linting complete"

format:
	@echo "💅 Formatting code..."
	npm run format
	@echo "✅ Formatting complete"

clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf node_modules apps/frontend/node_modules apps/frontend/dist
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Clean complete"

# ============================================================================
# Production Commands
# ============================================================================

deploy-prod:
	@echo "🚀 Deploying to production..."
	@if [ ! -f .env.production ]; then \
		echo "❌ .env.production not found!"; \
		echo "Run: cp .env.production.example .env.production"; \
		echo "Then edit .env.production with your values"; \
		exit 1; \
	fi
	docker-compose -f docker-compose.prod.yml --env-file .env.production build
	docker-compose -f docker-compose.prod.yml --env-file .env.production up -d
	@echo "✅ Production deployment complete"
	@echo "Run 'make health' to verify deployment"

prod-up:
	@echo "⬆️ Starting production containers..."
	docker-compose -f docker-compose.prod.yml --env-file .env.production up -d
	@echo "✅ Production containers started"

prod-down:
	@echo "⬇️ Stopping production containers..."
	docker-compose -f docker-compose.prod.yml down
	@echo "✅ Production containers stopped"

prod-restart:
	@echo "🔄 Restarting production containers..."
	docker-compose -f docker-compose.prod.yml restart
	@echo "✅ Production containers restarted"

prod-logs:
	@echo "📋 Viewing production logs..."
	docker-compose -f docker-compose.prod.yml logs -f

prod-status:
	@echo "📊 Production status:"
	docker-compose -f docker-compose.prod.yml ps

# ============================================================================
# Database Commands
# ============================================================================

db-setup:
	@echo "🗄️ Setting up database..."
	@if [ -f database/schema.sql ]; then \
		docker-compose exec -T postgres psql -U eclipselink_user -d eclipselink < database/schema.sql; \
		echo "✅ Database schema created"; \
	else \
		echo "❌ database/schema.sql not found"; \
	fi

db-migrate:
	@echo "🔄 Running database migrations..."
	@echo "ℹ️ Migrations not yet implemented"
	@echo "TODO: Add Alembic migrations"

db-backup:
	@echo "💾 Creating database backup..."
	@mkdir -p backups
	docker-compose exec -T postgres pg_dump -U eclipselink_user eclipselink | gzip > backups/eclipselink-$$(date +%Y%m%d-%H%M%S).sql.gz
	@echo "✅ Backup created in backups/"

db-restore:
	@echo "⚠️ WARNING: This will overwrite your current database!"
	@read -p "Enter backup file name (in backups/): " backup; \
	if [ -f "backups/$$backup" ]; then \
		gunzip -c "backups/$$backup" | docker-compose exec -T postgres psql -U eclipselink_user eclipselink; \
		echo "✅ Database restored from $$backup"; \
	else \
		echo "❌ Backup file not found: backups/$$backup"; \
	fi

# ============================================================================
# Health & Monitoring Commands
# ============================================================================

health:
	@echo "🏥 Checking application health..."
	@curl -f http://localhost:4000/health 2>/dev/null && echo "\n✅ Backend is healthy" || echo "\n❌ Backend is down"
	@curl -f http://localhost:3000 2>/dev/null > /dev/null && echo "✅ Frontend is healthy" || echo "❌ Frontend is down"

health-detail:
	@echo "🔍 Detailed health check..."
	@curl -f http://localhost:4000/api/health/detailed 2>/dev/null | python3 -m json.tool || echo "❌ Failed to get health details"

logs:
	@echo "📋 Viewing all logs..."
	docker-compose logs -f

logs-backend:
	@echo "📋 Viewing backend logs..."
	docker-compose logs -f backend

logs-frontend:
	@echo "📋 Viewing frontend logs..."
	docker-compose logs -f frontend

# ============================================================================
# Utility Commands
# ============================================================================

security-scan:
	@echo "🔒 Running security audit..."
	npm audit
	@echo ""
	@echo "Python security check:"
	cd apps/backend && pip list --outdated
	@echo "✅ Security scan complete"

check-deps:
	@echo "📦 Checking for outdated dependencies..."
	npm outdated
	@echo ""
	@echo "Backend dependencies:"
	cd apps/backend && pip list --outdated

update-deps:
	@echo "⬆️ Updating dependencies..."
	@echo "ℹ️ This will update package.json and requirements.txt"
	@read -p "Continue? (y/N): " confirm; \
	if [ "$$confirm" = "y" ]; then \
		npm update; \
		cd apps/backend && pip install --upgrade -r requirements.txt; \
		echo "✅ Dependencies updated"; \
	else \
		echo "❌ Update cancelled"; \
	fi

# ============================================================================
# Docker Quick Commands
# ============================================================================

docker-build:
	@echo "🐳 Building Docker images..."
	docker-compose build

docker-rebuild:
	@echo "🔨 Rebuilding Docker images (no cache)..."
	docker-compose build --no-cache

docker-clean:
	@echo "🧹 Cleaning Docker resources..."
	docker-compose down -v
	docker system prune -f
	@echo "✅ Docker cleanup complete"

# ============================================================================
# Environment Setup
# ============================================================================

setup-dev:
	@echo "🛠️ Setting up development environment..."
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✅ Created .env from .env.example"; \
		echo "⚠️ Edit .env with your API keys!"; \
	else \
		echo "ℹ️ .env already exists"; \
	fi
	make install
	@echo "✅ Development environment ready"

setup-prod:
	@echo "🏭 Setting up production environment..."
	@if [ ! -f .env.production ]; then \
		cp .env.production.example .env.production; \
		echo "✅ Created .env.production from example"; \
		echo "⚠️ Edit .env.production with your production values!"; \
		echo ""; \
		echo "Required:"; \
		echo "  - Generate SECRET_KEY: openssl rand -hex 32"; \
		echo "  - Add OPENAI_API_KEY"; \
		echo "  - Add ANTHROPIC_API_KEY"; \
		echo "  - Configure DATABASE_URL"; \
		echo "  - Configure REDIS_URL"; \
		echo "  - Set CORS_ORIGINS"; \
	else \
		echo "ℹ️ .env.production already exists"; \
	fi

# ============================================================================
# Pre-deployment Checks
# ============================================================================

preflight:
	@echo "✈️ Running pre-deployment checks..."
	@echo ""
	@echo "1. Checking environment file..."
	@test -f .env.production && echo "✅ .env.production exists" || (echo "❌ .env.production missing" && exit 1)
	@echo ""
	@echo "2. Checking required secrets..."
	@grep -q "SECRET_KEY=\[REQUIRED" .env.production && echo "❌ SECRET_KEY not set" || echo "✅ SECRET_KEY set"
	@grep -q "OPENAI_API_KEY=\[REQUIRED" .env.production && echo "❌ OPENAI_API_KEY not set" || echo "✅ OPENAI_API_KEY set"
	@grep -q "ANTHROPIC_API_KEY=\[REQUIRED" .env.production && echo "❌ ANTHROPIC_API_KEY not set" || echo "✅ ANTHROPIC_API_KEY set"
	@echo ""
	@echo "3. Checking Docker..."
	@docker --version > /dev/null 2>&1 && echo "✅ Docker installed" || (echo "❌ Docker not installed" && exit 1)
	@docker compose version > /dev/null 2>&1 && echo "✅ Docker Compose installed" || (echo "❌ Docker Compose not installed" && exit 1)
	@echo ""
	@echo "4. Building images..."
	@docker-compose -f docker-compose.prod.yml build > /dev/null 2>&1 && echo "✅ Images built successfully" || (echo "❌ Build failed" && exit 1)
	@echo ""
	@echo "✅ Preflight checks passed!"
	@echo "Ready to deploy with: make deploy-prod"

# ============================================================================
# Quick Start Commands
# ============================================================================

quickstart:
	@echo "🚀 EclipseLink AI - Quick Start"
	@echo ""
	@echo "Choose an option:"
	@echo "  1. Development (local)"
	@echo "  2. Development (Docker)"
	@echo "  3. Production (Docker)"
	@echo ""
	@read -p "Enter choice [1-3]: " choice; \
	case $$choice in \
		1) make setup-dev && make dev ;; \
		2) make setup-dev && make dev-docker ;; \
		3) make setup-prod && make preflight && make deploy-prod ;; \
		*) echo "Invalid choice" ;; \
	esac

# ============================================================================
# Documentation
# ============================================================================

docs:
	@echo "📚 Available documentation:"
	@echo ""
	@echo "  README.md                            - Project overview"
	@echo "  GETTING-STARTED.md                   - Beginner-friendly setup guide"
	@echo "  docs/DOCUMENTATION-INDEX.md          - Complete documentation index"
	@echo "  docs/deployment/PRODUCTION-DEPLOYMENT.md - Production deployment guide"
	@echo "  docs/security/SECURITY-CHECKLIST.md  - Security checklist"
	@echo "  docs/development/README-DEVELOPERS.md - Developer guide"
	@echo ""

# ============================================================================
# Version and Info
# ============================================================================

version:
	@echo "EclipseLink AI v1.0.0"
	@echo "Copyright © 2025 Rohimaya Health AI"

info:
	@echo "📊 System Information:"
	@echo ""
	@echo "Node: $$(node --version 2>/dev/null || echo 'Not installed')"
	@echo "NPM: $$(npm --version 2>/dev/null || echo 'Not installed')"
	@echo "Python: $$(python3 --version 2>/dev/null || echo 'Not installed')"
	@echo "Docker: $$(docker --version 2>/dev/null || echo 'Not installed')"
	@echo "Docker Compose: $$(docker compose version 2>/dev/null || echo 'Not installed')"
	@echo ""
	@echo "Repository: $$(git remote get-url origin 2>/dev/null || echo 'Not a git repository')"
	@echo "Branch: $$(git branch --show-current 2>/dev/null || echo 'N/A')"
	@echo ""
