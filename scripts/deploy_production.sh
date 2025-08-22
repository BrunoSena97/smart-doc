#!/bin/bash
# SmartDoc Production Deployment Script
# Complete automated deployment for RTX 4070 Ti SUPER

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEPLOYMENTS_DIR="$PROJECT_DIR/deployments"
BACKUP_DIR="$PROJECT_DIR/backups/$(date +%Y%m%d_%H%M%S)"

show_header() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                SmartDoc Production Deployment                ║"
    echo "║              RTX 4070 Ti SUPER Optimized                    ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

log_step() {
    echo -e "${GREEN}[$(date +'%H:%M:%S')] $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

log_error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

check_prerequisites() {
    log_step "Checking prerequisites..."

    if [[ -f "$PROJECT_DIR/scripts/check_prerequisites.sh" ]]; then
        bash "$PROJECT_DIR/scripts/check_prerequisites.sh"
    else
        log_warning "Prerequisites check script not found, continuing..."
    fi
}

backup_existing_data() {
    log_step "Creating backup of existing data..."

    mkdir -p "$BACKUP_DIR"

    # Backup existing database if it exists
    if [[ -f "$PROJECT_DIR/apps/api/instance/smartdoc.sqlite3" ]]; then
        cp "$PROJECT_DIR/apps/api/instance/smartdoc.sqlite3" "$BACKUP_DIR/"
        log_step "Database backed up to $BACKUP_DIR"
    fi

    # Backup any existing .env file
    if [[ -f "$PROJECT_DIR/.env" ]]; then
        cp "$PROJECT_DIR/.env" "$BACKUP_DIR/"
    fi

    if [[ -f "$DEPLOYMENTS_DIR/.env" ]]; then
        cp "$DEPLOYMENTS_DIR/.env" "$BACKUP_DIR/"
    fi
}

setup_environment() {
    log_step "Setting up environment configuration..."

    cd "$DEPLOYMENTS_DIR"

    # Create .env file if it doesn't exist
    if [[ ! -f ".env" ]]; then
        cp .env.example .env
        log_step "Created .env file from template"
    else
        log_warning ".env file already exists, keeping current configuration"
    fi

    # Show current configuration
    echo "Current environment configuration:"
    echo "--------------------------------"
    grep "OLLAMA_MODEL\|FLASK_ENV\|LOG_LEVEL" .env || echo "No configuration found"
    echo ""
}

pull_latest_images() {
    log_step "Pulling latest Docker images..."

    cd "$DEPLOYMENTS_DIR"
    docker compose pull
}

stop_existing_services() {
    log_step "Stopping any existing services..."

    cd "$DEPLOYMENTS_DIR"
    docker compose down || true

    # Clean up any orphaned containers
    docker container prune -f || true
}

deploy_services() {
    log_step "Deploying SmartDoc services with GPU support..."

    cd "$DEPLOYMENTS_DIR"

    # Build and start services
    docker compose up --build -d

    log_step "Services started. Waiting for health checks..."

    # Wait for services to be healthy
    local max_attempts=30
    local attempt=0

    while [[ $attempt -lt $max_attempts ]]; do
        if docker compose ps | grep -q "healthy"; then
            log_step "Services are healthy!"
            break
        fi

        ((attempt++))
        echo "Waiting for services to be ready... ($attempt/$max_attempts)"
        sleep 10
    done

    if [[ $attempt -eq $max_attempts ]]; then
        log_error "Services failed to become healthy in time"
        return 1
    fi
}

setup_models() {
    log_step "Setting up Ollama models..."

    cd "$DEPLOYMENTS_DIR"

    echo "Would you like to run interactive model setup? (y/N)"
    read -r setup_models_interactive

    if [[ "$setup_models_interactive" =~ ^[Yy]$ ]]; then
        ./scripts/ollama_model_setup.sh
    else
        log_step "Pulling default model (gemma3:4b-it-q4_K_M)..."
        docker compose exec ollama ollama pull gemma3:4b-it-q4_K_M
    fi
}

verify_deployment() {
    log_step "Verifying deployment..."

    cd "$DEPLOYMENTS_DIR"

    # Check service status
    echo "Service Status:"
    echo "---------------"
    docker compose ps
    echo ""

    # Test endpoints
    echo "Testing endpoints..."

    # Test health endpoint
    if curl -s http://localhost:8000/healthz > /dev/null; then
        log_step "✅ API health endpoint responding"
    else
        log_error "❌ API health endpoint not responding"
    fi

    # Test web interface
    if curl -s http://localhost:8000 > /dev/null; then
        log_step "✅ Web interface accessible"
    else
        log_error "❌ Web interface not accessible"
    fi

    # Test Ollama service
    if docker compose exec -T ollama ollama list > /dev/null 2>&1; then
        log_step "✅ Ollama service responding"
        echo "Available models:"
        docker compose exec -T ollama ollama list
    else
        log_error "❌ Ollama service not responding"
    fi
}

show_status() {
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                    Deployment Complete!                     ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "🌐 SmartDoc is now running at: http://localhost:8000"
    echo "🤖 Ollama service available internally"
    echo "💾 Data persisted in Docker volumes"
    echo ""
    echo "Management Commands:"
    echo "-------------------"
    echo "• Check status:        cd deployments && make status"
    echo "• Monitor GPU:         cd deployments && make monitor"
    echo "• View logs:           cd deployments && make logs"
    echo "• Restart services:    cd deployments && make restart"
    echo "• Stop services:       cd deployments && make down"
    echo ""
    echo "Backup created at: $BACKUP_DIR"
    echo ""
}

show_troubleshooting() {
    echo "Troubleshooting:"
    echo "----------------"
    echo "• View logs: docker compose logs -f"
    echo "• Check GPU: nvidia-smi"
    echo "• Test GPU in Docker: make nvidia-test"
    echo "• Reset deployment: make clean && make deploy"
    echo ""
}

# Main deployment process
main() {
    show_header

    # Step 1: Prerequisites
    check_prerequisites

    # Step 2: Backup
    backup_existing_data

    # Step 3: Environment setup
    setup_environment

    # Step 4: Pull images
    pull_latest_images

    # Step 5: Stop existing
    stop_existing_services

    # Step 6: Deploy
    deploy_services

    # Step 7: Setup models
    setup_models

    # Step 8: Verify
    verify_deployment

    # Step 9: Show status
    show_status

    echo "Would you like to open the monitoring interface? (y/N)"
    read -r open_monitor

    if [[ "$open_monitor" =~ ^[Yy]$ ]]; then
        cd "$DEPLOYMENTS_DIR"
        ./scripts/monitor_gpu.sh interactive
    fi
}

# Handle errors
trap 'log_error "Deployment failed at step: $BASH_COMMAND"' ERR

# Check if running as root
if [[ $EUID -eq 0 ]]; then
    log_warning "Running as root. Consider using a non-root user for Docker operations."
fi

# Run main deployment
main "$@"
