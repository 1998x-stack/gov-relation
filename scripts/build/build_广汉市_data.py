#!/usr/bin/env python3
"""Build 广汉市 (德阳市, 四川省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Sogou + 今日头条(2024-12).
Current: 市委书记王锐(兼三星堆景区党工委书记), 市长胡涛(男/1979/河南沈丘).
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "广汉市"
STAGING = data_path("tmp", "四川省_广汉市")
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
    {"id": 1, "name": "王锐", "gender": "男", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市委书记", "current_org": "中共广汉市委",
     "source": "今日头条(德阳高新区党工委常务副书记、广汉三星堆博物馆景区党工委书记、主持广汉市委全面工作)"},
    {"id": 2, "name": "胡涛", "gender": "男", "birth": "1979-",
     "birthplace": "河南沈丘", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市长/市委副书记", "current_org": "广汉市人民政府",
     "source": "今日头条(胡涛,汉族,1979年生,河南沈丘人,现任广汉市委副书记、市政府市长)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共广汉市委", "type": "党委", "level": "县级市", "parent": "中共德阳市委", "location": "德阳市广汉市"},
    {"id": 102, "name": "广汉市人民政府", "type": "政府", "level": "县级市", "parent": "德阳市人民政府", "location": "德阳市广汉市"},
    {"id": 103, "name": "广汉三星堆博物馆景区党工委", "type": "党工委", "level": "景区", "parent": "德阳市", "location": "广汉市"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "市委书记", "start": "", "end": "", "rank": "正处级", "note": "主持市委全面工作"},
    {"person_id": 1, "org_id": 103, "title": "三星堆景区党工委书记(兼)", "start": "", "end": "", "rank": "兼", "note": ""},
    {"person_id": 2, "org_id": 102, "title": "市长", "start": "", "end": "", "rank": "正处级", "note": "协助主持政府全面工作"},
    {"person_id": 2, "org_id": 101, "title": "市委副书记", "start": "", "end": "", "rank": "正处级", "note": ""},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "市委书记-市长", "overlap_org": "中共广汉市委/广汉市人民政府", "overlap_period": "当前"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
