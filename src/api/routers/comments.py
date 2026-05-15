from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.infrastructure.database import get_db
from src.schemas import comment as schemas
from src.api.dependencies import get_current_user
from src.infrastructure import models
from src.domain.use_cases.comment_use_case import CommentUseCase

router = APIRouter(prefix="/posts/{post_id}/comments", tags=["comments"])

@router.get("/", response_model=List[schemas.Comment])
async def read_comments(post_id: int, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    use_case = CommentUseCase(db)
    return await use_case.get_comments(post_id, skip=skip, limit=limit)

@router.post("/", response_model=schemas.Comment, status_code=status.HTTP_201_CREATED)
async def create_comment(
    post_id: int,
    comment: schemas.CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    use_case = CommentUseCase(db)
    return await use_case.create_comment(post_id, comment.model_dump(), current_user.id)
