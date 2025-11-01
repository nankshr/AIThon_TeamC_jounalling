#!/bin/bash

# Setup script for Wedding Journal MVP
# This script helps with initial setup of both backend and frontend

set -e

echo "🎉 Wedding Journal MVP - Setup Script"
echo "======================================"
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_step() {
    echo -e "${BLUE}→${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check prerequisites
print_step "Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+"
    exit 1
fi
print_success "Python 3 found"

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 20+"
    exit 1
fi
print_success "Node.js found"

# Backend setup
print_step "Setting up backend..."

cd backend

# Install poetry if needed
if ! command -v poetry &> /dev/null; then
    print_warning "Poetry not found, installing..."
    pip install poetry
fi
print_success "Poetry available"

# Install dependencies
print_step "Installing Python dependencies (this may take a moment)..."
poetry install
print_success "Backend dependencies installed"

# Check for .env file
if [ ! -f .env ]; then
    print_warning ".env file not found, creating from template..."
    cp .env.example .env
    print_warning "⚠️  Please edit backend/.env with your database credentials"
else
    print_success ".env file exists"
fi

# Frontend setup
cd ..
print_step "Setting up frontend..."

cd frontend

# Install node dependencies
print_step "Installing Node dependencies (this may take a moment)..."
npm install
print_success "Frontend dependencies installed"

# Check for .env.local file
if [ ! -f .env.local ]; then
    print_warning ".env.local file not found, creating from template..."
    cp .env.local.example .env.local
    print_success ".env.local created (using defaults)"
else
    print_success ".env.local file exists"
fi

cd ..

# Summary
echo ""
print_success "Setup complete! ✨"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env with your cloud PostgreSQL credentials"
echo "2. Run database migrations: cd backend && poetry run alembic upgrade head"
echo "3. Start backend: poetry run uvicorn app.main:app --reload"
echo "4. In another terminal, start frontend: cd frontend && npm run dev"
echo "5. Open http://localhost:3000 in your browser"
echo ""
echo "For more details, see SETUP_GUIDE.md"
