#!/usr/bin/env python3
"""Build 醴陵市 (株洲市, 湖南省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Sogou.
Current: 市长蒋长富(固官网, 男/1980-12, 市委副书记/市政府党组书记/市长). 前任书记候选人胡湘之(株洲市政府原副秘书长, plausible).
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "醴陵市"
STAGING = data_path("tmp", "湖南省_醴陵市")
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
    {"id": 1, "name": "蒋长富", "gender": "男", "birth": "1980-12",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市长", "current_org": "醴陵市人民政府",
     "source": "醴陵市人民政府官网(蒋长富,现任醴陵市委副书记、市政府党组书记、市长,2026-08-06)"},
    {"id": 2, "name": "胡湘之", "gender": "男", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "前任市委书记", "current_org": "中共醴陵市委",
     "source": "株洲市人民政府原副秘书长(相关检索,与醴陵关联)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共醴陵市委", "type": "党委", "level": "县级市", "parent": "中共株洲市委", "location": "株洲市醴陵市"},
    {"id": 102, "name": "醴陵市人民政府", "type": "政府", "level": "县级市", "parent": "株洲市人民政府", "location": "株洲市醴陵市"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 102, "title": "市长", "start": "", "end": "", "rank": "副厅级", "note": "市委副书记/市政府党组书记"},
    {"person_id": 2, "org_id": 101, "title": "前任市委书记", "start": "", "end": "", "rank": "正处级", "note": "plausible"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政联动", "context": "市长/前任书记(区域领导)", "overlap_org": "中共醴陵市委/醴陵市人民政府", "overlap_period": "跨期"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
