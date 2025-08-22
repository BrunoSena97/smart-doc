#!/usr/bin/env bash
set -euo pipefail

echo "Starting Ollama warmup process..."

# Wait for Ollama API
echo "Waiting for Ollama to be ready..."
for i in {1..60}; do
  if curl -sf http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
    echo "Ollama is ready!"
    break
  fi
  echo "Attempt $i/60 - Ollama not ready yet, waiting..."
  sleep 2
done

# Check if we successfully connected
if ! curl -sf http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
  echo "ERROR: Ollama failed to start within timeout"
  exit 1
fi

echo "Pulling default model: ${OLLAMA_MODEL:-gemma3:4b-it-q4_K_M}"
# Pull the configured model
ollama pull "${OLLAMA_MODEL:-gemma3:4b-it-q4_K_M}" || {
  echo "WARNING: Failed to pull default model, trying fallback..."
  ollama pull "gemma3:4b-it-q4_K_M" || true
}

# Pull embedding model if needed
echo "Pulling embedding model..."
ollama pull nomic-embed-text || true

# Optional quick generate to warm GPU memory
echo "Warming up GPU with test generation..."
curl -s http://127.0.0.1:11434/api/generate \
  -d "{\"model\":\"${OLLAMA_MODEL:-gemma3:4b-it-q4_K_M}\",\"prompt\":\"Hello\",\"options\":{\"num_predict\":5}}" >/dev/null 2>&1 || {
  echo "WARNING: Failed to warm up model, but continuing..."
}

echo "Ollama warmup completed successfully!"

# List available models
echo "Available models:"
ollama list || true
