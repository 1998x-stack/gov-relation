#!/usr/bin/env python3
"""Build 莱芜区 (济南市, 山东省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via 360搜索 + 中国新闻网山东(官方).
Current: 区委书记郅颂(女/1972-02/省委党校研究生/菏泽郓城人,2025跨区履新). 区长待核.
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "莱芜区"
STAGING = data_path("tmp", "山东省_莱芜区")
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
    {"id": 1, "name": "郅颂", "gender": "女", "birth": "1972-01",
     "birthplace": "山东郓城", "education": "省委党校研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "区委书记", "current_org": "中共济南市莱芜区委",
     "source": "中国新闻网山东(郅颂,女,汉族,1972-02生,省委党校研究生,曾任钢城区委书记,2025-12跨区履新任莱芜区委书记;菏泽郓城人,曾任商河县委)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共济南市莱芜区委", "type": "党委", "level": "县级(区级)", "parent": "中共济南市委", "location": "济南市莱芜区"},
    {"id": 102, "name": "济南市莱芜区人民政府", "type": "政府", "level": "县级(区级)", "parent": "济南市人民政府", "location": "济南市莱芜区"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "区委书记", "start": "2025-12", "end": "", "rank": "正处级", "note": "2025-12跨区履新"},
]

RELATIONSHIPS = []

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
