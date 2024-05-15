from sqlalchemy import select, insert

from forecaster.services import db
from forecaster.utilities.logging import logger
from forecaster.models.user import User as UserORM
from forecaster.schemas.user import User as UserSchema


async def get_user_by_telegram_chat_id(chat_id: int) -> UserSchema:
    async with db.async_sessionmaker.begin() as db_session:
        try:
            query_result = await db_session.execute(
                select(
                    UserORM.id,
                    UserORM.telegram_chat_id,
                    UserORM.telegram_username,
                    UserORM.telegram_first_name,
                    UserORM.telegram_last_name,
                    UserORM.telegram_language_code,
                ).where(UserORM.telegram_chat_id == chat_id)
            )
            user = query_result.mappings().one_or_none()
        except Exception:
            logger.exception(
                f'[BL][USER] Failed to get user by chat id {chat_id}'
            )
            raise

    if user is None:
        return None

    return UserSchema.from_raw(user)


async def create_user(user_data: UserSchema) -> bool:
    async with db.async_sessionmaker.begin() as db_session:
        try:
            await db_session.execute(
                insert(UserORM).values(
                    telegram_chat_id=user_data.telegram.chat_id,
                    telegram_username=user_data.telegram.username,
                    telegram_first_name=user_data.telegram.first_name,
                    telegram_last_name=user_data.telegram.last_name,
                    telegram_language_code=user_data.telegram.language_code,
                )
            )
            await db_session.commit()
            return True
        except Exception:
            await db_session.rollback()
            logger.exception(
                '[BL][USER] Failed save user to database with '
                f'chat id {user_data.telegram.chat_id}'
            )
            return False
