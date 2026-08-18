#!/usr/bin/env python3
"""Build 双流区 (成都市, 四川省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Sogou. 区委书记钟静远(2025-06-24接欧昭, 搜狗百科).
前任书记欧昭. 现任区长待核(未列入).
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "双流区"
STAGING = data_path("tmp", "四川省_双流区")
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
    {"id": 1, "name": "钟静远", "gender": "男", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委书记", "current_org": "中共成都市双流区委",
     "source": "搜狗百科; 2025-06-24 接欧昭任双流区委书记(曾任金堂县委书记)"},
    {"id": 2, "name": "欧昭", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "前任区委书记", "current_org": "中共成都市双流区委",
     "source": "相关检索(双流区委书记欧昭)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共成都市双流区委", "type": "党委", "level": "县级(区级)", "parent": "中共成都市委", "location": "成都市双流区"},
    {"id": 102, "name": "成都市双流区人民政府", "type": "政府", "level": "县级(区级)", "parent": "成都市人民政府", "location": "成都市双流区"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "区委书记", "start": "2025-06", "end": "", "rank": "副处级/正处级", "note": "2025-06-24 接任"},
    {"person_id": 2, "org_id": 101, "title": "前任区委书记", "start": "", "end": "2025-06", "rank": "副处级/正处级", "note": "2025-06 卸任"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "前任-继任", "context": "双流区委书记前任/继任(钟继欧)", "overlap_org": "中共成都市双流区委", "overlap_period": "2025-06 前后"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
