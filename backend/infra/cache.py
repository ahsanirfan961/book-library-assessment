

import os
from typing import Any, Optional

import redis.asyncio as redis
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
USERNAME = os.getenv("REDIS_USERNAME")
PASSWORD = os.getenv("REDIS_PASSWORD")


class RedisStorage:

    TTL: int = 60 * 5   # 5 minutes

    _instance: Optional["RedisStorage"] = None
    _initialized: bool = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:

        if self._initialized:
            return

        self._initialized = True

        self._local_db = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            decode_responses=True,
            username=USERNAME,
            password=PASSWORD,
        )

    async def close(self) -> None:
        await self._local_db.aclose()

    async def test_connection(self) -> None:
        try:
            await self._local_db.ping()  
            logger.success("Redis connection established")
        except Exception as exc:
            logger.warning(
                f"DataRepository: Redis connection failed, caching disabled: {exc}"
            )

    async def get(
        self,
        name: str,
    ) -> Any:
        return await self._local_db.get(name)

    async def set(
        self,
        name: str,
        value: Any,
        ex: Optional[int] = TTL,
    ) -> None:
        await self._local_db.set(name, value, ex=ex)
