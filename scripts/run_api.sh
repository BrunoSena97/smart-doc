#!/bin/bash
# Run the SmartDoc API server

set -e

echo "🚀 Starting SmartDoc API..."
export PYTHONPATH="${PYTHONPATH}:./packages/core/src:./packages/shared/src:./apps/api/src"
export SMARTDOC_CONFIG="${SMARTDOC_CONFIG:-configs/dev.yaml}"

cd apps/api
python -m smartdoc_api.main
