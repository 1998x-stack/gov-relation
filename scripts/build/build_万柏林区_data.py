#!/usr/bin/env python3
"""Build 万柏林区 (太原市, 山西省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via 360 search + 万柏林区政府门户.
Current (2026): 区委书记孙泉(2026-02仍任,confirmed). 前任书记/区长一肩挑 杨俊民. 现任区长信息待核.
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "万柏林区"
STAGING = data_path("tmp", "山西省_万柏林区")
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
    {"id": 1, "name": "孙泉", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委书记", "current_org": "中共太原市万柏林区委",
     "source": "万柏林区政府门户(2026-02-11 区委常委会2025年度民主生活会,孙泉主持)"},
    {"id": 2, "name": "杨俊民", "gender": "男", "ethnicity": "", "birth": "1970-12",
     "birthplace": "山西运城", "education": "省委党校研究生", "party_join": "中共党员(1992-05)", "work_start": "1993-06",
     "current_post": "(前任)区委书记/区长", "current_org": "中共太原市万柏林区委",
     "source": "360百科(曾任万柏林区委书记、区长一肩挑)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共太原市万柏林区委", "type": "党委", "level": "县级(区级)", "parent": "中共太原市委", "location": "太原市万柏林区"},
    {"id": 102, "name": "太原市万柏林区人民政府", "type": "政府", "level": "县级(区级)", "parent": "太原市人民政府", "location": "太原市万柏林区"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "区委书记", "start": "", "end": "", "rank": "副厅级", "note": "2026-02 仍任"},
    {"person_id": 2, "org_id": 101, "title": "前任区委书记/区长", "start": "", "end": "", "rank": "副厅级", "note": "曾任书记、区长一肩撬"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "前任-继任", "context": "万柏林区委书记前任/继任(孙继杨)", "overlap_org": "中共太原市万柏林区委", "overlap_period": "前后"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
