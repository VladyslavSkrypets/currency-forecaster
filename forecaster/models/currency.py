import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    BigInteger,
    Numeric,
    DateTime,
)

from forecaster.models import Base


class Currency(Base):
    __tablename__ = 'currency'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, index=True, nullable=False)
    sell: Mapped[float] = mapped_column(Numeric(16, 2), nullable=False)
    buy: Mapped[float] = mapped_column(Numeric(16, 2), nullable=False)
