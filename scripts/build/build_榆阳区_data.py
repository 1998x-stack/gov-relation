#!/usr/bin/env python3
"""Build 榆阳区 (榆林市, 陕西省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via 360 search + 网易新闻/官方任免.
Current (2026): 区委书记杨政(2025-07,confirmed). 区长崔飞(plausible). 前任书记李忠宏.
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "榆阳区"
STAGING = data_path("tmp", "陕西省_榆阳区")
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
    {"id": 1, "name": "杨政", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委书记", "current_org": "中共榆林市榆阳区委",
     "source": "网易新闻(2025-07-30 全区领导干部大会宣布省委、市委决定任榆阳区委书记)"},
    {"id": 2, "name": "崔飞", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "区长", "current_org": "榆林市榆阳区人民政府",
     "source": "相关检索(榆林市榆阳区区长崔飞简历)"},
    {"id": 3, "name": "李忠宏", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "(前任)区委书记", "current_org": "中共榆林市榆阳区委",
     "source": "相关检索(榆林市榆阳区委书记李忠宏)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共榆林市榆阳区委", "type": "党委", "level": "县级(区级)", "parent": "中共榆林市委", "location": "榆林市榆阳区"},
    {"id": 102, "name": "榆林市榆阳区人民政府", "type": "政府", "level": "县级(区级)", "parent": "榆林市人民政府", "location": "榆林市榆阳区"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "区委书记", "start": "2025-07", "end": "", "rank": "副厅级", "note": "2025-07 任"},
    {"person_id": 2, "org_id": 102, "title": "区长", "start": "", "end": "", "rank": "正处级", "note": "待核实"},
    {"person_id": 3, "org_id": 101, "title": "前任区委书记", "start": "", "end": "2025-07", "rank": "副厅级", "note": "杨政2025-07接任"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记-区长", "overlap_org": "中共榆林市榆阳区委/榆阳区人民政府", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 3, "type": "前任-继任", "context": "榆阳区委书记前任/继任(杨继李)", "overlap_org": "中共榆林市榆阳区委", "overlap_period": "2025-07 前后"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
