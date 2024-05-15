import asyncio

from forecaster_telegram.bot import create_bot, dp
from forecaster.utilities.logging import logger


async def main() -> None:
    logger.info('[TELEGRAM][BOT] Starting telegram bot')
    bot = create_bot()
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception:
        logger.exception('[TELEGRAM][BOT] Failed to start bot')
