import datetime

from sqlalchemy import select, update, desc, insert

from forecaster.services import db
from forecaster.schemas.user import User
from forecaster.utilities.logging import logger
from forecaster.schemas.forecast import ForecastSubscription
from forecaster.models.forecast import ForecastSubscription as ForecastSubscriptionORM


class ActiveForecastSubscriptionAlreasyExist(Exception):
    pass


class ActiveForecastSubscriptionNotExist(Exception):
    pass


async def get_forecast_subscription_by_user(
    user: User
) -> ForecastSubscription | None:
    async with db.async_sessionmaker.begin() as db_session:
        query_result = await db_session.execute(
            select(
                ForecastSubscriptionORM.id,
                ForecastSubscriptionORM.user_id,
                ForecastSubscriptionORM.is_active,
                ForecastSubscriptionORM.created_at_utc,
                ForecastSubscriptionORM.updated_at_utc,
            ).where(ForecastSubscriptionORM.user_id == user.id).order_by(
                desc(ForecastSubscriptionORM.id)
            )
        )
    
    forecast_subscription = query_result.mappings().first()

    if forecast_subscription is None:
        return None
    
    return ForecastSubscription.model_validate(forecast_subscription)


async def create_user_forecast_subscription(user: User) -> None:
    user_forecast_subscription = await get_forecast_subscription_by_user(user)

    if user_forecast_subscription and user_forecast_subscription.is_active:
        raise ActiveForecastSubscriptionAlreasyExist
    
    async with db.async_sessionmaker.begin() as db_session:
        try:
            await db_session.execute(
                insert(ForecastSubscriptionORM).values(
                    user_id=user.id,
                    is_active=True,
                )
            )
            await db_session.commit()
        except Exception:
            await db_session.rollback()
            logger.exception(
                '[BL][FORECAST] Failed to create forecast subscription '
                f'for user {user.id}'
            )
            raise
            

async def deactivate_user_forecast_subscription(user: User) -> None:
    user_forecast_subscription = await get_forecast_subscription_by_user(user)

    if user_forecast_subscription and not user_forecast_subscription.is_active:
        raise ActiveForecastSubscriptionNotExist

    async with db.async_sessionmaker.begin() as db_session:
        try:
            await db_session.execute(
                update(ForecastSubscriptionORM).values(
                    is_active=False,
                    updated_at_utc=datetime.datetime.now(datetime.UTC).replace(tzinfo=None),
                ).where(
                    ForecastSubscriptionORM.id == user_forecast_subscription.id
                )
            )
            await db_session.commit()
        except Exception:
            await db_session.rollback()
            logger.exception(
                '[BL][FORECAST] Failed to deactivate forecast subscription '
                f'for user {user.id}'
            )
            raise
