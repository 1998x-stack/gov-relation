#!/usr/bin/env python3
"""Build 慈溪市 (宁波市, 浙江省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via 360搜索 + 360百科.
Current: 市委书记林坚(男,1969-04/浙江宁波, 宁波市委常委/兼前湾新区党工委书记). 市长待核.
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "慈溪市"
STAGING = data_path("tmp", "浙江省_慈溪市")
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
    {"id": 1, "name": "林坚", "gender": "男", "birth": "1969-04",
     "birthplace": "浙江宁波", "education": "大学", "party_join": "中共党员(1991-06)", "work_start": "",
     "current_post": "市委书记/宁波市委常委", "current_org": "中共慈溪市委",
     "source": "360百科(林坚,男,1969-04浙江宁波人,1991入党,大学学历,现任宁波市委常委、慈溪市委书记、宁波前湾新区党工委书记(兼))"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共慈溪市委", "type": "党委", "level": "县级市", "parent": "中共宁波市委", "location": "宁波市慈溪市"},
    {"id": 102, "name": "慈溪市人民政府", "type": "政府", "level": "县级市", "parent": "宁波市人民政府", "location": "宁波市慈溪市"},
    {"id": 103, "name": "中共宁波市委", "type": "党委", "level": "副省级市", "parent": "中共浙江省委", "location": "宁波市"},
    {"id": 104, "name": "宁波前湾新区党工委", "type": "党工委", "level": "新区", "parent": "宁波市", "location": "宁波市"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 103, "title": "宁波市委常委", "start": "", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 101, "title": "慈溪市委书记", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 104, "title": "前湾新区党工委书记(兼)", "start": "", "end": "", "rank": "兼", "note": ""},
]

RELATIONSHIPS = []

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
