"""
AxAbsEnt Unified API Caching Middleware
Author: Ricardo Jorge Do Vale
License: AxAbsEnt-NC (Non-Commercial, Attribution Required)

Purpose:
Implements transparent caching logic for simulation, visualization, and force extraction APIs,
ensuring deterministic consistency, reduced computational load, and ontology-compliant immutability.

Supports in-memory and Redis-backed caching with configurable TTL, key hashing, and ontology safeguards.
"""

import hashlib
import json
import functools
import logging
from typing import Callable, Optional, Any, Dict, Tuple

from fastapi import Request, Response
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_409_CONFLICT

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

logger = logging.getLogger("axabsent.cache")

# In-memory fallback cache
_local_cache: Dict[str, Tuple[Response, float]] = {}

# Configuration
CACHE_ENABLED = True
CACHE_TTL_SECONDS = 900  # 15 minutes
REDIS_URL = "redis://localhost:6379/0"
IMMUTABLE_PATHS = {"/simulate", "/forces", "/visualization"}

# Redis client (optional)
redis_client = None
if REDIS_AVAILABLE:
    try:
        redis_client = redis.Redis.from_url(REDIS_URL)
        redis_client.ping()
        logger.info("Redis cache backend connected.")
    except Exception:
        redis_client = None
        logger.warning("Redis unavailable, using in-memory cache.")


def _hash_request(request: Request, body: dict) -> str:
    key_data = {
        "method": request.method,
        "path": request.url.path,
        "query": str(request.query_params),
        "body": body,
    }
    key_string = json.dumps(key_data, sort_keys=True)
    return hashlib.sha256(key_string.encode()).hexdigest()


async def get_request_body(request: Request) -> dict:
    body = await request.body()
    try:
        return json.loads(body.decode("utf-8"))
    except Exception:
        return {}


class CacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        if not CACHE_ENABLED or request.method != "POST":
            return await call_next(request)

        # Check cache eligibility
        if request.url.path not in IMMUTABLE_PATHS:
            return await call_next(request)

        body = await get_request_body(request)
        cache_key = _hash_request(request, body)

        # Redis cache path
        if redis_client:
            cached = redis_client.get(cache_key)
            if cached:
                logger.debug(f"Cache HIT [Redis]: {request.url.path}")
                return JSONResponse(content=json.loads(cached), status_code=200)
        else:
            # Fallback to in-memory
            cached_entry = _local_cache.get(cache_key)
            if cached_entry:
                logger.debug(f"Cache HIT [Memory]: {request.url.path}")
                return cached_entry[0]

        # No cache hit → proceed and cache response
        response = await call_next(request)
        if response.status_code == 200:
            content = b"".join([chunk async for chunk in response.body_iterator])
            response = Response(content=content, status_code=200, headers=dict(response.headers))

            try:
                parsed_json = json.loads(content.decode("utf-8"))
                if redis_client:
                    redis_client.setex(cache_key, CACHE_TTL_SECONDS, json.dumps(parsed_json))
                else:
                    _local_cache[cache_key] = (JSONResponse(content=parsed_json), CACHE_TTL_SECONDS)
                logger.debug(f"Cache SET: {request.url.path}")
            except Exception as e:
                logger.warning(f"Failed to cache response: {e}")

        return response


def cache_guard(func: Callable) -> Callable:
    """
    Route-level cache enforcement decorator.
    Prevents ontologically invalid overwrites by rejecting attempts
    to simulate identical requests with conflicting outputs.
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get("request")
        if not request:
            raise ValueError("Request context missing for cache_guard.")

        body = await get_request_body(request)
        cache_key = _hash_request(request, body)

        if redis_client and redis_client.exists(cache_key):
            logger.info("Blocked ontological overwrite attempt (Redis cache guard).")
            return JSONResponse(
                content={"detail": "This ontological simulation is immutable and already cached."},
                status_code=HTTP_409_CONFLICT,
            )

        if not redis_client and cache_key in _local_cache:
            logger.info("Blocked ontological overwrite attempt (Memory cache guard).")
            return JSONResponse(
                content={"detail": "This ontological simulation is immutable and already cached."},
                status_code=HTTP_409_CONFLICT,
            )

        return await func(*args, **kwargs)

    return wrapper
