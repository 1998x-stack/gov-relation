#!/usr/bin/env python3
"""One-time full migration from data/database/*_network.db to the central registry.

Reads every region DB, rekeys foreign keys using content hashes, and writes
into province-partitioned central DB files.

Usage:
    python3 scripts/migrate_to_central.py
    python3 scripts/migrate_to_central.py --dry-run
    python3 scripts/migrate_to_central.py --limit 10
    python3 scripts/migrate_to_central.py --resume
    python3 scripts/migrate_to_central.py --province 河南省
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
import time
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.central import Central
from gov_relation.paths import DATABASE_DIR, REGISTRY_DB
from gov_relation.province import build_slug_province_map


def _slug_from_stem(stem: str) -> str:
    """Convert '周口市_network' to '周口市'."""
    return stem.removesuffix("_network")


def _fetch_tuples(conn: sqlite3.Connection, table: str) -> list[dict[str, Any]]:
    """Read all rows from *table*, returning dicts keyed by column name."""
    cur = conn.execute(f"SELECT * FROM [{table}]")
    cols = [desc[0] for desc in cur.description]
    return [{col: (row[i] or "") for i, col in enumerate(cols)} for row in cur.fetchall()]


def migrate_one(db_path: Path, central: Central, slug: str) -> dict[str, int]:
    """Migrate a single region DB to central. Returns stats."""
    stats: dict[str, int] = {"persons": 0, "orgs": 0, "positions": 0, "rels": 0, "conflicts": 0}
    src = sqlite3.connect(str(db_path))
    src.row_factory = sqlite3.Row

    # 1. Persons — collect old id → hash mapping
    persons = _fetch_tuples(src, "persons")
    old_id_to_hash: dict[str, str] = {}
    for p in persons:
        try:
            h = central.merge_person(p)
            old_id_to_hash[str(p.get("id", ""))] = h
            stats["persons"] += 1
        except Exception:
            stats["conflicts"] += 1

    # 2. Organizations — use name as fqn fallback
    orgs_data = _fetch_tuples(src, "organizations")
    old_org_id_to_hash: dict[str, str] = {}
    for o in orgs_data:
        o["province"] = central.province
        o["fqn"] = o.get("fqn", o.get("name", ""))
        o["local_name"] = o.get("local_name", o.get("name", ""))
        try:
            h = central.merge_organization(o)
            old_org_id_to_hash[str(o.get("id", ""))] = h
            stats["orgs"] += 1
        except Exception:
            stats["conflicts"] += 1

    # 3. Positions — rekey foreign keys
    positions = _fetch_tuples(src, "positions")
    for pos in positions:
        p_hash = old_id_to_hash.get(str(pos.get("person_id", "")))
        o_hash = old_org_id_to_hash.get(str(pos.get("org_id", "")))
        if not p_hash or not o_hash:
            stats["conflicts"] += 1
            continue
        entry = {
            "person_hash": p_hash,
            "org_hash": o_hash,
            "title": pos.get("title", ""),
            "start_date": pos.get("start_date", pos.get("start", "")),
            "end_date": pos.get("end_date", pos.get("end", "")),
            "rank": pos.get("rank", ""),
            "note": pos.get("note", ""),
            "province": central.province,
            "source": "",
        }
        try:
            central.insert_position(entry)
            stats["positions"] += 1
        except Exception:
            stats["conflicts"] += 1

    # 4. Relationships — rekey person references
    try:
        rels_data = _fetch_tuples(src, "relationships")
    except Exception:
        rels_data = []
    for rel in rels_data:
        pa = old_id_to_hash.get(str(rel.get("person_a", "")))
        pb = old_id_to_hash.get(str(rel.get("person_b", "")))
        if not pa or not pb:
            stats["conflicts"] += 1
            continue
        entry = {
            "person_a_hash": pa,
            "person_b_hash": pb,
            "type": rel.get("type", ""),
            "context": rel.get("context", ""),
            "overlap_org_hash": "",
            "overlap_period": rel.get("overlap_period", ""),
            "province": central.province,
            "source": "",
        }
        oo = str(rel.get("overlap_org", ""))
        if oo in old_org_id_to_hash:
            entry["overlap_org_hash"] = old_org_id_to_hash[oo]
        try:
            central.insert_relationship(entry)
            stats["rels"] += 1
        except Exception:
            stats["conflicts"] += 1

    src.close()
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description="Migrate per-region DBs to central registry")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no writes")
    parser.add_argument("--limit", type=int, default=0, help="Max DBs to process (0 = all)")
    parser.add_argument("--resume", action="store_true", help="Skip already-migrated DBs")
    parser.add_argument("--province", help="Only migrate DBs in this province")
    args = parser.parse_args()

    print("Building slug → province map from TODO.json ...")
    slug_map = build_slug_province_map()

    db_files = sorted(DATABASE_DIR.glob("*_network.db"))
    if not db_files:
        print(f"No *_network.db files found in {DATABASE_DIR}")
        return

    # Prepare registry metadata DB
    REGISTRY_DB.parent.mkdir(parents=True, exist_ok=True)
    reg_conn = sqlite3.connect(str(REGISTRY_DB))
    from gov_relation.schema import create_registry_schema
    create_registry_schema(reg_conn)

    if args.resume:
        already = {r[0] for r in reg_conn.execute("SELECT slug FROM migration_audit").fetchall()}
    else:
        already = set()

    # Select DBs to process
    selected: list[tuple[str, str, Path]] = []
    for f in db_files:
        slug = _slug_from_stem(f.stem)
        if slug in already:
            continue
        province = slug_map.get(slug, "")
        if not province:
            # fuzzy fallback: if the slug ends with a known key
            for key, p in slug_map.items():
                if slug.endswith(key) or key.endswith(slug):
                    province = p
                    break
        if not province:
            print(f"  ⚠ Cannot determine province for '{slug}' — skipping")
            continue
        if args.province and province != args.province:
            continue
        selected.append((province, slug, f))

    if args.dry_run:
        print(f"\nDry run: would process {len(selected)} DBs:")
        for province, slug, path in selected:
            print(f"  {path.name}  →  {province}/{slug}")
        reg_conn.close()
        return

    total = {"persons": 0, "orgs": 0, "positions": 0, "rels": 0, "conflicts": 0}
    start_time = time.time()
    current_province = None
    central = None

    try:
        for i, (province, slug, db_path) in enumerate(selected):
            if args.limit and i >= args.limit:
                break

            if province != current_province:
                if central is not None:
                    central.flush_registry(str(REGISTRY_DB))
                    central.close()
                print(f"\n=== Province: {province} ===")
                central = Central(province)
                current_province = province

            print(f"  [{i+1}/{len(selected)}] {slug} ...", end=" ", flush=True)
            assert central is not None  # set above when province changed
            stats = migrate_one(db_path, central, slug)

            reg_conn.execute(
                """INSERT INTO migration_audit
                   (source_db, slug, province, persons_imported, orgs_imported,
                    positions_imported, rels_imported, merge_conflicts)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (str(db_path), slug, province,
                 stats["persons"], stats["orgs"],
                 stats["positions"], stats["rels"], stats["conflicts"]),
            )
            reg_conn.commit()
            for k in total:
                total[k] += stats[k]
            print(f"ok ({stats['persons']}p/{stats['orgs']}o/"
                  f"{stats['positions']}pos/{stats['rels']}r, {stats['conflicts']} conflicts)")

    finally:
        if central is not None:
            central.flush_registry(str(REGISTRY_DB))
            central.close()
        reg_conn.close()

    elapsed = time.time() - start_time
    print(f"\n Done. Processed {len(selected)} DBs in {elapsed:.1f}s")
    print(f"  Total — persons: {total['persons']}, orgs: {total['orgs']}, "
          f"positions: {total['positions']}, rels: {total['rels']}")
    print(f"  Conflicts: {total['conflicts']} (see merge_conflicts table in registry.db)")


if __name__ == "__main__":
    main()