import asyncio

from sqlalchemy import insert

from forecaster.services import db
from forecaster.services import redis
from forecaster.utilities.logging import logger
from forecaster.models.currency import Currency
from forecaster.services.monobank import MonoBankService
from forecaster.const import (
    MINUTE,
    SECOND,
    ACTUAL_CURRENCY_REDIS_KEY,
    REDIS_DEFAULT_TTL_FOR_CACHE,
)


async def update_currency() -> bool:
    monobank_service = MonoBankService()
    while True:
        actual_currency = await monobank_service.get_actual_currency()
        if actual_currency:
            break

        await asyncio.sleep(20 * SECOND)
    
    async with db.async_sessionmaker.begin() as db_session:
        try:
            await db_session.execute(
                insert(Currency).values(
                    created_at=actual_currency.created_at,
                    sell=actual_currency.sell,
                    buy=actual_currency.buy,
                )
            )
            await db_session.commit()
            logger.info('[UC][Job] Saved new currency data to database')
        except Exception:
            logger.exception(
                '[UC][Job] Failed to save new currency data to database'
            )
            return False
    
    try:
        await redis.client.setex(
            name=ACTUAL_CURRENCY_REDIS_KEY,
            time=REDIS_DEFAULT_TTL_FOR_CACHE,
            value=actual_currency.model_dump_json(),
        )
    except Exception:
        logger.exception(
            '[UC][Job] Failed to set new currency data to redis'
        )
        return False
    
    return True


async def runner() -> None:
    while True:
        try:
            await update_currency()
        except Exception:
            logger.exception(
                '[UC][Job] Failed to run update currency job'
            )
        await asyncio.sleep(5 * MINUTE)


if __name__ == '__main__':
    try:
        asyncio.run(runner())
    except Exception:
        logger.exception('[UC][Job] Failed to run update currency job')
