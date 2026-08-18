#!/usr/bin/env python3
"""Build 曲水县 (拉萨市, 西藏自治区) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Sogou + 官方人物简历/曲水县考核大会.
Current: 县委书记赤来塔吉(藏族/1974-11/比如人/中央党校大学/兼拉萨市人大副主任), 县长汤官中.
注意: 前任县长格桑邓珠2020-11接受纪律审查(负面信号).
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "曲水县"
STAGING = data_path("tmp", "西藏自治区_曲水县")
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
    {"id": 1, "name": "赤来塔吉", "gender": "男", "birth": "1974-11",
     "birthplace": "西藏比如", "education": "中央党校大学", "party_join": "中共党员(2001-07入党)", "work_start": "1995-07",
     "current_post": "县委书记", "current_org": "中共曲水县委",
     "source": "官方人物简历(男,藏族,1974-11生,西藏比如人,现任拉萨市人大常委会党组成员/副主任,曲水县委书记)"},
    {"id": 2, "name": "汤官中", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县长/县委副书记", "current_org": "曲水县人民政府",
     "source": "曲水县2023年度综合考核干部大会(县委副书记、县长汤官中)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共曲水县委", "type": "党委", "level": "县级(县)", "parent": "中共拉萨市委", "location": "拉萨市曲水县"},
    {"id": 102, "name": "曲水县人民政府", "type": "政府", "level": "县级(县)", "parent": "拉萨市人民政府", "location": "拉萨市曲水县"},
    {"id": 103, "name": "拉萨市人大常委会", "type": "人大", "level": "地级市", "parent": "", "location": "拉萨市"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "县委书记", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 103, "title": "拉萨市人大常委会副主任", "start": "", "end": "", "rank": "副厅级", "note": "兼"},
    {"person_id": 2, "org_id": 102, "title": "县长", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 101, "title": "县委副书记", "start": "", "end": "", "rank": "正处级", "note": ""},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记-县长", "overlap_org": "中共曲水县委/曲水县人民政府", "overlap_period": "2023-2026"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
