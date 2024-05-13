from redis.asyncio.client import Redis
from redis.asyncio.retry import Retry
from redis.backoff import NoBackoff
from redis.asyncio.connection import ConnectionPool

from forecaster.config import settings


def create_redis_client() -> Redis:
    retry = Retry(NoBackoff(), 1)
    pool = ConnectionPool(
        host=settings.redis_host,
        port=settings.redis_port,
        db=settings.redis_database,
        retry_on_timeout=True,
        retry=retry,
        retry_on_error=[ConnectionError],
    )
    return Redis(
        connection_pool=pool,
        socket_timeout=0.25,
        health_check_interval=1,
    )


client = create_redis_client()
