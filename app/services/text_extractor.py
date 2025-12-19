from fastapi import UploadFile
from pypdf import PdfReader

from app.core.exceptions import InvalidFileTypeError, PDFExtractionError
from app.core.logging import get_logger

logger = get_logger(__name__)


def validate_pdf_file(file: UploadFile) -> None:
    if not file.filename.lower().endswith('.pdf'):
        filename_info = f" '{file.filename}'" if file.filename else ""
        raise InvalidFileTypeError(
            f"O arquivo{filename_info} não é um PDF. Por favor, envie apenas arquivos PDF."
        )


async def extract_text_from_pdf(file: UploadFile) -> str:
    validate_pdf_file(file)
    
    reader = PdfReader(file.file)

    texts: list[str] = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        if page_text.strip():
            texts.append(page_text)

    full_text = "\n\n".join(texts).strip()
    if not full_text:
        filename_info = f" '{file.filename}'" if file.filename else ""
        logger.error(
            "PDF extraction failed",
            extra={"data": {"filename": file.filename, "pages": len(reader.pages)}},
        )
        raise PDFExtractionError(
            f"Não foi possível extrair texto do PDF{filename_info}. "
            f"Verifique se o arquivo está válido, não está corrompido e contém texto legível."
        )

    return full_text

