#!/usr/bin/env python3
"""Build 珠晖区 (衡阳市, 湖南省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Baidu + 衡阳智慧党建.
Current: 区委书记魏中发(主持区委常委会), 区长张伟(区委副书记/区长).
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "珠晖区"
STAGING = data_path("tmp", "湖南省_珠晖区")
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
    {"id": 1, "name": "魏中发", "gender": "男", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委书记", "current_org": "中共珠晖区委",
     "source": "衡阳智慧党建/珠晖政协(区委书记魏中发,主持2024年区委常委会)"},
    {"id": 2, "name": "张伟", "gender": "男", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区长/区委副书记", "current_org": "珠晖区人民政府",
     "source": "珠晖区政协五届四次会议(区委副书记、区长张伟)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共珠晖区委", "type": "党委", "level": "县级(区级)", "parent": "中共衡阳市委", "location": "衡阳市珠晖区"},
    {"id": 102, "name": "珠晖区人民政府", "type": "政府", "level": "县级(区级)", "parent": "衡阳市人民政府", "location": "衡阳市珠晖区"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "区委书记", "start": "", "end": "", "rank": "正处级", "note": "主持区委常委会"},
    {"person_id": 2, "org_id": 102, "title": "区长", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 101, "title": "区委副书记", "start": "", "end": "", "rank": "正处级", "note": ""},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记-区长", "overlap_org": "中共珠晖区委/珠晖区人民政府", "overlap_period": "当前"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
