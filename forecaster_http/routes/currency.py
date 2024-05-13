import datetime

from pydantic import BaseModel
from fastapi import APIRouter, Response
from starlette.status import HTTP_404_NOT_FOUND

from forecaster.bl.currency import get_actual_currency_data


router = APIRouter()


class ActualCurrecnyDataResponse(BaseModel):
    buy: float
    sell: float
    created_at: datetime.datetime


@router.get('/actual-currency')
async def get_actual_currency() -> ActualCurrecnyDataResponse:
    actual_currency_data = await get_actual_currency_data()
    if actual_currency_data is None:
        return Response(status_code=HTTP_404_NOT_FOUND)
    
    return ActualCurrecnyDataResponse(
        buy=actual_currency_data.buy,
        created_at=actual_currency_data.created_at,
        sell=actual_currency_data.sell,
    )
