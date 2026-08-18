#!/usr/bin/env python3
"""Build 潞州区 (长治市, 山西省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Sogou + 长治市潞州区政府网(权威机构).
Current: 区委书记兼区长崔云峰(中央党校研究生/中共党员, 一肩挑). 
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "潞州区"
STAGING = data_path("tmp", "山西省_潞州区")
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
    {"id": 1, "name": "崔云峰", "gender": "男", "birth": "",
     "birthplace": "", "education": "中央党校研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "区委书记/区长", "current_org": "中共长治市潞州区委/长治市潞州区人民政府",
     "source": "长治市潞州区政府网(崔云峰,现任潞州区委副书记、区政府党组书记、区长; 相关检索含潞州区委书记崔云峰)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共长治市潞州区委", "type": "党委", "level": "县级(区级)", "parent": "中共长治市委", "location": "长治市潞州区"},
    {"id": 102, "name": "长治市潞州区人民政府", "type": "政府", "level": "县级(区级)", "parent": "长治市人民政府", "location": "长治市潞州区"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "区委书记", "start": "", "end": "", "rank": "正处级", "note": "党政合一"},
    {"person_id": 1, "org_id": 102, "title": "区长", "start": "", "end": "", "rank": "正处级", "note": "区政府党组书记/区长,主持区政府全面工作"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 1, "type": "党政合一", "context": "潞州区委书记兼区长", "overlap_org": "中共长治市潞州区委/长治市潞州区人民政府", "overlap_period": "现职"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
