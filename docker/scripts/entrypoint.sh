#!/bin/bash
set -e

APP_DIR="/app"
LOG_DIR="/var/log/axabsent"
CACHE_DIR="/var/cache/axabsent"
DATA_DIR="/data"

# Ensure required directories exist
mkdir -p "$LOG_DIR" "$CACHE_DIR" "$DATA_DIR"

# Load environment variables if .env exists
if [ -f "$APP_DIR/.env" ]; then
    echo "[ENTRYPOINT] Loading environment from .env"
    export $(grep -v '^#' "$APP_DIR/.env" | xargs)
fi

# Pre-startup system checks
echo "[ENTRYPOINT] Validating environment..."
python3 -c "import sys; assert sys.version_info >= (3,10), 'Python 3.10+ required'"
python3 -c "import axabsent; print('[ENTRYPOINT] AxAbsEnt version:', axabsent.__version__)"

# Optional: Apply DB or simulation state migrations
if [ -f "$APP_DIR/scripts/setup/apply_migrations.py" ]; then
    echo "[ENTRYPOINT] Applying internal state migrations..."
    python3 "$APP_DIR/scripts/setup/apply_migrations.py"
fi

# Parse runtime arguments
CMD="$1"

case "$CMD" in
    --api)
        echo "[ENTRYPOINT] Launching API Server..."
        exec gunicorn api.server:app \
            --bind 0.0.0.0:8000 \
            --workers 4 \
            --worker-class uvicorn.workers.UvicornWorker \
            --timeout 120
        ;;
    --simulate)
        echo "[ENTRYPOINT] Running AxAbsEnt simulation engine..."
        exec python3 -m axabsent.simulation.base
        ;;
    --notebook)
        echo "[ENTRYPOINT] Launching Jupyter environment..."
        exec jupyter lab --ip=0.0.0.0 --port=8888 --allow-root --no-browser
        ;;
    --shell)
        echo "[ENTRYPOINT] Dropping into container shell..."
        exec /bin/bash
        ;;
    *)
        echo "[ENTRYPOINT] Unknown or no command provided: '$CMD'"
        echo "Usage:"
        echo "  docker run axabsent --api        # Start API server"
        echo "  docker run axabsent --simulate   # Run simulations"
        echo "  docker run axabsent --notebook   # Start Jupyter"
        echo "  docker run axabsent --shell      # Shell access"
        exit 1
        ;;
esac
