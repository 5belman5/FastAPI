from src.infrastructure.repositories.base import BaseRepository
from src.infrastructure.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    async def get_by_username(self, username: str):
        result = await self.db.execute(select(User).filter(User.username == username))
        return result.scalars().first()
