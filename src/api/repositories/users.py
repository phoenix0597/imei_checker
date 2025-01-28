from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.core.logger import logger


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_tg_id(self, tg_id: int) -> User:
        query = select(User).where(User.tg_id == tg_id)
        logger.info(f"Executing query: {query} for tg_id: {tg_id}")
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self) -> list[User]:
        query = select(User)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def exists(self, tg_id: int) -> bool:
        user = await self.get_user_by_tg_id(tg_id)
        return user is not None
