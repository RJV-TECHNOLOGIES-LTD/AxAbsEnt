#!/bin/bash
set -e

echo "[START] Starting AxAbsEnt core services..."

# Set working directory
cd /app

# Start the API server using gunicorn with uvicorn workers
echo "[START] Launching API server on port 8000..."
gunicorn api.server:app \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --log-level info \
    --timeout 180 &

API_PID=$!
echo "[START] API server running with PID $API_PID"

# Start the simulation job processor if configured
if [ "$START_SIM_ENGINE" = "true" ]; then
    echo "[START] Launching simulation engine..."
    python3 -m axabsent.simulation.parallel &
    SIM_PID=$!
    echo "[START] Simulation engine running with PID $SIM_PID"
fi

# Optional: Start background jobs (e.g., prediction pipelines, retraining)
if [ -f "./scripts/setup/start_jobs.py" ]; then
    echo "[START] Launching background job scheduler..."
    python3 ./scripts/setup/start_jobs.py &
    JOB_PID=$!
    echo "[START] Job scheduler running with PID $JOB_PID"
fi

# Trap SIGTERM and cleanup
trap 'echo "[SHUTDOWN] Stopping services..."; kill $API_PID $SIM_PID $JOB_PID 2>/dev/null || true; wait; exit 0' SIGTERM SIGINT

# Wait on background services
wait
