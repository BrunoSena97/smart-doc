# SmartDoc Docker Deployment Helper
# Main commands are in root Makefile: make deploy, make dev-docker

.PHONY: help health clean shell

help: ## Show deployment-specific commands
	@echo "SmartDoc Deployment Helper"
	@echo "========================="
	@echo "🔍 Main commands are in root Makefile:"
	@echo "  make deploy          - Production deployment (Ollama in Docker)"
	@echo "  make dev-docker      - Development with local Ollama"
	@echo "  make ollama-check    - Check if local Ollama is running"
	@echo ""
	@echo "Local utilities:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

health: ## Check service health (works for both prod and dev)
	@echo "🏥 Checking SmartDoc health..."
	@sleep 2
	@curl -s http://localhost:8000/health | jq '.' || echo "❌ SmartDoc API not responding"
	@curl -s http://localhost:11434/api/tags >/dev/null && echo "✅ Ollama is healthy" || echo "❌ Ollama not responding"

clean: ## Remove containers, networks, and volumes
	@echo "🧹 Cleaning up SmartDoc deployment..."
	docker compose down -v --remove-orphans
	docker compose -f docker-compose.dev.yml down -v --remove-orphans 2>/dev/null || true
	docker system prune -f

shell: ## Open shell in smartdoc container
	@echo "🐚 Opening shell in SmartDoc container..."
	docker compose exec smartdoc bash || docker compose -f docker-compose.dev.yml exec smartdoc bash
