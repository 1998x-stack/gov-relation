#!/usr/bin/env python3
"""Build 攸县 (株洲市, 湖南省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Sogou + 搜狗百科.
Current: 县委书记武挪强(兼县长, 男/1983-10/河南汝阳, 一肩挑). 县长同人.
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "攸县"
STAGING = data_path("tmp", "湖南省_攸县")
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
    {"id": 1, "name": "武挪强", "gender": "男", "birth": "1983-10",
     "birthplace": "河南汝阳", "education": "法学硕士", "party_join": "中共党员(2004-06)", "work_start": "",
     "current_post": "县委书记/县长", "current_org": "中共攸县县委/攸县人民政府",
     "source": "搜狗百科(武挪强,男,河南汝阳人,1983-10生,2004入党,法学硕士,现任攸县县委书记、县政府党组书记、县长)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共攸县县委", "type": "党委", "level": "县级(县)", "parent": "中共株洲市委", "location": "株洲市攸县"},
    {"id": 102, "name": "攸县人民政府", "type": "政府", "level": "县级(县)", "parent": "株洲市人民政府", "location": "株洲市攸县"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "县委书记", "start": "", "end": "", "rank": "正处级", "note": "一肩挑"},
    {"person_id": 1, "org_id": 102, "title": "县长", "start": "", "end": "", "rank": "正处级", "note": "县政府党组书记/县长"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 1, "type": "党政合一", "context": "县委书记兼县长(一肩挑)", "overlap_org": "中共攸县县委/攸县人民政府", "overlap_period": "现职"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
