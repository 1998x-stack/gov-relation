#!/usr/bin/env python3
"""Build 富顺县 (自贡市, 四川省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via 360/Sogou web search + 富顺县政府服务网
(zgsfsx.sczwfw.gov.cn) + 四川在线(scol) + 领导干部大会任免.
Current (2026) leadership: 县委书记杨斌, 县长曾柯. 前任 邹登权.
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "富顺县"
STAGING = data_path("tmp", "四川省_富顺县")
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
    {"id": 1, "name": "杨斌", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "县委书记", "current_org": "中共富顺县委",
     "source": "四川在线(2021-09-27 县委第十三届一次全会);任免大会(2021-07-31)"},
    {"id": 2, "name": "曾柯", "gender": "男", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "县长", "current_org": "富顺县人民政府",
     "source": "富顺县政府服务网;此前任自贡市统计局党组书记、局长"},
    {"id": 3, "name": "邹登权", "gender": "男", "ethnicity": "汉族", "birth": "1963-06",
     "birthplace": "四川荣县", "education": "", "party_join": "中共党员", "work_start": "1983",
     "current_post": "(前任)县委书记", "current_org": "中共富顺县委",
     "source": "360百科; 2021-07 领导干部大会(不再担任)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共富顺县委", "type": "党委", "level": "县级", "parent": "中共自贡市委", "location": "自贡市富顺县"},
    {"id": 102, "name": "富顺县人民政府", "type": "政府", "level": "县级", "parent": "自贡市人民政府", "location": "自贡市富顺县"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "县委书记", "start": "2021-07", "end": "", "rank": "正处级", "note": "2021-07任,2021-09当选,现任"},
    {"person_id": 2, "org_id": 102, "title": "县长", "start": "", "end": "", "rank": "正处级", "note": "县委副书记、县长;此前任自贡市统计局党组书记/局长"},
    {"person_id": 3, "org_id": 101, "title": "前任县委书记", "start": "", "end": "2021-07", "rank": "正处级", "note": "2021-07 不再担任"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记-县长", "overlap_org": "中共富顺县委/富顺县人民政府", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 3, "type": "前任-继任", "context": "富顺县委书记前任/继任(杨斌继邹登权)", "overlap_org": "中共富顺县委", "overlap_period": "2021-07 前后"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
