from typing import TypeVar, Generic, Type, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from src.infrastructure.models import Base
from src.core.exceptions import InfrastructureException

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    """
    Базовый класс репозитория, реализующий стандартные асинхронные операции CRUD.
    """
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def get(self, id: int) -> Optional[ModelType]:
        """Получение одной записи по её ID."""
        try:
            result = await self.db.execute(select(self.model).filter(self.model.id == id))
            return result.scalars().first()
        except SQLAlchemyError as e:
            raise InfrastructureException(message=f"Ошибка при получении записи: {str(e)}")

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Получение списка всех записей с поддержкой пагинации."""
        try:
            result = await self.db.execute(select(self.model).offset(skip).limit(limit))
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise InfrastructureException(message=f"Ошибка при получении списка: {str(e)}")

    async def create(self, obj_in_data: dict) -> ModelType:
        """Создание новой записи."""
        try:
            db_obj = self.model(**obj_in_data)
            self.db.add(db_obj)
            await self.db.commit()
            await self.db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise InfrastructureException(message=f"Ошибка при создании записи: {str(e)}")

    async def update(self, db_obj: ModelType, obj_in_data: dict) -> ModelType:
        """Обновление существующей записи."""
        try:
            for field, value in obj_in_data.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)
            await self.db.commit()
            await self.db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise InfrastructureException(message=f"Ошибка при обновлении записи: {str(e)}")

    async def delete(self, id: int) -> bool:
        """Удаление записи по ID."""
        try:
            db_obj = await self.get(id)
            if db_obj:
                await self.db.delete(db_obj)
                await self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise InfrastructureException(message=f"Ошибка при удалении записи: {str(e)}")
