#!/usr/bin/env python3
"""Build 义乌市 (金华市, 浙江省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via 360 search + 澎湃新闻/时政湃.
Current (2026): 市委书记叶帮锐(2025-01), 市长温建飞. Predecessor 林毅.
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "义乌市"
STAGING = data_path("tmp", "浙江省_义乌市")
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
    {"id": 1, "name": "叶帮锐", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "市委书记", "current_org": "中共义乌市委",
     "source": "澎湃新闻/时政派(2025-01-27 省委决定任中共金华市委常委、义乌市委书记)"},
    {"id": 2, "name": "温建飞", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "市长", "current_org": "义乌市人民政府",
     "source": "澎湃新闻(2025-01-27 提名为义乌市长候选人)"},
    {"id": 3, "name": "林毅", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "(前任)市委书记", "current_org": "中共义乌市委",
     "source": "相关检索(义乌市委书记林毅简历)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共义乌市委", "type": "党委", "level": "县级市", "parent": "中共金华市委", "location": "金华市义乌市"},
    {"id": 102, "name": "义乌市人民政府", "type": "政府", "level": "县级市", "parent": "金华市人民政府", "location": "金华市义乌市"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "市委书记", "start": "2025-01", "end": "", "rank": "副厅级(金华市委常委兼)", "note": "2025-01 任"},
    {"person_id": 2, "org_id": 102, "title": "市长", "start": "", "end": "", "rank": "正处级", "note": "2025-01 提名;待核实"},
    {"person_id": 3, "org_id": 101, "title": "前任市委书记", "start": "", "end": "2025-01", "rank": "副厅级/正处级", "note": "叶帮锐2025-01接任"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "市委书记-市长", "overlap_org": "中共义乌市委/义乌市人民政府", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 3, "type": "前任-继任", "context": "义乌市委书记前任/继任", "overlap_org": "中共义乌市委", "overlap_period": "2025-01 前后"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
