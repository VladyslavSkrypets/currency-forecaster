import json
import hashlib
import decimal
import datetime

from pydantic import BaseModel


class CurrencyData(BaseModel):
    sell: decimal.Decimal
    buy: decimal.Decimal
    created_at: datetime.datetime

    @classmethod
    def from_row(cls, row: dict) -> "CurrencyData":
        return cls(
            sell=row['Low'],
            buy=row['High'],
            created_at=datetime.datetime.strptime(
                row['Date'],
                '%m/%d/%Y',
            )
        )


class CurrencyDataToPredict(BaseModel):
    value: decimal.Decimal
    created_at: datetime.datetime

    def __hash__(self) -> int:
        json_str = json.dumps(self.model_dump(mode="json"), sort_keys=True)

        hash_object = hashlib.sha256(json_str.encode())

        return int(hash_object.hexdigest(), 16)
