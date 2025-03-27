# api/middleware/caching.py

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

from api.config import config

# Setup logger
logger = logging.getLogger("axabsent.cache")

# Try to import Redis, but don't fail if not available
try:
    import redis
    from redis.exceptions import RedisError
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("Redis not available, falling back to in-memory cache")

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
    
    def flush(self) -> bool:
        """Flush the entire cache storage"""
        raise NotImplementedError

class MemoryCache(CacheStorage):
    """In-memory cache implementation"""
    def __init__(self):
        self._cache: Dict[str, Tuple[Dict[str, Any], datetime]] = {}
        logger.info("Initialized in-memory cache")
    
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
    
    def flush(self) -> bool:
        """Clear all cache entries"""
        self._cache.clear()
        return True
    
    def get_stats(self) -> Dict[str, Any]:
        """Return cache statistics"""
        current_time = datetime.now()
        active_keys = [k for k, (_, exp) in self._cache.items() if exp > current_time]
        
        return {
            "total_entries": len(self._cache),
            "active_entries": len(active_keys),
            "expired_entries": len(self._cache) - len(active_keys),
            "memory_usage_approx": "N/A"  # Would require deep size calculation
        }

class RedisCache(CacheStorage):
    """Redis-backed cache implementation"""
    def __init__(self, redis_url: str, prefix: str = "axabsent:"):
        self.prefix = prefix
        try:
            self.client = redis.Redis.from_url(redis_url)
            # Test connection
            self.client.ping()
            logger.info(f"Successfully connected to Redis at {redis_url}")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
    
    def _prefixed_key(self, key: str) -> str:
        """Add prefix to key for namespace isolation"""
        return f"{self.prefix}{key}"
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        prefixed_key = self._prefixed_key(key)
        try:
            data = self.client.get(prefixed_key)
            if not data:
                return None
            return json.loads(data)
        except (RedisError, json.JSONDecodeError) as e:
            logger.error(f"Redis cache get error: {e}")
            return None
    
    def set(self, key: str, value: Dict[str, Any], ttl: int) -> bool:
        prefixed_key = self._prefixed_key(key)
        try:
            return bool(self.client.setex(
                prefixed_key, 
                ttl,
                json.dumps(value, default=str)
            ))
        except (RedisError, TypeError) as e:
            logger.error(f"Redis cache set error: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        prefixed_key = self._prefixed_key(key)
        try:
            return bool(self.client.exists(prefixed_key))
        except RedisError as e:
            logger.error(f"Redis cache exists error: {e}")
            return False
    
    def invalidate(self, key: str) -> bool:
        prefixed_key = self._prefixed_key(key)
        try:
            return bool(self.client.delete(prefixed_key))
        except RedisError as e:
            logger.error(f"Redis cache invalidate error: {e}")
            return False
    
    def flush(self) -> bool:
        """Clear all cache entries with this prefix"""
        try:
            keys = self.client.keys(f"{self.prefix}*")
            if keys:
                return bool(self.client.delete(*keys))
            return True
        except RedisError as e:
            logger.error(f"Redis cache flush error: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Return cache statistics"""
        try:
            keys = self.client.keys(f"{self.prefix}*")
            info = self.client.info("memory")
            
            return {
                "total_entries": len(keys),
                "memory_usage": info.get("used_memory_human", "N/A"),
                "max_memory": info.get("maxmemory_human", "N/A")
            }
        except RedisError as e:
            logger.error(f"Redis stats error: {e}")
            return {"error": str(e)}

# Cache configuration class from config.py
class CacheConfig:
    ENABLED = getattr(config, "CACHE_ENABLED", True)
    TTL_SECONDS = getattr(config, "CACHE_TTL_SECONDS", 900)  # 15 minutes
    REDIS_URL = getattr(config, "REDIS_URL", "redis://localhost:6379/0")
    REDIS_PREFIX = getattr(config, "REDIS_PREFIX", "axabsent:")
    IMMUTABLE_PATHS = {"/api/simulate", "/api/forces", "/api/visualization"}
    CACHE_CONTROL_HEADER = getattr(config, "CACHE_CONTROL_HEADER", True)
    USE_ETAGS = getattr(config, "USE_ETAGS", True)

# Cache factory with robust error handling
def get_cache_storage() -> CacheStorage:
    """
    Initialize cache storage with fallback mechanism.
    Attempts Redis first, falls back to in-memory if Redis fails or is unavailable.
    """
    if not CacheConfig.ENABLED:
        logger.info("Caching is disabled, returning dummy implementation")
        return MemoryCache()  # Still use memory cache but log that it's disabled
    
    if REDIS_AVAILABLE:
        try:
            return RedisCache(CacheConfig.REDIS_URL, CacheConfig.REDIS_PREFIX)
        except Exception as e:
            logger.warning(f"Redis cache initialization failed, falling back to in-memory cache: {e}")
    
    logger.info("Using in-memory cache storage")
    return MemoryCache()

# Initialize cache
try:
    cache_storage = get_cache_storage()
except Exception as e:
    logger.error(f"Failed to initialize cache storage: {e}")
    logger.warning("Using fallback memory cache")
    cache_storage = MemoryCache()

async def get_request_body(request: Request) -> dict:
    """Extract and parse request body"""
    try:
        body = await request.body()
        try:
            return json.loads(body.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {}
    except Exception:
        # Reset the stream position
        await request.body()
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
        if not any(request.url.path.startswith(path) for path in CacheConfig.IMMUTABLE_PATHS):
            return await call_next(request)
        
        try:
            # Extract body for POST requests, empty dict for GET
            body = await get_request_body(request) if request.method == "POST" else {}
            cache_key = _hash_request(request, body)
            
            # Check client-side cache with ETag
            if CacheConfig.USE_ETAGS:
                client_etag = request.headers.get("If-None-Match")
                if client_etag and client_etag == f'"{cache_key}"':
                    logger.debug(f"ETag match, returning 304: {request.url.path}")
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
                    
                # Add diagnostic header
                response.headers["X-Cache"] = "HIT"
                    
                return response
                
            # Reset body stream position
            await request.body()
            
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
                    
                    # Add diagnostic header
                    response.headers["X-Cache"] = "MISS"
                        
                    logger.debug(f"Cache SET: {request.url.path}")
                except Exception as e:
                    logger.warning(f"Failed to cache response: {e}")
                    # Reconstruct original response
                    response = Response(
                        content=content,
                        status_code=200, 
                        headers=dict(response.headers)
                    )
                    response.headers["X-Cache-Error"] = "Failed to cache response"
            
            return response
            
        except Exception as e:
            logger.exception(f"Cache middleware error: {e}")
            # Ensure we don't break the request pipeline on cache errors
            try:
                # Reset body stream position just in case
                await request.body()
                return await call_next(request)
            except Exception as inner_e:
                logger.critical(f"Catastrophic cache middleware error: {inner_e}")
                return JSONResponse(
                    status_code=500,
                    content={"detail": "Internal server error in cache middleware"}
                )

def cache_guard(func: Callable) -> Callable:
    """
    Route-level cache enforcement decorator.
    Prevents ontologically invalid overwrites by rejecting attempts
    to simulate identical requests with conflicting outputs.
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # Only enforce if caching is enabled
        if not CacheConfig.ENABLED:
            return await func(*args, **kwargs)
            
        request: Request = kwargs.get("request")
        if not request:
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            else:
                logger.error("Request context missing for cache_guard")
                return await func(*args, **kwargs)

        try:
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
                
            # Reset body stream position
            await request.body()
            return await func(*args, **kwargs)
            
        except Exception as e:
            logger.exception(f"Cache guard error: {e}")
            # Don't block the request on cache errors
            try:
                # Reset body stream position
                await request.body()
                return await func(*args, **kwargs)
            except Exception as inner_e:
                logger.critical(f"Catastrophic cache guard error: {inner_e}")
                return JSONResponse(
                    status_code=500,
                    content={"detail": "Internal server error in cache guard"}
                )

    return wrapper

# Cache admin endpoints (to be mounted in a separate admin router)
class CacheAdmin:
    @staticmethod
    async def get_stats():
        """Get cache statistics"""
        try:
            if hasattr(cache_storage, "get_stats"):
                stats = cache_storage.get_stats()
            else:
                stats = {"type": type(cache_storage).__name__}
                
            return {
                "enabled": CacheConfig.ENABLED,
                "ttl_seconds": CacheConfig.TTL_SECONDS,
                "storage_type": type(cache_storage).__name__,
                "stats": stats
            }
        except Exception as e:
            logger.error(f"Failed to get cache stats: {e}")
            return {"error": str(e)}
    
    @staticmethod
    async def flush_cache():
        """Flush the entire cache"""
        try:
            if hasattr(cache_storage, "flush"):
                success = cache_storage.flush()
            else:
                success = False
                
            return {
                "success": success,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to flush cache: {e}")
            return {"error": str(e)}
    
    @staticmethod
    async def invalidate_key(key: str):
        """Invalidate a specific cache key"""
        success = cache_storage.invalidate(key)
        return {
            "success": success,
            "key": key,
            "timestamp": datetime.now().isoformat()
        }
