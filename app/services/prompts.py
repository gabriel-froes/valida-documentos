from typing import Final


ARTICLES_OF_ASSOCIATION_PROMPT: Final[str] = """
Você é um assistente jurídico especializado em contratos sociais de empresas brasileiras.

Tarefa:
- Leia o texto do contrato social abaixo.
- Extraia as informações e responda EXCLUSIVAMENTE em JSON, seguindo exatamente a estrutura esperada.
- Não inclua nenhum texto fora do JSON.

Estrutura JSON esperada (use exatamente estes campos e esta organização):

{
  "tipo_documento": "Contrato Social",
  "informacoes_entidade": {
    "razao_social": "string (Razão Social COMPLETA normalizada: minúsculas, sem acentos, espaços únicos. Substitua: LTDA->LIMITADA, EIRELI->EMPRESA INDIVIDUAL DE RESPONSABILIDADE LIMITADA, ME->MICROEMPRESA, EPP->EMPRESA DE PEQUENO PORTE, SA->SOCIEDADE ANONIMA. Ex: 'EMPRESA EXEMPLO LTDA' -> 'empresa exemplo limitada')",
    "natureza_juridica": "string (Natureza jurídica normalizada: retorne EXATAMENTE um dos valores: 'limitada', 'sociedade anonima', 'empresa individual de responsabilidade limitada', 'microempresa', 'empresa de pequeno porte')",
    "nire": "string (apenas dígitos)",
    "data_registro": "YYYY-MM-DD",
    "data_inicio": "YYYY-MM-DD",
    "prazo_duracao": "Indeterminado ou YYYY-MM-DD"
  },
  "sede": {
    "logradouro": "string",
    "numero": "string",
    "complemento": "string ou null",
    "bairro": "string",
    "cep": "string (8 dígitos)",
    "cidade": "string",
    "estado": "string (2 letras)"
  },
  "objeto_social": ["lista de atividades encontradas no Objeto Social"],
  "capital_social": {
    "valor_total": "string",
    "moeda": "BRL",
    "total_acoes": "string",
    "valor_nominal_acao": "string"
  },
  "participacoes_societarias": [
    {
      "nome_ou_razao_social": "string (Nome completo se pessoa física ou razão social normalizada se pessoa jurídica)",
      "cpf_ou_cnpj": "string (11 dígitos se CPF, 14 dígitos se CNPJ)",
      "qualificacao": "string (Classificação funcional baseada no PODER DE GESTÃO. Normalize para minúsculas e retorne EXATAMENTE um destes valores: 'socio administrador' (qualquer sócio com poderes de administração/gerência/representação, mesmo que o título literal seja 'Diretor', 'Presidente', 'Sócio-Gerente' ou 'Administrador'), 'socio' (sócio sem poderes de gestão ou assinatura), 'diretor' (gestor que NÃO é sócio/proprietário). IMPORTANTE: No Contrato Social, se a cláusula indicar que sócio 'usará o título de Diretor' ou 'terá poderes de gerência', classifique obrigatoriamente como 'socio administrador' para compatibilidade com QSA do Cartão CNPJ)"
    }
  ]
}

Texto do documento:
__DOCUMENT_TEXT__
""".strip()


CNPJ_CARD_PROMPT: Final[str] = """
Você é um assistente jurídico especializado em cartões CNPJ de empresas brasileiras.

Tarefa:
- Leia o texto do cartão CNPJ abaixo.
- Extraia as informações e responda EXCLUSIVAMENTE em JSON, seguindo exatamente a estrutura esperada.
- Não inclua nenhum texto fora do JSON.

Estrutura JSON esperada (use exatamente estes campos e esta organização):

{
  "tipo_documento": "Cartão CNPJ",
  "informacoes_registro": {
    "cnpj": "string (14 dígitos)",
    "is_matriz": boolean,
    "data_abertura": "YYYY-MM-DD",
    "razao_social": "string (Razão Social COMPLETA normalizada: minúsculas, sem acentos, espaços únicos. Substitua: LTDA->LIMITADA, EIRELI->EMPRESA INDIVIDUAL DE RESPONSABILIDADE LIMITADA, ME->MICROEMPRESA, EPP->EMPRESA DE PEQUENO PORTE, SA->SOCIEDADE ANONIMA. Ex: 'EMPRESA EXEMPLO LTDA' -> 'empresa exemplo limitada')",
    "nome_fantasia": "string ou null",
    "porte": "string",
    "natureza_juridica": "string (Natureza jurídica normalizada: retorne EXATAMENTE um dos valores: 'limitada', 'sociedade anonima', 'empresa individual de responsabilidade limitada', 'microempresa', 'empresa de pequeno porte')"
  },
  "atividades": {
    "atividade_principal": {
      "codigo": "string",
      "descricao": "string"
    },
    "atividades_secundarias": [
      {
        "codigo": "string",
        "descricao": "string"
      }
    ]
  },
  "endereco": {
    "logradouro": "string",
    "numero": "string",
    "complemento": "string ou null",
    "bairro": "string",
    "cep": "string (8 dígitos)",
    "cidade": "string",
    "estado": "string (2 letras)"
  },
  "situacao_cadastral": {
    "situacao": "string (ex: ATIVA)",
    "data_situacao": "YYYY-MM-DD"
  },
  "socios_qsa": [
    {
      "nome_ou_razao_social": "string (Nome completo se pessoa física ou razão social normalizada se pessoa jurídica)",
      "cpf_ou_cnpj": "string (11 dígitos se CPF, 14 dígitos se CNPJ)",
      "qualificacao": "string (Classificação funcional baseada no PODER DE GESTÃO. Normalize para minúsculas e retorne EXATAMENTE um destes valores: 'socio administrador' (qualquer sócio com poderes de administração/gerência/representação, mesmo que o título literal seja 'Diretor', 'Presidente', 'Sócio-Gerente' ou 'Administrador'), 'socio' (sócio sem poderes de gestão ou assinatura), 'diretor' (gestor que NÃO é sócio/proprietário). IMPORTANTE: No Contrato Social, se a cláusula indicar que sócio 'usará o título de Diretor' ou 'terá poderes de gerência', classifique obrigatoriamente como 'socio administrador' para compatibilidade com QSA do Cartão CNPJ)"
    }
  ],
  "informacoes_emissao": {
    "emitido_em": "YYYY-MM-DDTHH:MM:SS",
    "codigo_controle": "string"
  }
}

Texto do documento:
__DOCUMENT_TEXT__
""".strip()


