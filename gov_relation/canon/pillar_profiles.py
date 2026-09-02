"""Pillar A — 数据导入 (profile ingestion into canonical profile_documents).

Ingests person profile JSON files into the canonical ``profile_documents``
stream idempotently. Each file maps to one record; the id is a stable hash of
the relative path, so re-runs add zero rows.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Callable

from .engine import rebuild_db_from_records
from .streams import iter_jsonl, write_jsonl


def _profile_files(roots: list[Path]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for root in roots:
        root = Path(root)
        if not root.exists():
            continue
        for p in sorted(root.rglob("*.json")):
            if "TODO" in p.name or p.name.startswith("."):
                continue
            out.append({"path": p, "rel": str(p.relative_to(root))})
    return out


def _profile_to_document(data: dict[str, Any], rel: str) -> dict[str, Any]:
    identity = data.get("identity", {})
    person_id = identity.get("person_id") or data.get("person_id") or ""
    profile_id = "profile_" + hashlib.sha256(rel.encode("utf-8")).hexdigest()[:16]
    return {
        "profile_id": profile_id,
        "person_id": person_id,
        "raw_record_id": "",
        "schema_version": data.get("schema_version", "1.0"),
        "generated_at": data.get("generated_at", ""),
        "profile_json": json.dumps(data, ensure_ascii=False, sort_keys=True),
    }


def _append_idempotent(path: Path, row: dict[str, Any], id_key: Callable) -> int:
    if path.exists() and str(id_key(row)) in _existing_ids.get(path, ()):
        return 0
    _existing_ids.setdefault(path, set()).add(str(id_key(row)))
    return 1


def _load_ids(path: Path, id_key: Callable) -> set[str]:
    if not path.exists():
        return set()
    return {str(id_key(r)) for r in iter_jsonl(path)}


def pillar_import_profiles(args) -> int:
    from gov_relation.paths import PERSONS_DIR, PROVINCES_DIR

    records_dir = Path(args.records)
    records_dir.mkdir(parents=True, exist_ok=True)

    roots = [PERSONS_DIR]
    for province in [p for p in PROVINCES_DIR.iterdir() if p.is_dir()]:
        roots.append(province / "persons")

    target = records_dir / "profile_documents.jsonl"

    def id_key(row):
        return str(row.get("profile_id"))

    # O(N): load the existing id set exactly once, then scan files once.
    global _existing_ids
    _existing_ids = {target: _load_ids(target, id_key)}
    existing = _existing_ids[target]

    count_added = 0
    total = 0
    new_rows: list[dict[str, Any]] = []
    for item in _profile_files(roots):
        total += 1
        try:
            data = json.loads(item["path"].read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        row = _profile_to_document(data, item["rel"])
        if row["profile_id"] not in existing:
            existing.add(row["profile_id"])
            new_rows.append(row)
            count_added += 1

    if new_rows:
        merged = list(iter_jsonl(target)) if target.exists() else []
        merged.extend(new_rows)
        write_jsonl(target, iter(merged))

    print(f"profiles: scanned={total} added={count_added} total_records={len(existing)}")
    return 0


_existing_ids: dict[Path, set[str]] = {}
