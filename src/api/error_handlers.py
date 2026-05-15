from fastapi import Request, status
from fastapi.responses import JSONResponse
from src.core.exceptions import BaseAppException

async def app_exception_handler(request: Request, exc: BaseAppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )
