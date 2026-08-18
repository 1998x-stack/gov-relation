#!/usr/bin/env python3
"""Build 秦都区 (咸阳市, 陕西省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Sogou + 秦都区人民政府/今日头条.
Current: 区委书记王洲(男/1976-09/中央党校大学/中共党员/主持区委全面工作,2019-01曾任区长). 现任区长待核.
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "秦都区"
STAGING = data_path("tmp", "陕西省_秦都区")
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
    {"id": 1, "name": "王洲", "gender": "男", "birth": "1976-09",
     "birthplace": "", "education": "中央党校大学", "party_join": "中共党员", "work_start": "",
     "current_post": "区委书记", "current_org": "中共咸阳市秦都区委",
     "source": "秦都区人民政府(区委书记王洲,男,1976-09生,中央党校大学,中共党员;2019-01任区长后现任区委书记)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共咸阳市秦都区委", "type": "党委", "level": "县级(区级)", "parent": "中共咸阳市委", "location": "咸阳市秦都区"},
    {"id": 102, "name": "咸阳市秦都区人民政府", "type": "政府", "level": "县级(区级)", "parent": "咸阳市人民政府", "location": "咸阳市秦都区"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "区委书记", "start": "", "end": "", "rank": "正处级", "note": "主持区委全面工作"},
    {"person_id": 1, "org_id": 102, "title": "区长(前)", "start": "2019-01", "end": "", "rank": "正处级", "note": "2019-01任区委副书记/区长"},
]

RELATIONSHIPS = []

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
