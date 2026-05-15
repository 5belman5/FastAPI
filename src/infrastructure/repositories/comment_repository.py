from src.infrastructure.repositories.base import BaseRepository
from src.infrastructure.models import Comment
from sqlalchemy.ext.asyncio import AsyncSession

class CommentRepository(BaseRepository[Comment]):
    def __init__(self, db: AsyncSession):
        super().__init__(Comment, db)
