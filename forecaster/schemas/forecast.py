import datetime

from pydantic import BaseModel


class ForecastSubscription(BaseModel):
    id: int
    user_id: int
    is_active: bool
    updated_at_utc: datetime.datetime
    created_at_utc: datetime.datetime
