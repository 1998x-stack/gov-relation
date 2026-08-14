#!/usr/bin/env python3
"""Repair-run an OLD-format build script (string person/org IDs) against the
current integer-id schema.

Some legacy build scripts (e.g. 商南县) use string IDs like
"shangnan_liu_hua" / "org_cpc_shangnan" in persons/positions/relationships.
Current gov_relation.schema requires INTEGER ids. This adapter AST-parses the
four list vars, remaps string ids to sequential integers consistently, and
invokes run_build into a staging dir.

Usage:
  python3 scripts/tools/run_old_format_build.py --build scripts/build/build_商南县_data.py \
      --stage data/tmp/shaanxi_商南县 --region 商南县
"""
from __future__ import annotations

import argparse
import ast
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))


def load_lists(path: Path) -> dict:
    src = path.read_text(encoding="utf-8")
    tree = ast.parse(src)
    out = {"PERSONS": [], "ORGANIZATIONS": [], "POSITIONS": [], "RELATIONSHIPS": []}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                name = getattr(target, "id", "")
                if name in out and isinstance(node.value, ast.List):
                    try:
                        out[name] = ast.literal_eval(node.value)
                    except Exception as e:
                        print(f"  WARN {name}: could not literal-eval ({e}); skipping")
    return out


def _is_int(x) -> bool:
    if isinstance(x, int):
        return True
    try:
        int(str(x).replace("_", ""))
        return x is not None
    except (ValueError, TypeError):
        return False


def remap(data: dict) -> dict:
    # persons first (authoritative ids) — assign sequential int to string ids
    persons = []
    pid_to_int = {}
    next_id = 1
    for p in data["PERSONS"]:
        orig = p.get("id")
        if _is_int(orig):
            iid = int(orig)
        else:
            iid = next_id
            next_id += 1
        pid_to_int[str(orig)] = iid
        p["id"] = iid
        persons.append(p)
    # organizations
    orgs, oid_to_int = [], {}
    for o in data["ORGANIZATIONS"]:
        orig = o.get("id")
        if _is_int(orig):
            iid = orig
        else:
            iid = next_id
            next_id += 1
        oid_to_int[str(orig)] = iid
        o["id"] = iid
        orgs.append(o)
    # positions
    positions = []
    for pos in data["POSITIONS"]:
        pos["person_id"] = pid_to_int.get(str(pos.get("person_id")), pos["person_id"])
        pos["org_id"] = oid_to_int.get(str(pos.get("org_id")), pos["org_id"])
        positions.append(pos)
    # relationships
    relationships = []
    for r in data["RELATIONSHIPS"]:
        r = dict(r)
        r["person_a"] = pid_to_int.get(str(r.get("person_a")), r["person_a"])
        r["person_b"] = pid_to_int.get(str(r.get("person_b")), r["person_b"])
        relationships.append(r)
    return {"persons": persons, "organizations": orgs,
            "positions": positions, "relationships": relationships}


def main_run() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", required=True)
    ap.add_argument("--stage", required=True)
    ap.add_argument("--region", required=True)
    a = ap.parse_args()

    data = load_lists(Path(a.build).resolve())
    fixed = remap(data)

    import sqlite3  # noqa
    from gov_relation.runner import run_build
    stage = Path(a.stage).resolve()
    stage.mkdir(parents=True, exist_ok=True)
    run_build(
        slug=a.region,
        persons=fixed["persons"],
        organizations=fixed["organizations"],
        positions=fixed["positions"],
        relationships=fixed["relationships"],
        db_path=stage / f"{a.region}_network.db",
        gexf_path=stage / f"{a.region}_network.gexf",
        overwrite=True,
    )
    print(f"[repair-run] OK wrote {a.region}_network.db/.gexf -> {stage}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main_run())