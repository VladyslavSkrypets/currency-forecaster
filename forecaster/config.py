import datetime

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = True
    app_name: str = 'Currency Forecaster 💲🚀'

    redis_host: str | None = None
    redis_port: int | None = None
    redis_database: int | None = None

    async_db_url: str | None = None
    db_url: str | None = None
    db_max_connections: int | None = None

    telegram_api_key: str | None = None

    mono_api_url: str | None = None

    @property
    def app_version(self) -> str:
        version_date = (
            datetime.datetime.now(datetime.UTC)
            .strftime("%Y.%m.%d.%H.%M")
        )
        return f'v{version_date}'



settings = Settings()
