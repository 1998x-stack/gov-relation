"""Compatibility exports for the canonical identity helpers."""

from gov_relation.identity import (  # noqa: F401
    date_precision,
    normalize_text,
    organization_key,
    person_key,
    sha256_bytes,
    stable_id,
)

__all__ = [
    "date_precision",
    "normalize_text",
    "organization_key",
    "person_key",
    "sha256_bytes",
    "stable_id",
]
