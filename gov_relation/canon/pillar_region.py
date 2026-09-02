"""Pillar A — 地区生成扩展（P 分区分 + 写 canonical JSONL）。

把一个地区（region）的 persons/organizations/positions/relationships 列表
写作规范分区 JSONL：``data/records/regions/<province>/<slug>/`` 下每个实体类型
一条流。这是步骤 3 的目标形态——生成器不再写 legacy SQLite 地区库，而是写
canonical 地区 JSONL，再经 ``gov2 backup`` 聚合进统一 SQLite 备份。

设计
----
- 地区包 = 一个 slug 对应 4 类基元(others…)的 JSONL，ID 以``<slug>:``为前缀，避免跨地区撞车。
- ``manifest.json``(地区级)记录该地区每流的 count/sha256，便于复核。
- ``backup`` 目前聚合统一库；地区级聚合由统一入库(importer/govdb)负责(步骤3后续)。
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .streams import iter_jsonl, write_jsonl


def _entity_id(slug: str, kind: str, raw: Any) -> str:
    """Stable region-scoped id (never collision-prone across regions)."""
    return f"{slug}:{kind}:{raw}"


def region_records(
    slug: str,
    *,
    persons: list[dict],
    organizations: list[dict],
    positions: list[dict],
    relationships: list[dict],
) -> dict[str, list[dict]]:
    """Convert a legacy-lists region build into canonical entity streams."""
    out: dict[str, list[dict]] = {
        "persons": [],
        "organizations": [],
        "positions": [],
        "relationships": [],
    }
    pkey = {}
    for i, p in enumerate(persons):
        rid = _entity_id(slug, "person", p.get("id", i))
        pkey[str(p.get("id", i))] = rid
        out["persons"].append({
            "person_id": rid,
            "canonical_name": p.get("name", ""),
            "normalized_name": p.get("name", ""),
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth_text": p.get("birth", ""),
            "birth_precision": "unknown",
            "birthplace": p.get("birthplace", ""),
            "native_place": p.get("native_place", ""),
            "education": str(p.get("education", "")),
            "party_join_text": p.get("party_join", ""),
            "work_start_text": p.get("work_start", ""),
            "identity_status": "probable",
            "merged_into_id": None,
            "created_at": None,
            "updated_at": None,
        })
    for i, o in enumerate(organizations):
        rid = _entity_id(slug, "org", o.get("id", i))
        out["organizations"].append({
            "organization_id": rid,
            "jurisdiction_id": None,
            "parent_organization_id": None,
            "canonical_name": o.get("name", ""),
            "normalized_name": o.get("name", ""),
            "organization_type": o.get("type", ""),
            "administrative_level": o.get("level", ""),
            "location_text": o.get("location", ""),
            "valid_from": None,
            "valid_to": None,
            "created_at": None,
        })
    for i, pos in enumerate(positions):
        pid = pos.get("person_id")
        pid = pkey.get(str(pid), f"{slug}:person:{pid}")
        out["positions"].append({
            "position_id": _entity_id(slug, "pos", i),
            "person_id": pid,
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
    for i, r in enumerate(relationships):
        a = pkey.get(str(r.get("person_a", "")), r.get("person_a", ""))
        b = pkey.get(str(r.get("person_b", "")), r.get("person_b", ""))
        out["relationships"].append({
            "relationship_id": _entity_id(slug, "rel", i),
            "person_from_id": a,
            "person_to_id": b,
            "relationship_type": r.get("type", ""),
            "direction": r.get("direction", "undirected"),
            "strength": r.get("strength", "unknown"),
            "confidence": r.get("confidence", "plausible"),
            "context": r.get("context", ""),
            "evidence_summary": r.get("evidence", ""),
            "overlap_organization_id": None,
            "overlap_organization_text": r.get("overlap_org", ""),
            "overlap_period_text": r.get("overlap_period", ""),
            "valid_from": None,
            "valid_to": None,
        })
    return out


def write_region(records_root: Path, slug: str, province: str, streams: dict[str, list[dict]]) -> Path:
    """Write per-type region JSONL under records/regions/<province>/<slug>/."""
    pdir = records_root / "regions" / _slug_clean(province, slug)
    pdir.mkdir(parents=True, exist_ok=True)
    count = 0
    for kind, rows in streams.items():
        if rows:
            write_jsonl(pdir / f"{kind}.jsonl", iter(rows))
            count += len(rows)
    meta = {"province": province, "slug": slug, "entity_count": count}
    (pdir / ".meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return pdir


def _slug_clean(province: str, slug: str) -> str:
    import re
    p = re.sub(r"[\s/\\]", "_", str(province))
    s = re.sub(r"[\s/\\]", "_", str(slug))
    return f"{p}__{s}"


def snapshot_regions(records_root) -> dict[str, int]:
    """Aggregate all region partitions into the flat unified streams (idempotent)."""
    from .streams import iter_jsonl, write_jsonl

    records_root = Path(records_root)
    regions_root = records_root / "regions"
    kinds = ("persons", "organizations", "positions", "relationships")
    total: dict[str, int] = {}
    if not regions_root.exists():
        return total
    for kind in kinds:
        paths = sorted(regions_root.rglob(f"{kind}.jsonl"))
        target = records_root / f"{kind}.jsonl"
        existing = {str(r.get(_ID_BY_KIND.get(kind, "id"))) for r in iter_jsonl(target)} if target.exists() else set()
        added = 0
        rows = []
        for p in paths:
            for r in iter_jsonl(p):
                if str(r.get(_ID_BY_KIND.get(kind, "id"))) in existing:
                    continue
                existing.add(str(r.get(_ID_BY_KIND.get(kind, "id"))))
                rows.append(r)
        if rows:
            merged = list(iter_jsonl(target)) if target.exists() else []
            merged.extend(rows)
            write_jsonl(target, iter(merged))
        total[kind] = len(rows)
    return total


_ID_BY_KIND = {
    "persons": "person_id",
    "organizations": "organization_id",
    "positions": "position_id",
    "relationships": "relationship_id",
}


def pillar_build_region(args) -> int:
    """gov2 region --province .. --slug .. --persons .. writes canonical region JSONL."""
    import json as _json
    with open(args.spec, encoding="utf-8") as fh:
        spec = _json.load(fh)
    rec = region_records(
        args.slug,
        persons=spec.get("persons", []),
        organizations=spec.get("organizations", []),
        positions=spec.get("positions", []),
        relationships=spec.get("relationships", []),
    )
    from gov_relation.paths import DATA_DIR
    root = Path(args.records) if args.records else DATA_DIR / "records"
    pdir = write_region(root, args.slug, args.province, rec)
    print("wrote region:", pdir, "counts:", {k: len(v) for k, v in rec.items()})
    return 0