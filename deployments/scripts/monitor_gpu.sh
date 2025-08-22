#!/bin/bash
# GPU and Ollama Monitoring Script for SmartDoc
# Monitor GPU usage, model performance, and system resources

set -e

COMPOSE_DIR="$(dirname "$0")/.."
cd "$COMPOSE_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

show_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE} SmartDoc GPU Monitoring Status${NC}"
    echo -e "${BLUE}================================${NC}"
    echo
}

show_gpu_status() {
    echo -e "${GREEN}🎯 GPU Status (RTX 4070 Ti SUPER)${NC}"
    echo "-----------------------------------"

    if command -v nvidia-smi &> /dev/null; then
        nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu,temperature.gpu --format=csv,noheader,nounits | while IFS=, read -r name mem_used mem_total gpu_util temp; do
            mem_used=$(echo $mem_used | xargs)
            mem_total=$(echo $mem_total | xargs)
            gpu_util=$(echo $gpu_util | xargs)
            temp=$(echo $temp | xargs)

            mem_percent=$(( mem_used * 100 / mem_total ))

            echo "GPU: $name"
            echo "Memory: ${mem_used}MB / ${mem_total}MB (${mem_percent}%)"
            echo "Utilization: ${gpu_util}%"
            echo "Temperature: ${temp}°C"
        done
    else
        echo -e "${RED}nvidia-smi not found${NC}"
    fi
    echo
}

show_ollama_status() {
    echo -e "${GREEN}🤖 Ollama Service Status${NC}"
    echo "------------------------"

    if docker-compose ps ollama | grep -q "running"; then
        echo -e "${GREEN}✓ Ollama service is running${NC}"

        # Show running models
        echo
        echo "Running models:"
        docker-compose exec -T ollama ollama ps 2>/dev/null || echo "No models currently running"

        # Show available models
        echo
        echo "Available models:"
        docker-compose exec -T ollama ollama list 2>/dev/null || echo "No models installed"

    else
        echo -e "${RED}✗ Ollama service is not running${NC}"
    fi
    echo
}

show_api_status() {
    echo -e "${GREEN}🌐 API Service Status${NC}"
    echo "---------------------"

    if docker-compose ps api | grep -q "running"; then
        echo -e "${GREEN}✓ API service is running${NC}"

        # Test health endpoint
        if curl -s http://localhost:8000/healthz > /dev/null; then
            echo -e "${GREEN}✓ Health endpoint responding${NC}"
        else
            echo -e "${YELLOW}⚠ Health endpoint not responding${NC}"
        fi
    else
        echo -e "${RED}✗ API service is not running${NC}"
    fi
    echo
}

show_web_status() {
    echo -e "${GREEN}🌍 Web Service Status${NC}"
    echo "---------------------"

    if docker-compose ps web | grep -q "running"; then
        echo -e "${GREEN}✓ Web service is running${NC}"

        # Test web endpoint
        if curl -s http://localhost:8000 > /dev/null; then
            echo -e "${GREEN}✓ Web interface accessible${NC}"
        else
            echo -e "${YELLOW}⚠ Web interface not responding${NC}"
        fi
    else
        echo -e "${RED}✗ Web service is not running${NC}"
    fi
    echo
}

show_performance_metrics() {
    echo -e "${GREEN}⚡ Performance Metrics${NC}"
    echo "----------------------"

    # Test Ollama response time
    if docker-compose ps ollama | grep -q "running"; then
        echo "Testing model response time..."
        start_time=$(date +%s.%N)
        response=$(docker-compose exec -T ollama ollama run llama3.1:8b-instruct-q4_K_M "Hello" 2>/dev/null || echo "Model test failed")
        end_time=$(date +%s.%N)
        duration=$(echo "$end_time - $start_time" | bc)

        if [[ "$response" != "Model test failed" ]]; then
            echo "Model response time: ${duration}s"
            token_count=$(echo "$response" | wc -w)
            if (( $(echo "$duration > 0" | bc -l) )); then
                tokens_per_sec=$(echo "scale=2; $token_count / $duration" | bc)
                echo "Estimated tokens/sec: $tokens_per_sec"
            fi
        else
            echo -e "${YELLOW}⚠ Model performance test failed${NC}"
        fi
    fi
    echo
}

