from pydantic import BaseModel
from aiogram.types import Message

from forecaster.schemas.telegram import TelegramUserData


class User(BaseModel):
    id: int | None
    telegram: TelegramUserData

    @classmethod
    def from_raw(cls, data: dict) -> "User":
        return cls(
            id=data["id"],
            telegram=TelegramUserData(
                chat_id=data["telegram_chat_id"],
                username=data["telegram_username"],
                first_name=data["telegram_first_name"],
                last_name=data["telegram_last_name"],
                language_code=data["telegram_language_code"],
            )
        )
    
    @classmethod
    def from_message(cls, message: Message) -> "User":
        return cls(
            id=None,
            telegram=TelegramUserData(
                chat_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                language_code=message.from_user.language_code,
            )
        )
