import pickle

from redis import asyncio as aioredis
from rss_proxy.core.config import REDIS_HOST, REDIS_PORT


class RedisManager:
    def __init__(self, host='localhost', port=6379):
        self._host = host
        self._port = port
        self._pool = None
        self.client = None

    async def init_redis(self):
        if not self._pool:
            self._pool = aioredis.ConnectionPool.from_url(f'redis://{self._host}:{self._port}')
            self.client = await aioredis.Redis.from_pool(self._pool)

    async def close_redis(self):
        if self.client:
            await self.client.close()

    async def set_cache(self, key, value, duration):
        value = pickle.dumps(value)
        await self.client.setex(key, duration, value)

    async def get_cache(self, key):
        result = await self.client.get(key)
        if result:
            return pickle.loads(result)


redis_manager_instance = RedisManager(REDIS_HOST, REDIS_PORT)
