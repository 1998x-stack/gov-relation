from __future__ import annotations

import json
from pathlib import Path

from .paths import TODO_PATH


def build_slug_province_map(todo_path: Path | None = None) -> dict[str, str]:
    """Parse TODO.json to map region slugs to province names."""
    path = todo_path or TODO_PATH
    if not path.exists():
        raise FileNotFoundError(f"TODO.json not found at {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    mapping: dict[str, str] = {}
    for p_entry in data.get("provinces", []):
        province = p_entry["province"]
        for task in p_entry.get("tasks", []):
            region = task.get("region", "")
            if region:
                mapping[region] = province
    return mapping


def detect_province(
    slug: str,
    todo_path: Path | None = None,
    map_cache: dict[str, str] | None = None,
) -> str:
    """Determine province name for a region slug/name.

    Raises ValueError if no match is found.
    """
    if map_cache is not None:
        mapping = map_cache
    else:
        mapping = build_slug_province_map(todo_path)

    if slug in mapping:
        return mapping[slug]

    raise ValueError(f"Cannot determine province for slug: {slug}")