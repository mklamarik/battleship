import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from api.v1.routes import router as v1_router
from core.exceptions import DuplicateShotError, InvalidStateError, OutOfBoundsError, PlacementError
from core.settings import settings

app = FastAPI(title=settings.app_name)
app.include_router(v1_router, prefix="/api/v1")


logger = logging.getLogger("battleships")


# Inspired by https://fastapi.tiangolo.com/tutorial/handling-errors/#install-custom-exception-handlers
# Bypassess need for try except blocks
@app.exception_handler(OutOfBoundsError)
async def out_of_bounds_error_exception_handler(request: Request, exc: OutOfBoundsError):
    logger.error(f"OUT OF BOUNDS ERROR: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": str(exc)},
    )


@app.exception_handler(DuplicateShotError)
async def duplicate_shot_error_exception_handler(request: Request, exc: DuplicateShotError):
    logger.error(f"DUPLICATE SHOT ERROR: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": str(exc)},
    )


@app.exception_handler(InvalidStateError)
async def invalid_state_error_exception_handler(request: Request, exc: InvalidStateError):
    logger.error(f"INVALID STATE ERROR: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


@app.exception_handler(KeyError)
async def key_error_exception_handler(request: Request, exc: KeyError):
    logger.error(f"KEY ERROR: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Resource not found"},
    )


@app.exception_handler(PlacementError)
async def placement_error_exception_handler(request: Request, exc: PlacementError):
    logger.error(f"PLACEMENT ERROR: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_SERVICE_UNAVAILABLE,
        content={
            "detail": "Server was unable to process the ship placement on the board because of how it is implemented."
        },
    )


@app.exception_handler(Exception)
async def universal_exception_handler(request: Request, exc: Exception):
    logger.error(f"FATAL ERROR: {str(exc)}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "The radar system has malfunctioned. Engineers have been notified.",
        },
    )
