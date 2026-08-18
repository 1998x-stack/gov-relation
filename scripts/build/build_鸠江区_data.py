#!/usr/bin/env python3
"""Build 鸠江区 (芜湖市, 安徽省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via 搜狗 + 搜狐/企鹅号.
Current (2026): 区委书记黄万勇(confirmed). 区长信息待核(相关检索黄万勇区长,疑一肩挑或前任区长).
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "鸠江区"
STAGING = data_path("tmp", "安徽省_鸠江区")
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
    {"id": 1, "name": "黄万勇", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委书记", "current_org": "中共芜湖市鸠江区委",
     "source": "搜狐/企鹅号(芜湖市鸠江区委书记黄万勇视察上海人本集团等报道)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共芜湖市鸠江区委", "type": "党委", "level": "县级(区级)", "parent": "中共芜湖市委", "location": "芜湖市鸠江区"},
    {"id": 102, "name": "芜湖市鸠江区人民政府", "type": "政府", "level": "县级(区级)", "parent": "芜湖市人民政府", "location": "芜湖市鸠江区"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "区委书记", "start": "", "end": "", "rank": "正处级", "note": "现职(related)"},
]

RELATIONSHIPS = []

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
