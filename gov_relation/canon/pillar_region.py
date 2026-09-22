"""Create canonical region partitions and refresh their flat JSONL snapshots.

Flat streams can also hold independently imported records. Snapshot ownership is
tracked separately so updating/removing a region does not delete unrelated data.
"""

from __future__ import annotations

import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any

from .streams import iter_jsonl, jsonl_sha256, write_jsonl

_ID_BY_KIND = {
    "persons": "person_id",
    "organizations": "organization_id",
    "positions": "position_id",
    "relationships": "relationship_id",
}
_STATE_FILE = ".region_snapshot_state.json"


def _entity_id(slug: str, kind: str, raw: Any) -> str:
    return f"{slug}:{kind}:{raw}"


def region_records(
    slug: str,
    *,
    persons: list[dict],
    organizations: list[dict],
    positions: list[dict],
    relationships: list[dict],
) -> dict[str, list[dict]]:
    """Convert a legacy region build into canonical entity streams."""
    out: dict[str, list[dict]] = {kind: [] for kind in _ID_BY_KIND}
    pkey: dict[str, str] = {}
    for i, person in enumerate(persons):
        raw_id = person.get("id", i)
        rid = _entity_id(slug, "person", raw_id)
        if str(raw_id) in pkey:
            raise ValueError(f"Duplicate person ID in region {slug!r}: {raw_id!r}")
        pkey[str(raw_id)] = rid
        out["persons"].append({
            "person_id": rid,
            "canonical_name": person.get("name", ""),
            "normalized_name": person.get("name", ""),
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth_text": person.get("birth", ""),
            "birth_precision": "unknown",
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("native_place", ""),
            "education": str(person.get("education", "")),
            "party_join_text": person.get("party_join", ""),
            "work_start_text": person.get("work_start", ""),
            "identity_status": "probable",
            "merged_into_id": None,
            "created_at": None,
            "updated_at": None,
        })
    for i, org in enumerate(organizations):
        rid = _entity_id(slug, "org", org.get("id", i))
        out["organizations"].append({
            "organization_id": rid,
            "jurisdiction_id": None,
            "parent_organization_id": None,
            "canonical_name": org.get("name", ""),
            "normalized_name": org.get("name", ""),
            "organization_type": org.get("type", ""),
            "administrative_level": org.get("level", ""),
            "location_text": org.get("location", ""),
            "valid_from": None,
            "valid_to": None,
            "created_at": None,
        })
    for i, pos in enumerate(positions):
        person_id = pos.get("person_id")
        person_id = pkey.get(str(person_id), _entity_id(slug, "person", person_id))
        out["positions"].append({
            "position_id": _entity_id(slug, "pos", i),
            "person_id": person_id,
            "organization_id": None,
            "organization_text": pos.get("org", ""),
            "title": pos.get("title", ""),
            "rank": pos.get("rank", ""),
            "category": "",
            "title_category": "",
            "start_text": pos.get("start_date", ""),
            "end_text": pos.get("end_date", ""),
            "start_date": pos.get("start_date", ""),
            "end_date": pos.get("end_date", ""),
            "date_precision": "unknown",
            "is_current": 0,
            "sort_order": i,
            "confidence": pos.get("confidence", "plausible"),
            "notes": pos.get("note", ""),
        })
    for i, rel in enumerate(relationships):
        a = pkey.get(str(rel.get("person_a", "")), rel.get("person_a", ""))
        b = pkey.get(str(rel.get("person_b", "")), rel.get("person_b", ""))
        out["relationships"].append({
            "relationship_id": _entity_id(slug, "rel", i),
            "person_from_id": a,
            "person_to_id": b,
            "relationship_type": rel.get("type", ""),
            "direction": rel.get("direction", "undirected"),
            "strength": rel.get("strength", "unknown"),
            "confidence": rel.get("confidence", "plausible"),
            "context": rel.get("context", ""),
            "evidence_summary": rel.get("evidence", ""),
            "overlap_organization_id": None,
            "overlap_organization_text": rel.get("overlap_org", ""),
            "overlap_period_text": rel.get("overlap_period", ""),
            "valid_from": None,
            "valid_to": None,
        })
    return out


def _slug_clean(province: str, slug: str) -> str:
    p = re.sub(r"[\s/\\]", "_", str(province))
    s = re.sub(r"[\s/\\]", "_", str(slug))
    return f"{p}__{s}"


def write_region(records_root: Path, slug: str, province: str, streams: dict[str, list[dict]]) -> Path:
    """Replace a region's four partitions, including any that became empty."""
    pdir = Path(records_root) / "regions" / _slug_clean(province, slug)
    pdir.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for kind in _ID_BY_KIND:
        rows = streams.get(kind, [])
        target = pdir / f"{kind}.jsonl"
        if rows:
            write_jsonl(target, iter(rows))
            manifest[kind] = {"count": len(rows), "sha256": jsonl_sha256(target)}
        else:
            target.unlink(missing_ok=True)
    meta = {
        "province": province,
        "slug": slug,
        "entity_count": sum(item["count"] for item in manifest.values()),
        "record_streams": manifest,
    }
    (pdir / ".meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8"
    )
    return pdir


