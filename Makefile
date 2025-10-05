.PHONY: help setup test api web docker-build docker-up format clean lint type-check install install-poetry

# Default target
help: ## Show this help message
	@echo "SmartDoc Development Commands"
	@echo "=============================="
	@echo ""
	@echo "🚀 Quick Start:"
	@echo "  make setup           - Set up all Poetry environments"
	@echo "  make api-local       - Run API locally (for development)"
	@echo "  make web             - Serve static frontend"
	@echo ""
	@echo "🧪 Testing Commands:"
	@echo "  make test            - Run all tests (core + API + integration)"
	@echo "  make test-core       - Run core package tests only"
	@echo "  make test-api-unit   - Run API package unit tests"
	@echo "  make test-integration - Run integration tests"
	@echo "  make test-frontend   - Run frontend demo scripts"
	@echo "  make test-dev        - Run development tools"
	@echo "  make test-file FILE=path - Run specific test file"
	@echo ""
	@echo "🐳 Docker Options:"
	@echo "  make dev-docker      - SmartDoc in Docker + local Ollama"
	@echo "  make deploy          - Full production deployment"
	@echo ""
	@echo "All commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install-poetry: ## Install Poetry if not present
	@which poetry > /dev/null || pip install poetry

setup: install-poetry ## Set up development environment with Poetry
	@echo "🔧 Setting up SmartDoc development environment with Poetry..."
	cd packages/core && poetry install
	cd apps/api && poetry install
	@echo "✅ Setup complete!"

install: install-poetry ## Install packages in development mode using Poetry
	cd packages/core && poetry install
	cd apps/api && poetry install

test: ## Run all tests (core, api, and integration tests)
	@echo "🧪 Running all tests..."
	@echo "📦 Testing core package..."
	cd packages/core && poetry run pytest -v
	@echo "🔌 Testing API package..."
	cd apps/api && poetry run pytest -v
	@echo "🔗 Running integration tests..."
	$(MAKE) test-integration
	@echo "✅ All tests completed!"

test-core: ## Run core package tests only
	@echo "📦 Running core package tests..."
	cd packages/core && poetry run pytest -v

test-api-unit: ## Run API package tests only
	@echo "🔌 Running API package tests..."
	cd apps/api && poetry run pytest -v

test-integration: ## Run integration tests
	@echo "🔗 Running integration tests..."
	cd packages/core && poetry run python ../../tests/integration/test_medication_escalation_flow.py
	cd packages/core && poetry run python ../../tests/integration/test_imaging_escalation_flow.py
	cd packages/core && poetry run python ../../tests/integration/test_labs_specific_intents.py

test-frontend: ## Run frontend demonstration scripts
	@echo "🎭 Running frontend demonstration tests..."
	cd packages/core && poetry run python ../../tests/frontend/test_correct_diagnosis_path.py
	cd packages/core && poetry run python ../../tests/frontend/test_biased_diagnosis_path.py

test-dev: ## Run development tools
	@echo "🛠️ Running development tools..."
	cd packages/core && poetry run python ../../dev-tools/check_intents.py
	cd packages/core && poetry run python ../../dev-tools/debug_lab_intent.py

# Test specific file - usage: make test-file FILE=path/to/test_file.py
test-file: ## Run a specific test file (usage: make test-file FILE=tests/integration/test_medication_escalation_flow.py)
	@if [ -z "$(FILE)" ]; then \
		echo "❌ Please specify a file: make test-file FILE=path/to/test_file.py"; \
		exit 1; \
	fi
	@echo "🎯 Running specific test file: $(FILE)"
	@if echo "$(FILE)" | grep -q "tests/integration\|tests/frontend\|dev-tools"; then \
		echo "🏃 Running in core environment..."; \
		cd packages/core && poetry run python "../../$(FILE)"; \
	elif echo "$(FILE)" | grep -q "packages/core"; then \
		echo "📦 Running in core environment..."; \
		cd packages/core && poetry run python "$(FILE)"; \
	elif echo "$(FILE)" | grep -q "apps/api"; then \
		echo "🔌 Running in API environment..."; \
		cd apps/api && poetry run python "$(FILE)"; \
	else \
		echo "❌ Unknown test file location. Please check the path."; \
		exit 1; \
	fi

api: ## Run the Flask API server
	@echo "🚀 Starting SmartDoc API..."
	cd apps/api && poetry run python -m smartdoc_api.main

api-dev: ## Run the alternative dev server
	@echo "🔧 Starting SmartDoc API (dev server)..."
	cd apps/api && poetry run python -m smartdoc_api.dev_server

api-flask: ## Run API using Flask CLI (alternative method)
	@echo "🌶️ Starting SmartDoc API with Flask CLI..."
	cd apps/api && poetry run flask --app smartdoc_api run --debug --host 0.0.0.0 --port 8000

