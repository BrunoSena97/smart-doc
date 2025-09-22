# SmartDoc Production Dockerfile
# Clean single-container deployment with external Ollama
FROM python:3.12-slim

ENV POETRY_VERSION=1.8.3 \
  PIP_NO_CACHE_DIR=1 \
  PYTHONUNBUFFERED=1 \
  PATH="/root/.local/bin:${PATH}"

WORKDIR /app

# System dependencies - minimal for production
RUN apt-get update && apt-get install -y --no-install-recommends \
  curl ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install "poetry==${POETRY_VERSION}"

# Copy dependency files
COPY packages/core/pyproject.toml packages/core/poetry.lock* packages/core/README.md /app/packages/core/
COPY apps/api/pyproject.toml apps/api/poetry.lock* apps/api/README.md apps/api/alembic.ini /app/apps/api/

# Copy source code
COPY packages/core/src /app/packages/core/src
COPY apps/api/src      /app/apps/api/src
COPY apps/web/public   /app/web
COPY configs           /app/configs
COPY data              /app/data

# Copy initialization scripts
COPY apps/api/utils/seed_admin_data.py apps/api/utils/query_users.py /app/apps/api/

# Install packages
WORKDIR /app/packages/core
RUN poetry config virtualenvs.create false && \
  poetry install --no-interaction --no-ansi --only=main

WORKDIR /app/apps/api
RUN poetry config virtualenvs.create false && \
  poetry lock --no-update && \
  poetry install --no-interaction --no-ansi --only=main

# Create data directory
RUN mkdir -p /data

# Create startup script
RUN echo '#!/bin/bash\n\
  set -e\n\
  echo "🔄 Running database migrations..."\n\
  cd /app/apps/api\n\
  poetry run alembic upgrade head\n\
  echo "🌱 Seeding admin data..."\n\
  poetry run python seed_admin_data.py\n\
  echo "🚀 Starting Gunicorn..."\n\
  exec poetry run gunicorn -w 1 -k gthread -b 0.0.0.0:8000 "smartdoc_api:create_app()" --access-logfile - --error-logfile -' > /start.sh && chmod +x /start.sh

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD curl -f http://127.0.0.1:8000/healthz || exit 1

CMD ["/start.sh"]
