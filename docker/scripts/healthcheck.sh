#!/bin/bash

set -e

# Check Python environment
if ! command -v python3 &> /dev/null; then
    echo "Python3 not found"
    exit 1
fi

# Check AxAbsEnt package is installed and functional
python3 -c "import axabsent; assert hasattr(axabsent, '__version__'), 'AxAbsEnt package corrupted or incomplete'"

# Optional: Ping API if running (adjust the port if needed)
API_HOST=${API_HOST:-"localhost"}
API_PORT=${API_PORT:-8000}
API_URL="http://${API_HOST}:${API_PORT}/health"

# Perform API health check only if port is open
if nc -z "$API_HOST" "$API_PORT"; then
    STATUS_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL")
    if [ "$STATUS_CODE" -ne 200 ]; then
        echo "AxAbsEnt API not healthy (HTTP $STATUS_CODE)"
        exit 1
    fi
    echo "AxAbsEnt API is healthy"
else
    echo "AxAbsEnt API port ${API_PORT} not open (may not be running)"
fi

echo "Container is healthy"
exit 0
