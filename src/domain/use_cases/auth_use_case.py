from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.repositories.user_repository import UserRepository
from src.core import security
from src.core.exceptions import BaseAppException

class AuthUseCase:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def login(self, username, password):
        user = await self.repo.get_by_username(username)
        if not user or not security.verify_password(password, user.password):
            # Используем кастомное исключение с кодом 401
            raise BaseAppException("Неверное имя пользователя или пароль", status_code=401)
        
        access_token = security.create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}
