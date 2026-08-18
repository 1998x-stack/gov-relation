#!/usr/bin/env python3
"""Build 茶陵县 (株洲市, 湖南省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via 360搜索 + 网易/株洲时政/人代会公告.
Current: 县委书记杨红兵(2025-02任,邓元连卸任), 县长朱毅强(2025-10-21人代会选出).
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "茶陵县"
STAGING = data_path("tmp", "湖南省_茶陵县")
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
    {"id": 1, "name": "杨红兵", "gender": "男", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委书记", "current_org": "中共茶陵县委",
     "source": "网易(2025-02省委/市委决定杨红兵任茶陵县委书记,邓元连卸任;曾任株洲市炎陵县委常委)"},
    {"id": 2, "name": "朱毅强", "gender": "男", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县长/县委副书记", "current_org": "茶陵县人民政府",
     "source": "网易/株洲时政(茶陵县第十八届人大第六次会议2025-10-21选举朱毅强为茶陵县长;县委副书记)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共茶陵县委", "type": "党委", "level": "县级(县)", "parent": "中共株洲市委", "location": "株洲市茶陵县"},
    {"id": 102, "name": "茶陵县人民政府", "type": "政府", "level": "县级(县)", "parent": "株洲市人民政府", "location": "株洲市茶陵县"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "县委书记", "start": "2025-02", "end": "", "rank": "正处级", "note": "2025-02任命"},
    {"person_id": 2, "org_id": 102, "title": "县长", "start": "2025-10", "end": "", "rank": "正处级", "note": "2025-10-21人代会选举"},
    {"person_id": 2, "org_id": 101, "title": "县委副书记", "start": "", "end": "", "rank": "正处级", "note": ""},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记-县长", "overlap_org": "中共茶陵县委/茶陵县人民政府", "overlap_period": "2025-10至今"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
