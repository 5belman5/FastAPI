from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.repositories.group_repository import GroupRepository
from src.core.exceptions import NotFoundException

class GroupUseCase:
    def __init__(self, db: AsyncSession):
        self.repo = GroupRepository(db)

    async def get_groups(self, skip: int = 0, limit: int = 100):
        return await self.repo.get_all(skip=skip, limit=limit)

    async def get_group(self, group_id: int):
        group = await self.repo.get(group_id)
        if not group:
            raise NotFoundException(f"Группа с id {group_id} не найдена")
        return group
