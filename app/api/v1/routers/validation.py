from fastapi import APIRouter, UploadFile, File

from app.api.v1.schemas import ValidationResultResponse
from app.services.validation_use_case import validate_supplier_documents_use_case

router = APIRouter(prefix='', tags=['validation'])

@router.post(
    '/validate-docs',
    response_model=ValidationResultResponse,
    summary='Valida contrato social, cartão CNPJ e certidão negativa',
)
async def validate_documents(
    articles_of_association: UploadFile = File(...),
    cnpj_card: UploadFile = File(...),
    tax_clearance_certificate: UploadFile = File(...),
) -> ValidationResultResponse:
    return await validate_supplier_documents_use_case(
        articles_of_association_file=articles_of_association,
        cnpj_card_file=cnpj_card,
        tax_clearance_certificate_file=tax_clearance_certificate,
    )