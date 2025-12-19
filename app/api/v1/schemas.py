from typing import Literal, List, Dict, Optional
from pydantic import BaseModel


ValidationStatus = Literal['APROVADO', 'REPROVADO']
Severity = Literal['CRITICA', 'AVISO']


class Inconsistency(BaseModel):
    field: str
    message: str
    severity: Severity
    values: Optional[Dict[str, Optional[str]]] = None


class ValidationResultResponse(BaseModel):
    status: ValidationStatus
    inconsistencies: List[Inconsistency]