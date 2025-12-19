from typing import List, Dict

from app.api.v1.schemas import Inconsistency
from app.domain.models import ArticlesOfAssociationData, CNPJCardData
from app.core.utils.normalization import normalize_text, only_digits


def _organize_partners_by_id(partners: List) -> Dict[str, Dict]:
    partners_by_id: Dict[str, Dict] = {}
    
    for partner in partners:
        normalized_id = only_digits(partner.cpf_or_cnpj)
        if normalized_id:
            partners_by_id[normalized_id] = {
                "name": normalize_text(partner.name_or_company_name),
                "qualification": normalize_text(partner.qualification),
                "id_type": "cpf" if len(normalized_id) == 11 else "cnpj",
            }
    
    return partners_by_id


def _validate_articles_partners(
    articles_by_id: Dict[str, Dict],
    card_by_id: Dict[str, Dict],
) -> List[Inconsistency]:
    inconsistencies: List[Inconsistency] = []

    for partner_id, articles_data in articles_by_id.items():
        id_type = articles_data["id_type"]
        
        if partner_id not in card_by_id:
            inconsistencies.append(
                Inconsistency(
                    field="socios",
                    message=f"{id_type.upper()} não encontrado no cartão CNPJ.",
                    severity="CRITICA",
                    values={
                        "contrato_social": articles_data["name"],
                        id_type: partner_id,
                    },
                )
            )
            continue
        
        card_data = card_by_id[partner_id]
        if articles_data["name"] != card_data["name"]:
            inconsistencies.append(
                Inconsistency(
                    field="socios",
                    message="Nome do sócio divergente entre documentos.",
                    severity="CRITICA",
                    values={
                        "contrato_social": articles_data["name"],
                        "cartao_cnpj": card_data["name"],
                        id_type: partner_id,
                    },
                )
            )
        
        if articles_data["qualification"] != card_data["qualification"]:
            inconsistencies.append(
                Inconsistency(
                    field="socios",
                    message="Qualificação do sócio divergente entre documentos.",
                    severity="AVISO",
                    values={
                        "contrato_social": articles_data["qualification"],
                        "cartao_cnpj": card_data["qualification"],
                        id_type: partner_id,
                    },
                )
            )

    return inconsistencies


def _validate_card_partners(
    articles_by_id: Dict[str, Dict],
    card_by_id: Dict[str, Dict],
) -> List[Inconsistency]:
    inconsistencies: List[Inconsistency] = []

    for partner_id, card_data in card_by_id.items():
        if partner_id not in articles_by_id:
            id_type = card_data["id_type"]
            inconsistencies.append(
                Inconsistency(
                    field="socios",
                    message=f"{id_type.upper()} não encontrado no contrato social.",
                    severity="CRITICA",
                    values={
                        "cartao_cnpj": card_data["name"],
                        id_type: partner_id,
                    },
                )
            )

    return inconsistencies


def validate_partners_consistency(
    articles: ArticlesOfAssociationData,
    cnpj_card: CNPJCardData,
) -> List[Inconsistency]:
    articles_by_id = _organize_partners_by_id(articles.shareholders)
    card_by_id = _organize_partners_by_id(cnpj_card.partners)

    inconsistencies: List[Inconsistency] = []
    inconsistencies.extend(_validate_articles_partners(articles_by_id, card_by_id))
    inconsistencies.extend(_validate_card_partners(articles_by_id, card_by_id))

    return inconsistencies