api-gunicorn: ## Run API with Gunicorn (production-like)
	@echo "🦄 Starting SmartDoc API with Gunicorn..."
	cd apps/api && poetry run gunicorn --bind 0.0.0.0:8000 --workers 2 --reload "smartdoc_api:create_app()"

web: ## Run the frontend static server
	@echo "🌐 Starting web frontend..."
	cd apps/web/public && python -m http.server 3000

health-check: ## Check if API is running
	@echo "🏥 Checking API health..."
	@curl -s http://localhost:8000/health | jq '.' || echo "API not responding or jq not installed"

test-api: ## Quick test of API endpoints
	@echo "🧪 Testing API endpoints..."
	@echo "Health check:" && curl -s http://localhost:8000/health
	@echo "\nChat API:" && curl -s -X POST http://localhost:8000/api/v1/chat -H "Content-Type: application/json" -d '{"message":"test"}'
	@echo "\nLegacy chat:" && curl -s -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message":"test"}'

# Development with local Ollama
dev-docker: ## Run SmartDoc in Docker with local Ollama (development)
	@echo "� Starting SmartDoc development with local Ollama..."
	@echo "📋 Make sure Ollama is running locally: ollama serve"
	@echo "📋 And model is available: ollama pull gemma3:4b-it-q4_K_M"
	cd deployments && docker compose -f docker-compose.dev.yml up --build

dev-docker-down: ## Stop development Docker deployment
	@echo "⏹️ Stopping development deployment..."
	cd deployments && docker compose -f docker-compose.dev.yml down

dev-docker-down-clean: ## Stop development Docker deployment and remove volumes
	@echo "⏹️ Stopping development deployment..."
	cd deployments && docker compose -f docker-compose.dev.yml down --volumes

dev-docker-logs: ## Show development deployment logs
	@echo "📋 Showing development logs..."
	cd deployments && docker compose -f docker-compose.dev.yml logs -f

# Production deployment (includes Ollama in Docker)
deploy: ## Deploy production (Ollama in Docker)
	@echo "� Deploying SmartDoc production..."
	cd deployments && docker compose up --build -d

deploy-logs: ## Show production deployment logs
	@echo "📋 Showing production logs..."
	cd deployments && docker compose logs -f

deploy-down: ## Stop production deployment
	@echo "⏹️ Stopping production deployment..."
	cd deployments && docker compose down

deploy-health: ## Check deployment health
	@echo "🏥 Checking deployment health..."
	cd deployments && make health

# Ollama helpers
ollama-check: ## Check if local Ollama is running
	@echo "🤖 Checking local Ollama..."
	@curl -s http://localhost:11434/api/tags >/dev/null && echo "✅ Ollama is running" || echo "❌ Ollama not running - start with: ollama serve"

ollama-models: ## List available models in local Ollama
	@echo "📋 Available models:"
	@curl -s http://localhost:11434/api/tags | jq -r '.models[].name' 2>/dev/null || echo "❌ Ollama not responding"

ollama-pull: ## Pull the required model
	@echo "� Pulling gemma3:4b-it-q4_K_M model..."
	ollama pull gemma3:4b-it-q4_K_M

format: ## Format and lint code
	@echo "🧹 Formatting code..."
	cd packages/core && poetry run black src/
	cd apps/api && poetry run black src/

lint: ## Run linting only
	@echo "🔍 Linting code..."
	cd packages/core && poetry run ruff check src/
	cd apps/api && poetry run ruff check src/

type-check: ## Run type checking
	@echo "📝 Type checking..."
	cd packages/core && poetry run mypy src/

clean: ## Clean up build artifacts
	@echo "🧽 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true

check: format lint type-check test ## Run all checks (format, lint, type-check, test)

# Database operations
db-rev: ## Generate a new database migration
	cd apps/api && poetry run alembic revision --autogenerate -m "auto"

db-up: ## Apply all pending database migrations
	cd apps/api && poetry run alembic upgrade head

db-down: ## Rollback one database migration
	cd apps/api && poetry run alembic downgrade -1

db-reset: ## Reset database (WARNING: deletes all data)
	cd apps/api && rm -f var/dev.sqlite3 && poetry run alembic upgrade head

db-inspect: ## Inspect the current database schema
	cd apps/api && poetry run python -c "import sqlite3; db=sqlite3.connect('var/dev.sqlite3'); [print(row) for row in db.execute('SELECT name FROM sqlite_master WHERE type=\"table\";')]; db.close()"

db-peek: ## Quick database stats
	cd apps/api && poetry run sqlite3 instance/smartdoc_dev.sqlite3 \
	"SELECT 'conversations',COUNT(*) FROM conversations UNION ALL \
	 SELECT 'messages',COUNT(*) FROM messages UNION ALL \
	 SELECT 'sessions',COUNT(*) FROM simulation_sessions UNION ALL \
	 SELECT 'discoveries',COUNT(*) FROM discovery_events;"

# Legacy aliases
dev: api ## Alias for api
run: api ## Alias for api
