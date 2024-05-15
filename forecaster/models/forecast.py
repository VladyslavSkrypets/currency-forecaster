import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Boolean
)

from forecaster.models import Base


class ForecastSubscription(Base):
    __tablename__ = 'forecast_subscription'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('user.id'), index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    updated_at_utc: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.datetime.now(datetime.UTC).replace(tzinfo=None),
    )
    created_at_utc: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.datetime.now(datetime.UTC).replace(tzinfo=None),
    )
