#!/usr/bin/env python3
"""Build 武乡县 (长治市, 山西省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Sogou + 黄河新闻网/武乡融媒(2026-04).
Current: 县委书记张磊(2026-04主持县委常委会). 县长待核.
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "武乡县"
STAGING = data_path("tmp", "山西省_武乡县")
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
    {"id": 1, "name": "张磊", "gender": "男", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委书记", "current_org": "中共武乡县委",
     "source": "黄河新闻网/武乡融媒(2026-04张磊已任长治市武乡县委书记,4月22日主持县委常委会会议)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共武乡县委", "type": "党委", "level": "县级(县)", "parent": "中共长治市委", "location": "长治市武乡县"},
    {"id": 102, "name": "武乡县人民政府", "type": "政府", "level": "县级(县)", "parent": "长治市人民政府", "location": "长治市武乡县"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "县委书记", "start": "2026-04", "end": "", "rank": "正处级", "note": "2026-04在任"},
]

RELATIONSHIPS = []

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
