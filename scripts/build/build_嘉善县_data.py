#!/usr/bin/env python3
"""Build 嘉善县 (嘉兴市, 浙江省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Baidu + 嘉善版数字报.
Current: 县委书记江海洋(嘉兴市委常委兼), 县长张锡锋(2021-11任代县长后转正).
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "嘉善县"
STAGING = data_path("tmp", "浙江省_嘉善县")
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
    {"id": 1, "name": "江海洋", "gender": "男", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委书记/嘉兴市委常委", "current_org": "中共嘉善县委",
     "source": "百度/嘉善数字报(嘉兴市委常委、嘉善县委书记江海洋)"},
    {"id": 2, "name": "张锡锋", "gender": "男", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县长", "current_org": "嘉善县人民政府",
     "source": "嘉善版数字报(县人大常委会第40次会议决定张锡锋为代理县长,2021-11-29)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共嘉善县委", "type": "党委", "level": "县级(县)", "parent": "中共嘉兴市委", "location": "嘉兴市嘉善县"},
    {"id": 102, "name": "嘉善县人民政府", "type": "政府", "level": "县级(县)", "parent": "嘉兴市人民政府", "location": "嘉兴市嘉善县"},
    {"id": 103, "name": "中共嘉兴市委", "type": "党委", "level": "地级市", "parent": "中共浙江省委", "location": "嘉兴市"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 103, "title": "嘉兴市委常委", "start": "", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 101, "title": "县委书记", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 102, "title": "县长", "start": "2021-11", "end": "", "rank": "正处级", "note": "2021-11代理县长后任县长"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记-县长", "overlap_org": "中共嘉善县委/嘉善县人民政府", "overlap_period": "当前"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
