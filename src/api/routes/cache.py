# src/api/routes/cache.py
from fastapi import APIRouter, Depends
from src.core.redis_client import redis_client
from src.repositories.user_repo import UserRepository
from src.api.dependencies import get_user_repo
import json

router = APIRouter(prefix="/cache", tags=["cache"])


@router.get("/users/{user_id}")
async def get_user_cached(
        user_id: int,
        repo: UserRepository = Depends(get_user_repo)
):
    # 1. Проверяем кеш
    cache_key = f"user:{user_id}"
    cached_data = await redis_client.get(cache_key)

    if cached_data:
        return {"source": "cache", "data": json.loads(cached_data)}

    # 2. Нет в кеше — запрос к БД
    user = await repo.get_by_id(user_id)
    if not user:
        return {"error": "User not found"}

    # 3. Сохраняем в кеш на 5 минут
    user_data = {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "role": user.role
    }
    await redis_client.setex(
        cache_key,
        300,  # TTL 5 минут
        json.dumps(user_data)
    )

    return {"source": "db", "data": user_data}


@router.delete("/users/{user_id}/cache")
async def invalidate_user_cache(user_id: int):
    """Инвалидация кеша"""
    await redis_client.delete(f"user:{user_id}")
    return {"status": "cache invalidated"}
