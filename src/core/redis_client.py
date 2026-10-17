# src/core/redis_client.py
import redis.asyncio as aioredis

redis_client = aioredis.from_url(
    "redis://localhost:6379/0",
    decode_responses=True
)
