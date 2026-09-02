"""Pillar A — 数据生成 (data generation).

Canonical output is always JSONL streams under ``data/records/``; the SQLite
backup is rebuilt afterwards. This module ingests source artefacts (person
profile JSON) into the canonical streams idempotently (by stable id), then the
CLI rebuilds the SQLite backup.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .engine import rebuild_db_from_records
from .streams import iter_jsonl, write_jsonl

_ID_BY_KIND = {
    "persons": "person_id",
    "positions": "position_id",
    "relationships": "relationship_id",
    "sources": "source_id",
    "claims": "claim_id",
    "organizations": "organization_id",
}


def _profile_dirs():
    from gov_relation.paths import PERSONS_DIR, PROVINCES_DIR

    dirs = [PERSONS_DIR]
    for province in [p for p in PROVINCES_DIR.glob("*") if p.is_dir()]:
        pd = province / "persons"
        if pd.exists():
            dirs.append(pd)
    return dirs


def _read_profiles(profile_dir: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for p in sorted(profile_dir.rglob("*.json")):
        if "TODO" in p.name or p.name.startswith("."):
            continue
        try:
            out.append(json.loads(p.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, OSError):
            continue
    return out


def profile_to_records(profile: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """Flatten a person profile into canonical person/position/relationship records."""
    identity = profile.get("identity", {})
    person_id = identity.get("person_id") or profile.get("person_id")
    records: dict[str, list[dict[str, Any]]] = {
        "persons": [],
        "positions": [],
        "relationships": [],
        "sources": [],
        "claims": [],
    }
    if not person_id:
        return records
    records["persons"].append({
        "person_id": person_id,
        "canonical_name": identity.get("name") or profile.get("name", ""),
        "gender": identity.get("gender", ""),
        "ethnicity": identity.get("ethnicity", ""),
        "birth_text": identity.get("birth", ""),
        "birthplace": identity.get("birthplace", ""),
        "native_place": identity.get("native_place", ""),
        "education": json.dumps(identity.get("education", []), ensure_ascii=False),
        "party_join_text": identity.get("party_join", ""),
        "work_start_text": identity.get("work_start", ""),
        "identity_status": "complete",
        "merged_into_id": None,
    })
    for i, seg in enumerate(profile.get("career_timeline", [])):
        records["positions"].append({
            "position_id": f"{person_id}:pos:{i}",
            "person_id": person_id,
            "organization_id": None,
            "organization_text": seg.get("org", ""),
            "title": seg.get("title", ""),
            "rank": seg.get("rank", "") or seg.get("level", ""),
            "category": seg.get("system", ""),
            "title_category": seg.get("system", ""),
            "start_text": seg.get("start", ""),
            "end_text": seg.get("end", ""),
            "start_date": seg.get("start", ""),
            "end_date": seg.get("end", ""),
            "date_precision": "",
            "is_current": int(bool(seg.get("is_current"))),
            "sort_order": i,
            "confidence": seg.get("confidence", ""),
            "notes": seg.get("notes", ""),
        })
    for i, rel in enumerate(profile.get("relationships", [])):
        records["relationships"].append({
            "relationship_id": f"{person_id}:rel:{i}",
            "person_from_id": person_id,
            "person_to_id": rel.get("person_id") or rel.get("name", ""),
            "relationship_type": rel.get("type", ""),
            "direction": rel.get("direction", ""),
            "strength": rel.get("strength", ""),
            "confidence": rel.get("confidence", ""),
            "context": rel.get("context", ""),
            "evidence_summary": rel.get("evidence", ""),
            "overlap_organization_text": rel.get("overlap_org", ""),
            "overlap_period_text": rel.get("overlap_period", ""),
        })
    return records


def _append_idempotent(path: Path, kind: str, rows: list[dict[str, Any]]) -> int:
    id_key = _ID_BY_KIND.get(kind, "id")
    existing: set[str] = set()
    if path.exists():
        existing = {str(r.get(id_key)) for r in iter_jsonl(path)}
    added = [r for r in rows if str(r.get(id_key)) not in existing]
    if not added:
        return 0
    merged = list(iter_jsonl(path)) if path.exists() else []
    merged.extend(added)
    write_jsonl(path, iter(merged))
    return len(added)


def pillar_build(args) -> int:
    """Ingest person profile JSONs into canonical streams, then rebuild backup."""
    records_dir = Path(args.records)
    records_dir.mkdir(parents=True, exist_ok=True)

    dirs = [Path(d) for d in getattr(args, "profiles", None)] if getattr(args, "profiles", None) else _profile_dirs()

    tallies: dict[str, int] = {}
    for d in dirs:
        for profile in _read_profiles(d):
            recs = profile_to_records(profile)
            for kind, rows in recs.items():
                if not rows:
                    continue
                tallies[kind] = tallies.get(kind, 0) + _append_idempotent(
                    records_dir / f"{kind}.jsonl", kind, rows
                )

    backup = records_dir.parent / "database" / "platform.db"
    rebuild_db_from_records(records_dir, backup, overwrite=True)
    print(f"generation done (added): {tallies}")
    return 0