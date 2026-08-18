#!/usr/bin/env python3
"""Build 北仑区 (宁波市, 浙江省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Sogou + 搜狗百科.
Current: 区长王程(男/1973-06/陕西西安/西交大博士). 区委书记姚力(相关检索, plausible).
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "北仑区"
STAGING = data_path("tmp", "浙江省_北仑区")
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
    {"id": 1, "name": "王程", "gender": "男", "birth": "1973-06",
     "birthplace": "陕西西安", "education": "西安交通大学研究生/管理学博士", "party_join": "中共党员", "work_start": "2007-03",
     "current_post": "区长", "current_org": "宁波市北仑区人民政府",
     "source": "搜狗百科(王程,男/1973-06/陕西西安/1996入党/2007参加工作/西交大博士/现任宁波北仑区区长)"},
    {"id": 2, "name": "姚力", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "区委书记(候选)", "current_org": "中共宁波市北仑区委",
     "source": "相关检索(宁波北仑区委书记姚力, plausible)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共宁波市北仑区委", "type": "党委", "level": "县级(区级)", "parent": "中共宁波市委", "location": "宁波市北仑区"},
    {"id": 102, "name": "宁波市北仑区人民政府", "type": "政府", "level": "县级(区级)", "parent": "宁波市人民政府", "location": "宁波市北仑区"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 102, "title": "区长", "start": "", "end": "", "rank": "正处级", "note": "2026在任"},
    {"person_id": 2, "org_id": 101, "title": "区委书记(候选)", "start": "", "end": "", "rank": "正处级/副厅级", "note": "相关检索(plausible)"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区长-区委书记", "overlap_org": "中共宁波市北仑区委/宁波市北仑区人民政府", "overlap_period": "当前"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
