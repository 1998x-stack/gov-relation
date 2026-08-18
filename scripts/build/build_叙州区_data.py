#!/usr/bin/env python3
"""Build 叙州区 (宜宾市, 四川省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Sogou + 人民网/金台资讯.
Current: 区长铁强(彝族/1990-10/博士/2025-09当选), 区委书记黄修国(2024曾任,拟任副厅).
"""
import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "叙州区"
STAGING = data_path("tmp", "四川省_叙州区")
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
    {"id": 1, "name": "黄修国", "gender": "男", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委书记", "current_org": "中共宜宾市叙州区委",
     "source": "网易(现任宜宾市叙州区委书记黄修国,2024-10拟任副厅级领导职务)"},
    {"id": 2, "name": "铁强", "gender": "男", "birth": "1990-10",
     "birthplace": "", "education": "博士研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "区长/区委副书记", "current_org": "宜宾市叙州区人民政府",
     "source": "人民网(2025-09-29叙州区二届人大五次会议选举铁强为区长;男,彝族,1990-10生,博士)"},
]
ORGANIZATIONS = [
    {"id": 101, "name": "中共宜宾市叙州区委", "type": "党委", "level": "县级(区级)", "parent": "中共宜宾市委", "location": "宜宾市叙州区"},
    {"id": 102, "name": "宜宾市叙州区人民政府", "type": "政府", "level": "县级(区级)", "parent": "宜宾市人民政府", "location": "宜宾市叙州区"},
]
POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "区委书记", "start": "", "end": "", "rank": "正处级", "note": "2024拟任副厅"},
    {"person_id": 2, "org_id": 102, "title": "区长", "start": "2025-09", "end": "", "rank": "正处级", "note": "2025-09-29区人大会选举"},
    {"person_id": 2, "org_id": 101, "title": "区委副书记", "start": "", "end": "", "rank": "正处级", "note": ""},
]
RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记-区长", "overlap_org": "中共宜宾市叙州区委/宜宾市叙州区人民政府", "overlap_period": "2024-2025"},
]
if __name__ == "__main__":
    run_build(slug="叙州区", persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
