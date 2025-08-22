#!/bin/bash
# Ollama Model S# Recommended models for RTX 4070 Ti SUPER (in order of preference)
echo "🎯 Installing recommended models for your hardware..."

# 1. Gemma 3 4B - Default SmartDoc model (small and efficient)
pull_model "gemma3:4b-it-q4_K_M"

# 2. Llama 3.1 8B - Enhanced capability option
echo "🔧 Would you like to install Llama 3.1 8B for enhanced capability? (y/N)"
read -r install_llama8b
if [[ "$install_llama8b" =~ ^[Yy]$ ]]; then
    pull_model "llama3.1:8b-instruct-q4_K_M"
fi

# 3. Llama 3.1 13B - Highest capability, more VRAM
echo "🔧 Would you like to install Llama 3.1 13B (higher capability, more VRAM)? (y/N)"
read -r install_13b
if [[ "$install_13b" =~ ^[Yy]$ ]]; then
    pull_model "llama3.1:13b-instruct-q4_K_M"
fi 4070 Ti SUPER (16GB VRAM)
# Optimized model selection for high performance local inference

set -e

# Configuration
COMPOSE_FILE="compose.yaml"
COMPOSE_DIR="$(dirname "$0")/.."

echo "🚀 Setting up Ollama models for RTX 4070 Ti SUPER..."

# Start Ollama service first if not running
echo "📦 Starting Ollama service..."
cd "$COMPOSE_DIR"
docker-compose up -d ollama

# Wait for Ollama to be ready
echo "⏳ Waiting for Ollama to be ready..."
sleep 10

# Function to pull model
pull_model() {
    local model_name="$1"
    echo "📥 Pulling model: $model_name"
    docker-compose exec ollama ollama pull "$model_name"
}

# Recommended models for 16GB VRAM (in order of preference)
echo "🎯 Installing recommended models for your hardware..."

# 1. Llama 3.1 8B - Excellent balance of performance and capability
pull_model "llama3.1:8b-instruct-q4_K_M"

# 2. Llama 3.1 13B - Higher capability, still fits comfortably
echo "🔧 Would you like to install Llama 3.1 13B (higher capability)? (y/N)"
read -r install_13b
if [[ "$install_13b" =~ ^[Yy]$ ]]; then
    pull_model "llama3.1:13b-instruct-q4_K_M"
fi

# 3. Code-specific model
echo "💻 Would you like to install CodeLlama for code assistance? (y/N)"
read -r install_code
if [[ "$install_code" =~ ^[Yy]$ ]]; then
    pull_model "codellama:13b-instruct-q4_K_M"
fi

# 4. Medical/Clinical model option
echo "🏥 Would you like to install a medical-specialized model? (y/N)"
read -r install_medical
if [[ "$install_medical" =~ ^[Yy]$ ]]; then
    pull_model "meditron:7b-chat-q4_K_M"
fi

# Show available models
echo "✅ Installation complete! Available models:"
docker-compose exec ollama ollama list

# Model performance recommendations
cat << EOF

🎯 Model Recommendations for RTX 4070 Ti SUPER:

📊 Performance Tiers:
- llama3.1:8b-instruct-q4_K_M   → ~6GB VRAM, 15-25 tokens/sec (RECOMMENDED)
- llama3.1:13b-instruct-q4_K_M  → ~9GB VRAM, 10-15 tokens/sec (High Quality)
- codellama:13b-instruct-q4_K_M → ~9GB VRAM, specialized for code
- meditron:7b-chat-q4_K_M       → ~5GB VRAM, medical domain

🔧 Performance Tuning:
- Current config: OLLAMA_NUM_PARALLEL=2 (good for concurrent requests)
- Monitor GPU utilization: nvidia-smi
- Adjust num_parallel based on usage patterns

🚀 Usage:
- Default model: llama3.1:8b-instruct-q4_K_M
- Change model via OLLAMA_MODEL environment variable
- API endpoint: http://localhost:8000/api/v1/chat

EOF

echo "🎉 Ollama setup complete! Your SmartDoc deployment now has local GPU-accelerated LLM capabilities."
