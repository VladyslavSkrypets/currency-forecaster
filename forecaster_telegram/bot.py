from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from forecaster.config import settings
from forecaster_telegram.handlers import help
from forecaster_telegram.handlers import start
from forecaster_telegram.handlers import currency
from forecaster_telegram.handlers import forecast


dp = Dispatcher()

dp.include_routers(
    start.router,
    help.router,
    currency.router,
    forecast.router,
)


def create_bot() -> Bot:
    bot = Bot(
        token=settings.telegram_api_key,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    return bot
