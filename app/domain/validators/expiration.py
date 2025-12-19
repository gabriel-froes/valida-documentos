from datetime import date
from typing import List

from app.api.v1.schemas import Inconsistency
from app.domain.models import TaxClearanceCertificateData


def validate_certificate_expiration(
    certificate: TaxClearanceCertificateData,
) -> List[Inconsistency]:
    inconsistencies: List[Inconsistency] = []

    today = date.today()

    if certificate.expiration_date < today:
        formatted_date = certificate.expiration_date.strftime("%d/%m/%Y")
        inconsistencies.append(
            Inconsistency(
                field="data_validade",
                message=f"Certidão negativa vencida.",
                severity="CRITICA",
                values={
                    "data_validade": formatted_date,
                    "data_atual": today.strftime("%d/%m/%Y"),
                },
            )
        )

    return inconsistencies



