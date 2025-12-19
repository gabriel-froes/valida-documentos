from fastapi import UploadFile
from pypdf import PdfReader

from app.core.exceptions import PDFExtractionError
from app.core.logging import get_logger

logger = get_logger(__name__)


async def extract_text_from_pdf(file: UploadFile) -> str:
    reader = PdfReader(file.file)

    texts: list[str] = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        if page_text.strip():
            texts.append(page_text)

    full_text = "\n\n".join(texts).strip()
    if not full_text:
        logger.error(
            "PDF extraction failed",
            extra={"data": {"filename": file.filename, "pages": len(reader.pages)}},
        )
        raise PDFExtractionError("Could not extract any text from PDF")

    return full_text

