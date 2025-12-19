from typing import Any, Dict

from pydantic import ValidationError

from app.core.exceptions import DocumentValidationError
from app.core.logging import get_logger
from app.domain.models import (
    ArticlesOfAssociationData,
    CNPJCardData,
    TaxClearanceCertificateData,
)
from app.services.llm_client import call_llm_and_parse
from app.services.prompts import build_prompt

logger = get_logger(__name__)


async def _extract_with_prompt(prompt_name: str, text: str) -> Dict[str, Any]:
    user_content = build_prompt(prompt_name, {"document_text": text})
    return await call_llm_and_parse(user_content)


def _handle_validation_error(
    document_type: str, validation_error: ValidationError, json_data: Dict[str, Any]
) -> None:
    logger.error(
        f"Validation error for {document_type}",
        extra={
            "data": {
                "document_type": document_type,
                "validation_errors": validation_error.errors(),
                "json_keys": list(json_data.keys()) if json_data else None,
            },
        },
    )
    raise DocumentValidationError(
        f"Failed to validate {document_type} data from LLM response. "
        f"Errors: {validation_error.errors()}"
    ) from validation_error


async def extract_articles_of_association_data(text: str) -> ArticlesOfAssociationData:
    json_data = await _extract_with_prompt("articles_of_association", text)
    try:
        return ArticlesOfAssociationData.model_validate(json_data)
    except ValidationError as exc:
        _handle_validation_error("articles_of_association", exc, json_data)


async def extract_cnpj_card_data(text: str) -> CNPJCardData:
    json_data = await _extract_with_prompt("cnpj_card", text)
    try:
        return CNPJCardData.model_validate(json_data)
    except ValidationError as exc:
        _handle_validation_error("cnpj_card", exc, json_data)


async def extract_tax_clearance_certificate_data(text: str) -> TaxClearanceCertificateData:
    json_data = await _extract_with_prompt("tax_clearance_certificate", text)
    try:
        return TaxClearanceCertificateData.model_validate(json_data)
    except ValidationError as exc:
        _handle_validation_error("tax_clearance_certificate", exc, json_data)

