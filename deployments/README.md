# SmartDoc Production Deployment

## Overview

Professional deployment setup for SmartDoc with external GPU-accelerated Ollama.

## Architecture

- **External Ollama**: GPU-accelerated LLM service on host machine
- **SmartDoc Container**: Single production container (Flask API + static web)
- **Database**: SQLite with persistent Docker volume
- **Communication**: Container → Host Ollama via `host.docker.internal:11434`

## Quick Start

### Prerequisites

1. **Install Ollama on host machine:**
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```

2. **Start Ollama service:**
   ```bash
   ollama serve
   ```

3. **Pull required model:**
   ```bash
   ollama pull gemma2:9b-instruct-q4_K_M
   ```

### Deployment

```bash
# Production deployment (detached)
make deploy

# Development deployment (with logs)
make dev

# Check health
make health

# Stop deployment
make down
```

## Management Commands

| Command | Description |
|---------|-------------|
| `make deploy` | Deploy production (background) |
| `make dev` | Deploy with logs (foreground) |
| `make down` | Stop and remove containers |
| `make logs` | Show container logs |
| `make health` | Check deployment health |
| `make clean` | Clean up Docker resources |
| `make build` | Rebuild container |
| `make shell` | Open shell in container |

## Database Management

The container automatically:
1. ✅ **Runs migrations** (`alembic upgrade head`)
2. ✅ **Seeds admin data** (admin user + default LLM profiles)
3. ✅ **Starts application** (Gunicorn server)

### Default Admin Access
- **Username**: `admin`
- **Access Code**: `#Admin13`
- **Role**: `admin`

### Query Database
```bash
# List all users
docker compose exec smartdoc poetry run python query_users.py

# Create test user
docker compose exec smartdoc poetry run python query_users.py create "Student Name" "email@example.com"
```

## Endpoints

- **Web Interface**: http://localhost:8000
- **API Health**: http://localhost:8000/health
- **Chat API**: http://localhost:8000/api/v1/chat
- **Admin Panel**: http://localhost:8000/admin (after login)

## Files

```
deployments/
├── docker-compose.yml    # Main deployment configuration
├── Dockerfile           # Production container build
├── Makefile            # Deployment commands
├── README.md           # This documentation
├── .env.example        # Environment template
└── .gitignore          # Git ignore rules
```

## Environment Variables

See `.env.example` for configuration options. Key variables:

- `OLLAMA_BASE_URL`: External Ollama endpoint
- `OLLAMA_MODEL`: LLM model to use
- `SMARTDOC_DB_URL`: Database connection string
- `FLASK_ENV`: Application environment

## Troubleshooting

### Ollama Not Reachable
```bash
# Check Ollama status
curl http://localhost:11434/api/tags

# Start if not running
ollama serve
```

### Database Issues
```bash
# Reset database (WARNING: deletes all data)
make clean
make deploy
```

### Container Issues
```bash
# Rebuild from scratch
make build
make deploy
```

## Production Notes

- ✅ **Secure**: No GPU container complexity
- ✅ **Scalable**: External Ollama can serve multiple instances
- ✅ **Maintainable**: Standard Docker Compose deployment
- ✅ **Reliable**: Health checks and automatic restarts
