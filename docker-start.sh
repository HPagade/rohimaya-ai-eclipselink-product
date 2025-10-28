#!/bin/bash

# =============================================================================
# EclipseLink AI - Docker Quick Start Script
# =============================================================================
# This script helps you get EclipseLink AI running with Docker quickly
# =============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Header
echo ""
echo -e "${BLUE}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                               ║${NC}"
echo -e "${BLUE}║              EclipseLink AI™ - Docker Setup                   ║${NC}"
echo -e "${BLUE}║        Voice-Enabled Clinical Handoff Platform                ║${NC}"
echo -e "${BLUE}║                                                               ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if Docker is installed
print_info "Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed!"
    echo ""
    echo "Please install Docker from: https://docs.docker.com/get-docker/"
    exit 1
fi
print_success "Docker is installed"

# Check if Docker Compose is installed
print_info "Checking Docker Compose installation..."
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    print_error "Docker Compose is not installed!"
    echo ""
    echo "Please install Docker Compose from: https://docs.docker.com/compose/install/"
    exit 1
fi
print_success "Docker Compose is installed"

# Check if .env file exists
print_info "Checking for .env file..."
if [ ! -f .env ]; then
    print_warning ".env file not found. Creating from .env.example..."
    cp .env.example .env
    print_success "Created .env file"
    echo ""
    print_warning "IMPORTANT: Please edit .env and add your Azure OpenAI credentials!"
    echo ""
    echo "Required variables:"
    echo "  - AZURE_OPENAI_KEY"
    echo "  - AZURE_OPENAI_ENDPOINT"
    echo ""
    read -p "Press Enter after you've edited .env (or Ctrl+C to exit and edit later)..."
else
    print_success ".env file exists"
fi

# Check if Azure OpenAI credentials are set
print_info "Checking Azure OpenAI configuration..."
if grep -q "your-azure-openai-api-key-here" .env; then
    print_warning "Azure OpenAI credentials not configured!"
    echo ""
    echo "Please edit .env and add your Azure OpenAI credentials."
    echo "The application will start, but AI features won't work without these."
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Exiting. Please configure .env and run this script again."
        exit 0
    fi
fi

# Stop any existing containers
print_info "Stopping any existing EclipseLink containers..."
docker-compose down 2>/dev/null || true
print_success "Existing containers stopped"

# Remove old volumes (optional - ask user)
echo ""
read -p "Remove old data volumes? This will delete all existing data. (y/N) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_info "Removing old volumes..."
    docker volume rm eclipselink-postgres-data 2>/dev/null || true
    docker volume rm eclipselink-redis-data 2>/dev/null || true
    print_success "Old volumes removed"
fi

# Build images
echo ""
print_info "Building Docker images (this may take a few minutes)..."
docker-compose build
print_success "Docker images built successfully"

# Start services
echo ""
print_info "Starting EclipseLink AI services..."
docker-compose up -d
print_success "Services started"

# Wait for services to be healthy
echo ""
print_info "Waiting for services to be ready..."
sleep 5

# Check if database is ready
print_info "Checking PostgreSQL..."
timeout=60
counter=0
until docker-compose exec -T postgres pg_isready -U eclipselink_user -d eclipselink &>/dev/null; do
    sleep 1
    counter=$((counter + 1))
    if [ $counter -ge $timeout ]; then
        print_error "PostgreSQL failed to start within $timeout seconds"
        echo ""
        echo "Check logs with: docker-compose logs postgres"
        exit 1
    fi
done
print_success "PostgreSQL is ready"

# Check if Redis is ready
print_info "Checking Redis..."
counter=0
until docker-compose exec -T redis redis-cli ping &>/dev/null; do
    sleep 1
    counter=$((counter + 1))
    if [ $counter -ge $timeout ]; then
        print_error "Redis failed to start within $timeout seconds"
        echo ""
        echo "Check logs with: docker-compose logs redis"
        exit 1
    fi
done
print_success "Redis is ready"

# Check if backend is ready
print_info "Checking Backend API..."
counter=0
until curl -f http://localhost:4000/health &>/dev/null; do
    sleep 2
    counter=$((counter + 2))
    if [ $counter -ge $timeout ]; then
        print_warning "Backend may still be starting..."
        break
    fi
done
print_success "Backend API is ready"

# Success message
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                               ║${NC}"
echo -e "${GREEN}║          🎉 EclipseLink AI is now running! 🎉                ║${NC}"
echo -e "${GREEN}║                                                               ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""
print_info "Access the application:"
echo ""
echo "  Frontend (UI):        http://localhost:3000"
echo "  Backend API:          http://localhost:4000"
echo "  API Documentation:    http://localhost:4000/api/docs"
echo "  PostgreSQL:           localhost:5432"
echo "  Redis:                localhost:6379"
echo ""
print_info "Useful commands:"
echo ""
echo "  View logs (all):      docker-compose logs -f"
echo "  View logs (backend):  docker-compose logs -f backend"
echo "  View logs (frontend): docker-compose logs -f frontend"
echo "  Stop services:        docker-compose down"
echo "  Restart services:     docker-compose restart"
echo "  Run database migrations: docker-compose exec backend npm run migrate"
echo ""
print_info "Default credentials:"
echo ""
echo "  Email:    admin@eclipselink.ai"
echo "  Password: changeme"
echo ""
print_warning "Remember to change the default password after first login!"
echo ""
print_success "Setup complete! Happy coding! 🚀"
echo ""
