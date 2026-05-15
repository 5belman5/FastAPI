from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database import get_db
from src.api.dependencies import get_current_user
from src.infrastructure import models
from src.domain.use_cases.follow_use_case import FollowUseCase

router = APIRouter(prefix="/follow", tags=["follow"])

@router.get("/")
async def read_follows(db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    use_case = FollowUseCase(db)
    return await use_case.get_follows(current_user.id)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def follow_user(
    following_username: str,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    use_case = FollowUseCase(db)
    return await use_case.follow_user(current_user.id, following_username)
