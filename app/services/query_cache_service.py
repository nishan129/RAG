import hashlib
import json
import logging
import threading
import time
from collections import defaultdict
from typing import Any

from app.config import settings

logger = logging.getLogger(__name__)

class QueryCacheService:
    _TIERS = ("intent","rag_answer","sql_gen","sql_result","embedding")

    def __init__(self):
        self._redis_client: Any | None = self._build_redis_client()
        self._memory_store: dict[str, tuple[float, str]] = {}
        self._stats: dict[str, dict[str, int]] = {
            tier: defaultdict(int) for tier in self._TIERS
        }
        self._lock = threading.RLock()


    def _build_redis_client(self) -> Any | None:
        if not settings.upstash_redis_url or not settings.upstash_redis_token:
            logger.info("Redis cache disabled; missing Upstash config")
            return None
        try:
            from upstash_redis import Redis

            return Redis(url=settings.upstash_redis_url, token=settings.upstash_redis_token)
        except Exception as e:
            logger.exception("Failed to initialize Redis cache; using in-memory ")
            return None 
    
    def _key(self, namespace:str, raw:str) -> str:
        hashed = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        return f"{namespace}:{hashed}"
    
    def intent_key(self, question:str) -> str:
        return self._key("intent", question.strip().lower())
    
    def rag_answer_key(self, question:str, cache_context:dict[str, Any] | None):
        raw: str | dict[str, Any] = question.strip()
        if cache_context is not None:
            raw = {'question': question.strip(), 'context':cache_context}
        return self._key("rag_answer", json.dumps(raw, sort_key=True) if isinstance)
    
    def sql_gen_key(self, question: str) -> str:
        return self._key("sql_gen", question.strip())
    

    def sql_result_key(self, sql: str) -> str:
        return self._key("sql_result:v2", " ".join(sql.split()).strip().lower())
    




query_cache = QueryCacheService()