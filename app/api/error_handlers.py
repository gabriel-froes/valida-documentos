from fastapi import Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.core.exceptions import (
    DocumentValidationError,
    LLMClientError,
    LLMJSONParseError,
    LLMResponseError,
    LLMTimeoutError,
    PDFExtractionError,
)
from app.core.logging import get_logger

logger = get_logger(__name__)


async def llm_timeout_error_handler(request: Request, exc: LLMTimeoutError) -> JSONResponse:
    logger.error(
        "LLM timeout in request",
        extra={"data": {"path": request.url.path, "error": str(exc)}},
    )
    return JSONResponse(
        status_code=status.HTTP_504_GATEWAY_TIMEOUT,
        content={
            "error": "LLM service timeout",
            "message": str(exc),
        },
    )


async def llm_client_error_handler(request: Request, exc: LLMClientError) -> JSONResponse:
    logger.error(
        "LLM client error in request",
        extra={"data": {"path": request.url.path, "error": str(exc)}},
    )
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={
            "error": "LLM service error",
            "message": str(exc),
        },
    )


async def llm_json_parse_error_handler(request: Request, exc: LLMJSONParseError) -> JSONResponse:
    logger.error(
        "LLM JSON parse error in request",
        extra={"data": {"path": request.url.path, "error": str(exc)}},
    )
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={
            "error": "LLM response parsing error",
            "message": str(exc),
        },
    )


async def llm_response_error_handler(request: Request, exc: LLMResponseError) -> JSONResponse:
    logger.error(
        "LLM response structure error in request",
        extra={"data": {"path": request.url.path, "error": str(exc)}},
    )
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={
            "error": "LLM response structure error",
            "message": str(exc),
        },
    )


async def pdf_extraction_error_handler(request: Request, exc: PDFExtractionError) -> JSONResponse:
    logger.error(
        "PDF extraction error in request",
        extra={"data": {"path": request.url.path, "error": str(exc)}},
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "PDF extraction failed",
            "message": str(exc),
        },
    )


async def validation_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
    logger.error(
        "Validation error in request",
        extra={
            "data": {
                "path": request.url.path,
                "errors": exc.errors(),
            },
        },
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation error",
            "message": "Dados inválidos recebidos. Por favor, verifique os documentos enviados e tente novamente.",
        },
    )


async def document_validation_error_handler(
    request: Request, exc: DocumentValidationError
) -> JSONResponse:
    logger.error(
        "Document validation error in request",
        extra={"data": {"path": request.url.path, "error": str(exc)}},
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Document validation error",
            "message": str(exc),
        },
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception(
        "Unexpected error in request",
        extra={"data": {"path": request.url.path, "error_type": type(exc).__name__, "error": str(exc)}},
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "message": "Ocorreu um erro inesperado. Tente novamente mais tarde.",
        },
    )

