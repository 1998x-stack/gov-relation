#!/usr/bin/env python3
"""Build 广饶县 (东营市, 山东省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Sogou + 东营市人民政府官网(官方任免).
Current: 县委书记陈伟颂(confirmed),县长候选人陈银鹏(提名), 前任县长王学春(不再担任).
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "广饶县"
STAGING = data_path("tmp", "山东省_广饶县")
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
    {"id": 1, "name": "陈伟颂", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委书记", "current_org": "中共广饶县委", "source": "东营市人民政府(广饶县召开县级领导干部会议,陈伟颂主持)"},
    {"id": 2, "name": "陈银鹏", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县长(提名)", "current_org": "广饶县人民政府", "source": "东营市人民政府(经市委研究并报省委组织部批复,提名陈银鹏为县长候选人)"},
    {"id": 3, "name": "王学春", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "前任县长", "current_org": "广饶县人民政府", "source": "东营市人民政府(王学春不再担任县长)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共广饶县委", "type": "党委", "level": "县级(县)", "parent": "中共东营市委", "location": "东营市广饶县"},
    {"id": 102, "name": "广饶县人民政府", "type": "政府", "level": "县级(县)", "parent": "东营市人民政府", "location": "东营市广饶县"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "县委书记", "start": "", "end": "", "rank": "正处级", "note": "现职"},
    {"person_id": 2, "org_id": 102, "title": "县长(提名)", "start": "", "end": "", "rank": "正处级", "note": "经省委组织部批复,县长候选人"},
    {"person_id": 3, "org_id": 102, "title": "前任县长", "start": "", "end": "", "rank": "正处级", "note": "不再担任"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记-县长(新任)", "overlap_org": "中共广饶县委/广饶县人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 3, "type": "前任-继任", "context": "广饶县县长前任/继任", "overlap_org": "广饶县人民政府", "overlap_period": "前后"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
