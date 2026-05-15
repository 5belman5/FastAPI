from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.api.routers import posts, auth, groups, comments, follows
from src.core.exceptions import BaseAppException
from src.api.error_handlers import app_exception_handler
from src.core.logging_config import logger
import time
import os

# Создаем экземпляр приложения FastAPI
app = FastAPI(title="Yatube API на FastAPI")

# Создаем папку для медиафайлов, если её нет
if not os.path.exists("media"):
    os.makedirs("media")

# Монтируем папку media для раздачи статических файлов (картинок)
app.mount("/media", StaticFiles(directory="media"), name="media")

# Регистрация глобального обработчика исключений
app.add_exception_handler(BaseAppException, app_exception_handler)

# Middleware для логирования времени выполнения запросов
@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.2f}ms")
    return response

@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в Yatube API на FastAPI"}

# Подключение роутеров для различных сущностей
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(groups.router)
app.include_router(comments.router)
app.include_router(follows.router)
