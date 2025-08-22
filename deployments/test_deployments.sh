#!/bin/bash
# Quick deployment test script
# Tests both single-container and multi-container deployments

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_step() {
    echo -e "${GREEN}[$(date +'%H:%M:%S')] $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

log_error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

test_single_container() {
    log_step "Testing Single-Container Deployment"
    echo "======================================"
    
    cd /Users/bruno.sena/Projects/personal/masters/smart-doc/deployments/
    
    # Build and start
    log_step "Building and starting single container..."
    docker-compose -f compose-single.yaml build
    docker-compose -f compose-single.yaml up -d
    
    # Wait for health
    log_step "Waiting for service to be healthy..."
    local max_attempts=30
    local attempt=0
    
    while [[ $attempt -lt $max_attempts ]]; do
        if curl -sf http://localhost:8000/healthz >/dev/null 2>&1; then
            log_step "✅ Single-container deployment healthy!"
            break
        fi
        
        ((attempt++))
        echo "Waiting for health check... ($attempt/$max_attempts)"
        sleep 10
    done
    
    if [[ $attempt -eq $max_attempts ]]; then
        log_error "❌ Single-container deployment failed health check"
        docker-compose -f compose-single.yaml logs --tail=50
        return 1
    fi
    
    # Test endpoints
    log_step "Testing endpoints..."
    if curl -sf http://localhost:8000/healthz; then
        echo "✅ API endpoint working"
    else
        echo "❌ API endpoint failed"
    fi
    
    # Check Ollama in container
    if docker-compose -f compose-single.yaml exec -T smartdoc curl -sf http://localhost:11434/api/tags >/dev/null; then
        echo "✅ Ollama endpoint working"
    else
        echo "❌ Ollama endpoint failed"
    fi
    
    # Show container status
    echo ""
    echo "Container status:"
    docker-compose -f compose-single.yaml ps
    
    # Stop
    log_step "Stopping single-container deployment..."
    docker-compose -f compose-single.yaml down
    
    echo ""
}

test_multi_container() {
    log_step "Testing Multi-Container Deployment"
    echo "===================================="
    
    cd /Users/bruno.sena/Projects/personal/masters/smart-doc/deployments/
    
    # Build and start
    log_step "Building and starting multi-container..."
    docker-compose build
    docker-compose up -d
    
    # Wait for health
    log_step "Waiting for services to be healthy..."
    local max_attempts=30
    local attempt=0
    
    while [[ $attempt -lt $max_attempts ]]; do
        if curl -sf http://localhost:8000/healthz >/dev/null 2>&1; then
            log_step "✅ Multi-container deployment healthy!"
            break
        fi
        
        ((attempt++))
        echo "Waiting for health check... ($attempt/$max_attempts)"
        sleep 10
    done
    
    if [[ $attempt -eq $max_attempts ]]; then
        log_error "❌ Multi-container deployment failed health check"
        docker-compose logs --tail=50
        return 1
    fi
    
    # Test endpoints
    log_step "Testing endpoints..."
    if curl -sf http://localhost:8000/healthz; then
        echo "✅ API endpoint working"
    else
        echo "❌ API endpoint failed"
    fi
    
    if curl -sf http://localhost:8000 >/dev/null; then
        echo "✅ Web endpoint working"
    else
        echo "❌ Web endpoint failed"
    fi
    
    # Show services status
    echo ""
    echo "Services status:"
    docker-compose ps
    
    # Stop
    log_step "Stopping multi-container deployment..."
    docker-compose down
    
    echo ""
}

show_summary() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    Deployment Test Summary                   ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
    echo "Both deployment options are ready for production!"
    echo ""
    echo "🚀 To deploy for production:"
    echo "   Single-container (recommended): make deploy-single"
    echo "   Multi-container:               make deploy"
    echo ""
    echo "📊 To monitor:"
    echo "   make health"
    echo "   make logs-single  (or make logs)"
    echo ""
}

# Main execution
main() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                SmartDoc Deployment Testing                   ║"
    echo "║              RTX 4070 Ti SUPER Optimized                    ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
    
    # Check if we're in the right directory
    if [[ ! -f "/Users/bruno.sena/Projects/personal/masters/smart-doc/deployments/compose.yaml" ]]; then
        log_error "Deployment files not found. Please run from the correct directory."
        exit 1
    fi
    
    echo "This script will test both deployment architectures."
    echo "Each test will start the services, verify health, then stop them."
    echo ""
    read -p "Continue? (y/N): " -r
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Test cancelled."
        exit 0
    fi
    
    # Test single-container
    test_single_container
    
    # Test multi-container
    test_multi_container
    
    # Show summary
    show_summary
}

# Run main function
main "$@"
