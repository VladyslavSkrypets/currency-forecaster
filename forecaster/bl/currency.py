from sqlalchemy import select, Result

from forecaster.services import db
from forecaster.services import redis
from forecaster.utilities.logging import logger
from forecaster.schemas.currency import CurrencyData
from forecaster.models.currency import Currency
from forecaster.const import (
    ACTUAL_CURRENCY_REDIS_KEY,
    REDIS_DEFAULT_TTL_FOR_CACHE,
)


async def get_actual_currency_data() -> CurrencyData | None:
    try:
        currency_data_cached = await redis.client.get(
            name=ACTUAL_CURRENCY_REDIS_KEY,
        )
        currency_data_cached = None
    except Exception:
        currency_data_cached = None
        logger.exception('[CF] Failed to get currency data from redis')

    if currency_data_cached is not None:
        return CurrencyData.model_validate_json(currency_data_cached)
    
    async with db.async_sessionmaker.begin() as db_session:
        query_result: Result = await db_session.execute(
            select(
                Currency.sell,
                Currency.buy,
                Currency.created_at,
            ).order_by(Currency.created_at.desc())
        )
    try:
        currency_data = query_result.mappings().first()
    except Exception:
        logger.exception('[CF] Failed to get currency data from database')
        return None
    
    if currency_data is None:
        return None
    
    currency_data = CurrencyData.model_validate(currency_data)
    
    try:
        await redis.client.setex(
            name=ACTUAL_CURRENCY_REDIS_KEY,
            time=REDIS_DEFAULT_TTL_FOR_CACHE,
            value=currency_data.model_dump_json(),
        )
    except Exception:
        logger.exception('[CF] Failed to set currency data to redis')

    return currency_data
