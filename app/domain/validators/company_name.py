from typing import List

from app.api.v1.schemas import Inconsistency
from app.domain.models import (
    ArticlesOfAssociationData,
    CNPJCardData,
    TaxClearanceCertificateData,
)
from app.core.utils.normalization import normalize_text
from app.domain.validators.helpers import compare_documents


def validate_company_name_consistency(
    articles: ArticlesOfAssociationData,
    cnpj_card: CNPJCardData,
    certificate: TaxClearanceCertificateData,
) -> List[Inconsistency]:
    articles_company_name = normalize_text(articles.entity_info.company_name)
    card_company_name = normalize_text(cnpj_card.registration_info.company_name)
    cert_company_name = normalize_text(certificate.company_name)

    return compare_documents(
        field_name="razao_social",
        document_values={
            "contrato_social": articles_company_name,
            "cartao_cnpj": card_company_name,
            "certidao_negativa": cert_company_name,
        },
        message="Razão social divergente entre documentos.",
        severity="CRITICA",
    )


