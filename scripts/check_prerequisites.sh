#!/bin/bash
# Production Deployment Prerequisites Check
# Run this script to verify your machine is ready for SmartDoc deployment

set -e

echo "🔍 SmartDoc Production Deployment Prerequisites Check"
echo "===================================================="

# Check Docker
echo "1. Checking Docker installation..."
if command -v docker &> /dev/null; then
    echo "✅ Docker found: $(docker --version)"
else
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi

# Check Docker Compose
echo "2. Checking Docker Compose..."
if docker compose version &> /dev/null; then
    echo "✅ Docker Compose found: $(docker compose version)"
else
    echo "❌ Docker Compose not found. Please install Docker Compose."
    exit 1
fi

# Check NVIDIA drivers
echo "3. Checking NVIDIA drivers..."
if command -v nvidia-smi &> /dev/null; then
    echo "✅ NVIDIA drivers found:"
    nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
else
    echo "❌ NVIDIA drivers not found. Please install NVIDIA drivers."
    exit 1
fi

# Check nvidia-container-toolkit
echo "4. Checking nvidia-container-toolkit..."
if docker run --rm --gpus all nvidia/cuda:11.8-base-ubuntu22.04 nvidia-smi &> /dev/null; then
    echo "✅ nvidia-container-toolkit working correctly"
else
    echo "❌ nvidia-container-toolkit not working. Installation needed."
    echo "Run the following commands:"
    echo ""
    echo "curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg"
    echo "curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list"
    echo "sudo apt-get update"
    echo "sudo apt-get install -y nvidia-container-toolkit"
    echo "sudo nvidia-ctk runtime configure --runtime=docker"
    echo "sudo systemctl restart docker"
    exit 1
fi

# Check system resources
echo "5. Checking system resources..."
echo "CPU cores: $(nproc)"
echo "RAM: $(free -h | awk '/^Mem:/ {print $2}')"
echo "Available disk space: $(df -h . | awk 'NR==2 {print $4}')"

# Check ports
echo "6. Checking port availability..."
if ss -tuln | grep -q ":8000 "; then
    echo "⚠️  Port 8000 is in use. You may need to stop existing services."
else
    echo "✅ Port 8000 is available"
fi

echo ""
echo "🎉 Prerequisites check complete!"
echo "If all checks passed, you're ready for production deployment."
