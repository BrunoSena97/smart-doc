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

# Docker deployment commands (requires external Ollama)
deploy: ## Deploy production (requires external Ollama running)
	@echo "🚀 Deploying SmartDoc with external Ollama..."
	@echo "📋 Ensure Ollama is running: ollama serve"
	cd deployments && docker compose up --build -d

deploy-dev: ## Deploy with logs (development mode)
	@echo "🔧 Deploying SmartDoc in development mode..."
	cd deployments && docker compose up --build

deploy-down: ## Stop deployment
	@echo "⏹️ Stopping deployment..."
	cd deployments && docker compose down

deploy-logs: ## Show deployment logs
	@echo "📋 Showing deployment logs..."
	cd deployments && docker compose logs -f

deploy-health: ## Check deployment health
	@echo "🏥 Checking deployment health..."
	@curl -s http://localhost:8000/health | jq '.' || echo "Deployment not responding"

docker-build: ## Build Docker containers
	@echo "🐳 Building Docker containers..."
	cd deployments && docker compose build

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
