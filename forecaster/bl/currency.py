import io
import typing
import datetime
from itertools import groupby
from dateutil.relativedelta import relativedelta

import matplotlib.pyplot as plt
from sqlalchemy import select, Result

from forecaster.services import db
from forecaster.services import redis
from forecaster.utilities.logging import logger
from forecaster.const import CurrencyDymanicPeriod
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


async def get_currency_data_by_period(
    period: CurrencyDymanicPeriod
) -> typing.Sequence[CurrencyData]:
    current_datetime = datetime.datetime.today()
    if period == CurrencyDymanicPeriod.WEEK:
        after_date = current_datetime - relativedelta(weeks=1)
    elif period == CurrencyDymanicPeriod.MONTH:
        after_date = current_datetime - relativedelta(months=1)
    elif period == CurrencyDymanicPeriod.YEAR:
        after_date = current_datetime - relativedelta(years=1)
    elif period == CurrencyDymanicPeriod.LAST_5_YEARS:
        after_date = current_datetime - relativedelta(years=5)
    else:
        raise ValueError(f"Incorrect period value {period}")

    async with db.async_sessionmaker.begin() as db_session:
        query_result = await db_session.execute(
            select(
                Currency.buy,
                Currency.sell,
                Currency.created_at,
            ).where(Currency.created_at >= after_date)
        )
    
    currency_data = query_result.mappings().all()
    return [CurrencyData.model_validate(data) for data in currency_data]


def build_currency_by_period_graphic(
    period: CurrencyDymanicPeriod,
    data: typing.Sequence[CurrencyData],
) -> bytes:
    def currency_data_key(data_item: CurrencyData) -> datetime.date:
        return data_item.created_at.date()
    
    sorted_data = sorted(data, key=currency_data_key)
    grouped_data = [
        {
            "date": date,
            "group": list(data_group),
        } for date, data_group in groupby(sorted_data, key=currency_data_key)
    ]
    prepared_data = [
        {
            "sell": sum([item.sell for item in data["group"]]) / len(data["group"]),
            "buy": sum([item.buy for item in data["group"]]) / len(data["group"]),
            "date": data["date"],
        } for data in grouped_data
    ]
    dates = [data["date"] for data in prepared_data]
    sell_prices = [data["sell"] for data in prepared_data]
    buy_prices = [data["buy"] for data in prepared_data]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, sell_prices, label='Продаж', color='red')
    plt.plot(dates, buy_prices, label='Купівля', color='green')
    plt.title(f'Динаміка змін цін валюти UAH/USD за {period.value}')
    plt.xlabel('Дата')
    plt.ylabel('Ціна')
    plt.legend()
    plt.grid(True)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)

    return buffer.read()
    