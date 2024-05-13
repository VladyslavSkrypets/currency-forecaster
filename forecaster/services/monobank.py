import typing
import decimal
import datetime

import httpx
from pydantic import Field, field_validator

from forecaster.config import settings
from forecaster.utilities.logging import logger
from forecaster.schemas.currency import CurrencyData
from forecaster.const import (
    UAH_ISO_4217,
    USD_ISO_4217,
    RESPONSE_STATUS_CODE_TOO_MANY_REQUESTS,
)


CURRENCY_HTTP_TIMEOUT = 2 * 60  # 2 min


class CurrencyData(CurrencyData):
    sell: decimal.Decimal = Field(validation_alias="rateSell")
    buy: decimal.Decimal = Field(validation_alias="rateBuy")

    @field_validator('date', mode='before')
    def convert_date_from_timestamp_to_date(cls, value: int) -> datetime.date:
        return datetime.datetime.fromtimestamp(value)


class HTTPClient(httpx.AsyncClient):
    async def get(self, *, url: str, **kwargs) -> httpx.Response:
        return await super().get(url, **kwargs)


class MonoBankService:
    _instance: typing.Optional['MonoBankService'] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    @property
    def _client(self) -> HTTPClient:
        return HTTPClient(
            base_url=settings.mono_api_url,
            timeout=CURRENCY_HTTP_TIMEOUT,
        )
    
    async def get_actual_currency(self) -> CurrencyData | None:
        try:
            async with self._client as client:
                response = await client.get(
                    url='/bank/currency'
                )
            if response.status_code == RESPONSE_STATUS_CODE_TOO_MANY_REQUESTS:
                logger.error(
                    '[MONO] Failed to get actual currency data. '
                    'Too many requests'
                )
                return None
    
            response.raise_for_status()
            data = [
                raw_data for raw_data in response.json()
                if (
                    raw_data.get("currencyCodeA") == USD_ISO_4217 
                    and raw_data.get("currencyCodeB") == UAH_ISO_4217
                )
            ]
        except Exception:
            logger.exception('[MONO] Failed to get actual currency data')
            return None
    
        if data:
            return CurrencyData.model_validate(data[0])
        
        return None
