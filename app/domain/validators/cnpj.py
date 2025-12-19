from typing import List

from app.api.v1.schemas import Inconsistency
from app.domain.models import (
    CNPJCardData,
    TaxClearanceCertificateData,
)
from app.core.utils.normalization import only_digits
from app.domain.validators.helpers import compare_documents


def validate_cnpj_consistency(
    cnpj_card: CNPJCardData,
    certificate: TaxClearanceCertificateData,
) -> List[Inconsistency]:
    card_cnpj = only_digits(cnpj_card.registration_info.tax_id)
    cert_cnpj = only_digits(certificate.tax_id)

    return compare_documents(
        field_name="cnpj",
        document_values={
            "cartao_cnpj": card_cnpj,
            "certidao_negativa": cert_cnpj,
        },
        message="CNPJ divergente entre documentos.",
        severity="CRITICA",
    )


