import glob
import typing
import asyncio

import aiofiles
from aiocsv import AsyncDictReader
from sqlalchemy.dialects.postgresql import insert

from forecaster.services import db
from forecaster.utilities.logging import logger
from forecaster.models.currency import Currency
from forecaster.schemas.currency import CurrencyData


ROOT_DATA_DIRECTORY = 'data'

ALL_DATA_FILES = glob.glob(f'{ROOT_DATA_DIRECTORY}/*')


async def read_currency_data(file_path: str) -> typing.AsyncIterator[dict]:
    async with aiofiles.open(file_path, encoding='utf-8-sig') as file:
        async for row in AsyncDictReader(file):
            yield row


async def store_currency_data_to_database(
    data: typing.Sequence[CurrencyData],
) -> None:
    async with db.async_sessionmaker.begin() as db_session:    
        try:
            stmt = insert(Currency).values([
                {
                    'buy': data_item.buy,
                    'sell': data_item.sell,
                    'created_at': data_item.created_at,
                } for data_item in data
            ]).on_conflict_do_nothing()
            await db_session.execute(stmt)
        except Exception:
            await db_session.rollback()
            logger.exception(
                f'[DATA MIGRATION] Failed to save all currency data to database'
            )


async def process_currency_data(file_path: str) -> None:
    batch_to_proccess = []
    batch_max_size = 100
    async for row in read_currency_data(file_path):
        batch_to_proccess.append(CurrencyData.from_row(row))
        if len(batch_to_proccess) >= batch_max_size:
            await store_currency_data_to_database(batch_to_proccess)
            batch_to_proccess.clear()
    
    if batch_to_proccess:
        await store_currency_data_to_database(batch_to_proccess)
        

async def main():
    for file_path in ALL_DATA_FILES:
        logger.info(f"[DATA MIGRATION] START PROCESS {file_path.split('/')[-1]}")
        await process_currency_data(file_path)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception:
        logger.exception(
            '[DATA MIGRATION] Failed to run migration '
            'currency data to database'
        )
