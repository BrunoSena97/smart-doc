#!/usr/bin/env bash
set -euo pipefail

echo "Starting SmartDoc container..."

# Ensure DB path from env or default
: "${SMARTDOC_DB_PATH:=/data/smartdoc.sqlite3}"
export SMARTDOC_DB_PATH

# Ensure the data directory exists
mkdir -p "$(dirname "$SMARTDOC_DB_PATH")"

# Set permissions for log directory
chown -R root:root /var/log/smartdoc
chmod -R 755 /var/log/smartdoc

# Initialize database if it doesn't exist
if [[ ! -f "$SMARTDOC_DB_PATH" ]]; then
  echo "Initializing database at $SMARTDOC_DB_PATH"
  cd /app/apps/api
  # Run any database initialization if needed
  # poetry run python -c "from smartdoc_api.database import init_db; init_db()" || true
fi

echo "Starting supervisor with all services..."
echo "Services will start in order: Ollama -> Warmup -> Gunicorn -> Cron"

# Start supervisor (which starts: ollama, warmup, gunicorn, cron)
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
