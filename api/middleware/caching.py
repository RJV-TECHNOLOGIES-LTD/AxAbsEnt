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
from typing import Callable, Optional, Any, Dict, Tuple, Union
from datetime import datetime, timedelta

from fastapi import Request, Response, Depends
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_409_CONFLICT, HTTP_304_NOT_MODIFIED

try:
    import redis
    from redis.exceptions import RedisError
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

logger = logging.getLogger("axabsent.cache")

# Cache storage types
class CacheStorage:
    """Base class for cache storage implementations"""
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError
    
    def set(self, key: str, value: Dict[str, Any], ttl: int) -> bool:
        raise NotImplementedError
    
    def exists(self, key: str) -> bool:
        raise NotImplementedError
    
    def invalidate(self, key: str) -> bool:
        raise NotImplementedError

class MemoryCache(CacheStorage):
    """In-memory cache implementation"""
    def __init__(self):
        self._cache: Dict[str, Tuple[Dict[str, Any], datetime]] = {}
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        if key not in self._cache:
            return None
        
        value, expiry = self._cache[key]
        if expiry < datetime.now():
            del self._cache[key]
            return None
        
        return value
    
    def set(self, key: str, value: Dict[str, Any], ttl: int) -> bool:
        expiry = datetime.now() + timedelta(seconds=ttl)
        self._cache[key] = (value, expiry)
        return True
    
    def exists(self, key: str) -> bool:
        if key not in self._cache:
            return False
        
        _, expiry = self._cache[key]
        if expiry < datetime.now():
            del self._cache[key]
            return False
        
        return True
    
    def invalidate(self, key: str) -> bool:
        if key in self._cache:
            del self._cache[key]
            return True
        return False

class RedisCache(CacheStorage):
    """Redis-backed cache implementation"""
    def __init__(self, redis_url: str):
        self.client = redis.Redis.from_url(redis_url)
        # Test connection
        self.client.ping()
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        try:
            data = self.client.get(key)
            if not data:
                return None
            return json.loads(data)
        except (RedisError, json.JSONDecodeError) as e:
            logger.error(f"Redis cache get error: {e}")
            return None
    
    def set(self, key: str, value: Dict[str, Any], ttl: int) -> bool:
        try:
            return self.client.setex(
                key, 
                ttl,
                json.dumps(value, default=str)
            )
        except (RedisError, TypeError) as e:
            logger.error(f"Redis cache set error: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        try:
            return bool(self.client.exists(key))
        except RedisError as e:
            logger.error(f"Redis cache exists error: {e}")
            return False
    
    def invalidate(self, key: str) -> bool:
        try:
            return bool(self.client.delete(key))
        except RedisError as e:
            logger.error(f"Redis cache invalidate error: {e}")
            return False

# Configuration from environment (can be moved to config.py)
class CacheConfig:
    ENABLED = True
    TTL_SECONDS = 900  # 15 minutes
    REDIS_URL = "redis://localhost:6379/0"
    IMMUTABLE_PATHS = {"/api/simulate", "/api/forces", "/api/visualization"}
    CACHE_CONTROL_HEADER = True
    USE_ETAGS = True

# Cache factory
def get_cache_storage() -> CacheStorage:
    if REDIS_AVAILABLE:
        try:
            return RedisCache(CacheConfig.REDIS_URL)
        except Exception as e:
            logger.warning(f"Redis cache initialization failed: {e}")
    
    logger.info("Using in-memory cache storage")
    return MemoryCache()

# Initialize cache
cache_storage = get_cache_storage()

async def get_request_body(request: Request) -> dict:
    """Extract and parse request body"""
    body = await request.body()
    try:
        return json.loads(body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {}

def _hash_request(request: Request, body: dict) -> str:
    """Generate a unique hash for the request"""
    key_data = {
        "method": request.method,
        "path": request.url.path,
        "query": str(request.query_params),
        "body": body,
    }
    key_string = json.dumps(key_data, sort_keys=True)
    return hashlib.sha256(key_string.encode()).hexdigest()

class CacheMiddleware(BaseHTTPMiddleware):
    """Middleware for transparent API response caching"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Early bailout for non-cacheable requests
        if not CacheConfig.ENABLED or request.method not in ["GET", "POST"]:
            return await call_next(request)
            
        # Check if path is cacheable
        if request.url.path not in CacheConfig.IMMUTABLE_PATHS:
            return await call_next(request)
        
        # Extract body for POST requests, empty dict for GET
        body = await get_request_body(request) if request.method == "POST" else {}
        cache_key = _hash_request(request, body)
        
        # Check client-side cache with ETag
        if CacheConfig.USE_ETAGS:
            client_etag = request.headers.get("If-None-Match")
            if client_etag and client_etag == f'"{cache_key}"':
                return Response(
                    status_code=HTTP_304_NOT_MODIFIED,
                    headers={"ETag": f'"{cache_key}"'}
                )
        
        # Check server-side cache
        cached_data = cache_storage.get(cache_key)
        if cached_data:
            logger.debug(f"Cache HIT: {request.url.path}")
            response = JSONResponse(content=cached_data)
            
            # Add cache control headers
            if CacheConfig.CACHE_CONTROL_HEADER:
                response.headers["Cache-Control"] = f"max-age={CacheConfig.TTL_SECONDS}"
            
            if CacheConfig.USE_ETAGS:
                response.headers["ETag"] = f'"{cache_key}"'
                
            return response
        
        # Cache miss - process request normally
        response = await call_next(request)
        
        # Only cache successful responses
        if response.status_code == 200:
            # Extract response body
            body_bytes = [chunk async for chunk in response.body_iterator]
            content = b"".join(body_bytes)
            
            try:
                # Parse and cache JSON response
                data = json.loads(content.decode("utf-8"))
                cache_storage.set(cache_key, data, CacheConfig.TTL_SECONDS)
                
                # Create new response with caching headers
                response = JSONResponse(content=data)
                
                if CacheConfig.CACHE_CONTROL_HEADER:
                    response.headers["Cache-Control"] = f"max-age={CacheConfig.TTL_SECONDS}"
                
                if CacheConfig.USE_ETAGS:
                    response.headers["ETag"] = f'"{cache_key}"'
                    
                logger.debug(f"Cache SET: {request.url.path}")
            except Exception as e:
                logger.warning(f"Failed to cache response: {e}")
                # Reconstruct original response
                response = Response(
                    content=content,
                    status_code=200, 
                    headers=dict(response.headers)
                )
        
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
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            else:
                raise ValueError("Request context missing for cache_guard.")

        body = await get_request_body(request)
        cache_key = _hash_request(request, body)

        if cache_storage.exists(cache_key):
            logger.info(f"Blocked ontological overwrite attempt: {request.url.path}")
            return JSONResponse(
                content={
                    "detail": "This ontological simulation is immutable and already cached.",
                    "status": "conflict",
                    "code": "IMMUTABLE_ENTITY"
                },
                status_code=HTTP_409_CONFLICT,
            )

        return await func(*args, **kwargs)

    return wrapper

# Dependency for clearing cache (admin operations)
def invalidate_cache(key_pattern: str = None):
    """
    Dependency for invalidating cache entries.
    Currently simplistic - would need pattern matching for Redis.
    """
    # This is a placeholder for a more sophisticated implementation
    # that would allow targeted cache invalidation
    pass
