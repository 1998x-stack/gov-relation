#!/usr/bin/env python3
"""Build 林周县 (拉萨市, 西藏自治区) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Sogou + 百度百科.
Current: 县长德吉央宗(女/中共党员, 县委副书记/县长), 县委书记高军(候选,plausible).
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "林周县"
STAGING = data_path("tmp", "西藏自治区_林周县")
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
    {"id": 1, "name": "德吉央宗", "gender": "女", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县长", "current_org": "林周县人民政府",
     "source": "百度百科(德吉央宗,女,中共党员,现任西藏自治区拉萨市林周县委副书记、县长)"},
    {"id": 2, "name": "高军", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "县委书记(候选)", "current_org": "中共林周县委",
     "source": "相关检索(林周县县委书记高军简介, plausible)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共林周县委", "type": "党委", "level": "县级(县)", "parent": "中共拉萨市委", "location": "拉萨市林周县"},
    {"id": 102, "name": "林周县人民政府", "type": "政府", "level": "县级(县)", "parent": "拉萨市人民政府", "location": "拉萨市林周县"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 102, "title": "县长", "start": "", "end": "", "rank": "正处级", "note": "县委副书记/县长"},
    {"person_id": 2, "org_id": 101, "title": "县委书记(候选)", "start": "", "end": "", "rank": "正处级", "note": "相关检索(plausible)"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县长-县委书记", "overlap_org": "中共林周县委/林周县人民政府", "overlap_period": "当前"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
