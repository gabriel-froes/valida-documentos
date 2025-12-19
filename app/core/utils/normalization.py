import unicodedata
from typing import Optional


def _strip_accents(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(ch for ch in normalized if not unicodedata.combining(ch))


def _normalize_whitespace(value: str) -> str:
    return " ".join(value.split())


def only_digits(value: Optional[str]) -> str:
    if not value:
        return ""
    return "".join(ch for ch in value if ch.isdigit())


def normalize_text(value: Optional[str]) -> str:
    if not value:
        return ""
    value = _strip_accents(value)
    value = _normalize_whitespace(value)
    return value.strip().lower()

