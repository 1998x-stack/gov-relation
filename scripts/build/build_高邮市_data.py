#!/usr/bin/env python3
"""Build 高邮市 (扬州市, 江苏省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via 360 search + 新华网江苏频道
(郑志明任高邮市委书记, 2026-06-26). 市长刘晓涛, 前任书记田醒民.
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "高邮市"
STAGING = data_path("tmp", "江苏省_高邮市")
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
    {"id": 1, "name": "郑志明", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "市委书记", "current_org": "中共高邮市委",
     "source": "新华网江苏频道/今日高邮(2026-06-26 领导干部会议宣布省委决定)"},
    {"id": 2, "name": "刘晓涛", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "市长", "current_org": "高邮市人民政府",
     "source": "360搜索(高邮市现任市长刘晓涛)"},
    {"id": 3, "name": "田醒民", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "(前任)市委书记", "current_org": "中共高邮市委",
     "source": "360搜索(高邮市委书记田醒民;郑志明接任)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共高邮市委", "type": "党委", "level": "县级市", "parent": "中共扬州市委", "location": "扬州市高邮市"},
    {"id": 102, "name": "高邮市人民政府", "type": "政府", "level": "县级市", "parent": "扬州市人民政府", "location": "扬州市高邮市"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "市委书记", "start": "2026-06", "end": "", "rank": "副厅级/正处级", "note": "2026-06-26 任"},
    {"person_id": 2, "org_id": 102, "title": "市长", "start": "", "end": "", "rank": "正处级", "note": "待核实"},
    {"person_id": 3, "org_id": 101, "title": "前任市委书记", "start": "", "end": "2026-06", "rank": "副厅级/正处级", "note": "郑志明2026-06接任"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "市委书记-市长", "overlap_org": "中共高邮市委/高邮市人民政府", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 3, "type": "前任-继任", "context": "高邮市委书记前任/继任(郑志明继田醒民)", "overlap_org": "中共高邮市委", "overlap_period": "2026-06 前后"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
