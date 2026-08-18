#!/usr/bin/env python3
"""Build 常熟市 (苏州市, 江苏省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via Sogou + 常熟市人民政府/江苏省委组织部公示.
Current: 市长张伟(男/1977-11/硕士/市委副书记/市长). 市委书记虞伟(plausible). 前任市长秦猛(1980生,2024任前公示拟任设区市副职).
"""
import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "常熟市"
STAGING = data_path("tmp", "江苏省_常熟市")
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
    {"id": 1, "name": "张伟", "gender": "男", "birth": "1977-11",
     "birthplace": "", "education": "硕士研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "市长/市委副书记", "current_org": "常熟市人民政府",
     "source": "常熟市人民政府领导(市委副书记、市长张伟,男,1977-11生,硕士)"},
    {"id": 2, "name": "虞伟", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市委书记(plausible)", "current_org": "中共常熟市委",
     "source": "相关检索(常熟市委书记虞伟, plausible)"},
    {"id": 3, "name": "秦猛", "gender": "男", "birth": "1980",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "(前任市长)", "current_org": "常熟市人民政府",
     "source": "江苏省委组织部任前公示(2024:现任常熟市委副书记/市长秦猛,1980年生,拟任设区市副职)"},
]
ORGANIZATIONS = [
    {"id": 101, "name": "中共常熟市委", "type": "党委", "level": "县级市", "parent": "中共苏州市委", "location": "苏州市常熟市"},
    {"id": 102, "name": "常熟市人民政府", "type": "政府", "level": "县级市", "parent": "苏州市人民政府", "location": "苏州市常熟市"},
]
POSITIONS = [
    {"person_id": 1, "org_id": 102, "title": "市长", "start": "", "end": "", "rank": "正处级", "note": "兼市委副书记"},
    {"person_id": 2, "org_id": 101, "title": "市委书记(plausible)", "start": "", "end": "", "rank": "正处级", "note": "待核实"},
    {"person_id": 3, "org_id": 102, "title": "市长(前任)", "start": "", "end": "", "rank": "正处级", "note": "2024拟任设区市副职"},
]
RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档(plausible)", "context": "市长-市委书记", "overlap_org": "中共常熟市委/常熟市人民政府", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 3, "type": "前任-继任", "context": "秦猛前任市长,张伟现任", "overlap_org": "常熟市人民政府", "overlap_period": "交接"},
]
if __name__ == "__main__":
    run_build(slug="常熟市", persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
