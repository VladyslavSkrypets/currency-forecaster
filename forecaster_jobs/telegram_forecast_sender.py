import typing
import asyncio
import datetime

from sqlalchemy import select
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from forecaster.services import db
from forecaster.schemas.user import User
from forecaster.schemas.currency import CurrencyDataToPredict
from forecaster_telegram.bot import create_bot
from forecaster.utilities.logging import logger
from forecaster.models.user import User as UserORM
from forecaster.models.forecast import ForecastSubscription
from forecaster.bl.currency import get_actual_currency_data
from forecaster.ml.model import get_prediction
from forecaster_telegram.messages import (
    currency_forecasted_by_subscription_message,
)


SLEEP_HOURS = set([
    *list(range(0, 7)),
    22, 23,
])


async def get_users_to_send_forecasts() -> typing.Sequence[User]:
    async with db.async_sessionmaker.begin() as db_session:
        try:
            query_result = await db_session.execute(
                select(
                    UserORM.id,
                    UserORM.telegram_chat_id,
                    UserORM.telegram_username,
                    UserORM.telegram_first_name,
                    UserORM.telegram_last_name,
                    UserORM.telegram_language_code,
                ).join(
                    ForecastSubscription, UserORM.id == ForecastSubscription.user_id
                ).where(
                    ForecastSubscription.is_active.is_(True)
                )
            )
        except Exception:
            logger.exception(
                '[JOB][FORECAST SENDER] Failed to get users to send forecasts'
            )
            return []
        
    try:
        return [User.from_raw(user) for user in query_result.mappings().all()]
    except Exception:
        logger.exception(
            '[JOB][FORECAST SENDER] Failed to map users to send forecasts'
        )
        return []
    

async def sender() -> None:
    bot = create_bot()
    users_to_send_forecasts = await get_users_to_send_forecasts()

    try:
        actual_currency_data = await get_actual_currency_data()
    except Exception:
        logger.exception(
            '[JOB][FORECAST SENDER] Failed to get actual currency data'
        )
        return
    
    try:
        forecast_sell_price = await get_prediction(
            currency_data=CurrencyDataToPredict(
                buy_price=actual_currency_data.buy,
                created_at=actual_currency_data.created_at,
            )
        )
    except Exception:
        logger.exception(
            '[JOB][FORECAST SENDER] Failed to forecast currency buy price'
        )
        return

    for user in users_to_send_forecasts:
        await bot.send_message(
            chat_id=user.telegram.chat_id,
            text=currency_forecasted_by_subscription_message(
                user=user,
                sell_forecast=forecast_sell_price,
                currecy_data=actual_currency_data,
            ),
            parse_mode=ParseMode.HTML,
        )


async def run_sender() -> None:
    if datetime.datetime.now().hour in SLEEP_HOURS:
        return

    try:
        await sender()
    except Exception:
        logger.exception('[JOB][FORECAST SENDER] Failed to run sender')


if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    trigger = IntervalTrigger(hours=3)
    scheduler.add_job(run_sender, trigger=trigger)
    scheduler.start()
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
