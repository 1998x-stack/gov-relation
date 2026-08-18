#!/usr/bin/env python3
"""Build 桑珠孜区 (日喀则市, 西藏自治区) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via 360搜索 + 桑珠孜区政府新闻网(官方).
Current: 区委书记陈钢(主持召开区委常委会议/督导重点工作, 2026). 区长待核.
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "桑珠孜区"
STAGING = data_path("tmp", "西藏自治区_桑珠孜区")
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
    {"id": 1, "name": "陈钢", "gender": "男", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委书记", "current_org": "中共桑珠孜区委",
     "source": "桑珠孜区政府新闻网(陈钢主持召开桑珠孜区委常委会会议/督导重点工作, 2026-06在任)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共桑珠孜区委", "type": "党委", "level": "县级(区级)", "parent": "中共日喀则市委", "location": "日喀则市桑珠孜区"},
    {"id": 102, "name": "桑珠孜区人民政府", "type": "政府", "level": "县级(区级)", "parent": "日喀则市人民政府", "location": "日喀则市桑珠孜区"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "区委书记", "start": "", "end": "", "rank": "正处级", "note": "2026-06在任"},
]

RELATIONSHIPS = []

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
