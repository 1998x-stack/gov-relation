#!/usr/bin/env python3
"""Build 蒲江县 (成都市, 四川省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Sogou + 四川观察/蒲江县人民政府.
Current: 县委书记杨钒(2026-08-10省委/市委决定任命,人大金融本硕), 县长王志海. 前任书记蒲发友.
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "蒲江县"
STAGING = data_path("tmp", "四川省_蒲江县")
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
    {"id": 1, "name": "杨钒", "gender": "男", "birth": "",
     "birthplace": "", "education": "中国人民大学金融学硕士", "party_join": "中共党员", "work_start": "2005-07",
     "current_post": "县委书记", "current_org": "中共蒲江县委",
     "source": "四川观察(2026-08-10成都市蒲江县领导干部大会宣布省委/市委决定,杨钒任蒲江县委书记)"},
    {"id": 2, "name": "王志海", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县长/县委副书记", "current_org": "蒲江县人民政府",
     "source": "蒲江县人民政府领导(县委副书记、县长王志海)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共蒲江县委", "type": "党委", "level": "县级(县)", "parent": "中共成都市委", "location": "成都市蒲江县"},
    {"id": 102, "name": "蒲江县人民政府", "type": "政府", "level": "县级(县)", "parent": "成都市人民政府", "location": "成都市蒲江县"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "县委书记", "start": "2026-08", "end": "", "rank": "正处级", "note": "2026-08-10领导干部大会宣布"},
    {"person_id": 2, "org_id": 102, "title": "县长", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 101, "title": "县委副书记", "start": "", "end": "", "rank": "正处级", "note": ""},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记-县长", "overlap_org": "中共蒲江县委/蒲江县人民政府", "overlap_period": "2026-08起"},
]

if __name__ == "__main__":
    run_build(slug="蒲江县", persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
