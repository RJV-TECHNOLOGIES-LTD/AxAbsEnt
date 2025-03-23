# api/wsgi.py

"""
WSGI/ASGI Entry Point for AxAbsEnt API
This file exposes the unified FastAPI app for:
- Uvicorn standalone:          uvicorn api.wsgi:app
- Gunicorn + UvicornWorker:    gunicorn api.wsgi:app -k uvicorn.workers.UvicornWorker
- Dockerfile CMD:              CMD ["uvicorn", "api.wsgi:app", "--host", "0.0.0.0", "--port", "8000"]
- Kubernetes deployments with readiness checks
"""

import logging
from api import app
from api.config import config

# Optional: custom logging setup for WSGI/ASGI processes
logger = logging.getLogger("uvicorn.error")
logger.setLevel(config.LOG_LEVEL)

# ✅ Exposed app instance (FastAPI is ASGI-compliant)
__all__ = ["app"]
