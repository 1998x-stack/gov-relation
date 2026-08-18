#!/usr/bin/env python3
"""Build 晋宁区 (昆明市, 云南省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Sogou + 百度百科.
Current: 区委书记李松(省委党校研究生,2023-02任区长后转区委书记). 区长杨万红(候选).
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "晋宁区"
STAGING = data_path("tmp", "云南省_晋宁区")
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
    {"id": 1, "name": "李松", "gender": "男", "birth": "",
     "birthplace": "", "education": "省委党校研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "区委书记", "current_org": "中共昆明市晋宁区委",
     "source": "百度百科(李松,省委党校研究生;2023-02任晋宁区长;现任晋宁区委书记;云南省十四届人大代表)"},
    {"id": 2, "name": "杨万红", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "区长(候选)", "current_org": "昆明市晋宁区人民政府",
     "source": "相关检索(昆明晋宁区现任区长杨万红, plausible)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共昆明市晋宁区委", "type": "党委", "level": "县级(区级)", "parent": "中共昆明市委", "location": "昆明市晋宁区"},
    {"id": 102, "name": "昆明市晋宁区人民政府", "type": "政府", "level": "县级(区级)", "parent": "昆明市人民政府", "location": "昆明市晋宁区"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "区委书记", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 102, "title": "区长(前)", "start": "2023-02", "end": "", "rank": "正处级", "note": "2023-02任区长"},
    {"person_id": 2, "org_id": 102, "title": "区长(候选)", "start": "", "end": "", "rank": "正处级", "note": "相关检索"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "前任-继任", "context": "李松(前区长→区委书记)-杨万红(区长候选)", "overlap_org": "昆明市晋宁区人民政府", "overlap_period": "近期"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
