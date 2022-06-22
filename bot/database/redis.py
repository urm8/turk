from datetime import timedelta
from typing import Any

import aioredis
from aioredis import client

redis = aioredis.from_url(
    'redis://localhost', encoding='utf-8', decode_responses=True,
)


async def set(key: str, value: Any, ttl: timedelta = timedelta(minutes=5)) -> Any:
    async with redis.client() as connection:
        await connection.set(key, value, ex=ttl.total_seconds())


async def unset(key: str) -> Any:
    async with redis.client() as connection:
        await connection.delete(key)


async def get(key: str) -> Any:
    async with redis.client() as connection:
        return await connection.get(key)
