# api/__init__.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from api.routes import api_router
from api.config import config
from api.errors import setup_error_handlers
from api.middleware.caching import CacheMiddleware
import logging

# Setup logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("axabsent")

# Create FastAPI application
app = FastAPI(
    title="AxAbsEnt: Unified Absolute Interaction Engine",
    description=(
        "High-precision API for absolute entity modeling, "
        "force emergence, simulation pipelines, and visualization logic — "
        "based on the Enhanced Mathematical Ontology of Absolute Nothingness."
    ),
    version=config.VERSION,
    docs_url=None,  # We'll use custom docs
    redoc_url=None,  # We'll use custom redoc
    openapi_url="/openapi.json"
)

# ✅ CORS middleware for frontend interaction and cross-platform integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Add caching middleware
app.add_middleware(CacheMiddleware)

# ✅ Register error handlers
setup_error_handlers(app)

# 🔗 Mount all domain-specific routes
app.include_router(api_router)

# Custom OpenAPI and documentation
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        swagger_js_url="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.15.5/swagger-ui-bundle.min.js",
        swagger_css_url="https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.15.5/swagger-ui.min.css",
        swagger_favicon_url="/static/favicon.ico"
    )

@app.get("/redoc", include_in_schema=False)
async def custom_redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - ReDoc",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js",
        redoc_favicon_url="/static/favicon.ico"
    )

# ✅ System healthcheck with enhanced details
@app.get("/health")
def health():
    return {
        "status": "OK",
        "version": app.version,
        "system": {
            "memory_used": "N/A",  # Would be implemented with psutil
            "uptime": "N/A",       # Would be implemented with uptime monitoring
            "nodes": 1 if not config.ENABLE_DISTRIBUTED else "N/A"
        },
        "features": {
            "distributed": config.ENABLE_DISTRIBUTED,
            "gpu_acceleration": config.ENABLE_GPU
        }
    }

# ✅ Root redirect with enhanced metadata
@app.get("/")
def root():
    return {
        "name": app.title,
        "description": app.description,
        "version": app.version,
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json"
        },
        "endpoints": {
            "health": "/health",
            "simulation": "/api/simulation",
            "forces": "/api/forces",
            "absolute": "/api/absolute",
            "visualization": "/api/visualization",
            "interactions": "/api/interactions"
        }
    }
