# SmartDoc Production Deployment
# External Ollama Architecture

.PHONY: help deploy dev down logs health clean

help: ## Show this help message
	@echo "SmartDoc Production Deployment"
	@echo "=============================="
	@echo "Prerequisites: Ollama running on host with GPU"
	@echo "  curl -fsSL https://ollama.com/install.sh | sh"
	@echo "  ollama serve &"
	@echo "  ollama pull gemma2:9b-instruct-q4_K_M"
	@echo ""
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

deploy: ## Deploy SmartDoc production (requires external Ollama)
	@echo "🚀 Deploying SmartDoc..."
	@echo "📋 Ensure Ollama is running: ollama serve"
	docker compose up --build -d
	@echo "✅ Deployment complete!"

dev: ## Deploy with logs (development mode)
	@echo "🔧 Starting development deployment..."
	docker compose up --build

down: ## Stop and remove containers
	@echo "🛑 Stopping deployment..."
	docker compose down

logs: ## Show container logs
	docker compose logs -f smartdoc

health: ## Check deployment health
	@echo "🏥 Checking deployment health..."
	@docker compose ps
	@echo ""
	@echo "Testing endpoints:"
	@curl -s http://localhost:8000/health && echo "✅ API healthy" || echo "❌ API unhealthy"
	@echo "Checking external Ollama:"
	@curl -s http://localhost:11434/api/tags >/dev/null && echo "✅ Ollama reachable" || echo "❌ Ollama not reachable"

clean: ## Clean up Docker resources
	@echo "🧹 Cleaning up..."
	docker compose down -v
	docker system prune -f

restart: ## Restart deployment
	@echo "🔄 Restarting..."
	docker compose restart

build: ## Rebuild container
	docker compose build --no-cache

shell: ## Open shell in container
	docker compose exec smartdoc bash

# External Ollama helpers
ollama-status: ## Check external Ollama status
	@echo "🤖 External Ollama status:"
	@curl -s http://localhost:11434/api/tags && echo "" || echo "❌ Ollama not responding"

ollama-models: ## List available models in external Ollama
	@echo "📋 Available models:"
	@curl -s http://localhost:11434/api/tags | grep -o '"name":"[^"]*"' | cut -d'"' -f4 || echo "No models or Ollama not running"
