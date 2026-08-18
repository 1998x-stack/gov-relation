#!/usr/bin/env python3
"""Build 云冈区 (大同市, 山西省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Sogou + 手机搜狐/省委拟任职公示(2024-10).
Current: 区委书记刘利新(1975-09/大学/中共党员/曾任区长,2024-10拟任/现任). 区长郝源(plausible).
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "云冈区"
STAGING = data_path("tmp", "山西省_云冈区")
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

def _verify_db():
    conn = sqlite3.connect(str(DB_PATH))
    for table in ("persons", "organizations", "positions", "relationships"):
        try:
            n = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"  {table}: {n} rows")
        except Exception as exc:
            print(f"  {table}: (none) {exc}")
    conn.close()

PERSONS = [
    {"id": 1, "name": "刘利新", "gender": "男", "birth": "1975-09",
     "birthplace": "", "education": "大学", "party_join": "中共党员", "work_start": "",
     "current_post": "区委书记", "current_org": "中共大同市云冈区委",
     "source": "山西省委组织部拟任公示/手机搜狐(刘利新,1975-09,大学,曾任云冈区委副书记/区长,2024-10拟任现任区委书记)"},
    {"id": 2, "name": "郝源", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区长(plausible)", "current_org": "云冈区人民政府",
     "source": "相关检索(大同云冈区区长郝源, plausible)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共大同市云冈区委", "type": "党委", "level": "县级(区级)", "parent": "中共大同市委", "location": "大同市云冈区"},
    {"id": 102, "name": "大同市云冈区人民政府", "type": "政府", "level": "县级(区级)", "parent": "大同市人民政府", "location": "大同市云冈区"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "区委书记", "start": "2024-10", "end": "", "rank": "正处级", "note": "2024-10省委拟任/现任"},
    {"person_id": 1, "org_id": 102, "title": "区长(前)", "start": "", "end": "2024", "rank": "正处级", "note": "曾任区委副书记/区长"},
    {"person_id": 2, "org_id": 102, "title": "区长(plausible)", "start": "", "end": "", "rank": "正处级", "note": "待核实"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "前任-继任", "context": "刘利新(区长升书记)-郝源(区长候选)", "overlap_org": "大同市云冈区人民政府", "overlap_period": "2024-2025"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
