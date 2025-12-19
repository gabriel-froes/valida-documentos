from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict


class Address(BaseModel):
    street: str = Field(alias="logradouro")
    number: str = Field(alias="numero")
    complement: Optional[str] = Field(default=None, alias="complemento")
    district: str = Field(alias="bairro")
    postal_code: str = Field(alias="cep")
    city: str = Field(alias="cidade")
    state: str = Field(alias="estado")


class ShareholderParticipation(BaseModel):
    name_or_company_name: str = Field(alias="nome_ou_razao_social")
    cpf_or_cnpj: str = Field(alias="cpf_ou_cnpj")
    qualification: str = Field(alias="qualificacao")


class ShareCapital(BaseModel):
    total_amount: str = Field(alias="valor_total")
    currency: str = Field(alias="moeda")
    total_shares: str = Field(alias="total_acoes")
    nominal_share_value: str = Field(alias="valor_nominal_acao")


class EntityInfo(BaseModel):
    company_name: str = Field(alias="razao_social")
    legal_nature: str = Field(alias="natureza_juridica")
    nire: str
    registration_date: date = Field(alias="data_registro")
    start_date: date = Field(alias="data_inicio")
    term: str = Field(alias="prazo_duracao")


class ArticlesOfAssociationData(BaseModel):
    document_type: str = Field(alias="tipo_documento")
    entity_info: EntityInfo = Field(alias="informacoes_entidade")
    head_office: Address = Field(alias="sede")
    business_purpose: List[str] = Field(alias="objeto_social")
    share_capital: ShareCapital = Field(alias="capital_social")
    shareholders: List[ShareholderParticipation] = Field(alias="participacoes_societarias")

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
    )


class EmissionInfo(BaseModel):
    issued_at: datetime = Field(alias="emitido_em")
    control_code: str = Field(alias="codigo_controle")


class PartnerSummary(BaseModel):
    name_or_company_name: str = Field(alias="nome_ou_razao_social")
    cpf_or_cnpj: str = Field(alias="cpf_ou_cnpj")
    qualification: str = Field(alias="qualificacao")


class TaxStatus(BaseModel):
    status: str = Field(alias="situacao")
    status_date: date = Field(alias="data_situacao")


class Activity(BaseModel):
    code: str = Field(alias="codigo")
    description: str = Field(alias="descricao")


class Activities(BaseModel):
    main_activity: Activity = Field(alias="atividade_principal")
    secondary_activities: List[Activity] = Field(alias="atividades_secundarias")


class RegistrationInfo(BaseModel):
    tax_id: str = Field(alias="cnpj")
    is_head_office: bool = Field(alias="is_matriz")
    opening_date: date = Field(alias="data_abertura")
    company_name: str = Field(alias="razao_social")
    trade_name: Optional[str] = Field(default=None, alias="nome_fantasia")
    size: str = Field(alias="porte")
    legal_nature: str = Field(alias="natureza_juridica")


class CNPJCardData(BaseModel):
    document_type: str = Field(alias="tipo_documento")
    registration_info: RegistrationInfo = Field(alias="informacoes_registro")
    activities: Activities = Field(alias="atividades")
    address: Address = Field(alias="endereco")
    tax_status: TaxStatus = Field(alias="situacao_cadastral")
    partners: List[PartnerSummary] = Field(alias="socios_qsa")
    emission_info: EmissionInfo = Field(alias="informacoes_emissao")

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
    )

class TaxClearanceCertificateData(BaseModel):
    document_type: str = Field(alias="tipo_documento")
    company_name: str = Field(alias="razao_social")
    legal_nature: str = Field(alias="natureza_juridica")
    tax_id: str = Field(alias="cnpj")
    issue_date: date = Field(alias="data_emissao")
    expiration_date: date = Field(alias="data_validade")
    status: str
    control_code: str = Field(alias="codigo_controle")

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
    )