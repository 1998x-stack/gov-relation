#!/usr/bin/env python3
"""Build 昌吉市 (昌吉回族自治州, 新疆维吾尔自治区) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via 360搜索 + 昌吉市人民政府网(cjs.gov.cn,官方).
Current: 市长马德(男/回族/1979-11/市委副书记/市政府党组书记, 研究生经济学博士). 市委书记待核.
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "昌吉市"
STAGING = data_path("tmp", "新疆维吾尔自治区_昌吉市")
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
    {"id": 1, "name": "马德", "gender": "男", "birth": "1979-11",
     "birthplace": "", "education": "研究生(经济学博士)", "ethnicity": "回族", "party_join": "中共党员", "work_start": "",
     "current_post": "市长", "current_org": "昌吉市人民政府",
     "source": "昌吉市人民政府网(马德,男,回族,1979-11生,研究生(经济学博士),现任昌吉市委副书记、市政府党组书记、市长)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共昌吉市委", "type": "党委", "level": "县级市", "parent": "中共昌吉回族自治州委", "location": "昌吉回族自治州昌吉市"},
    {"id": 102, "name": "昌吉市人民政府", "type": "政府", "level": "县级市", "parent": "昌吉回族自治州人民政府", "location": "昌吉回族自治州昌吉市"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 102, "title": "市长", "start": "", "end": "", "rank": "正处级", "note": "市政府党组书记"},
    {"person_id": 1, "org_id": 101, "title": "市委副书记", "start": "", "end": "", "rank": "正处级", "note": ""},
]

RELATIONSHIPS = []

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
