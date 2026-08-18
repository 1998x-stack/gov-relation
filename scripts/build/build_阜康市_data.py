#!/usr/bin/env python3
"""Build 阜康市 (昌吉回族自治州, 新疆维吾尔自治区) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Sogou + 百度百科/阜康市政府官网.
Current: 市长李星辰(1982-08/汉族/市委副书记/市政府党组书记). 市委书记陈雷(plausible).
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "阜康市"
STAGING = data_path("tmp", "新疆维吾尔自治区_阜康市")
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
    {"id": 1, "name": "李星辰", "gender": "男", "birth": "1982-08",
     "birthplace": "", "education": "大学(伊犁师范学院)", "party_join": "中共党员", "work_start": "2001-09",
     "current_post": "市长", "current_org": "阜康市人民政府",
     "source": "百度百科/阜康市政府官网(市委副书记、市政府党组书记、市长,1982-08生)"},
    {"id": 2, "name": "陈雷", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市委书记(plausible)", "current_org": "中共阜康市委",
     "source": "相关检索(阜康市委书记陈雷简历, plausible)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共阜康市委", "type": "党委", "level": "县级市", "parent": "中共昌吉州委", "location": "昌吉州阜康市"},
    {"id": 102, "name": "阜康市人民政府", "type": "政府", "level": "县级市", "parent": "昌吉州人民政府", "location": "昌吉州阜康市"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 102, "title": "市长", "start": "", "end": "", "rank": "正处级", "note": "兼市政府党组书记"},
    {"person_id": 1, "org_id": 101, "title": "市委副书记", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 101, "title": "市委书记(plausible)", "start": "", "end": "", "rank": "正处级", "note": "待核实"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档(plausible)", "context": "市长-市委书记", "overlap_org": "中共阜康市委/阜康市人民政府", "overlap_period": "当前"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
