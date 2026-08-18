#!/usr/bin/env python3
"""Build 呈贡区 (昆明市, 云南省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Sogou + 昆明市呈贡区人大常委会公告.
Current: 区长杨凯(2026-03-01四届人大五次会议选出). 区委书记陈净(候选,plausible).
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "呈贡区"
STAGING = data_path("tmp", "云南省_呈贡区")
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
    {"id": 1, "name": "杨凯", "gender": "男", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区长", "current_org": "昆明市呈贡区人民政府",
     "source": "昆明市呈贡区第四届人大第五次会议公告(2026-03-01,选出区长杨凯)"},
    {"id": 2, "name": "陈净", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "区委书记(候选)", "current_org": "中共昆明市呈贡区委",
     "source": "相关检索(呈贡区委书记陈净简历, plausible)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共昆明市呈贡区委", "type": "党委", "level": "县级(区级)", "parent": "中共昆明市委", "location": "昆明市呈贡区"},
    {"id": 102, "name": "昆明市呈贡区人民政府", "type": "政府", "level": "县级(区级)", "parent": "昆明市人民政府", "location": "昆明市呈贡区"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 102, "title": "区长", "start": "2026-03", "end": "", "rank": "正处级", "note": "2026-03-01人代会选出"},
    {"person_id": 2, "org_id": 101, "title": "区委书记(候选)", "start": "", "end": "", "rank": "正处级", "note": "相关检索(plausible)"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区长-区委书记", "overlap_org": "中共昆明市呈贡区委/昆明市呈贡区人民政府", "overlap_period": "当前"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
