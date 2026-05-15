from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.infrastructure.database import get_db
from src.schemas import group as schemas
from src.domain.use_cases.group_use_case import GroupUseCase

router = APIRouter(prefix="/groups", tags=["groups"])

@router.get("/", response_model=List[schemas.Group])
async def read_groups(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    use_case = GroupUseCase(db)
    return await use_case.get_groups(skip=skip, limit=limit)

@router.get("/{group_id}", response_model=schemas.Group)
async def read_group(group_id: int, db: AsyncSession = Depends(get_db)):
    use_case = GroupUseCase(db)
    return await use_case.get_group(group_id)
