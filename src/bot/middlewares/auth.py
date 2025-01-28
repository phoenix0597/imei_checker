from typing import Any, Callable, Awaitable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.repositories.users import UserRepository
from src.core.database import get_session


class AuthMiddleware(BaseMiddleware):
    def __init__(self):
        self.user_repository = UserRepository(session=get_session())

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        session: AsyncSession = data["session"]
        user_repo = UserRepository(session=session)

        if not await user_repo.exists(event.from_user.id):
            await event.answer(
                "Извините, вы не имеете доступа к этому боту.\n"
                "Пожалуйста, обратитесь к администратору."
            )
            return

        return await handler(event, data)
