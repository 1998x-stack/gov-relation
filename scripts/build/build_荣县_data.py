#!/usr/bin/env python3
"""Build 荣县 (自贡市, 四川省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via 360/Sogou web search + 四川在线/网易/官方公示.
Current (2026) leadership: 县委书记赵磊(2025-01任), 县长张华. Predecessor 易冬(2021-11起).
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "荣县"
STAGING = data_path("tmp", "四川省_荣县")
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
    {"id": 1, "name": "赵磊", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "县委书记", "current_org": "中共荣县县委",
     "source": "中共四川省委组织部干部任前公示(2025-01-10);官方确认(2025-01-27)"},
    {"id": 2, "name": "张华", "gender": "男", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "县长", "current_org": "荣县人民政府",
     "source": "四川在线(张华当选荣县县长)"},
    {"id": 3, "name": "易冬", "gender": "男", "ethnicity": "汉族", "birth": "1971-01",
     "birthplace": "四川富顺", "education": "在职大学;西南政法大学成教学院法律专业", "party_join": "中共党员", "work_start": "1991-09",
     "current_post": "(前任)县委书记", "current_org": "中共荣县县委",
     "source": "360百科;四川省委组织部"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共荣县县委", "type": "党委", "level": "县级", "parent": "中共自贡市委", "location": "自贡市荣县"},
    {"id": 102, "name": "荣县人民政府", "type": "政府", "level": "县级", "parent": "自贡市人民政府", "location": "自贡市荣县"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "县委书记", "start": "2025-01", "end": "", "rank": "正处级", "note": "2025-01 由荣县县长转任县委书记"},
    {"person_id": 2, "org_id": 102, "title": "县长", "start": "", "end": "", "rank": "正处级", "note": "当选荣县县长"},
    {"person_id": 3, "org_id": 101, "title": "前任县委书记", "start": "2021-11", "end": "2025-01", "rank": "正处级/副厅级", "note": "2024-01 拟任副厅级"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记-县长", "overlap_org": "中共荣县县委/荣县人民政府", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 3, "type": "前任-继任", "context": "荣县县委书记前任/继任(赵磊继易冬)", "overlap_org": "中共荣县县委", "overlap_period": "2025-01 前后"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
