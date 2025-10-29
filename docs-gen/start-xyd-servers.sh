#!/bin/bash

# XYD Examples Startup Script
# This script starts all XYD documentation servers for S2DM examples

echo "🚀 Starting XYD Documentation Servers for S2DM Examples..."

BASE_DIR="/Users/q674786/s2dm/docs-gen/xyd-examples"

# Function to start XYD server in background
start_xyd_server() {
    local example_name=$1
    local port=$2
    local dir="$BASE_DIR/$example_name"
    
    if [ -d "$dir" ]; then
        echo "Starting $example_name on port $port..."
        cd "$dir"
        xyd dev --port $port > "/tmp/xyd-$example_name.log" 2>&1 &
        echo $! > "/tmp/xyd-$example_name.pid"
        echo "✅ $example_name started (PID: $(cat /tmp/xyd-$example_name.pid))"
    else
        echo "❌ Directory $dir not found"
    fi
}

# Start all XYD servers
start_xyd_server "seat-capabilities" 5176
start_xyd_server "trailer-domain-model" 5177  
start_xyd_server "seat-domain-model" 5178
start_xyd_server "multiple-domains" 5179
start_xyd_server "multiple-classification-schemes" 5180
start_xyd_server "specification-history-registry" 5181

echo ""
echo "🎯 XYD Servers Status:"
echo "- Seat Capabilities:           http://localhost:5176/api/seat-capabilities"
echo "- Trailer Domain Model:       http://localhost:5177/api/trailer-domain-model"
echo "- Seat Domain Model:          http://localhost:5178/api/seat-domain-model"
echo "- Multiple Domains:           http://localhost:5179/api/multiple-domains"
echo "- Classification Schemes:     http://localhost:5180/api/multiple-classification-schemes"
echo "- Specification History:      http://localhost:5181/api/specification-history-registry"
echo ""
echo "📖 Hugo Documentation: http://localhost:61623/examples/"
echo ""
echo "To stop all servers, run: ./stop-xyd-servers.sh"
