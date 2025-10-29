#!/bin/bash

# XYD Examples Stop Script
# This script stops all XYD documentation servers

echo "🛑 Stopping XYD Documentation Servers..."

# Function to stop XYD server
stop_xyd_server() {
    local example_name=$1
    local pid_file="/tmp/xyd-$example_name.pid"
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p $pid > /dev/null 2>&1; then
            kill $pid
            echo "✅ Stopped $example_name (PID: $pid)"
            rm "$pid_file"
        else
            echo "⚠️  $example_name process not found"
            rm "$pid_file"
        fi
    else
        echo "⚠️  No PID file found for $example_name"
    fi
}

# Stop all XYD servers
stop_xyd_server "seat-capabilities"
stop_xyd_server "trailer-domain-model"
stop_xyd_server "seat-domain-model"
stop_xyd_server "multiple-domains"
stop_xyd_server "multiple-classification-schemes"
stop_xyd_server "specification-history-registry"

echo ""
echo "✅ All XYD servers stopped"
