from typing import List

from app.api.v1.schemas import ValidationResultResponse, ValidationStatus, Inconsistency
from app.domain.models import (
    ArticlesOfAssociationData,
    CNPJCardData,
    TaxClearanceCertificateData,
)
from app.domain.validators.cnpj import validate_cnpj_consistency
from app.domain.validators.company_name import validate_company_name_consistency
from app.domain.validators.legal_nature import validate_legal_nature_consistency
from app.domain.validators.expiration import validate_certificate_expiration
from app.domain.validators.address import validate_address_consistency
from app.domain.validators.tax_status import validate_tax_status
from app.domain.validators.partners import validate_partners_consistency
from app.domain.validators.business_purpose import validate_business_purpose_consistency


async def validate_documents_domain(
    articles: ArticlesOfAssociationData,
    cnpj_card: CNPJCardData,
    certificate: TaxClearanceCertificateData,
) -> ValidationResultResponse:
    inconsistencies: List[Inconsistency] = []

    inconsistencies.extend(
        validate_cnpj_consistency(cnpj_card, certificate)
    )
    inconsistencies.extend(
        validate_company_name_consistency(articles, cnpj_card, certificate)
    )
    inconsistencies.extend(
        validate_legal_nature_consistency(articles, cnpj_card, certificate)
    )
    inconsistencies.extend(
        validate_certificate_expiration(certificate)
    )
    inconsistencies.extend(
        validate_address_consistency(articles, cnpj_card)
    )
    inconsistencies.extend(
        validate_tax_status(cnpj_card)
    )
    inconsistencies.extend(
        validate_partners_consistency(articles, cnpj_card)
    )
    inconsistencies.extend(
        await validate_business_purpose_consistency(articles, cnpj_card)
    )

    has_critical_inconsistencies = any(
        inconsistency.severity == "CRITICA" for inconsistency in inconsistencies
    )
    status: ValidationStatus = "REPROVADO" if has_critical_inconsistencies else "APROVADO"

    return ValidationResultResponse(
        status=status,
        inconsistencies=inconsistencies,
    )

