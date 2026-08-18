#!/usr/bin/env python3
"""Build 泽州县 (晋城市, 山西省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Sogou + 泽州县人民政府官网(权威机构).
Current: 县长武小雅(女/1977-12, 县委副书记/县政府党组书记, 2026-08-02官网). 县委书记待核.
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "泽州县"
STAGING = data_path("tmp", "山西省_泽州县")
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
    {"id": 1, "name": "武小雅", "gender": "女", "birth": "1977-12",
     "birthplace": "", "education": "中央党校大学", "degre": "法律硕士", "party_join": "中共党员", "work_start": "",
     "current_post": "县长", "current_org": "泽州县人民政府",
     "source": "泽州县人民政府官网(武小雅,现任县委副书记、县政府党组书记、县长,2026-08-02)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共泽州县委", "type": "党委", "level": "县级(县)", "parent": "中共晋城市委", "location": "晋城市泽州县"},
    {"id": 102, "name": "泽州县人民政府", "type": "政府", "level": "县级(县)", "parent": "晋城市人民政府", "location": "晋城市泽州县"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 102, "title": "县长", "start": "", "end": "", "rank": "正处级", "note": "县委副书记/县政府党组书记"},
]

RELATIONSHIPS = []

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
