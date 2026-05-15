from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.repositories.post_repository import PostRepository
from src.core.exceptions import NotFoundException, DomainException
from src.infrastructure import models
import os
import uuid
import aiofiles

class PostUseCase:
    def __init__(self, db: AsyncSession):
        self.repo = PostRepository(db)
        self.db = db

    async def get_posts(self, skip: int = 0, limit: int = 100):
        return await self.repo.get_all(skip=skip, limit=limit)

    async def get_post(self, post_id: int):
        post = await self.repo.get(post_id)
        if not post:
            raise NotFoundException(f"Пост с id {post_id} не найден")
        return post

    async def create_post(self, post_data: dict, author_id: int):
        return await self.repo.create(obj_in_data={**post_data, "author_id": author_id})

    async def update_post(self, post_id: int, post_data: dict, user_id: int):
        post = await self.get_post(post_id)
        if post.author_id != user_id:
            raise DomainException("Вы не являетесь автором этого поста")
        return await self.repo.update(post, obj_in_data=post_data)

    async def delete_post(self, post_id: int, user_id: int):
        post = await self.get_post(post_id)
        if post.author_id != user_id:
            raise DomainException("Вы не являетесь автором этого поста")
        
        if post.image:
            image_path = f"media/{post.image}"
            if os.path.exists(image_path):
                os.remove(image_path)
        
        return await self.repo.delete(post_id)

    async def upload_image(self, post_id: int, file, user_id: int):
        post = await self.get_post(post_id)
        if post.author_id != user_id:
            raise DomainException("Вы не являетесь автором этого поста")

        filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = f"media/{filename}"

        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)

        return await self.repo.update(post, obj_in_data={"image": filename})

    async def delete_image(self, post_id: int, user_id: int):
        post = await self.get_post(post_id)
        if post.author_id != user_id:
            raise DomainException("Вы не являетесь автором этого поста")

        if post.image:
            image_path = f"media/{post.image}"
            if os.path.exists(image_path):
                os.remove(image_path)
            return await self.repo.update(post, obj_in_data={"image": None})
        return post
