from fastapi import Request, HTTPException

API_KEY = "axabsent-secret-token"

async def verify_api_key(request: Request):
    token = request.headers.get("X-API-Key")
    if token != API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")
