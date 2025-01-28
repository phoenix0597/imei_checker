from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.database import get_session
from src.bot.middlewares.auth import AuthMiddleware
from src.bot.handlers import imei
from src.core.logger import logger


async def create_bot() -> Bot:
    return Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )


async def create_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    dp.message.middleware(AuthMiddleware())

    dp.include_router(imei.router)

    return dp


async def main() -> None:
    bot = await create_bot()
    dp = await create_dispatcher()
    try:
        async with get_session() as session:
            await dp.start_polling(bot, session=session)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

    logger.info("Bot stopped")
