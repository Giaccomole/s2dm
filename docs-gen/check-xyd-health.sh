#!/bin/bash

# XYD Servers Health Check Script
# Checks if all XYD documentation servers are running and accessible

echo "🩺 S2DM XYD Servers Health Check"
echo "================================="
echo

# Server configuration: name, port, endpoint
servers=(
    "Seat Capabilities|5176|seat-capabilities"
    "Trailer Domain Model|5177|trailer-domain-model"
    "Seat Domain Model|5178|seat-domain-model"
    "Multiple Domains|5179|multiple-domains"
    "Classification Schemes|5180|multiple-classification-schemes"
    "Specification History|5181|specification-history-registry"
)

all_healthy=true

for server in "${servers[@]}"; do
    IFS='|' read -r name port endpoint <<< "$server"
    
    echo -n "Checking $name (port $port)... "
    
    # Check if port is listening
    if ! lsof -i :$port > /dev/null 2>&1; then
        echo "❌ Not running (port $port not listening)"
        all_healthy=false
        continue
    fi
    
    # Check if endpoint responds
    response=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:$port/api/$endpoint" 2>/dev/null)
    
    if [ "$response" = "200" ]; then
        echo "✅ Healthy (HTTP $response)"
    else
        echo "⚠️  Port listening but endpoint not responding (HTTP $response)"
        all_healthy=false
    fi
done

echo
if [ "$all_healthy" = true ]; then
    echo "🎉 All XYD servers are healthy!"
    echo
    echo "🌐 Access your documentation:"
    echo "   Hugo site: http://localhost:61623/examples/"
    echo "   Direct XYD: http://localhost:5176-5181/api/{endpoint}"
else
    echo "⚠️  Some servers need attention. Run './start-xyd-servers.sh' to restart all."
fi

echo
echo "💡 Tip: Use './stop-xyd-servers.sh' to stop all servers"
echo "📖 See XYD_EXAMPLES_README.md for detailed documentation"
