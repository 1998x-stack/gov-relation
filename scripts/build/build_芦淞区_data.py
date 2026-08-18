#!/usr/bin/env python3
"""Build 芦淞区 (株洲市, 湖南省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via 搜狗 + 芦淞区人民政府门户(www.lusong.gov.cn)/株洲日报.
Current (2026): 区委书记杨喜兰, 区长王强(2022起). 前任书记唐卫湘.

注: 于2026-08-17 生成。芦淞区位于株洲市。
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "芦淞区"
STAGING = data_path("tmp", "湖南省_芦淞区")
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
    {"id": 1, "name": "杨喜兰", "gender": "女", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委书记", "current_org": "中共株洲市芦淞区委",
     "source": "芦淞区人民政府门户(领导之窗);现任区委书记(截至2026-07)"},
    {"id": 2, "name": "王强", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区长", "current_org": "株洲市芦淞区人民政府",
     "source": "芦淞区政府门户/株洲日报(王强2022起代理/区长;当选区长)"},
    {"id": 3, "name": "唐卫湘", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "前任区委书记", "current_org": "中共株洲市芦淞区委",
     "source": "2022 时任芦淞区委书记(相关报道)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共株洲市芦淞区委", "type": "党委", "level": "县级(区级)", "parent": "中共株洲市委", "location": "株洲市芦淞区"},
    {"id": 102, "name": "株洲市芦淞区人民政府", "type": "政府", "level": "县级(区级)", "parent": "株洲市人民政府", "location": "株洲市芦淞区"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "区委书记", "start": "", "end": "", "rank": "正处级", "note": "现职(2026-07在任)"},
    {"person_id": 2, "org_id": 102, "title": "区长", "start": "2022", "end": "", "rank": "正处级", "note": "2022起代理/区长"},
    {"person_id": 3, "org_id": 101, "title": "前任区委书记", "start": "2022", "end": "", "rank": "正处级", "note": "2022时任"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记-区长", "overlap_org": "中共株洲市芦淞区委/芦淞区人民政府", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 3, "type": "前任-继任", "context": "芦淞区委书记前任/继任", "overlap_org": "中共株洲市芦淞区委", "overlap_period": "前后"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
