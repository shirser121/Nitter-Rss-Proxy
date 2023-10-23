import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://status.d420.de/api/v1/instances")

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

REDIS_CACHE_DURATION_SECONDS = int(os.getenv("REDIS_CACHE_DURATION_SECONDS", 60 * 2))
HOSTS_CACHE_DURATION_SECONDS = int(os.getenv("HOSTS_CACHE_DURATION_SECONDS", 60 * 60 * 24))

SECURITY_CODE = os.getenv("SECURITY_CODE", None)