TAX_CLEARANCE_CERTIFICATE_PROMPT: Final[str] = """
Você é um assistente jurídico especializado em certidões negativas de débitos federais.

Tarefa:
- Leia o texto da certidão abaixo.
- Extraia as informações e responda EXCLUSIVAMENTE em JSON, seguindo exatamente a estrutura esperada.
- Não inclua nenhum texto fora do JSON.

Estrutura JSON esperada (use exatamente estes campos e esta organização):

{
  "tipo_documento": "Certidão Negativa de Débitos",
  "razao_social": "string (Razão Social COMPLETA normalizada: retorne o nome completo da empresa em minúsculas, sem acentos, espaços únicos. Substitua abreviações pelo termo completo: LTDA->LIMITADA, EIRELI->EMPRESA INDIVIDUAL DE RESPONSABILIDADE LIMITADA, ME->MICROEMPRESA, EPP->EMPRESA DE PEQUENO PORTE, SA->SOCIEDADE ANONIMA. Exemplo: 'EMPRESA EXEMPLO LTDA' deve retornar 'empresa exemplo limitada')",
  "natureza_juridica": "string (Natureza jurídica normalizada: minúsculas, sem acentos, espaços únicos. Valores: 'limitada', 'sociedade anonima', 'empresa individual de responsabilidade limitada', 'microempresa', 'empresa de pequeno porte')",
  "cnpj": "string (14 dígitos)",
  "data_emissao": "YYYY-MM-DD",
  "data_validade": "YYYY-MM-DD",
  "status": "string (ex: VALIDA, POSSUI DÉBITOS)",
  "codigo_controle": "string"
}

Texto do documento:
__DOCUMENT_TEXT__
""".strip()


BUSINESS_PURPOSE_VALIDATION_PROMPT: Final[str] = """
Você é um auditor jurídico especializado em compliance empresarial brasileiro.

Tarefa:
1. Compare o Objeto Social (Contrato) com as Atividades CNAE (CNPJ).
2. Verifique se TODAS as atividades listadas no CNPJ possuem embasamento jurídico no Objeto Social do Contrato.
3. Ignore se o Contrato for mais abrangente que o CNPJ (isso é normal). O foco é garantir que o CNPJ não tenha atividades "órfãs" de contrato.

Critérios de Análise:
- Use análise semântica para identificar sinônimos (ex: "Desenvolvimento de software" é compatível com "Consultoria em Tecnologia").
- "Match: True" se o CNPJ estiver 100% coberto pelo Contrato.
- "Match: False" apenas se houver atividade no CNPJ que não tenha nenhuma relação com o texto do Contrato.

Estrutura JSON:
{
  "match": boolean,
  "reason": "Justificativa clara em português (ex: 'A atividade de transporte de cargas no CNPJ não consta no objeto social')."
}

Objeto Social: __OBJETO_SOCIAL__
Atividades CNPJ: __ATIVIDADES__
""".strip()


PROMPTS: Final[dict[str, str]] = {
    "articles_of_association": ARTICLES_OF_ASSOCIATION_PROMPT,
    "cnpj_card": CNPJ_CARD_PROMPT,
    "tax_clearance_certificate": TAX_CLEARANCE_CERTIFICATE_PROMPT,
    "business_purpose_validation": BUSINESS_PURPOSE_VALIDATION_PROMPT,
}


def build_prompt(name: str, replacements: dict[str, str]) -> str:
    try:
        template = PROMPTS[name]
    except KeyError as exc:
        raise ValueError(f"Unknown prompt name: {name}") from exc

    result = template
    for placeholder, value in replacements.items():
        result = result.replace(f"__{placeholder.upper()}__", value)
    
    return result