def _read_state(path: Path) -> dict[str, set[str]]:
    if not path.exists():
        return {kind: set() for kind in _ID_BY_KIND}
    state = json.loads(path.read_text(encoding="utf-8"))
    if state.get("version") != 1 or not isinstance(state.get("owned_ids"), dict):
        raise ValueError("Unsupported region snapshot state; do not overwrite existing streams")
    owned = state["owned_ids"]
    if any(not isinstance(owned.get(kind, []), list) for kind in _ID_BY_KIND):
        raise ValueError("Invalid region snapshot ownership state")
    return {kind: set(owned.get(kind, [])) for kind in _ID_BY_KIND}


def _row_id(row: dict, id_key: str, path: Path) -> str:
    if not isinstance(row, dict):
        raise ValueError(f"Expected JSON object in {path}")
    value = row.get(id_key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"Missing string {id_key} in {path}")
    return value


def snapshot_regions(records_root: Path | str) -> dict[str, int]:
    """Refresh region-owned records, retaining unrelated flat stream records.

    Existing generated rows without a state file can be adopted only when they
    exactly match their partition. A conflicting flat row is never overwritten
    without proof that the prior snapshot owned that ID.
    """
    records_root = Path(records_root)
    regions_root = records_root / "regions"
    if not regions_root.exists():
        return {}
    state_path = records_root / _STATE_FILE
    previously_owned = _read_state(state_path)
    replacements: dict[str, list[dict]] = {}
    new_owned: dict[str, set[str]] = {}
    totals: dict[str, int] = {}

    # Validate every stream before writing any flat output.
    for kind, id_key in _ID_BY_KIND.items():
        region_rows: dict[str, dict] = {}
        owners: dict[str, Path] = {}
        for partition in sorted(regions_root.rglob(f"{kind}.jsonl")):
            for row in iter_jsonl(partition):
                rid = _row_id(row, id_key, partition)
                if rid in region_rows:
                    raise ValueError(
                        f"Duplicate {kind} ID {rid!r} across {owners[rid]} and {partition}"
                    )
                region_rows[rid] = row
                owners[rid] = partition
        target = records_root / f"{kind}.jsonl"
        flat_rows: dict[str, dict] = {}
        flat_order: list[str] = []
        if target.exists():
            for row in iter_jsonl(target):
                rid = _row_id(row, id_key, target)
                if rid in flat_rows:
                    raise ValueError(f"Duplicate {kind} ID {rid!r} in {target}")
                flat_rows[rid] = row
                flat_order.append(rid)
        for rid, row in region_rows.items():
            if rid in flat_rows and rid not in previously_owned[kind] and flat_rows[rid] != row:
                raise ValueError(
                    f"Unowned flat {kind} record {rid!r} conflicts with a region partition; "
                    "rebuild the disposable flat stream from verified sources"
                )
        independent = [flat_rows[rid] for rid in flat_order if rid not in previously_owned[kind] and rid not in region_rows]
        # Keep existing row order, replacing region-owned rows in place.
        merged: list[dict] = []
        included: set[str] = set()
        for rid in flat_order:
            if rid in region_rows:
                merged.append(region_rows[rid])
                included.add(rid)
            elif rid not in previously_owned[kind]:
                merged.append(flat_rows[rid])
        for rid, row in region_rows.items():
            if rid not in included:
                merged.append(row)
        replacements[kind] = merged
        new_owned[kind] = set(region_rows)
        totals[kind] = len(set(region_rows) - set(flat_rows))

    for kind, rows in replacements.items():
        target = records_root / f"{kind}.jsonl"
        if rows or target.exists():
            write_jsonl(target, iter(rows))
    state = {"version": 1, "owned_ids": {kind: sorted(ids) for kind, ids in new_owned.items()}}
    fd, temp_path = tempfile.mkstemp(prefix=".region-snapshot-", suffix=".tmp", dir=records_root)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as file:
            json.dump(state, file, ensure_ascii=False, sort_keys=True)
            file.write("\n")
        os.replace(temp_path, state_path)
    except BaseException:
        Path(temp_path).unlink(missing_ok=True)
        raise
    return totals


def pillar_build_region(args) -> int:
    """gov2 region --province ... --slug ... --spec ..."""
    with open(args.spec, encoding="utf-8") as file:
        spec = json.load(file)
    rec = region_records(
        args.slug,
        persons=spec.get("persons", []),
        organizations=spec.get("organizations", []),
        positions=spec.get("positions", []),
        relationships=spec.get("relationships", []),
    )
    from gov_relation.paths import DATA_DIR

    root = Path(args.records) if args.records else DATA_DIR / "records"
    path = write_region(root, args.slug, args.province, rec)
    print("wrote region:", path, "counts:", {kind: len(rows) for kind, rows in rec.items()})
    return 0
