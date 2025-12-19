class PDFExtractionError(Exception):
    """Raised when PDF text extraction fails."""
    pass


class LLMClientError(Exception):
    """Raised when an error occurs while interacting with the LLM client."""
    pass


class LLMTimeoutError(LLMClientError):
    """Raised when LLM request times out."""
    pass


class LLMJSONParseError(LLMClientError):
    """Raised when LLM response cannot be parsed as JSON."""
    pass


class LLMResponseError(LLMClientError):
    """Raised when LLM response has unexpected structure."""
    pass


class DocumentValidationError(Exception):
    """Raised when document validation fails."""
    pass