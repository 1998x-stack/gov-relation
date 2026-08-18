#!/usr/bin/env python3
"""Build 平阴县 (济南市, 山东省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Baidu + 平阴县政府网.
Current: 县委书记王秀成(主持县委常委会). 县长待核.
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "平阴县"
STAGING = data_path("tmp", "山东省_平阴县")
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
    {"id": 1, "name": "王秀成", "gender": "男", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委书记", "current_org": "中共平阴县委",
     "source": "平阴县政府网(县委常委会召开会议,王秀成主持并讲话)"},
    {"id": 2, "name": "杨旭东", "gender": "男", "birth": "1969-11",
     "birthplace": "山东青岛", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "山东省供销合作社理事会主任", "current_org": "山东省供销合作社",
     "source": "百度百科(2019.08-2022.01曾任平阴县委书记,现任省供销合作社理事会主任)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共平阴县委", "type": "党委", "level": "县级(县)", "parent": "中共济南市委", "location": "济南市平阴县"},
    {"id": 102, "name": "平阴县人民政府", "type": "政府", "level": "县级(县)", "parent": "济南市人民政府", "location": "济南市平阴县"},
    {"id": 103, "name": "山东省供销合作社", "type": "机构", "level": "省属", "parent": "", "location": "济南市"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "县委书记", "start": "", "end": "", "rank": "正处级", "note": "主持县委常委会并讲话"},
    {"person_id": 2, "org_id": 101, "title": "县委书记(前)", "start": "2019-08", "end": "2022-02", "rank": "正处级", "note": "2019.08-2022.01平阴县委书记"},
    {"person_id": 2, "org_id": 103, "title": "理事会主任", "start": "", "end": "", "rank": "", "note": "现任"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "继任关系", "context": "王秀成接任平阴县委书记(杨旭东2022年离任)", "overlap_org": "中共平阴县委", "overlap_period": "2022年交接"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
