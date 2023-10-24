from fastapi import HTTPException, Request, APIRouter
from fastapi.responses import Response
import httpx

from rss_proxy.services.host_updater import rss_updater
from rss_proxy.services.redis_manager import redis_manager_instance
from rss_proxy.utils.logger import logger
from rss_proxy.utils.rss_refactor import refactor_rss_feed
from rss_proxy.core.config import REDIS_CACHE_DURATION_SECONDS

router = APIRouter()


@router.get("/")
async def read_root():
    return {"message": "Welcome to the proxy server!"}


@router.get("/rss/{username}")
async def proxy_to_healthy_rss_host(username: str, request: Request, force_update: bool = False):
    logger.info(f"Rss request to {username}")

    cache_key = f"rss:{username}"
    cached_content: bytes = await redis_manager_instance.get_cache(cache_key)

    if cached_content and not force_update:
        logger.info("Resolve rss from cache")
        if cached_content.decode("UTF-8") == 'NOT EXIST':
            logger.warn(f"Requested rss not found - maybe use not exist {username}")
            await redis_manager_instance.set_cache(cache_key, 'NOT EXIST', REDIS_CACHE_DURATION_SECONDS)
            raise HTTPException(status_code=404, detail=f"Failed to fetch from {username} - maybe "
                                                        f"username not exist")
        else:
            return Response(content=cached_content, media_type="application/xml")

    host = await rss_updater.get_round_robin_host()
    target_url = f"{host['url']}/{username}/rss"

    query_params = request.query_params
    if query_params:
        target_url += "?" + "&".join([f"{k}={v}" for k, v in query_params.items()])

    async with httpx.AsyncClient() as client:
        response = await client.get(target_url)

    logger.info(f"Get rss feed from {target_url}")
    if response.status_code != 200:
        logger.warn(f"Requested rss not found - maybe use not exist {username}")
        await redis_manager_instance.set_cache(cache_key, 'NOT EXIST', REDIS_CACHE_DURATION_SECONDS)

        raise HTTPException(status_code=response.status_code, detail=f"Failed to fetch from {target_url}")

    rss_feed = await refactor_rss_feed(response.text)

    await redis_manager_instance.set_cache(cache_key, rss_feed, REDIS_CACHE_DURATION_SECONDS)

    return Response(content=rss_feed, media_type="application/xml")
