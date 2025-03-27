# api/server.py

import uvicorn
from api import app
from api.config import config
import os

def run():
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    reload = os.getenv("RELOAD", "false").lower() == "true"

    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=reload,
        log_level=config.LOG_LEVEL.lower()
    )

if __name__ == "__main__":
    run()
