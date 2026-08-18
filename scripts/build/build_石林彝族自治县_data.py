#!/usr/bin/env python3
"""Build 石林彝族自治县 (昆明市, 云南省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Baidu(百度百科/石林县政府官网).
Current: 县委书记杨泽松(1975-04/云南嵩明/兼县人武部党委第一书记/石林产业园区党工委书记), 代县长高鸣.
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "石林彝族自治县"
STAGING = data_path("tmp", "云南省_石林彝族自治县")
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
    {"id": 1, "name": "杨泽松", "gender": "男", "birth": "1975-04",
     "birthplace": "云南嵩明", "education": "大学本科", "party_join": "中共党员(2001-11入党)", "work_start": "1994-09",
     "current_post": "县委书记", "current_org": "中共石林县委",
     "source": "百度百科/石林县政府官网(现任石林县委书记、县人武部党委第一书记、兼石林产业园区党工委书记)"},
    {"id": 2, "name": "高鸣", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委副书记/代县长", "current_org": "石林县人民政府",
     "source": "石林县政府官网(县委副书记、代理县长)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共石林彝族自治县委", "type": "党委", "level": "县级(自治县)", "parent": "中共昆明市委", "location": "昆明市石林县"},
    {"id": 102, "name": "石林彝族自治县人民政府", "type": "政府", "level": "县级(自治县)", "parent": "昆明市人民政府", "location": "昆明市石林县"},
    {"id": 103, "name": "云南石林产业园区党工委", "type": "党工委", "level": "园区", "parent": "", "location": "石林县"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "县委书记", "start": "", "end": "", "rank": "正处级", "note": "兼县人武部党委第一书记"},
    {"person_id": 1, "org_id": 103, "title": "石林产业园区党工委书记(兼)", "start": "", "end": "", "rank": "兼", "note": ""},
    {"person_id": 2, "org_id": 102, "title": "县委副书记/代理县长", "start": "", "end": "", "rank": "正处级", "note": ""},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记-代理县长", "overlap_org": "中共石林县委/石林县人民政府", "overlap_period": "2026"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
