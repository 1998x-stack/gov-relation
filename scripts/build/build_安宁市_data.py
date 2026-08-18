#!/usr/bin/env python3
"""Build 安宁市 (昆明市, 云南省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Sogou + 昆明发布/云南网(官方任免).
Current: 市委书记浦泰(兼云南安宁产业园区党工委书记,接毕绍刚), 前任书记毕绍刚.
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "安宁市"
STAGING = data_path("tmp", "云南省_安宁市")
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
    {"id": 1, "name": "浦泰", "gender": "男", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市委书记", "current_org": "中共安宁市委",
     "source": "昆明发布/云南网(1月13日领导干部会议,浦泰任中共安宁市委书记,兼云南安宁产业园区党工委书记)"},
    {"id": 2, "name": "毕绍刚", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "前任市委书记", "current_org": "中共安宁市委",
     "source": "昆明发布/云南网(毕绍刚不再担任中共安宁市委书记职务)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共安宁市委", "type": "党委", "level": "县级市", "parent": "中共昆明市委", "location": "昆明市安宁市"},
    {"id": 102, "name": "安宁市人民政府", "type": "政府", "level": "县级市", "parent": "昆明市人民政府", "location": "昆明市安宁市"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "市委书记", "start": "", "end": "", "rank": "正处级", "note": "兼云南安宁产业园区党工委书记"},
    {"person_id": 2, "org_id": 101, "title": "前任市委书记", "start": "", "end": "", "rank": "正处级", "note": "不再担任"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "前任-继任", "context": "安宁市委书记前任/继任(浦继毕)", "overlap_org": "中共安宁市委", "overlap_period": "前后"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
