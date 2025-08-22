.PHONY: help setup test api web docker-build docker-up format clean lint type-check install install-poetry

# Default target
help: ## Show this help message
	@echo "SmartDoc Development Commands"
	@echo "=============================="
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

test: ## Run all tests
	@echo "🧪 Running tests..."
	cd packages/core && poetry run pytest
	cd apps/api && poetry run pytest

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

docker-build: ## Build Docker containers
	@echo "🐳 Building Docker containers..."
	cd deployments && docker compose build

docker-up: ## Start Docker containers
	@echo "🐳 Starting Docker containers..."
	cd deployments && docker compose up --build

docker-down: ## Stop Docker containers
	cd deployments && docker compose down

# Production deployment commands
deploy-production: ## Complete automated production deployment
	@echo "🚀 Starting automated production deployment..."
	./scripts/deploy_production.sh

deploy-check: ## Check prerequisites for production deployment
	@echo "🔍 Checking production deployment prerequisites..."
	./scripts/check_prerequisites.sh

deploy: ## Deploy to production with GPU support (multi-container)
	@echo "🚀 Deploying SmartDoc with multi-container architecture..."
	cd deployments && docker compose up --build -d

deploy-single: ## Deploy to production with GPU support (single-container, RECOMMENDED)
	@echo "🚀 Deploying SmartDoc with single-container architecture..."
	cd deployments && docker compose -f compose-single.yaml up --build -d

deploy-test: ## Test both deployment architectures
	@echo "🧪 Testing both deployment architectures..."
	cd deployments && ./test_deployments.sh

deploy-dev: ## Deploy development version with GPU support (for testing)
	@echo "🔧 Deploying SmartDoc in development mode with GPU..."
	cd deployments && docker compose up --build

deploy-status: ## Check deployment status and GPU utilization
	@echo "📊 Checking deployment status..."
	cd deployments && make status

deploy-monitor: ## Launch interactive deployment monitoring
	@echo "📊 Starting deployment monitoring..."
	cd deployments && make monitor

deploy-setup-models: ## Setup Ollama models for GPU deployment
	@echo "🤖 Setting up Ollama models..."
	cd deployments && make setup-models

dev-up: ## Start development environment with Docker (live reload)
	@echo "🚀 Starting development environment..."
	cd deployments && docker compose --profile dev up --build

prod-up: ## Start production environment with Docker
	@echo "🏭 Starting production environment..."
	cd deployments && docker compose --profile prod up --build -d

down: ## Stop all Docker containers
	@echo "⏹️ Stopping containers..."
	cd deployments && docker compose down

logs: ## Show Docker container logs
	@echo "📋 Showing container logs..."
	cd deployments && docker compose logs -f api

logs-web: ## Show web container logs
	cd deployments && docker compose logs -f web

ps: ## Show running containers
	@echo "📊 Container status:"
	cd deployments && docker compose ps

restart: ## Restart containers
	@echo "🔄 Restarting containers..."
	cd deployments && docker compose restart

test-deployment: ## Test deployment health
	@echo "🧪 Testing deployment..."
	cd deployments && python test_deployment.py

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

db-peek:
	cd apps/api && poetry run sqlite3 instance/smartdoc_dev.sqlite3 \
	"SELECT 'conversations',COUNT(*) FROM conversations UNION ALL \
	 SELECT 'messages',COUNT(*) FROM messages UNION ALL \
	 SELECT 'sessions',COUNT(*) FROM simulation_sessions UNION ALL \
	 SELECT 'discoveries',COUNT(*) FROM discovery_events;"

# Legacy aliases
dev: api ## Alias for api
run: api ## Alias for api
