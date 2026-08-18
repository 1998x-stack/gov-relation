#!/usr/bin/env python3
"""Build 卡若区 (昌都市, 西藏自治区) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Sogou + 中国经济网/昌都发布/昌都新闻网.
Current: 区委书记邓文昌(2023-10任昌都市委常委、卡若区委书记). 区长泽仁(2021). 前任书记任厚明(2021任).
"""
import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "卡若区"
STAGING = data_path("tmp", "西藏自治区_卡若区")
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
    {"id": 1, "name": "邓文昌", "gender": "男", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委书记/昌都市委常委", "current_org": "中共昌都市卡若区委",
     "source": "中国经济网(2023-10-07干部大会宣布邓文昌任昌都市委常委、卡若区委书记,来源昌都发布)"},
    {"id": 2, "name": "泽仁", "gender": "男", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区长/区委副书记", "current_org": "卡若区人民政府",
     "source": "昌都新闻网(卡若区委副书记、区长泽仁,2021表态发言)"},
    {"id": 3, "name": "任厚明", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "(前任书记)", "current_org": "中共昌都市卡若区委",
     "source": "昌都新闻网(任厚明任卡若区委书记,2021-05)"},
]
ORGANIZATIONS = [
    {"id": 101, "name": "中共昌都市卡若区委", "type": "党委", "level": "县级(区级)", "parent": "中共昌都市委", "location": "昌都市卡若区"},
    {"id": 102, "name": "卡若区人民政府", "type": "政府", "level": "县级(区级)", "parent": "昌都市人民政府", "location": "昌都市卡若区"},
]
POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "区委书记", "start": "2023-10", "end": "", "rank": "正处级(兼昌都市委常委)", "note": ""},
    {"person_id": 2, "org_id": 102, "title": "区长", "start": "", "end": "", "rank": "正处级", "note": "2021在任"},
    {"person_id": 3, "org_id": 101, "title": "区委书记(前任)", "start": "", "end": "2023-10", "rank": "正处级", "note": ""},
]
RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记-区长", "overlap_org": "中共昌都市卡若区委/卡若区人民政府", "overlap_period": "2023至今"},
    {"person_a": 1, "person_b": 3, "type": "继任关系", "context": "邓文昌继任任厚明任卡若区委书记", "overlap_org": "中共昌都市卡若区委", "overlap_period": "2023交接"},
]
if __name__ == "__main__":
    run_build(slug="卡若区", persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
