FROM python:3.13-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1

# System deps (build tools only if needed by deps; remove if not)
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential curl ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m -u 10001 appuser

WORKDIR /app

# Copy pyprojects & locks first for layer caching
# Core package first (path dependency)
COPY packages/core/pyproject.toml packages/core/poetry.lock* /app/packages/core/
# Shared package
COPY packages/shared/pyproject.toml packages/shared/poetry.lock* /app/packages/shared/
# API
COPY apps/api/pyproject.toml apps/api/poetry.lock* /app/apps/api/

# Install Poetry matching your version
RUN pip install --no-cache-dir "poetry==2.1.4"
RUN poetry config virtualenvs.create false

# Install dependencies in order (core -> shared -> api)
RUN cd /app/packages/core && poetry install --only main --no-ansi --no-interaction
RUN cd /app/packages/shared && poetry install --only main --no-ansi --no-interaction
RUN cd /app/apps/api && poetry install --only main --no-ansi --no-interaction

# Install gunicorn for production
RUN pip install --no-cache-dir gunicorn

# Copy sources
COPY packages/core/src /app/packages/core/src
COPY packages/shared/src /app/packages/shared/src
COPY apps/api/src /app/apps/api/src
COPY apps/api/alembic.ini /app/apps/api/alembic.ini
COPY apps/api/migrations /app/apps/api/migrations
COPY configs /app/configs

# Ensure instance dir for SQLite exists & is owned by appuser
# Also create /data for volume mount
RUN mkdir -p /app/apps/api/instance /data && chown -R appuser:appuser /app /data

# Switch to non-root
USER appuser

ENV PYTHONPATH=/app/apps/api/src:/app/packages/core/src:/app/packages/shared/src
ENV PORT=8000

# Healthcheck endpoint expected at /healthz
EXPOSE 8000

# Alembic -> Gunicorn entrypoint
CMD ["python", "-c", "import os, subprocess; subprocess.run(['alembic','-c','/app/apps/api/alembic.ini','upgrade','head'], check=True, cwd='/app/apps/api'); subprocess.run(['gunicorn','-w','2','-k','gthread','-t','60','-b',f'0.0.0.0:{os.environ.get(\"PORT\",\"8000\")}','smartdoc_api.main:app'], cwd='/app/apps/api')"]
