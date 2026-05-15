from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.infrastructure import models
from src.core.exceptions import NotFoundException, DomainException

class FollowUseCase:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_follows(self, user_id: int):
        query = select(models.Follow).filter(models.Follow.user_id == user_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def follow_user(self, user_id: int, following_username: str):
        query = select(models.User).filter(models.User.username == following_username)
        result = await self.db.execute(query)
        following_user = result.scalar_one_or_none()
        
        if not following_user:
            raise NotFoundException(f"Пользователь {following_username} не найден")
        
        if following_user.id == user_id:
            raise DomainException("Нельзя подписаться на самого себя")

        check_query = select(models.Follow).filter(
            models.Follow.user_id == user_id,
            models.Follow.following_id == following_user.id
        )
        check_result = await self.db.execute(check_query)
        if check_result.scalar_one_or_none():
            raise DomainException("Вы уже подписаны на этого пользователя")

        db_follow = models.Follow(user_id=user_id, following_id=following_user.id)
        self.db.add(db_follow)
        await self.db.commit()
        return {"message": "Успешная подписка"}
