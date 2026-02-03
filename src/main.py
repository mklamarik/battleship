import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from api.v1.routes import router as v1_router
from core.exceptions import DuplicateShotError, InvalidStateError, OutOfBoundsError, PlacementError
from core.logging import setup_logging
from core.settings import settings

app = FastAPI(title=settings.app_name)
app.include_router(v1_router, prefix="/api/v1")

setup_logging()
logger = logging.getLogger("battleships")


@app.exception_handler(OutOfBoundsError)
async def out_of_bounds_error_exception_handler(request: Request, exc: OutOfBoundsError):
    logger.warning(f"Validation Error (422): {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": str(exc)},
    )


@app.exception_handler(DuplicateShotError)
async def duplicate_shot_error_exception_handler(request: Request, exc: DuplicateShotError):
    logger.warning(f"Conflict Error (409): {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc)},
    )


@app.exception_handler(InvalidStateError)
async def invalid_state_error_exception_handler(request: Request, exc: InvalidStateError):
    logger.warning(f"State Error (400): {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


@app.exception_handler(KeyError)
async def key_error_exception_handler(request: Request, exc: KeyError):
    logger.warning(f"Resource Not Found (404): {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "The requested game session does not exist."},
    )


@app.exception_handler(PlacementError)
async def placement_error_exception_handler(request: Request, exc: PlacementError):
    logger.error(f"Logic Failure: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "detail": "Failed to generate a valid ship layout, probably due to how the placement is implemented. Please try again."
        },
    )


@app.exception_handler(Exception)
async def universal_exception_handler(request: Request, exc: Exception):
    logger.error(f"UNHANDLED RUNTIME ERROR: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal error occurred which shouldn't have."},
    )
