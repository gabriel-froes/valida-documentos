from typing import List

from app.api.v1.schemas import Inconsistency
from app.domain.models import (
    ArticlesOfAssociationData,
    CNPJCardData,
    TaxClearanceCertificateData,
)
from app.core.utils.normalization import normalize_text
from app.domain.validators.helpers import compare_documents


def validate_legal_nature_consistency(
    articles: ArticlesOfAssociationData,
    cnpj_card: CNPJCardData,
    certificate: TaxClearanceCertificateData,
) -> List[Inconsistency]:
    articles_legal_nature = normalize_text(articles.entity_info.legal_nature)
    card_legal_nature = normalize_text(cnpj_card.registration_info.legal_nature)
    cert_legal_nature = normalize_text(certificate.legal_nature)

    return compare_documents(
        field_name="natureza_juridica",
        document_values={
            "contrato_social": articles_legal_nature,
            "cartao_cnpj": card_legal_nature,
            "certidao_negativa": cert_legal_nature,
        },
        message="Natureza jurídica divergente entre documentos.",
        severity="CRITICA",
    )

