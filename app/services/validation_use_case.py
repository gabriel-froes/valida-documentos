import asyncio

from fastapi import UploadFile

from app.api.v1.schemas import ValidationResultResponse
from app.core.logging import get_logger
from app.domain.models import (
    ArticlesOfAssociationData,
    CNPJCardData,
    TaxClearanceCertificateData,
)
from app.domain.document_validator import validate_documents_domain
from app.services.text_extractor import extract_text_from_pdf
from app.services.structured_extractor import (
    extract_articles_of_association_data,
    extract_cnpj_card_data,
    extract_tax_clearance_certificate_data,
)


logger = get_logger(__name__)


async def validate_supplier_documents_use_case(
    articles_of_association_file: UploadFile,
    cnpj_card_file: UploadFile,
    tax_clearance_certificate_file: UploadFile,
) -> ValidationResultResponse:
    logger.info("Starting document validation")
    
    logger.info("Starting PDF text extraction")
    articles_text, cnpj_card_text, certificate_text = await asyncio.gather(
        extract_text_from_pdf(articles_of_association_file),
        extract_text_from_pdf(cnpj_card_file),
        extract_text_from_pdf(tax_clearance_certificate_file),
    )
    logger.info("PDF text extraction completed")

    logger.info("Starting structured data extraction with LLM")
    articles_data, cnpj_card_data, certificate_data = await asyncio.gather(
        extract_articles_of_association_data(articles_text),
        extract_cnpj_card_data(cnpj_card_text),
        extract_tax_clearance_certificate_data(certificate_text),
    )
    logger.info("Structured data extraction completed")

    logger.info("Starting domain validation")
    result = await validate_documents_domain(
        articles=articles_data,
        cnpj_card=cnpj_card_data,
        certificate=certificate_data,
    )
    logger.info("Domain validation completed")

    total_inconsistencies = len(result.inconsistencies)
    critical_count = sum(1 for inc in result.inconsistencies if inc.severity == "CRITICA")
    warning_count = total_inconsistencies - critical_count
    
    inconsistency_summary = [
        {"field": inc.field, "severity": inc.severity}
        for inc in result.inconsistencies
    ]

    logger.info(
        "Document validation completed",
        extra={
            "data": {
                "status": result.status,
                "total_inconsistencies": total_inconsistencies,
                "critical_count": critical_count,
                "warning_count": warning_count,
                "inconsistencies": inconsistency_summary,
            },
        },
    )

    return result

