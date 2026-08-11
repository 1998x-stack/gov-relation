"""Conservative normalization and deterministic identifiers."""

from __future__ import annotations

import hashlib
import re
import unicodedata
import uuid

_NAMESPACE = uuid.UUID("99f1252f-a5e0-4d43-a4d5-087776ec44f8")
_DATE_YEAR = re.compile(r"^\d{4}年?$")
_DATE_MONTH = re.compile(r"^\d{4}(?:[-./]\d{1,2}|年\d{1,2}月)$")
_DATE_DAY = re.compile(
    r"^\d{4}(?:[-./]\d{1,2}[-./]\d{1,2}|年\d{1,2}月\d{1,2}日)$"
)


def normalize_text(value: object) -> str:
    """Return a stable NFKC value with all whitespace removed."""
    text = unicodedata.normalize("NFKC", str(value or "")).strip()
    return re.sub(r"\s+", "", text)


def stable_id(kind: str, key: str) -> str:
    """Return a readable deterministic UUIDv5 identifier."""
    return f"{kind}_{uuid.uuid5(_NAMESPACE, f'{kind}:{key}').hex}"


def sha256_bytes(value: bytes) -> str:
    """Return the SHA-256 hex digest for bytes."""
    return hashlib.sha256(value).hexdigest()


def date_precision(value: object) -> str:
    """Classify a date-like value without inventing missing precision."""
    text = str(value or "").strip()
    if _DATE_DAY.fullmatch(text):
        return "day"
    if _DATE_MONTH.fullmatch(text):
        return "month"
    if _DATE_YEAR.fullmatch(text):
        return "year"
    return "unknown"


def person_key(
    *, name: object, birth: object, dataset_key: str, source_pk: object
) -> tuple[str, str]:
    """Build an identity key and status without unsafe name-only merging."""
    normalized_name = normalize_text(name)
    if normalized_name and date_precision(birth) != "unknown":
        return f"verified:{normalized_name}|{normalize_text(birth)}", "verified"
    return f"scoped:{dataset_key}|{source_pk}|{normalized_name}", "unresolved"


def organization_key(*, name: object, jurisdiction_key: str, dataset_key: str) -> str:
    """Scope organization identity to jurisdiction, falling back to dataset."""
    scope = jurisdiction_key or dataset_key
    return f"{scope}|{normalize_text(name)}"
