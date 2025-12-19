from fastapi import FastAPI
from pydantic import ValidationError

from app.api.error_handlers import (
    document_validation_error_handler,
    generic_exception_handler,
    invalid_file_type_error_handler,
    llm_client_error_handler,
    llm_json_parse_error_handler,
    llm_response_error_handler,
    llm_timeout_error_handler,
    pdf_extraction_error_handler,
    validation_error_handler,
)
from app.api.v1.routers.validation import router as validation_router
from app.core.exceptions import (
    DocumentValidationError,
    InvalidFileTypeError,
    LLMClientError,
    LLMJSONParseError,
    LLMResponseError,
    LLMTimeoutError,
    PDFExtractionError,
)
from app.core.logging import setup_logging

setup_logging()
app = FastAPI(title='Validador de Contratos', version='1.0.0')

# Register exception handlers (order matters - most specific first)
app.add_exception_handler(LLMTimeoutError, llm_timeout_error_handler)
app.add_exception_handler(LLMJSONParseError, llm_json_parse_error_handler)
app.add_exception_handler(LLMResponseError, llm_response_error_handler)
app.add_exception_handler(LLMClientError, llm_client_error_handler)
app.add_exception_handler(InvalidFileTypeError, invalid_file_type_error_handler)
app.add_exception_handler(PDFExtractionError, pdf_extraction_error_handler)
app.add_exception_handler(DocumentValidationError, document_validation_error_handler)
app.add_exception_handler(ValidationError, validation_error_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(validation_router, prefix='/api/v1')

@app.get('/health', tags=['health'])
def health() -> dict[str, str]:
    return {'status': 'ok'}