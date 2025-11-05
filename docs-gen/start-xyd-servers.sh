#!/bin/bash

# XYD Examples Startup Script
# This script starts XYD documentation servers for the two main S2DM examples

echo "🚀 Starting XYD Documentation Servers..."

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

# Start XYD servers (seat-capabilities serves the seat-domain-model page)
start_xyd_server "seat-capabilities" 5176
start_xyd_server "trailer-domain-model" 5177  

echo ""
echo "🎯 XYD Servers Running:"
echo "- Seat Domain Model:      http://localhost:5176/api/seat-capabilities"
echo "- Trailer Domain Model:   http://localhost:5177/api/trailer-domain-model"
echo ""
echo "📖 Hugo Documentation Pages:"
echo "- Seat Domain Model:      http://localhost:1313/examples/seat-domain-model/example-documentation/"
echo "- Trailer Domain Model:   http://localhost:1313/examples/trailer-domain-model/example-documentation/"
echo ""
echo "💡 Wait ~10 seconds for servers to fully initialize."
echo "📋 To stop servers, run: ./stop-xyd-servers.sh"
echo ""
echo "View logs:"
echo "  tail -f /tmp/xyd-seat-capabilities.log"
echo "  tail -f /tmp/xyd-trailer-domain-model.log"
