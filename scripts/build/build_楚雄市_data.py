#!/usr/bin/env python3
"""Build 楚雄市 (楚雄彝族自治州, 云南省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Sogou.
Current: 市委书记冯毅(州委常委/主持市委常委会议), 市长罗兴贵(彝族/1975-10/市委副书记/兼楚雄高新区主任).
"""
import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "楚雄市"
STAGING = data_path("tmp", "云南省_楚雄市")
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
    {"id": 1, "name": "冯毅", "gender": "男", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市委书记/州委常委", "current_org": "中共楚雄市委",
     "source": "网媒(州委常委、楚雄市委书记冯毅主持会议并讲话)"},
    {"id": 2, "name": "罗兴贵", "gender": "男", "birth": "1975-10",
     "birthplace": "", "education": "省委党校大学", "party_join": "中共党员", "work_start": "",
     "current_post": "市长/市委副书记", "current_org": "楚雄市人民政府",
     "source": "人物简历(男,彝族,1975-10生,省委党校大学,楚雄市委副书记/市长/党组书记,兼楚雄高新区管委会主任)"},
]
ORGANIZATIONS = [
    {"id": 101, "name": "中共楚雄市委", "type": "党委", "level": "县级市", "parent": "中共楚雄州委", "location": "楚雄州楚雄市"},
    {"id": 102, "name": "楚雄市人民政府", "type": "政府", "level": "县级市", "parent": "楚雄州人民政府", "location": "楚雄州楚雄市"},
    {"id": 103, "name": "楚雄高新区管委会", "type": "管委会", "level": "园区", "parent": "", "location": "楚雄市"},
]
POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "市委书记", "start": "", "end": "", "rank": "正处级", "note": "州委常委"},
    {"person_id": 2, "org_id": 102, "title": "市长", "start": "", "end": "", "rank": "正处级", "note": "兼市政府党组书记"},
    {"person_id": 2, "org_id": 101, "title": "市委副书记", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 103, "title": "高新区管委会主任(兼)", "start": "", "end": "", "rank": "", "note": ""},
]
RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "市委书记-市长", "overlap_org": "中共楚雄市委/楚雄市人民政府", "overlap_period": "当前"},
]
if __name__ == "__main__":
    run_build(slug="楚雄市", persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
