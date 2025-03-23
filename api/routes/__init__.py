# api/routes/__init__.py

from fastapi import APIRouter

from .interaction import router as interaction_router
from .simulation import router as simulation_router
from .forces import router as forces_router
from .absolute import router as absolute_router
api_router = APIRouter()

# 🔗 Attach all module routes
api_router.include_router(interaction_router)
api_router.include_router(simulation_router)
api_router.include_router(forces_router)
api_router.include_router(absolute_router)
