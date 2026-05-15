from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.core.config import get_settings

settings = get_settings()

# Создаем асинхронный движок базы данных
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
)

# Фабрика асинхронных сессий
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    """Зависимость для получения асинхронной сессии БД в эндпоинтах"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
