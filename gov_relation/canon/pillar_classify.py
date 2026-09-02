"""Pillar C — 数据分类/归纳 (data classification / induction).

Reads the canonical JSONL streams and derives taxonomy facets: persons by
jurisdiction / identity-status, positions by system-category, relationships by
type. Outputs are written to ``data/taxonomy/`` as JSONL (one classification
record per line) plus a returned summary.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

from .streams import iter_jsonl


def _load(records_dir: Path, kind: str) -> list[dict]:
    path = records_dir / f"{kind}.jsonl"
    return list(iter_jsonl(path)) if path.exists() else []


def _province_of(person_id: str) -> str:
    """Best-effort province attribution from a person id; never crashes."""
    m = re.search(r"([\u4e00-\u9fff]{2,8}?(?:省|市|自治区|自治州))", person_id)
    if m:
        return m.group(1)
    pieces = person_id.split("_")
    return pieces[0] if pieces and pieces[0] else "unknown"


def classify(records_dir: Path, out_dir: Path) -> dict:
    persons = _load(records_dir, "persons")
    positions = _load(records_dir, "positions")
    relationships = _load(records_dir, "relationships")

    prov_counter = Counter(_province_of(p.get("person_id", "")) for p in persons)
    status_counter = Counter(p.get("identity_status", "unknown") for p in persons)
    category_counter = Counter(p.get("category", "unknown") for p in positions)
    rel_type_counter = Counter(
        r.get("relationship_type", "unknown") for r in relationships
    )

    facets: list[dict] = []
    for value, count in prov_counter.most_common():
        facets.append({"facet": "person_by_province", "value": value, "count": count})
    for value, count in status_counter.most_common():
        facets.append({"facet": "person_by_status", "value": value, "count": count})
    for value, count in category_counter.most_common():
        facets.append({"facet": "position_by_category", "value": value, "count": count})
    for value, count in rel_type_counter.most_common():
        facets.append({"facet": "relationship_by_type", "value": value, "count": count})

    out_dir = out_dir / "taxonomy"
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "classification.jsonl", "w", encoding="utf-8") as fh:
        for f in facets:
            fh.write(json.dumps(f, ensure_ascii=False, sort_keys=True) + "\n")

    return {
        "persons": len(persons),
        "positions": len(positions),
        "relationships": len(relationships),
        "top_provinces": prov_counter.most_common(10),
        "top_status": status_counter.most_common(10),
        "top_categories": category_counter.most_common(10),
        "top_relationship_types": rel_type_counter.most_common(10),
    }


def pillar_classify(args) -> int:
    from gov_relation.paths import DATA_DIR

    records_dir = Path(args.records)
    summary = classify(records_dir, DATA_DIR)
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0