# SmartDoc Production Deployment

Production-ready deployment configurations for SmartDoc with local GPU-accelerated LLM support.

## 🚀 Quick Start

### Prerequisites

1. **Docker with GPU Support**

   ```bash
   # Install nvidia-container-toolkit
   curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
   curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
     sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
     sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
   sudo apt-get update
   sudo apt-get install -y nvidia-container-toolkit
   sudo nvidia-ctk runtime configure --runtime=docker
   sudo systemctl restart docker
   ```

2. **Verify GPU Access**
   ```bash
   docker run --rm --gpus all nvidia/cuda:11.8-base-ubuntu22.04 nvidia-smi
   ```

### Production Deployment

```bash
# Configure environment
cp .env.example .env

# Deploy all services
make deploy

# Setup Ollama models (interactive)
./scripts/ollama_model_setup.sh

# Health check
make test-deployment

# Stop everything
make down
```

### Development Testing

```bash
# Deploy in development mode
make deploy-dev

# View logs
docker-compose logs -f
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│                 │    │                  │    │                 │
│   Nginx Web     │────│   Flask API      │────│   SQLite DB     │
│   (Port 8000)   │    │   (Internal)     │    │   (/data vol)   │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │
         │                        │
         ▼                        ▼
┌─────────────────┐    ┌─────────────────────┐
│    Traefik      │    │   Ollama + GPU      │
│ HTTPS → :8000   │    │  (RTX 4070 Ti S)    │
└─────────────────┘    └─────────────────────┘
```

### Production Setup

- **Traefik**: Terminates HTTPS at `https://mestrados.logimade.com`
- **Nginx**: Serves static files + proxies `/api/*` to Flask (port 8000)
- **Flask API**: Internal service, connects to local Ollama
- **Ollama**: GPU-accelerated LLM service with model persistence

## 🎯 RTX 4070 Ti SUPER Optimization

### Recommended Models

| Model                           | VRAM | Performance   | Use Case                   |
| ------------------------------- | ---- | ------------- | -------------------------- |
| `llama3.1:8b-instruct-q4_K_M`   | ~6GB | 15-25 tok/sec | **Default recommendation** |
| `llama3.1:13b-instruct-q4_K_M`  | ~9GB | 10-15 tok/sec | Higher quality             |
| `codellama:13b-instruct-q4_K_M` | ~9GB | 10-15 tok/sec | Code assistance            |
| `meditron:7b-chat-q4_K_M`       | ~5GB | 20-30 tok/sec | Medical domain             |

### GPU Configuration

```yaml
# Ollama service optimized for RTX 4070 Ti SUPER
deploy:
  resources:
    reservations:
      devices:
        - capabilities: [gpu]
environment:
  - OLLAMA_NUM_PARALLEL=2 # Concurrent requests
  - OLLAMA_KEEP_ALIVE=30m # Model retention
  - OLLAMA_GPU=1 # GPU acceleration
```

- **SQLite**: Persistent database volume at `/data/smartdoc.sqlite3`

## Configuration

### Environment Variables

```bash
# LLM Settings
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=gemma3:4b-it-q4_K_M

# Database (SQLite with volume persistence)
SMARTDOC_DB_URL=sqlite:////data/smartdoc.sqlite3
```

### Port Configuration

- **Production**: Only port 8000 exposed (Traefik → Nginx → API)
- **Development**: Same port 8000 for consistency

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│                 │    │                  │    │                 │
│   Nginx Web     │────│   Flask API      │────│   SQLite DB     │
│   (Port 3000)   │    │   (Port 8000)    │    │   (Volume)      │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

- **Nginx**: Serves static frontend + reverse proxies `/api/*` to Flask
- **Flask API**: Production WSGI server (Gunicorn) with health checks
- **SQLite**: Persistent database volume for data storage

## Environment Configuration

Copy and customize the environment file:

```bash
cp .env.example .env
```

Key configurations:

```bash
# Environment
FLASK_ENV=production          # or development
LOG_LEVEL=INFO               # DEBUG, INFO, WARNING, ERROR

# LLM Settings
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=gemma3:4b-it-q4_K_M

# Database
SMARTDOC_DB_PATH=/app/apps/api/instance/smartdoc.sqlite3
```

## Profiles

The deployment uses Docker Compose profiles:

- **`dev`**: Development with live file mounting and direct API access
- **`prod`**: Production with optimized containers and health checks

## API Health Checks

The API container includes health checks:

- `/health` - Detailed health status
- `/healthz` - Simple OK/FAIL check (used by Docker)

## Database Persistence

SQLite database is stored in a Docker volume (`api_data`) that persists across container restarts.

## Frontend Configuration

The frontend automatically detects the environment:

- **Development**: Uses absolute URLs to `http://localhost:8000`
- **Production**: Uses relative URLs (proxied through Nginx)

## Production Considerations

### Security Headers

The Nginx configuration includes basic security headers:

- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`

### Performance

- Gunicorn with 2 workers and thread pool
- Nginx serving static assets efficiently
- SQLite with WAL mode for better concurrency

### Monitoring

- Health checks for container orchestration
- Structured logging with configurable levels
- Container restart policies

## Scaling Considerations

For high-traffic production:

1. **Database**: Switch from SQLite to PostgreSQL
2. **API**: Increase Gunicorn workers
3. **Caching**: Add Redis for session storage
4. **Load Balancing**: Use multiple API containers
5. **TLS**: Add Caddy/Traefik for HTTPS termination

## Troubleshooting

### Container Logs

```bash
# API logs
make logs

# Web logs
make logs-web

# All containers
docker compose logs
```

### Database Issues

```bash
# Access the database volume
docker volume inspect deployments_api_data

# Connect to running API container
docker compose exec api bash
```

### Network Issues

```bash
# Check container networking
docker compose ps
docker network ls
```

### Frontend API Calls

If API calls fail, check:

1. Nginx proxy configuration (`web.nginx.conf`)
2. API container health (`/healthz`)
3. CORS settings in Flask app
4. Frontend config detection (`js/config.js`)
