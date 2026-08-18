#!/usr/bin/env python3
"""Build 龙泉驿区 (成都市, 四川省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Sogou(15篇资料汇总).
Current: 区长周健(区委副书记/区政府党组书记/成都经开区党工委副书记管委会主任). 区委书记待核.
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "龙泉驿区"
STAGING = data_path("tmp", "四川省_龙泉驿区")
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
    {"id": 1, "name": "周健", "gender": "男", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区长", "current_org": "成都市龙泉驿区人民政府",
     "source": "Sogou(注:成都龙泉驿区现任区长周健,区委副书记、区政府党组书记,兼成都经开区党工委副书记、管委会主任)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共成都市龙泉驿区委", "type": "党委", "level": "县级(区级)", "parent": "中共成都市委", "location": "成都市龙泉驿区"},
    {"id": 102, "name": "成都市龙泉驿区人民政府", "type": "政府", "level": "县级(区级)", "parent": "成都市人民政府", "location": "成都市龙泉驿区"},
    {"id": 103, "name": "成都经济技术开发区管委会", "type": "开发区", "level": "国家级经开区", "parent": "成都市", "location": "成都市龙泉驿区"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 102, "title": "区长", "start": "", "end": "", "rank": "正处级", "note": "区委副书记/区政府党组书记"},
    {"person_id": 1, "org_id": 103, "title": "管委会主任", "start": "", "end": "", "rank": "副厅级(兼)", "note": "成都经开区党工委副书记/管委会主任"},
]

RELATIONSHIPS = []

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
