#!/usr/bin/env python3
"""Build 长清区 (济南市, 山东省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via 360 search + 央广网/济南日报.
Current (2022+): 区委书记肖辉, 区长王士强. Predecessor 赵居安, 曹军.
Note: 相关检索有"肖辉调走"传闻, 继任者待核实 (open gap).
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "长清区"
STAGING = data_path("tmp", "山东省_长清区")
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
    {"id": 1, "name": "肖辉", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "区委书记", "current_org": "中共济南市长清区委",
     "source": "济南日报(2022-02-19 区第五届委员会一次全会当选区委书记); 相关检索提'肖辉调走'待核"},
    {"id": 2, "name": "王士强", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "区长", "current_org": "济南市长清区人民政府",
     "source": "相关检索(长清区区长王士强简介; 2022 当选区委副书记)"},
    {"id": 3, "name": "赵居安", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "(前任)区委书记", "current_org": "中共济南市长清区委",
     "source": "央广网(2020-08-29 赵居安任中共济南长清区委书记,此前任区长)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共济南市长清区委", "type": "党委", "level": "县级(区级)", "parent": "中共济南市委", "location": "济南市长清区"},
    {"id": 102, "name": "济南市长清区人民政府", "type": "政府", "level": "县级(区级)", "parent": "济南市人民政府", "location": "济南市长清区"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "区委书记", "start": "2022-02", "end": "", "rank": "副厅级", "note": "2022-02 当选(继任状态待核)"},
    {"person_id": 2, "org_id": 102, "title": "区长", "start": "", "end": "", "rank": "正处级", "note": "区委副书记、区长"},
    {"person_id": 3, "org_id": 101, "title": "前任区委书记", "start": "2020-08", "end": "", "rank": "副厅级", "note": "此前任区长"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记-区长", "overlap_org": "中共济南市长清区委/长清区人民政府", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 3, "type": "前任-继任", "context": "长清区委书记前任/继任", "overlap_org": "中共济南市长清区委", "overlap_period": "前后"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
