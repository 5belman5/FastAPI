from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database import get_db
from src.domain.use_cases.auth_use_case import AuthUseCase

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    use_case = AuthUseCase(db)
    return await use_case.login(form_data.username, form_data.password)
