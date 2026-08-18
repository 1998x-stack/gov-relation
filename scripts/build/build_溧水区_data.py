#!/usr/bin/env python3
"""Build 溧水区 (南京市, 江苏省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Sogou + 溧水区人民政府网(权威机构, www.njls.gov.cn).
Current: 高军玲(江苏南京人/1996-08参加工作/1996-07入党/党校研究生, 溧水区政府领导). 区委书记待核.
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "溧水区"
STAGING = data_path("tmp", "江苏省_溧水区")
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
    {"id": 1, "name": "高军玲", "gender": "女", "birth": "1972-",
     "birthplace": "江苏南京", "education": "党校研究生", "party_join": "中共党员(1996-07)", "work_start": "1996-08",
     "current_post": "区长", "current_org": "溧水区人民政府",
     "source": "溧水区人民政府网(高军玲,江苏南京人,1996-08参加工作,1996-07入党,党校研究生学历)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共南京市溧水区委", "type": "党委", "level": "县级(区级)", "parent": "中共南京市委", "location": "南京市溧水区"},
    {"id": 102, "name": "溧水区人民政府", "type": "政府", "level": "县级(区级)", "parent": "南京市人民政府", "location": "南京市溧水区"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 102, "title": "区长", "start": "", "end": "", "rank": "副厅级", "note": "溧水区政府领导"},
]

RELATIONSHIPS = []

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
