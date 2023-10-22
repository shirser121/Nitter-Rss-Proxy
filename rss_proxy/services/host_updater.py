import asyncio
from datetime import datetime, timedelta
import httpx
from rss_proxy.utils.logger import logger
from rss_proxy.core.config import BASE_URL, HOSTS_CACHE_DURATION_SECONDS
from rss_proxy.services.redis_manager import redis_manager_instance


class RSSHostUpdater:
    def __init__(self, base_url, redis_manager):
        self.base_url = base_url
        self.healthy_rss_hosts_cache = []
        self.current_host_index = 0
        self.last_update = datetime.now() - timedelta(seconds=HOSTS_CACHE_DURATION_SECONDS)
        self.redis_manager = redis_manager
        self.redis_key = "healthy_rss_hosts_cache_key"

    async def get_hosts(self):
        cached_data: bytes = await self.redis_manager.get_cache(self.redis_key)
        logger.info(f"Loaded cached_data bytes from cache")
        logger.info(f"cached_data: {cached_data}")
        if cached_data:
            self.healthy_rss_hosts_cache = cached_data
            logger.info("Loaded healthy RSS hosts from cache.")
            logger.info(f"Fetched {len(self.healthy_rss_hosts_cache)} hosts")
            return True
        else:
            logger.info("No cached data found.")
            return await self.update_healthy_rss_hosts()

    async def update_healthy_rss_hosts(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.base_url)
                response.raise_for_status()
                data = response.json()
                self.healthy_rss_hosts_cache = [host for host in data["hosts"] if host["healthy"] and host["rss"]]
                await self.redis_manager.set_cache(self.redis_key, self.healthy_rss_hosts_cache,
                                                   HOSTS_CACHE_DURATION_SECONDS)
                logger.info("Working hosts fetched successfully")
                logger.info(f"Fetched {len(self.healthy_rss_hosts_cache)} hosts")
                return True
        except httpx.RequestError as e:
            logger.error(f"Failed to fetch hosts: {e}")
            return False

    async def get_round_robin_host(self):
        if not await self.get_hosts():
            raise Exception("There is no healthy_rss_hosts_cache")

        host = self.healthy_rss_hosts_cache[self.current_host_index]
        self.current_host_index = (self.current_host_index + 1) % len(self.healthy_rss_hosts_cache)
        return host


rss_updater = RSSHostUpdater(BASE_URL, redis_manager_instance)
