from rss_proxy.services.host_updater import rss_updater
from rss_proxy.services.redis_manager import redis_manager_instance


async def startup_event():
    await redis_manager_instance.init_redis()


async def shutdown_event():
    await redis_manager_instance.close_redis()
