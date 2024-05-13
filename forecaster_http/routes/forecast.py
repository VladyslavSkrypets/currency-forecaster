import decimal
import datetime

from pydantic import BaseModel
from fastapi import APIRouter

from forecaster.ml.model import get_prediction
from forecaster.schemas.currency import CurrencyDataToPredict


router = APIRouter()


class BasePredictionData(BaseModel):
    value: decimal.Decimal


class PredictCurrencyRequest(BasePredictionData):
    current_datetime: datetime.datetime


class PredictCurrencyResponse(BasePredictionData):
    predicted_at: datetime.datetime


@router.post('/predict')
async def get_actual_currency(
    data: PredictCurrencyRequest
) -> PredictCurrencyResponse:
    payload = CurrencyDataToPredict(
        value=data.value,
        created_at=data.current_datetime,
    ) if data is not None else None

    prediction = await get_prediction(currency_data=payload)

    return PredictCurrencyResponse(
        value=round(prediction, 3),
        predicted_at=datetime.datetime.now(),
    )
