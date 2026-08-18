#!/usr/bin/env python3
"""Build 凤翔区 (宝鸡市, 陕西省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via 360 search + 凤翔区人民政府门户.
Current (2026): 区委书记彭世忠(2026-06,confirmed官方). 区长刘维军(related). 常务副区长刘飞注意(非区长).
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "凤翔区"
STAGING = data_path("tmp", "陕西省_凤翔区")
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
    {"id": 1, "name": "彭世忠", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委书记", "current_org": "中共宝鸡市凤翔区委",
     "source": "凤翔区政府门户(2026-06-08 区委书记彭世忠调研稳增长等工作)"},
    {"id": 2, "name": "刘维军", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "区长", "current_org": "宝鸡市凤翔区人民政府",
     "source": "相关检索(凤翔区区长刘维军简历/个人简介)"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共宝鸡市凤翔区委", "type": "党委", "level": "县级(区级)", "parent": "中共宝鸡市委", "location": "宝鸡市凤翔区"},
    {"id": 102, "name": "宝鸡市凤翔区人民政府", "type": "政府", "level": "县级(区级)", "parent": "宝鸡市人民政府", "location": "宝鸡市凤翔区"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "区委书记", "start": "", "end": "", "rank": "副处级", "note": "2026-06 在任"},
    {"person_id": 2, "org_id": 102, "title": "区长", "start": "", "end": "", "rank": "正处级", "note": "相关检索;待核实"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记-区长", "overlap_org": "中共宝鸡市凤翔区委/凤翔区人民政府", "overlap_period": "当前"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
