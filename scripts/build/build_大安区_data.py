#!/usr/bin/env python3
"""Build 大安区 (自贡市, 四川省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via 360/Sogou web search + 自贡网.
Core facts current as of 2026-08; leadership confirmed via 自贡网 2025-10 news.
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "大安区"
STAGING = data_path("tmp", "四川省_大安区")
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
    {"id": 1, "name": "彭长林", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "区委书记", "current_org": "中共自贡市大安区委",
     "source": "自贡网(2025-10-10 新闻报道);自贡日报人事任免(2021-08)"},
    {"id": 2, "name": "刘勇", "gender": "男", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "区长", "current_org": "自贡市大安区人民政府",
     "source": "自贡网/360搜索 综合"},
    {"id": 3, "name": "张昭国", "gender": "男", "ethnicity": "汉族", "birth": "1966-01",
     "birthplace": "", "education": "党校研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "(前任)区委书记", "current_org": "中共自贡市大安区委",
     "source": "360百科", "history": "2016-09-任区委书记"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共自贡市大安区委", "type": "党委", "level": "县级(区级)", "parent": "中共自贡市委", "location": "自贡市大安区"},
    {"id": 102, "name": "自贡市大安区人民政府", "type": "政府", "level": "县级(区级)", "parent": "自贡市人民政府", "location": "自贡市大安区"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "区委书记", "start": "2018-08", "end": "", "rank": "正处级", "note": "历任大安区委书记"},
    {"person_id": 2, "org_id": 102, "title": "区长", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 3, "org_id": 101, "title": "前任区委书记", "start": "2016-09", "end": "2018-08", "rank": "正处级", "note": "前任"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记-区长", "overlap_org": "中共自贡市大安区委/大安区人民政府", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 3, "type": "前任-继任", "context": "大安区委书记前任/继任", "overlap_org": "中共自贡市大安区委", "overlap_period": "2018-08 前后"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
