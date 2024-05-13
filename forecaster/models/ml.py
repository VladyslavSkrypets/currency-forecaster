import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import (
    BigInteger,
    Numeric,
    DateTime,
    BLOB,
)

from forecaster.models import Base


class TrainedModel(Base):
    __tablename__ = 'trained_model'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    model: Mapped[bytes] = mapped_column(BLOB, nullable=False)
    mse: Mapped[float] =  mapped_column(Numeric(16, 2), nullable=False)
    training_params: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, 
        default=datetime.datetime.today(),
    )