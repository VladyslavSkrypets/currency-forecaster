from aiogram import Router
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import Command

from forecaster.ml.model import get_prediction
from forecaster.utilities.logging import logger
from forecaster.schemas.currency import CurrencyDataToPredict
from forecaster.bl.currency import get_actual_currency_data
from forecaster.bl.user import get_user_by_telegram_chat_id
from forecaster.bl.forecast import (
    create_user_forecast_subscription,
    deactivate_user_forecast_subscription,
    ActiveForecastSubscriptionAlreasyExist,
    ActiveForecastSubscriptionNotExist,
)
from forecaster_telegram.messages import (
    error_occurred_message,
    forecast_command_message,
    forecast_subscribe_command_message,
    forecast_unsubscribe_command_message,
    forecast_command_actual_currency_data_not_exist_message,
    forecast_subscribe_command_subscription_already_exist_message,
    forecast_unsubscribe_command_active_subscription_not_exist_message,
)


router = Router(name=__name__)


@router.message(Command(commands=['forecast']))
async def command_forecast_handler(message: Message) -> None:
    try:
        actual_currency = await get_actual_currency_data()
    except Exception:
        logger.exception('[TELEGRAM][BOT] Failed to get actual currency')
        await message.answer(
            text=error_occurred_message(),
            parse_mode=ParseMode.HTML,
        )
        return
    
    if actual_currency is None:
        await message.answer(
            text=forecast_command_actual_currency_data_not_exist_message(),
            parse_mode=ParseMode.HTML,
        )
        return 

    try:
        forecast_sell_price = await get_prediction(
            currency_data=CurrencyDataToPredict(
                buy_price=actual_currency.buy,
                created_at=actual_currency.created_at,
            )
        )
    except Exception:
        logger.exception('[TELEGRAM][BOT] Failed to forecast buy price')
        await message.answer(
            text=error_occurred_message(),
            parse_mode=ParseMode.HTML,
        )
        return
    
    await message.answer(
        text=forecast_command_message(
            sell_forecast=forecast_sell_price,
            currecy_data=actual_currency,
        )
    )    


@router.message(Command(commands=['forecast_subscribe']))
async def command_forecast_subscribe_handler(message: Message) -> None:
    try:
        user = await get_user_by_telegram_chat_id(chat_id=message.chat.id)
    except Exception:
        await message.answer(
            text=error_occurred_message(),
            parse_mode=ParseMode.HTML,
        )
        return
    try:
        await create_user_forecast_subscription(user)
    except ActiveForecastSubscriptionAlreasyExist:
        await message.answer(
            text=forecast_subscribe_command_subscription_already_exist_message(),
            parse_mode=ParseMode.HTML,
        )
        return
    except Exception:
        await message.answer(
            text=error_occurred_message(),
            parse_mode=ParseMode.HTML,
        )
        return
    
    await message.answer(
        text=forecast_subscribe_command_message(),
        parse_mode=ParseMode.HTML,
    )


@router.message(Command(commands=['forecast_unsubscribe']))
async def command_forecast_unsubscribe_handler(message: Message) -> None:
    try:
        user = await get_user_by_telegram_chat_id(chat_id=message.chat.id)
    except Exception:
        await message.answer(
            text=error_occurred_message(),
            parse_mode=ParseMode.HTML,
        )
        return
    try:
        await deactivate_user_forecast_subscription(user)
    except ActiveForecastSubscriptionNotExist:
        await message.answer(
            text=forecast_unsubscribe_command_active_subscription_not_exist_message(),
            parse_mode=ParseMode.HTML,
        )
        return
    except Exception:
        await message.answer(
            text=error_occurred_message(),
            parse_mode=ParseMode.HTML,
        )
        return

    await message.answer(
        text=forecast_unsubscribe_command_message(),
        parse_mode=ParseMode.HTML,
    )
