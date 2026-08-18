#!/usr/bin/env python3
"""Build 高昌区 (吐鲁番市, 新疆维吾尔自治区) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Sogou. 区委书记朱继坤(吐鲁番市委常委兼, 2026-07仍任).
区长待核. 前任书记候选单丽萍(plausible).
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "高昌区"
STAGING = data_path("tmp", "新疆维吾尔自治区_高昌区")
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
    {"id": 1, "name": "朱继坤", "gender": "男", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委书记", "current_org": "中共吐鲁番市高昌区委",
     "source": "Sogou(现任吐鲁番高昌区党委书记朱继坤,兼吐鲁番市委常委; 2026-07-16调研工作)"},
    {"id": 2, "name": "单丽萍", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "(前)高昌区书记", "current_org": "中共吐鲁番高昌区委",
     "source": "相关检索(吐鲁番高昌区书记单丽萍,前任)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共吐鲁番市高昌区委", "type": "党委", "level": "县级(区级)", "parent": "中共吐鲁番市委", "location": "吐鲁番市高昌区"},
    {"id": 102, "name": "吐鲁番市高昌区人民政府", "type": "政府", "level": "县级(区级)", "parent": "吐鲁番市人民政府", "location": "吐鲁番市高昌区"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "区委书记", "start": "", "end": "", "rank": "副厅级(吐鲁番市委常委兼)", "note": "2026-07仍任"},
    {"person_id": 2, "org_id": 101, "title": "前任区委书记", "start": "", "end": "", "rank": "副处级/正处级", "note": "相关检索(plausible)"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "前任-继任", "context": "高昌区委书记前任/继任(候选)", "overlap_org": "中共吐鲁番市高昌区委", "overlap_period": "前后"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
