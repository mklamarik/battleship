from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from api.v1.routes import router as v1_router
from core.settings import settings

app = FastAPI(title=settings.app_name)
app.include_router(v1_router, prefix="/api/v1")


@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


@app.exception_handler(KeyError)
async def key_error_exception_handler(request: Request, exc: KeyError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Resource not found"},
    )
