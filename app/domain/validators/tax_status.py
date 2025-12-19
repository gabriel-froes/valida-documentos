from typing import List

from app.api.v1.schemas import Inconsistency
from app.domain.models import CNPJCardData


def validate_tax_status(cnpj_card: CNPJCardData) -> List[Inconsistency]:
    inconsistencies: List[Inconsistency] = []

    status = cnpj_card.tax_status.status.upper().strip()

    if status != "ATIVA":
        inconsistencies.append(
            Inconsistency(
                field="situacao_cadastral",
                message=f"Situação cadastral do CNPJ não está ativa.",
                severity="CRITICA",
                values={
                    "situacao_atual": cnpj_card.tax_status.status,
                    "situacao_esperada": "ATIVA",
                },
            )
        )

    return inconsistencies

