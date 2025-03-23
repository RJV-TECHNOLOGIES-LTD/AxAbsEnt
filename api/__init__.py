# api/__init__.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import api_router

app = FastAPI(
    title="AxAbsEnt: Unified Absolute Interaction Engine",
    description=(
        "High-precision API for absolute entity modeling, "
        "force emergence, simulation pipelines, and visualization logic — "
        "based on the Enhanced Mathematical Ontology of Absolute Nothingness."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# ✅ CORS middleware for frontend interaction and cross-platform integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 🔗 Mount all domain-specific routes
app.include_router(api_router)

# ✅ System healthcheck
@app.get("/health")
def health():
    return { "status": "OK", "version": app.version }

# ✅ Root redirect
@app.get("/")
def root():
    return {
        "name": app.title,
        "description": app.description,
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "openapi": "/openapi.json"
    }

