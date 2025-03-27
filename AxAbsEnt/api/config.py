# api/config.py

import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv

# ✅ Load environment variables from .env (if present)
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# ✅ Core Configuration Class
class Config:
    # Metadata
    PROJECT_NAME: str = "AxAbsEnt API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = (
        "Unified Absolute Interaction Simulation and Force Emergence API, "
        "backed by the Enhanced Mathematical Ontology of Absolute Nothingness."
    )

    # CORS & Security
    ALLOWED_ORIGINS: List[str] = os.getenv("ALLOWED_ORIGINS", "*").split(",")

    # Runtime Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    RESULTS_DIR: Path = BASE_DIR / "data" / "simulation_results"

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Simulation defaults
    DEFAULT_RESOLUTION: int = int(os.getenv("DEFAULT_RESOLUTION", 100))
    DEFAULT_STEPS: int = int(os.getenv("DEFAULT_STEPS", 300))

    # File Limits
    MAX_RESULT_FILES: int = int(os.getenv("MAX_RESULT_FILES", 1000))

    # Cluster Mode / Feature Flags
    ENABLE_DISTRIBUTED: bool = os.getenv("ENABLE_DISTRIBUTED", "false").lower() == "true"
    ENABLE_GPU: bool = os.getenv("ENABLE_GPU", "false").lower() == "true"

# 🔗 Singleton config
config = Config()
