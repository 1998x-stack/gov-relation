#!/usr/bin/env python3
"""Build 扬中市 (镇江市, 江苏省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Baidu + 扬中发布/上观新闻.
Current: 市委书记贾晟(2024-12省委批准任扬中市委书记), 市长李莉珺(女,2024-12-30任代市长后转正).
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "扬中市"
STAGING = data_path("tmp", "江苏省_扬中市")
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
    {"id": 1, "name": "贾晟", "gender": "男", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市委书记", "current_org": "中共扬中市委",
     "source": "上观新闻(2024-12-31江苏省委批准贾晟任扬中市委书记;前扬中市长;2026出席科创大会)"},
    {"id": 2, "name": "李莉珺", "gender": "女", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市长/市委副书记", "current_org": "扬中市人民政府",
     "source": "扬中发布(2024-12-30人大常委会任命李莉珺为代市长;2026以市委副书记/市长主持大会)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共扬中市委", "type": "党委", "level": "县级市", "parent": "中共镇江市委", "location": "镇江市扬中市"},
    {"id": 102, "name": "扬中市人民政府", "type": "政府", "level": "县级市", "parent": "镇江市人民政府", "location": "镇江市扬中市"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "市委书记", "start": "2024-12", "end": "", "rank": "正处级", "note": "2024-12省委批准任职"},
    {"person_id": 1, "org_id": 102, "title": "市长(前)", "start": "", "end": "2024-12", "rank": "正处级", "note": "辞去市长任书记"},
    {"person_id": 2, "org_id": 102, "title": "市长", "start": "2024-12", "end": "", "rank": "正处级", "note": "2024-12-30任代市长后转正"},
    {"person_id": 2, "org_id": 101, "title": "市委副书记", "start": "", "end": "", "rank": "正处级", "note": ""},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "前任-继任", "context": "贾晟辞市长任书记,李莉珺接任市长", "overlap_org": "扬中市人民政府", "overlap_period": "2024-12交接"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
