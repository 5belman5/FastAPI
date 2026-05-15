from src.infrastructure.repositories.base import BaseRepository
from src.infrastructure.models import Group
from sqlalchemy.ext.asyncio import AsyncSession

class GroupRepository(BaseRepository[Group]):
    def __init__(self, db: AsyncSession):
        super().__init__(Group, db)
