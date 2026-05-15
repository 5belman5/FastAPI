from fastapi import APIRouter, Depends, status, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.infrastructure.database import get_db
from src.schemas import post as schemas
from src.api.dependencies import get_current_user
from src.infrastructure import models
from src.domain.use_cases.post_use_case import PostUseCase

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/", response_model=List[schemas.Post])
async def read_posts(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    use_case = PostUseCase(db)
    return await use_case.get_posts(skip=skip, limit=limit)

@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: schemas.PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    use_case = PostUseCase(db)
    return await use_case.create_post(post.model_dump(), current_user.id)

@router.get("/{post_id}", response_model=schemas.Post)
async def read_post(post_id: int, db: AsyncSession = Depends(get_db)):
    use_case = PostUseCase(db)
    return await use_case.get_post(post_id)

@router.put("/{post_id}", response_model=schemas.Post)
async def update_post(
    post_id: int,
    post: schemas.PostUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    use_case = PostUseCase(db)
    return await use_case.update_post(post_id, post.model_dump(exclude_unset=True), current_user.id)

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    use_case = PostUseCase(db)
    await use_case.delete_post(post_id, current_user.id)
    return None

@router.post("/{post_id}/image", response_model=schemas.Post)
async def upload_post_image(
    post_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    use_case = PostUseCase(db)
    return await use_case.upload_image(post_id, file, current_user.id)

@router.delete("/{post_id}/image", response_model=schemas.Post)
async def delete_post_image(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    use_case = PostUseCase(db)
    return await use_case.delete_image(post_id, current_user.id)
