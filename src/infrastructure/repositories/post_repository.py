from src.infrastructure.repositories.base import BaseRepository
from src.infrastructure.models import Post
from sqlalchemy.ext.asyncio import AsyncSession

class PostRepository(BaseRepository[Post]):
    def __init__(self, db: AsyncSession):
        super().__init__(Post, db)
