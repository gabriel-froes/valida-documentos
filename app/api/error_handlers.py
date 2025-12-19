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
    """Handle LLM timeout errors."""
    logger.error(
        "LLM timeout in request",
        extra={"data": {"path": request.url.path, "error": str(exc)}},
    )
    return JSONResponse(
        status_code=status.HTTP_504_GATEWAY_TIMEOUT,
        content={
            "error": "LLM service timeout",
            "message": "O serviço de IA demorou muito para responder. Tente novamente.",
            "detail": str(exc),
        },
    )


async def llm_client_error_handler(request: Request, exc: LLMClientError) -> JSONResponse:
    """Handle LLM client errors."""
    logger.error(
        "LLM client error in request",
        extra={"data": {"path": request.url.path, "error": str(exc)}},
    )
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={
            "error": "LLM service error",
            "message": "Erro ao comunicar com o serviço de IA. Tente novamente mais tarde.",
            "detail": str(exc),
        },
    )


async def llm_json_parse_error_handler(request: Request, exc: LLMJSONParseError) -> JSONResponse:
    """Handle LLM JSON parsing errors."""
    logger.error(
        "LLM JSON parse error in request",
        extra={"data": {"path": request.url.path, "error": str(exc)}},
    )
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={
            "error": "LLM response parsing error",
            "message": "Erro ao processar resposta do serviço de IA. Tente novamente.",
            "detail": str(exc),
        },
    )


async def llm_response_error_handler(request: Request, exc: LLMResponseError) -> JSONResponse:
    """Handle LLM response structure errors."""
    logger.error(
        "LLM response structure error in request",
        extra={"data": {"path": request.url.path, "error": str(exc)}},
    )
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={
            "error": "LLM response structure error",
            "message": "Resposta inválida do serviço de IA. Tente novamente.",
            "detail": str(exc),
        },
    )


async def pdf_extraction_error_handler(request: Request, exc: PDFExtractionError) -> JSONResponse:
    """Handle PDF extraction errors."""
    logger.error(
        "PDF extraction error in request",
        extra={"data": {"path": request.url.path, "error": str(exc)}},
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "PDF extraction failed",
            "message": "Não foi possível extrair texto do PDF. Verifique se o arquivo está válido.",
            "detail": str(exc),
        },
    )


async def validation_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """Handle Pydantic validation errors."""
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
            "message": "Dados inválidos recebidos do serviço de IA.",
            "detail": exc.errors(),
        },
    )


async def document_validation_error_handler(
    request: Request, exc: DocumentValidationError
) -> JSONResponse:
    """Handle document validation errors."""
    logger.error(
        "Document validation error in request",
        extra={"data": {"path": request.url.path, "error": str(exc)}},
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Document validation error",
            "message": "Erro ao validar documentos.",
            "detail": str(exc),
        },
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions."""
    logger.exception(
        "Unexpected error in request",
        extra={"data": {"path": request.url.path, "error_type": type(exc).__name__}},
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "message": "Ocorreu um erro inesperado. Tente novamente mais tarde.",
            "detail": "An unexpected error occurred",
        },
    )

