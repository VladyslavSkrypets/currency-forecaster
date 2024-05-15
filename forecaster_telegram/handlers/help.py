from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from forecaster_telegram.messages import help_command_message


router = Router(name=__name__)


@router.message(Command(commands=['help']))
async def command_help_handler(message: Message) -> None:
    await message.answer(
        text=help_command_message(),
    )
