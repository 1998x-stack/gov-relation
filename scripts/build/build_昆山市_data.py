#!/usr/bin/env python3
"""Build 昆山市 (苏州市, 江苏省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Sogou + 网易新闻.
Current: 市委书记陈丽艳(曾任市长,接周伟), 市长范建青(代市长,2024-12). 前任书记周伟(履新常州).
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "昆山市"
STAGING = data_path("tmp", "江苏省_昆山市")
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
    {"id": 1, "name": "陈丽艳", "gender": "女", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市委书记", "current_org": "中共昆山市委",
     "source": "网易新闻(此前任昆山市委副书记、市长,已任昆山市委书记)"},
    {"id": 2, "name": "范建青", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市长(代)", "current_org": "昆山市人民政府",
     "source": "网易新闻(范建青任昆山市代市长,2024-12)"},
    {"id": 3, "name": "周伟", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "前任市委书记", "current_org": "中共昆山市委",
     "source": "网易新闻(前苏州市委常委、昆山市委书记,已履新常州市委副书记/代市长)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共昆山市委", "type": "党委", "level": "县级市", "parent": "中共苏州市委", "location": "苏州市昆山市"},
    {"id": 102, "name": "昆山市人民政府", "type": "政府", "level": "县级市", "parent": "苏州市人民政府", "location": "苏州市昆山市"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "市委书记", "start": "", "end": "", "rank": "副厅级(苏州市委常委兼)", "note": "曾任市长,今任书记"},
    {"person_id": 2, "org_id": 102, "title": "市长(代)", "start": "2024", "end": "", "rank": "正处级", "note": "代市长(2024-12)"},
    {"person_id": 3, "org_id": 101, "title": "前任市委书记", "start": "", "end": "", "rank": "副厅级", "note": "履新常州市委副书记/代市长"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "市委书记-市长", "overlap_org": "中共昆山市委/昆山市人民政府", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 3, "type": "前任-继任", "context": "昆山市委书记前任/继任", "overlap_org": "中共昆山市委", "overlap_period": "前后"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
