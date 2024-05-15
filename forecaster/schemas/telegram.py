from pydantic import BaseModel, Field


class TelegramUserData(BaseModel):
    chat_id: int
    username: str | None
    first_name: str | None
    last_name: str | None
    language_code: str | None = Field(max_length=2)
