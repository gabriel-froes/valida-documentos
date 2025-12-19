from typing import List, Optional, Dict
from itertools import combinations

from app.api.v1.schemas import Inconsistency, Severity


def compare_documents(
    field_name: str,
    document_values: Dict[str, Optional[str]],
    message: str,
    severity: Severity = "CRITICA",
) -> List[Inconsistency]:
    inconsistencies: List[Inconsistency] = []
    
    document_names = list(document_values.keys())
    
    for doc1_name, doc2_name in combinations(document_names, 2):
        doc1_value = document_values[doc1_name]
        doc2_value = document_values[doc2_name]
        
        if doc1_value and doc2_value and doc1_value != doc2_value:
            inconsistencies.append(
                Inconsistency(
                    field=field_name,
                    message=message,
                    severity=severity,
                    values={
                        doc1_name: doc1_value,
                        doc2_name: doc2_value,
                    },
                )
            )
    
    return inconsistencies
