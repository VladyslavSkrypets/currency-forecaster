import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    BigInteger,
    Numeric,
    DateTime,
    String,
)

from forecaster.models import Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    telegram_chat_id: Mapped[int] = mapped_column(BigInteger, index=True, nullable=False)
    telegram_username: Mapped[str] = mapped_column(String, nullable=False)
    telegram_first_name: Mapped[str | None]
    telegram_last_name: Mapped[str | None]
    telegram_language_code: Mapped[str | None] = mapped_column(String(2))
    created_at_utc: Mapped[datetime.datetime] = mapped_column(
        DateTime, 
        nullable=False, 
        default=datetime.datetime.now(datetime.UTC).replace(tzinfo=None)
    )
    updated_at_utc: Mapped[datetime.datetime] = mapped_column(
        DateTime, 
        nullable=False, 
        default=datetime.datetime.now(datetime.UTC).replace(tzinfo=None)
    )
