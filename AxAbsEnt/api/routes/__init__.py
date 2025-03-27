# api/routes/__init__.py

from fastapi import APIRouter

# 🔌 Import all route modules
from .interaction import router as interaction_router
from .simulation import router as simulation_router
from .forces import router as forces_router
from .absolute import router as absolute_router
from .visualization import router as visualization_router

# 🚦 Main API router object
api_router = APIRouter()

# 🔗 Attach every sub-route
api_router.include_router(interaction_router)
api_router.include_router(simulation_router)
api_router.include_router(forces_router)
api_router.include_router(absolute_router)
api_router.include_router(visualization_router)
