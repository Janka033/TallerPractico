from __future__ import annotations
from typing import Optional
import time
import logging
from src.infrastructure.config.settings import get_settings

try:
    import redis  # type: ignore
except Exception:  # pragma: no cover
    redis = None  # type: ignore

logger = logging.getLogger(__name__)

class CacheClient:
    def __init__(self):
        settings = get_settings()
        self.ttl = settings.cache_ttl_seconds
        self._client = None
        self._memory_cache: dict[str, tuple[float, str]] = {}
        if settings.redis_url and redis is not None:
            try:
                self._client = redis.from_url(settings.redis_url, decode_responses=True)
                # Test conexión
                self._client.ping()
            except Exception as e:
                logger.warning("Redis no disponible en %s: %s", settings.redis_url, e)
                self._client = None

    def get(self, key: str) -> Optional[str]:
        if self._client:
            try:
                return self._client.get(key)
            except Exception as e:
                logger.warning("Fallo Redis GET para key %s: %s", key, e)
                return None
        # caché en memoria con TTL
        item = self._memory_cache.get(key)
        if not item:
            return None
        expires_at, value = item
        if time.time() > expires_at:
            del self._memory_cache[key]
            return None
        return value

    def set(self, key: str, value: str, ttl: Optional[int] = None) -> None:
        ttl = ttl or self.ttl
        if self._client:
            try:
                self._client.set(key, value, ex=ttl)
                return
            except Exception as e:
                logger.warning("Fallo Redis SET para key %s: %s (fallback a memoria)", key, e)
        self._memory_cache[key] = (time.time() + ttl, value)

    def delete(self, key: str) -> None:
        if self._client:
            try:
                self._client.delete(key)
                return
            except Exception as e:
                logger.warning("Fallo Redis DEL para key %s: %s (continuando)", key, e)
        if key in self._memory_cache:
            del self._memory_cache[key]