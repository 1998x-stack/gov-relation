#!/usr/bin/env python3
"""Build 伊州区 (哈密市, 新疆维吾尔自治区) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Sogou(2026-05官方消息).
Current: 区长亚迪卡尔·吐尔洪(区委副书记/区长). 区委书记待核.
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "伊州区"
STAGING = data_path("tmp", "新疆维吾尔自治区_伊州区")
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
    {"id": 1, "name": "亚迪卡尔·吐尔洪", "gender": "男", "birth": "",
     "birthplace": "", "education": "", "ethnicity": "维吾尔", "party_join": "中共党员", "work_start": "",
     "current_post": "区长", "current_org": "哈密市伊州区人民政府",
     "source": "Sogou(2026-05官方消息,现任伊州区区委副书记、区政府区长亚迪卡尔·吐尔洪)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共哈密市伊州区委", "type": "党委", "level": "县级(区级)", "parent": "中共哈密市委", "location": "哈密市伊州区"},
    {"id": 102, "name": "哈密市伊州区人民政府", "type": "政府", "level": "县级(区级)", "parent": "哈密市人民政府", "location": "哈密市伊州区"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 102, "title": "区长", "start": "", "end": "", "rank": "正处级", "note": "区委副书记/区长"},
]

RELATIONSHIPS = []

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
