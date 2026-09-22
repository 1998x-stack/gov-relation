"""Pillar A: ingest profile JSON into canonical person/position/relationship streams.

A name alone cannot establish a person ID. Such relationship candidates are
recorded as unreviewed claims rather than graph edges with a fabricated target.
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
_CONFIDENCE = {"confirmed", "plausible", "unverified"}
_DIRECTIONS = {"undirected", "from_to", "to_from"}
_STRENGTHS = {"strong", "medium", "weak", "unknown"}
_DATE_PRECISIONS = {"day", "month", "year", "range", "unknown"}
_IDENTITIES = {"verified", "probable", "unresolved", "merged"}


def _enum(value: object, accepted: set[str], fallback: str) -> str:
    return value if isinstance(value, str) and value in accepted else fallback


def _current(value: object) -> int:
    """Do not interpret strings such as 'false' as truthy."""
    return int(value is True or value == 1 or (isinstance(value, str) and value.lower() in {"true", "yes"}))


def _profile_dirs() -> list[Path]:
    from gov_relation.paths import PERSONS_DIR, PROVINCES_DIR

    dirs = [PERSONS_DIR]
    if PROVINCES_DIR.exists():
        for province in sorted(p for p in PROVINCES_DIR.iterdir() if p.is_dir()):
            path = province / "persons"
            if path.exists():
                dirs.append(path)
    return dirs


def _read_profiles(profile_dir: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    if not profile_dir.exists():
        return out
    for path in sorted(profile_dir.rglob("*.json")):
        if "TODO" in path.name or path.name.startswith("."):
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if isinstance(data, dict):
            out.append(data)
    return out


def profile_to_records(profile: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """Produce schema-compatible records without inventing relationship IDs."""
    identity = profile.get("identity") or {}
    person_id = identity.get("person_id") or profile.get("person_id")
    records: dict[str, list[dict[str, Any]]] = {
        "persons": [], "positions": [], "relationships": [], "sources": [], "claims": [],
    }
    if not person_id:
        return records
    person_id = str(person_id)
    name = identity.get("name") or profile.get("name") or ""
    records["persons"].append({
        "person_id": person_id,
        "canonical_name": name,
        "normalized_name": name,
        "gender": identity.get("gender", ""),
        "ethnicity": identity.get("ethnicity", ""),
        "birth_text": identity.get("birth", ""),
        "birth_precision": "unknown",
        "birthplace": identity.get("birthplace", ""),
        "native_place": identity.get("native_place", ""),
        "education": json.dumps(identity.get("education", []), ensure_ascii=False),
        "party_join_text": identity.get("party_join", ""),
        "work_start_text": identity.get("work_start", ""),
        "identity_status": _enum(identity.get("identity_status"), _IDENTITIES, "unresolved"),
        "merged_into_id": None,
        "created_at": None,
        "updated_at": None,
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
            "date_precision": _enum(seg.get("date_precision"), _DATE_PRECISIONS, "unknown"),
            "is_current": _current(seg.get("is_current")),
            "sort_order": i,
            "confidence": _enum(seg.get("confidence"), _CONFIDENCE, "unverified"),
            "notes": seg.get("notes", ""),
        })
    for i, rel in enumerate(profile.get("relationships", [])):
        target = rel.get("person_id")
        if target is None or str(target).strip() == "":
            # Keep the original candidate discoverable for later identity review,
            # but do not misrepresent a person's display name as an entity ID.
            records["claims"].append({
                "claim_id": f"{person_id}:unresolved-rel:{i}",
                "subject_type": "person",
                "subject_id": person_id,
                "predicate": "unresolved_relationship_candidate",
                "value_json": json.dumps(rel, ensure_ascii=False, sort_keys=True),
                "confidence": "unverified",
                "review_status": "pending",
            })
            continue
        target = str(target)
        if target == person_id:
            raise ValueError(f"Self relationship for {person_id!r}")
        records["relationships"].append({
            "relationship_id": f"{person_id}:rel:{i}",
            "person_from_id": person_id,
            "person_to_id": target,
            "relationship_type": rel.get("type", ""),
            "direction": _enum(rel.get("direction"), _DIRECTIONS, "undirected"),
            "strength": _enum(rel.get("strength"), _STRENGTHS, "unknown"),
            "confidence": _enum(rel.get("confidence"), _CONFIDENCE, "unverified"),
            "context": rel.get("context", ""),
            "evidence_summary": rel.get("evidence", ""),
            "overlap_organization_id": None,
            "overlap_organization_text": rel.get("overlap_org", ""),
            "overlap_period_text": rel.get("overlap_period", ""),
            "valid_from": None,
            "valid_to": None,
        })
    return records


def _append_idempotent(path: Path, kind: str, rows: list[dict[str, Any]]) -> int:
    """Append unique IDs, refusing silently conflicting existing facts."""
    key = _ID_BY_KIND[kind]
    existing_rows = list(iter_jsonl(path)) if path.exists() else []
    by_id = {str(row[key]): row for row in existing_rows}
    if len(by_id) != len(existing_rows):
        raise ValueError(f"Duplicate existing {kind} IDs in {path}")
    added = []
    for row in rows:
        rid = str(row[key])
        prior = by_id.get(rid)
        if prior is not None:
            if prior != row:
                raise ValueError(f"Conflicting {kind} record {rid!r}; review source changes")
            continue
        by_id[rid] = row
        added.append(row)
    if added:
        write_jsonl(path, iter([*existing_rows, *added]))
    return len(added)


def pillar_build(args) -> int:
    """Ingest profiles into streams and rebuild the derived SQLite backup."""
    records_dir = Path(args.records)
    records_dir.mkdir(parents=True, exist_ok=True)
    dirs = [Path(d) for d in args.profiles] if getattr(args, "profiles", None) else _profile_dirs()
    tallies: dict[str, int] = {}
    for directory in dirs:
        for profile in _read_profiles(directory):
            recs = profile_to_records(profile)
            for kind, rows in recs.items():
                if rows:
                    tallies[kind] = tallies.get(kind, 0) + _append_idempotent(
                        records_dir / f"{kind}.jsonl", kind, rows
                    )
    backup = records_dir.parent / "database" / "platform.db"
    rebuild_db_from_records(records_dir, backup, overwrite=True)
    print(f"generation done (added): {tallies}")
    return 0
