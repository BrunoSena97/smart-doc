# SmartDoc Deployment Management
# RTX 4070 Ti SUPER Optimized

.PHONY: help deploy deploy-dev down logs health setup-models monitor clean

help: ## Show this help message
	@echo "SmartDoc Deployment Commands (RTX 4070 Ti SUPER Optimized)"
	@echo "=========================================================="
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

deploy: ## Deploy production services with GPU support
	@echo "🚀 Deploying SmartDoc with GPU acceleration..."
	docker-compose up -d
	@echo "✅ Deployment complete! Services starting..."
	@echo "📊 Run 'make setup-models' to configure Ollama models"

deploy-dev: ## Deploy with logs attached for development
	@echo "🔧 Starting development deployment with logs..."
	docker-compose up

down: ## Stop all services and remove containers
	@echo "🛑 Stopping all services..."
	docker-compose down

logs: ## Show logs from all services
	docker-compose logs -f

logs-api: ## Show API service logs
	docker-compose logs -f api

logs-ollama: ## Show Ollama service logs
	docker-compose logs -f ollama

logs-web: ## Show web service logs
	docker-compose logs -f web

health: ## Check health of all services
	@echo "🏥 Checking service health..."
	@docker-compose ps
	@echo ""
	@echo "🌐 Testing web endpoint..."
	@curl -s http://localhost:8000/healthz && echo "✅ API healthy" || echo "❌ API unhealthy"
	@curl -s http://localhost:8000 > /dev/null && echo "✅ Web healthy" || echo "❌ Web unhealthy"

setup-models: ## Interactive Ollama model setup for RTX 4070 Ti SUPER
	@echo "🤖 Setting up Ollama models..."
	./scripts/ollama_model_setup.sh

monitor: ## Launch interactive GPU monitoring
	@echo "📊 Starting GPU monitoring interface..."
	./scripts/monitor_gpu.sh interactive

status: ## Show quick status overview
	./scripts/monitor_gpu.sh status

gpu-status: ## Show GPU utilization
	@echo "🎯 GPU Status:"
	@nvidia-smi || echo "❌ nvidia-smi not available"

pull-model: ## Pull a specific model (usage: make pull-model MODEL=llama3.1:8b-instruct-q4_K_M)
	@if [ -z "$(MODEL)" ]; then echo "❌ Usage: make pull-model MODEL=model-name"; exit 1; fi
	@echo "📥 Pulling model: $(MODEL)"
	docker-compose exec ollama ollama pull $(MODEL)

list-models: ## List available and installed models
	@echo "📋 Installed models:"
	@docker-compose exec ollama ollama list || echo "❌ Ollama service not running"

clean: ## Clean up Docker resources
	@echo "🧹 Cleaning up Docker resources..."
	docker-compose down -v
	docker system prune -f
	@echo "✅ Cleanup complete"

restart: ## Restart all services
	@echo "🔄 Restarting services..."
	docker-compose restart

restart-api: ## Restart API service only
	docker-compose restart api

restart-ollama: ## Restart Ollama service only
	docker-compose restart ollama

backup-db: ## Backup SQLite database
	@echo "💾 Backing up database..."
	@timestamp=$$(date +%Y%m%d_%H%M%S); \
	docker-compose exec api cp /data/smartdoc.sqlite3 /data/backup_$$timestamp.sqlite3 && \
	echo "✅ Database backed up to backup_$$timestamp.sqlite3"

performance-test: ## Run performance test on current model
	@echo "⚡ Testing model performance..."
	@./scripts/monitor_gpu.sh performance

# Docker management
build: ## Rebuild all images
	docker-compose build --no-cache

pull: ## Pull latest images
	docker-compose pull

# Development helpers
shell-api: ## Open shell in API container
	docker-compose exec api /bin/bash

shell-ollama: ## Open shell in Ollama container
	docker-compose exec ollama /bin/bash

# Deployment verification
test-deployment: health ## Alias for health check

# GPU-specific commands
nvidia-test: ## Test GPU access in Docker
	@echo "🧪 Testing GPU access..."
	@docker run --rm --gpus all nvidia/cuda:11.8-base-ubuntu22.04 nvidia-smi || echo "❌ GPU access failed"

ollama-info: ## Show Ollama service information
	@echo "🤖 Ollama service info:"
	@docker-compose exec ollama ollama --version || echo "❌ Ollama not running"
	@echo ""
	@echo "Running models:"
	@docker-compose exec ollama ollama ps || echo "No models running"
