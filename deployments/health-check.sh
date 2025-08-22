#!/bin/bash
# Quick health check for SmartDoc deployment

echo "🏥 SmartDoc Health Check"
echo "======================="

# Check if containers are running
echo "📊 Container Status:"
cd deployments && docker compose ps

echo ""
echo "🌐 Service Health:"

# Test frontend (now on port 8000)
if curl -s http://localhost:8000 >/dev/null 2>&1; then
    echo "✅ Frontend is accessible"
else
    echo "❌ Frontend is not responding"
fi

# Test API proxy (through nginx on port 8000)
if curl -s http://localhost:8000/api/v1/health >/dev/null 2>&1; then
    echo "✅ API proxy is working"
else
    echo "❌ API proxy is not working"
fi

echo ""
echo "📋 Recent logs (last 10 lines):"
cd deployments && docker compose logs --tail=10 api
