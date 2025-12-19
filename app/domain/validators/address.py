from typing import List

from app.api.v1.schemas import Inconsistency
from app.domain.models import ArticlesOfAssociationData, CNPJCardData
from app.core.utils.normalization import normalize_text, only_digits
from app.domain.validators.helpers import compare_documents


def validate_address_consistency(
    articles: ArticlesOfAssociationData,
    cnpj_card: CNPJCardData,
) -> List[Inconsistency]:
    inconsistencies: List[Inconsistency] = []

    articles_address = articles.head_office
    card_address = cnpj_card.address

    articles_normalized = {
        "cep": only_digits(articles_address.postal_code),
        "cidade": normalize_text(articles_address.city),
        "estado": normalize_text(articles_address.state),
        "bairro": normalize_text(articles_address.district),
        "numero": normalize_text(articles_address.number),
        "complemento": normalize_text(articles_address.complement),
        "logradouro": normalize_text(articles_address.street),
    }

    card_normalized = {
        "cep": only_digits(card_address.postal_code),
        "cidade": normalize_text(card_address.city),
        "estado": normalize_text(card_address.state),
        "bairro": normalize_text(card_address.district),
        "numero": normalize_text(card_address.number),
        "complemento": normalize_text(card_address.complement),
        "logradouro": normalize_text(card_address.street),
    }

    address_fields = [
        ("cep", "CEP divergente entre documentos.", "CRITICA"),
        ("cidade", "Cidade divergente entre documentos.", "CRITICA"),
        ("estado", "Estado divergente entre documentos.", "CRITICA"),
        ("bairro", "Bairro divergente entre documentos.", "CRITICA"),
        ("numero", "Número divergente entre documentos.", "CRITICA"),
        ("complemento", "Complemento divergente entre documentos.", "AVISO"),
        ("logradouro", "Logradouro divergente entre documentos.", "AVISO"),
    ]

    for field_name, message, severity in address_fields:
        inconsistencies.extend(
            compare_documents(
                field_name=field_name,
                document_values={
                    "contrato_social": articles_normalized[field_name],
                    "cartao_cnpj": card_normalized[field_name],
                },
                message=message,
                severity=severity,
            )
        )

    return inconsistencies


