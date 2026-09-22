"""Import profile documents into canonical JSONL without losing source identity.

The profile identifier is derived from the repository-relative source path, not
from the filename relative to each province's persons/ directory. Historical
filename-only IDs are retained when their provenance is unambiguous and their
content matches exactly. Ambiguous legacy IDs require a reviewed migration.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .streams import iter_jsonl, write_jsonl


def _profile_files(roots: list[Path]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for root in roots:
        root = Path(root)
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.json")):
            if "TODO" in path.name or path.name.startswith("."):
                continue
            out.append({"path": path, "rel": path.relative_to(root).as_posix()})
    return out


def _source_key(path: Path, repo_root: Path) -> str:
    """A clone-independent key for tracked files; absolute fallback for external roots."""
    resolved = path.resolve()
    try:
        return resolved.relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return resolved.as_posix()


def _profile_to_document(data: dict[str, Any], source_key: str) -> dict[str, Any]:
    identity = data.get("identity") or {}
    if not isinstance(identity, dict):
        raise ValueError("profile identity must be a JSON object")
    person_id = identity.get("person_id") or data.get("person_id") or ""
    profile_id = "profile_" + hashlib.sha256(source_key.encode("utf-8")).hexdigest()[:16]
    return {
        "profile_id": profile_id,
        "person_id": person_id,
        "raw_record_id": "",
        "schema_version": data.get("schema_version", "1.0"),
        "generated_at": data.get("generated_at", ""),
        "profile_json": json.dumps(data, ensure_ascii=False, sort_keys=True),
    }


def _existing_documents(path: Path) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    rows = list(iter_jsonl(path)) if path.exists() else []
    by_id: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("profile_id"), str) or not row["profile_id"]:
            raise ValueError(f"invalid profile document in {path}")
        profile_id = row["profile_id"]
        if profile_id in by_id:
            raise ValueError(f"duplicate existing profile_id: {profile_id}")
        by_id[profile_id] = row
    return rows, by_id


def pillar_import_profiles(args) -> int:
    """Stage and validate all imports before atomically replacing one JSONL file."""
    from gov_relation.paths import PERSONS_DIR, PROVINCES_DIR, REPO_ROOT

    records_dir = Path(args.records)
    records_dir.mkdir(parents=True, exist_ok=True)
    roots = [PERSONS_DIR]
    if PROVINCES_DIR.exists():
        roots.extend(p / "persons" for p in sorted(PROVINCES_DIR.iterdir()) if p.is_dir())

    target = records_dir / "profile_documents.jsonl"
    previous_rows, by_id = _existing_documents(target)
    files = _profile_files(roots)

    # Resolve overlapping roots to one source, and detect old relative-path IDs
    # that could correspond to several distinct profiles in different provinces.
    sources: dict[str, dict[str, Any]] = {}
    relative_sources: dict[str, set[str]] = {}
    for item in files:
        key = _source_key(item["path"], REPO_ROOT)
        sources.setdefault(key, item)
        relative_sources.setdefault(item["rel"], set()).add(key)

    staged: list[dict[str, Any]] = []
    skipped = 0
    for source_key, item in sorted(sources.items()):
        try:
            data = json.loads(item["path"].read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            skipped += 1
            continue
        if not isinstance(data, dict):
            raise ValueError(f"profile must be a JSON object: {item['path']}")

        row = _profile_to_document(data, source_key)
        new_id = row["profile_id"]
        legacy_id = _profile_to_document(data, item["rel"])["profile_id"]
        old = by_id.get(new_id)
        legacy = by_id.get(legacy_id) if legacy_id != new_id else None

        if legacy is not None and len(relative_sources[item["rel"]]) > 1:
            raise ValueError(
                f"ambiguous legacy profile_id {legacy_id}: {item['rel']} exists in "
                "multiple source roots; migrate with provenance review"
            )
        if old is not None and legacy is not None:
            raise ValueError(
                f"both legacy and namespaced profile IDs exist for {item['path']}; "
                "reconcile duplicates before importing"
            )
        if old is None and legacy is not None:
            # Keep a historical ID only when one source can own it. Never
            # create a second record for the same existing profile on upgrade.
            row["profile_id"] = legacy_id
            old = legacy
        if old is not None:
            if old != row:
                raise ValueError(
                    f"profile changed or ID collided: {item['path']} "
                    "(review and version the existing canonical record explicitly)"
                )
            continue
        by_id[new_id] = row
        staged.append(row)

    if staged:
        write_jsonl(target, iter(previous_rows + staged))
    print(
        f"profiles: scanned={len(sources)} added={len(staged)} "
        f"skipped={skipped} total_records={len(previous_rows) + len(staged)}"
    )
    return 0
