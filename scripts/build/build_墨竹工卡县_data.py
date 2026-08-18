#!/usr/bin/env python3
"""Build 墨竹工卡县 (拉萨市, 西藏自治区) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via 360 search + 墨竹工卡县政务网/澎湃.
Current (2025): 县委书记沈鹏里(official), 县长巴桑(2025-04澎湃). 前任县长旦增尼玛(2020).
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "墨竹工卡县"
STAGING = data_path("tmp", "西藏自治区_墨竹工卡县")
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
    {"id": 1, "name": "沈鹏里", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委书记", "current_org": "中共墨竹工卡县委",
     "source": "墨竹工卡县政务网(县委书记沈鹏里初心分享)"},
    {"id": 2, "name": "巴桑", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县长", "current_org": "墨竹工卡县人民政府",
     "source": "澎湃新闻·政务(2025-04-18 县委副书记、县长巴桑率队春风行动调研)"},
    {"id": 3, "name": "旦增尼玛", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "(前任)县长", "current_org": "墨竹工卡县人民政府",
     "source": "西藏统一战线(2020-02-13 县委副书记、县长旦增尼玛)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共墨竹工卡县委", "type": "党委", "level": "县级(县)", "parent": "中共拉萨市委", "location": "拉萨市墨竹工卡县"},
    {"id": 102, "name": "墨竹工卡县人民政府", "type": "政府", "level": "县级(县)", "parent": "拉萨市人民政府", "location": "拉萨市墨竹工卡县"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "县委书记", "start": "", "end": "", "rank": "正处级", "note": "现职"},
    {"person_id": 2, "org_id": 102, "title": "县长", "start": "", "end": "", "rank": "正处级", "note": "2025 在任"},
    {"person_id": 3, "org_id": 102, "title": "前任县长", "start": "2020之前", "end": "", "rank": "正处级", "note": "2020 在任(前任)"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记-县长", "overlap_org": "中共墨竹工卡县委/墨竹工卡县人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 3, "type": "前任-继任", "context": "墨竹工卡县县长前任/继任", "overlap_org": "墨竹工卡县人民政府", "overlap_period": "前后"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
