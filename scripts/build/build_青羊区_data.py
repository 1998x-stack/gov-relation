#!/usr/bin/env python3
"""Build 青羊区 (成都市) leadership network: SQLite + GEXF.

Pilot artifact for gap-investigation pipeline. Researched via web search
(360/Sogou) + 成都市青羊区人民政府 official leadership page (2026-05-26).
Core facts current as of 2026-08.
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "青羊区"
STAGING = data_path("tmp", "四川省_青羊区")
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
    {"id": 1, "name": "周德强", "gender": "男", "ethnicity": "汉族", "birth": "1973-12",
     "birthplace": "", "education": "硕士研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "区委书记", "current_org": "中共成都市青羊区委",
     "source": "成都市青羊区人民政府 leadership page(2026-05-26)"},
    {"id": 2, "name": "冯胜", "gender": "男", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "区长", "current_org": "成都市青羊区人民政府",
     "source": "成都市青羊区人民政府 leadership page(2026-05-26)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共成都市青羊区委", "type": "党委", "level": "县级(中心城区)", "parent": "中共成都市委", "location": "成都市青羊区"},
    {"id": 102, "name": "成都市青羊区人民政府", "type": "政府", "level": "县级(区级)", "parent": "成都市人民政府", "location": "成都市青羊区"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "区委书记", "start": "", "end": "", "rank": "副厅级", "note": "现任区委书记"},
    {"person_id": 2, "org_id": 102, "title": "区长", "start": "", "end": "", "rank": "副厅级", "note": "区委副书记、区长"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记-区长", "overlap_org": "中共成都市青羊区委/青羊区人民政府", "overlap_period": "当前"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
