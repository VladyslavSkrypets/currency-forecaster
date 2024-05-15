import datetime

from aiogram import F
from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types.input_file import BufferedInputFile
from aiogram.types import Message, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from forecaster.utilities.logging import logger
from forecaster.const import CurrencyDymanicPeriod
from forecaster.bl.currency import (
    get_actual_currency_data,
    get_currency_data_by_period,
    build_currency_by_period_graphic,
)
from forecaster_telegram.messages import (
    error_occurred_message,
    actual_currency_data_not_exist_message,
    actual_currency_command_message,
    currency_data_by_period_caption,
)


router = Router(name=__name__)


@router.message(Command(commands=['actual_currency']))
async def command_actual_currency_handler(message: Message) -> None:
    try:
        actual_currency = await get_actual_currency_data()
    except Exception:
        await message.answer(
            text=error_occurred_message(),
            parse_mode=ParseMode.HTML,
        )
        return
    if actual_currency is None:
        await message.answer(
            text=actual_currency_data_not_exist_message(),
            parse_mode=ParseMode.HTML,
        )
        return
    
    await message.answer(
        text=actual_currency_command_message(actual_currency),
        parse_mode=ParseMode.HTML,
    )


@router.message(Command(commands=['currency_dynamics']))
async def command_actual_currency_handler(message: Message) -> None:
    buttons_builder = ReplyKeyboardBuilder()

    for period in CurrencyDymanicPeriod:
        buttons_builder.add(KeyboardButton(text=period.value))

    buttons_builder.adjust(1)
    await message.answer(
        "Обери за який період ти хочеш отримати інфорграфіку 📈", 
        reply_markup=buttons_builder.as_markup(one_time_keyboard=True)
    )


@router.message(F.text.in_([period.value for period in CurrencyDymanicPeriod]))
async def command_actual_currency_period_handler(message: Message) -> None:
    period = CurrencyDymanicPeriod(message.text)
    try:
        data = await get_currency_data_by_period(period)
        graphic_data = build_currency_by_period_graphic(
            data=data,
            period=period,
        )
    except Exception:
        logger.exception(
            "[TELEGRAM][BOT] Failed to create currency dynamic changes"
        )
        await message.answer(
            text=error_occurred_message(),
            parse_mode=ParseMode.HTML,
        )

    graphic = BufferedInputFile(
        graphic_data, 
        filename=f"{datetime.datetime.today()}_currency_data_by_period.png"
    )
    await message.answer_photo(
        photo=graphic,
        caption=currency_data_by_period_caption(period),
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.HTML,
    )