show_resource_usage() {
    echo -e "${GREEN}💾 System Resources${NC}"
    echo "-------------------"

    # Docker stats
    echo "Container resource usage:"
    docker-compose exec -T api sh -c 'ps aux | head -1; ps aux | grep -v grep | grep python' 2>/dev/null || echo "Could not get process stats"

    # Disk usage for volumes
    echo
    echo "Volume usage:"
    docker system df --format "table {{.Type}}\t{{.TotalCount}}\t{{.Size}}\t{{.Reclaimable}}"
    echo
}

show_logs() {
    local service=${1:-""}
    local lines=${2:-20}

    echo -e "${GREEN}📋 Recent Logs${NC}"
    echo "---------------"

    if [[ -n "$service" ]]; then
        echo "Last $lines lines from $service:"
        docker-compose logs --tail="$lines" "$service"
    else
        echo "Last $lines lines from all services:"
        docker-compose logs --tail="$lines"
    fi
}

interactive_mode() {
    while true; do
        clear
        show_header
        show_gpu_status
        show_ollama_status
        show_api_status
        show_web_status

        echo -e "${YELLOW}Options:${NC}"
        echo "1) Show performance metrics"
        echo "2) Show resource usage"
        echo "3) Show logs (all)"
        echo "4) Show logs (ollama)"
        echo "5) Show logs (api)"
        echo "6) Pull new model"
        echo "7) Switch model"
        echo "r) Refresh"
        echo "q) Quit"
        echo

        read -p "Choose option: " choice

        case $choice in
            1) show_performance_metrics; read -p "Press Enter to continue..." ;;
            2) show_resource_usage; read -p "Press Enter to continue..." ;;
            3) show_logs "" 50; read -p "Press Enter to continue..." ;;
            4) show_logs "ollama" 50; read -p "Press Enter to continue..." ;;
            5) show_logs "api" 50; read -p "Press Enter to continue..." ;;
            6)
                echo "Available models for RTX 4070 Ti SUPER:"
                echo "1) llama3.1:8b-instruct-q4_K_M (6GB VRAM)"
                echo "2) llama3.1:13b-instruct-q4_K_M (9GB VRAM)"
                echo "3) codellama:13b-instruct-q4_K_M (9GB VRAM)"
                echo "4) meditron:7b-chat-q4_K_M (5GB VRAM)"
                read -p "Model name: " model_name
                if [[ -n "$model_name" ]]; then
                    docker-compose exec ollama ollama pull "$model_name"
                fi
                read -p "Press Enter to continue..."
                ;;
            7)
                echo "Current models:"
                docker-compose exec -T ollama ollama list
                echo
                read -p "Enter model name to run: " model_name
                if [[ -n "$model_name" ]]; then
                    echo "Testing model..."
                    docker-compose exec ollama ollama run "$model_name" "Hello, test message"
                fi
                read -p "Press Enter to continue..."
                ;;
            r) continue ;;
            q) break ;;
        esac
    done
}

# Main execution
case "${1:-status}" in
    "status")
        show_header
        show_gpu_status
        show_ollama_status
        show_api_status
        show_web_status
        ;;
    "performance")
        show_performance_metrics
        ;;
    "resources")
        show_resource_usage
        ;;
    "logs")
        show_logs "${2:-}" "${3:-20}"
        ;;
    "interactive"|"monitor")
        interactive_mode
        ;;
    *)
        echo "Usage: $0 {status|performance|resources|logs [service] [lines]|interactive}"
        echo
        echo "Examples:"
        echo "  $0                          # Show status overview"
        echo "  $0 performance              # Show performance metrics"
        echo "  $0 logs ollama 50           # Show last 50 ollama logs"
        echo "  $0 interactive              # Interactive monitoring mode"
        exit 1
        ;;
esac
