# 4.2.5 Deployment Configuration and Scalability

A critical requirement for SmartDoc is reliable deployment in both research and educational settings. The deployment architecture was designed with three guiding principles:

1. **Reproducibility** — ensuring that the same configuration can be reproduced across different sites and machines
2. **Scalability** — enabling the platform to support cohorts of learners by scaling model inference capacity when needed
3. **Accessibility** — minimizing technical barriers for institutions, favoring lightweight setups that do not require specialized infrastructure

## Containerization and Reproducibility

To guarantee consistent behavior across environments, the system is distributed as containerized services using Docker. This encapsulation ensures that all dependencies are versioned and portable, allowing educational institutions or research collaborators to reproduce experiments without lengthy installation procedures.

**Table 4.6: Docker Container Components**

| Component       | Technology       | Role                                      | Configuration                                |
| --------------- | ---------------- | ----------------------------------------- | -------------------------------------------- |
| Web Application | Flask + Gunicorn | HTTP server for API and static files      | 4 worker processes, port 8000                |
| LLM Inference   | Ollama           | Local model hosting with GPU acceleration | Gemma 3:4b-it-q4_K_M loaded in memory        |
| Database        | SQLite           | Persistent storage with ACID guarantees   | Single-file, ~50MB typical size              |
| CORS Middleware | Flask-CORS       | Cross-origin request support              | Development frontend access enabled          |
| Logging System  | Python logging   | Structured audit trail                    | JSON format, daily rotation, 7-day retention |

### Container Definition

The primary application container is built on `python:3.13-slim` base image and includes:

```dockerfile
FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Install Python dependencies via Poetry
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-root --no-dev

# Copy application code
COPY apps/api /app/api
COPY packages/ /app/packages

# Expose ports
EXPOSE 8000

# Startup script
CMD ["./start.sh"]
```

### Startup Sequence

The container initialization follows a deterministic sequence to ensure all components are operational before accepting requests:

```bash
#!/bin/bash
# start.sh

# 1. Start Ollama service in background
ollama serve &

# 2. Wait for Ollama to be ready
sleep 5

# 3. Load LLM models into memory
ollama pull gemma3:4b-it-q4_K_M

# 4. Initialize database (run migrations)
cd /app/api
poetry run alembic upgrade head

# 5. Start Flask application via Gunicorn
poetry run gunicorn \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 120 \
    --access-logfile /app/logs/access.log \
    --error-logfile /app/logs/error.log \
    smartdoc_api:app
```

This sequence ensures that LLM models are pre-loaded (avoiding cold-start latency during first student query) and the database schema is current.

## Model Hosting and Flexibility

SmartDoc supports two deployment modes to accommodate different institutional contexts:

### Local Hosting (Research/Privacy-Focused)

**Configuration:**

- Ollama running within the application container
- Gemma 3:4b quantized model (~3GB memory)
- GPU acceleration via NVIDIA Container Toolkit (optional but recommended)
- No internet connectivity required after initial model download

**Advantages:**

- Complete data privacy (no external API calls)
- Reproducible model behavior (fixed version)
- No API costs
- Suitable for research studies requiring exact replication

**Limitations:**

- Requires capable hardware (8GB+ RAM, GPU recommended)
- Lower accuracy than state-of-the-art commercial models
- Self-managed updates and maintenance

### Cloud Hosting (Production-Scale)

**Configuration:**

- Provider abstraction switched to OpenAI or Anthropic
- API keys managed via environment variables
- Model selection: GPT-4o-mini or Claude 3.5 Sonnet
- Rate limiting and cost controls enabled

**Advantages:**

- State-of-the-art model performance
- No local hardware requirements
- Automatic scaling
- Professional reliability and uptime

**Limitations:**

- API costs per inference
- Data transmitted to external services
- Potential latency from network round-trips
- Model updates may change behavior

The dual-mode design reflects a balance between cost, accuracy, and data governance, allowing institutions to select the configuration best suited to their pedagogical and ethical context.

## Scalability Considerations

Although individual learners typically interact with SmartDoc in isolation, classroom or cohort settings require concurrent session support. The architecture supports horizontal scaling through several mechanisms:

### Application Scaling

Gunicorn worker processes enable concurrent request handling:

```yaml
# docker-compose.yml
services:
  smartdoc-api:
    build: .
    environment:
      GUNICORN_WORKERS: 4 # Adjust based on CPU cores
      GUNICORN_TIMEOUT: 120
    deploy:
      replicas: 2 # Multiple container instances
```

### LLM Inference Scaling

For local deployment, multiple Ollama instances can be launched in parallel:

```yaml
services:
  ollama-1:
    image: ollama/ollama
    ports: ["11434:11434"]

  ollama-2:
    image: ollama/ollama
    ports: ["11435:11434"]

  smartdoc-api:
    environment:
      OLLAMA_HOSTS: "http://ollama-1:11434,http://ollama-2:11434"
```

Load balancing distributes inference requests across instances, reducing wait times.

### Database Considerations

SQLite is sufficient for cohorts up to ~50 concurrent users. For larger deployments, migration to PostgreSQL is straightforward via SQLAlchemy:

```python
# Minimal configuration change
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///smartdoc.db")
engine = create_engine(DATABASE_URL)
```

PostgreSQL supports thousands of concurrent connections and enables distributed deployments across multiple servers.

## Persistent Storage and Operational Logging

Two Docker volumes ensure data persistence across container restarts:

```yaml
volumes:
  smartdoc-data:
    # Database files, session state
    driver: local

  smartdoc-logs:
    # Application logs, audit trails
    driver: local
```

### Database Volume

Stores the complete SQLite database file. Backed up automatically via cron job every 24 hours:

```bash
# Backup script
#!/bin/bash
timestamp=$(date +%Y%m%d_%H%M%S)
cp /app/data/smartdoc.db /app/backups/smartdoc_$timestamp.db
# Retain last 7 backups
ls -t /app/backups/smartdoc_*.db | tail -n +8 | xargs rm -f
```

### Logs Volume

Gathers comprehensive operational logs:

- **Application logs** — Flask route handling, request/response cycles
- **LLM inference logs** — prompt/completion pairs, inference times, token counts
- **Error traces** — stack traces, exception contexts, recovery actions
- **Audit logs** — user authentication, data access, administrative actions

Log files are structured JSON for machine parsing:

```json
{
  "timestamp": "2025-10-13T22:47:52.289182Z",
  "level": "INFO",
  "module": "intent_classifier",
  "event": "classification_success",
  "data": {
    "query": "What is her past medical history?",
    "intent": "pmh_general",
    "confidence": 0.95,
    "inference_time_ms": 234
  }
}
```

This enables programmatic analysis of system behavior and identification of performance bottlenecks.

## Educational Impact of Deployment Design

By prioritizing reproducibility and portability, SmartDoc enables institutions to adopt the platform with minimal setup, making bias-aware clinical simulation accessible beyond well-resourced centers. The containerization approach means that:

- **Technical staff** can deploy SmartDoc with a single `docker-compose up` command
- **Researchers** can replicate study environments exactly across multiple sites
- **Educators** can run the system on laptops for small workshops or on servers for entire courses

The scalability features ensure that response times remain low (<2 seconds per interaction), preserving immersion and educational value even with larger groups. The emphasis on local deployment and data privacy reinforces trust in the system for formal training contexts.

Together, these deployment choices demonstrate that architectural decisions are not merely technical concerns but **educational enablers**, supporting widespread adoption and rigorous empirical evaluation of diagnostic reasoning pedagogy.
