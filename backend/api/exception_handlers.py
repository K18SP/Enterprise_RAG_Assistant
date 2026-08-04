from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from exceptions.base_exception import BaseCustomException

from schemas.api_error import APIError, ErrorDetail

from utils.logger import setup_logger

from exceptions.document_not_found_exception import DocumentNotFoundError

logger = setup_logger(__name__)


def register_exception_handlers(app: FastAPI):

    # Handling custom exceptions
    @app.exception_handler(BaseCustomException)
    async def custom_exception_handler(
        request: Request,
        exc: BaseCustomException
    ):

        logger.error(f"{exc.__class__.__name__}: {exc}")

        response = APIError(
            error=ErrorDetail(
                type=exc.__class__.__name__,
                message=str(exc)
            )
        )

        return JSONResponse(
            status_code=500,
            content=response.model_dump() #returns the object into a standard python dictionary
        )

    # Handling Global exception
    @app.exception_handler(Exception)
    async def unexpected_exception_handler(
        request: Request,
        exc: Exception
    ):

        logger.exception("Unexpected Exception")

        response = APIError(
            error=ErrorDetail(
                type="InternalServerError",
                message="An unexpected error occurred."
            )
        )

        return JSONResponse(
            status_code=500,
            content=response.model_dump()
        )

    #HandlingDocumentNotFoundException
    @app.exception_handler(DocumentNotFoundError)
    async def document_not_found_handler(
        request: Request,
        exc: DocumentNotFoundError
    ):

        logger.warning(
            f"DocumentNotFoundError: {exc}"
        )

        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "error": {
                    "type": "DOCUMENT_NOT_FOUND",
                    "message": str(exc)
                }
            }
        )