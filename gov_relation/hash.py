"""Content-hash functions for person/org dedup in the central registry.

Person merge key ::

    SHA256(normalize(name) + "|" + birth)[:16]

Organization merge key ::

    SHA256(province + "|" + normalize(fqn))[:16]

All SHA256 output is hex lowercase.
"""

from __future__ import annotations

import hashlib
import unicodedata


import re

def normalize(s: str | None) -> str:
    """Normalize for hashing: NFKC, strip all whitespace."""
    if s is None:
        return ""
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r'\s+', '', s)
    return s


def person_hash(name: str, birth: str) -> str:
    """SHA256(normalize(name) + "|" + (birth or ""))[:16] hex."""
    raw = normalize(name) + "|" + (birth or "")
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def org_hash(province: str, fqn: str) -> str:
    """SHA256(province + "|" + normalize(fqn))[:16] hex."""
    raw = province + "|" + normalize(fqn)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]