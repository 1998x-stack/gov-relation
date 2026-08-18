#!/usr/bin/env python3
"""Build 滨江区 (杭州市, 浙江省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Sogou. 郑迪 confirmed (百度百科):
杭州市滨江区委副书记、区政府区长(2022-02至2025-10), 2025- 杭州高新技术产业开发区党工委书记、杭州市滨江区委书记.
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "滨江区"
STAGING = data_path("tmp", "浙江省_滨江区")
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
    {"id": 1, "name": "郑迪", "gender": "男", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委书记", "current_org": "中共杭州市滨江区委",
     "source": "百度百科(2022-02至2025-10 任滨江区区长; 2025- 高新区党工委书记、滨江区委书记)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共杭州市滨江区委", "type": "党委", "level": "县级(区级)", "parent": "中共杭州市委", "location": "杭州市滨江区"},
    {"id": 102, "name": "杭州市滨江区人民政府", "type": "政府", "level": "县级(区级)", "parent": "杭州市人民政府", "location": "杭州市滨江区"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "区委书记", "start": "2025", "end": "", "rank": "副处级/正处级", "note": "2025 起任"},
    {"person_id": 1, "org_id": 102, "title": "区长(前)", "start": "2022-02", "end": "2025-10", "rank": "正处级", "note": "2022-02至2025-10 任区长"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 1, "type": "职务晋升", "context": "郑迪由区长升任区委书记", "overlap_org": "杭州市滨江区人民政府/中共杭州市滨江区委", "overlap_period": "2025 前后"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
