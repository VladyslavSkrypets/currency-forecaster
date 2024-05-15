import decimal
import datetime

from pydantic import BaseModel
from fastapi import APIRouter

from forecaster.ml.model import get_prediction
from forecaster.schemas.currency import CurrencyDataToPredict


router = APIRouter()


class PredictCurrencyRequest(BaseModel):
    buy_price: decimal.Decimal
    current_datetime: datetime.datetime


class PredictCurrencyResponse(BaseModel):
    sell_price: decimal.Decimal
    predicted_at: datetime.datetime


@router.post('/predict')
async def get_actual_currency(
    data: PredictCurrencyRequest
) -> PredictCurrencyResponse:
    payload = CurrencyDataToPredict(
        buy_price=data.buy_price,
        created_at=data.current_datetime,
    ) if data is not None else None

    prediction = await get_prediction(currency_data=payload)

    return PredictCurrencyResponse(
        sell_price=round(prediction, 3),
        predicted_at=datetime.datetime.now(),
    )
