#!/usr/bin/env python3
"""Build 天山区 (乌鲁木齐市, 新疆维吾尔自治区) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via 360 search + 天山区人民政府门户
(www.xjtsq.gov.cn, 区长阿里木·马木提 2026-03). 区委书记李刚 (plausible).
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "天山区"
STAGING = data_path("tmp", "新疆维吾尔自治区_天山区")
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
    {"id": 1, "name": "李刚", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "区委书记", "current_org": "中共乌鲁木齐市天山区委",
     "source": "360搜索(乌鲁木齐天山区区委书记李刚)"},
    {"id": 2, "name": "阿里木·马木提", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "区长", "current_org": "乌鲁木齐市天山区人民政府",
     "source": "天山区人民政府门户网(2026-03-11 乌鲁木齐晚报专访)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共乌鲁木齐市天山区委", "type": "党委", "level": "县级(区级)", "parent": "中共乌鲁木齐市委", "location": "乌鲁木齐市天山区"},
    {"id": 102, "name": "乌鲁木齐市天山区人民政府", "type": "政府", "level": "县级(区级)", "parent": "乌鲁木齐市人民政府", "location": "乌鲁木齐市天山区"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "区委书记", "start": "", "end": "", "rank": "副厅级", "note": "待核实"},
    {"person_id": 2, "org_id": 102, "title": "区长", "start": "", "end": "", "rank": "正处级/副厅级", "note": "区委副书记、区长"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记-区长", "overlap_org": "中共乌鲁木齐市天山区委/天山区人民政府", "overlap_period": "当前"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
