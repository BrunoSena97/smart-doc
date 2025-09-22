# SmartDoc Development Guide

## Quick Start

1. **Set up the environment:**

   ```bash
   make setup
   ```

2. **Choose your development approach:**

   **Option A: Local Development (Recommended for development)**

   ```bash
   # Terminal 1: Start local Ollama
   ollama serve

   # Terminal 2: Run API locally
   make api

   # Terminal 3: Serve frontend
   make web
   ```

   **Option B: Docker Development (Uses local Ollama)**

   ```bash
   # Start local Ollama
   ollama serve

   # Run SmartDoc in Docker
   make dev-docker
   ```

   **Option C: Full Production Deployment**

   ```bash
   # Everything in Docker including Ollama
   make deploy
   ```

## Development Workflows

### Local Development (Fastest iteration)

- API runs locally with hot reload
- Frontend served statically
- Uses local Ollama for LLM calls
- Best for rapid development and debugging

**Endpoints:**

- API: http://localhost:8000
- Frontend: http://localhost:3000
- Ollama: http://localhost:11434

### Docker Development

- SmartDoc runs in Docker
- Uses local Ollama via host networking
- Good for testing Docker environment without full deployment

**Endpoints:**

- API: http://localhost:8000
- Ollama: http://localhost:11434 (local)

### Production Deployment

- Everything runs in Docker
- Ollama runs in container with model persistence
- Optimized for production with eternal model memory

**Endpoints:**

- API: http://localhost:8000
- Ollama: http://localhost:11434 (containerized)

## Ollama Setup

### Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Pull the required model

```bash
make ollama-pull
# or manually:
ollama pull gemma3:4b-it-q4_K_M
```

### Check Ollama status

```bash
make ollama-check
make ollama-models
```

## Common Commands

### Development

```bash
make setup          # Initial setup
make api            # Run API locally
make web            # Run frontend
make test           # Run all tests
make check          # Run format, lint, type-check, test
```

### Docker Operations

```bash
make dev-docker     # Development with local Ollama
make deploy         # Production deployment
make deploy-logs    # Show logs
make deploy-down    # Stop deployment
```

### Database Operations

```bash
make db-up          # Apply migrations
make db-rev         # Create new migration
make db-reset       # Reset database (⚠️ destructive)
make db-peek        # Quick stats
```

### Troubleshooting

```bash
make health-check   # Check API health
make ollama-check   # Check Ollama status
make deploy-health  # Check deployment health
```

## Memory Requirements

- **Development**: 2GB+ (local Ollama)
- **Docker Development**: 6GB+ (Docker + local Ollama)
- **Production**: 8GB+ (Docker + containerized Ollama)

For Docker environments, ensure your Docker runtime has sufficient memory:

```bash
# For Colima users
colima start --memory 8
```

## Architecture

- **Flask API** (`apps/api`): REST endpoints with blueprint structure
- **Static Frontend** (`apps/web/public`): Vanilla JS, ES modules
- **Core Logic** (`packages/core`): Domain logic and LLM integration
- **Shared** (`packages/shared`): Common schemas and clients

## Configuration

Configuration files in `configs/`:

- `dev.yaml`: Development settings
- `prod.yaml`: Production settings
- `default.yaml`: Base configuration

Environment-specific settings override defaults.
