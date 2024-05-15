from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import CommandStart

from forecaster.schemas.user import User
from forecaster_telegram.messages import (
    start_command_message,
    error_occurred_message,
)
from forecaster.bl.user import (
    get_user_by_telegram_chat_id,
    create_user,
)


router = Router(name=__name__)


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    try:
        user = await get_user_by_telegram_chat_id(
            chat_id=message.from_user.id,
        )
    except Exception:
        await message.answer(
            text=error_occurred_message(),
            parse_mode=ParseMode.HTML,
        )
        return

    if user is not None:
        await message.answer(
            text=start_command_message(user),
            parse_mode=ParseMode.HTML,
        )
        return
    
    user_data = User.from_message(message)
    user_created = await create_user(user_data)
    if not user_created:
        await message.answer(
            text=error_occurred_message(),
            parse_mode=ParseMode.HTML,
        )
        return

    await message.answer(
        text=start_command_message(user_data),
        parse_mode=ParseMode.HTML,
    )

    
    
