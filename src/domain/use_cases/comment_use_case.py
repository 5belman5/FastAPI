from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.infrastructure.repositories.comment_repository import CommentRepository
from src.infrastructure import models
from src.core.exceptions import NotFoundException, DomainException

class CommentUseCase:
    def __init__(self, db: AsyncSession):
        self.repo = CommentRepository(db)
        self.db = db

    async def get_comments(self, post_id: int, skip: int = 0, limit: int = 100):
        query = select(models.Comment).filter(models.Comment.post_id == post_id).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create_comment(self, post_id: int, comment_data: dict, author_id: int):
        # Проверка существования поста (можно через PostRepository, но для простоты здесь)
        post_query = select(models.Post).filter(models.Post.id == post_id)
        post_result = await self.db.execute(post_query)
        if not post_result.scalar_one_or_none():
            raise NotFoundException(f"Пост с id {post_id} не найден")
            
        return await self.repo.create(obj_in_data={
            **comment_data, 
            "author_id": author_id, 
            "post_id": post_id
        })
