FROM python:3.12-slim
ENV POETRY_VERSION=1.8.3
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

# Copy and install core first (layer caching)
COPY packages/core/pyproject.toml /app/packages/core/pyproject.toml
RUN cd /app/packages/core && poetry install --no-interaction --no-ansi

# Copy API pyproject and install (includes path dep to core)
COPY apps/api/pyproject.toml /app/apps/api/pyproject.toml
RUN cd /app/apps/api && poetry install --no-interaction --no-ansi

# Copy sources
COPY packages/core/src /app/packages/core/src
COPY apps/api/src /app/apps/api/src
ENV PYTHONPATH=/app/apps/api/src

EXPOSE 8000
CMD ["poetry", "run", "flask", "--app", "smartdoc_api.main_simple", "run", "--host", "0.0.0.0", "--port", "8000"]
