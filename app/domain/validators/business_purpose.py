from typing import List

from app.api.v1.schemas import Inconsistency
from app.domain.models import ArticlesOfAssociationData, CNPJCardData
from app.services.llm_client import call_llm_and_parse
from app.services.prompts import build_prompt


def _format_business_purpose(business_purpose: List[str]) -> str:
    if not business_purpose:
        return "Objeto social não especificado."
    return "\n".join(f"- {item}" for item in business_purpose)


def _format_activities(cnpj_card: CNPJCardData) -> str:
    activities_text = []
    
    main = cnpj_card.activities.main_activity
    activities_text.append(f"Atividade Principal:")
    activities_text.append(f"  Código CNAE: {main.code}")
    activities_text.append(f"  Descrição: {main.description}")
    
    if cnpj_card.activities.secondary_activities:
        activities_text.append(f"\nAtividades Secundárias:")
        for sec in cnpj_card.activities.secondary_activities:
            activities_text.append(f"  Código CNAE: {sec.code}")
            activities_text.append(f"  Descrição: {sec.description}")
    
    return "\n".join(activities_text)


async def validate_business_purpose_consistency(
    articles: ArticlesOfAssociationData,
    cnpj_card: CNPJCardData,
) -> List[Inconsistency]:
    inconsistencies: List[Inconsistency] = []
    
    objeto_social_text = _format_business_purpose(articles.business_purpose)
    atividades_text = _format_activities(cnpj_card)
    
    prompt = build_prompt(
        "business_purpose_validation",
        {
            "objeto_social": objeto_social_text,
            "atividades": atividades_text,
        },
    )
    
    result = await call_llm_and_parse(prompt)
    
    if not result.get("match", True):
        reason = result.get("reason", "Objeto social não contempla as atividades do cartão CNPJ.")
        inconsistencies.append(
            Inconsistency(
                field="objeto_social",
                message=f"Objeto social não está alinhado com as atividades do cartão CNPJ. {reason}",
                severity="CRITICA",
            )
        )
    
    return inconsistencies

