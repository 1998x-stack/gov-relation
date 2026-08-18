#!/usr/bin/env python3
"""Build 盘龙区 (昆明市, 云南省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via 360 search + 昆明市盘龙区人民政府官网
(区长张云简历, 2025-04). 区委书记沃磊 (plausible, via related search).
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "盘龙区"
STAGING = data_path("tmp", "云南省_盘龙区")
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
    {"id": 1, "name": "沃磊", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "区委书记", "current_org": "中共昆明市盘龙区委",
     "source": "360搜索 综合(昆明市盘龙区区委书记沃磊)"},
    {"id": 2, "name": "张云", "gender": "男", "ethnicity": "彝族", "birth": "1985-11",
     "birthplace": "", "education": "在职硕士研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "区长", "current_org": "昆明市盘龙区人民政府",
     "source": "昆明市盘龙区人民政府官网(2025-04-18)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共昆明市盘龙区委", "type": "党委", "level": "县级(区级)", "parent": "中共昆明市委", "location": "昆明市盘龙区"},
    {"id": 102, "name": "昆明市盘龙区人民政府", "type": "政府", "level": "县级(区级)", "parent": "昆明市人民政府", "location": "昆明市盘龙区"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "区委书记", "start": "", "end": "", "rank": "正处级/副厅级", "note": "待核实"},
    {"person_id": 2, "org_id": 102, "title": "区长", "start": "", "end": "", "rank": "正处级/副厅级", "note": "区委副书记、区政府区长"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记-区长", "overlap_org": "中共昆明市盘龙区委/盘龙区人民政府", "overlap_period": "当前"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
