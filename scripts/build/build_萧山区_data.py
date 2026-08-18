#!/usr/bin/env python3
"""Build 萧山区 (杭州市, 浙江省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via 360 search + 澎湃新闻/人民日报.
Current (2026): 区委书记孙旭东, 区长姜永柱. Previous: 章登峰, 卢春强.
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "萧山区"
STAGING = data_path("tmp", "浙江省_萧山区")
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
    {"id": 1, "name": "孙旭东", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "区委书记", "current_org": "中共杭州市萧山区委",
     "source": "澎湃新闻/thepaper.cn(2026-02-02 督导调研); 人民日报(2025-12-09 署名文章)"},
    {"id": 2, "name": "姜永柱", "gender": "男", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "区长", "current_org": "杭州市萧山区人民政府",
     "source": "澎湃新闻(2025-03-21 区领导专题听取世预赛筹备)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共杭州市萧山区委", "type": "党委", "level": "县级(区级)", "parent": "中共杭州市委", "location": "杭州市萧山区"},
    {"id": 102, "name": "杭州市萧山区人民政府", "type": "政府", "level": "县级(区级)", "parent": "杭州市人民政府", "location": "杭州市萧山区"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "区委书记", "start": "", "end": "", "rank": "副厅级(市委常委兼)", "note": "市委常委、区委书记"},
    {"person_id": 2, "org_id": 102, "title": "区长", "start": "", "end": "", "rank": "正处级", "note": "区委副书记、区长"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记-区长", "overlap_org": "中共杭州市萧山区委/萧山区人民政府", "overlap_period": "当前"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
