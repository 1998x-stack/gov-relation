#!/usr/bin/env python3
"""Build 小店区 (太原市, 山西省) leadership network: SQLite + GEXF.

Gap-investigation artifact. Researched via 360 search + 太原市政府/网易新闻.
Current (2026): 区委书记康建斌(2025-08), 区长王黄林(2026-03). 前任书记袁尔铭.
"""

import sqlite3, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import data_path

SLUG = "小店区"
STAGING = data_path("tmp", "山西省_小店区")
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
    {"id": 1, "name": "康建斌", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "区委书记", "current_org": "中共太原市小店区委",
     "source": "网易新闻(2025-08-06 全省干部大会,省委决定康建斌任小店区委书记)"},
    {"id": 2, "name": "王黄林", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "区长", "current_org": "太原市小店区人民政府",
     "source": "网易新闻(2026-03-29 区第六届人大七次会议公告第1号选举)"},
    {"id": 3, "name": "袁尔铭", "gender": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "(前任)区委书记", "current_org": "中共太原市小店区委",
     "source": "2025-08-06 省委决定袁尔铭不再担任" },
]

ORGANIZATIONS = [
    {"id": 101, "name": "中共太原市小店区委", "type": "党委", "level": "县级(区级)", "parent": "中共太原市委", "location": "太原市小店区"},
    {"id": 102, "name": "太原市小店区人民政府", "type": "政府", "level": "县级(区级)", "parent": "太原市人民政府", "location": "太原市小店区"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "区委书记", "start": "2025-08", "end": "", "rank": "副厅级", "note": "2025-08-06 任"},
    {"person_id": 2, "org_id": 102, "title": "区长", "start": "2026-03", "end": "", "rank": "正处级", "note": "2026-03 当选"},
    {"person_id": 3, "org_id": 101, "title": "前任区委书记", "start": "", "end": "2025-08", "rank": "副厅级", "note": "2025-08 卸任"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记-区长", "overlap_org": "中共太原市小店区委/小店区人民政府", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 3, "type": "前任-继任", "context": "小店区委书记前任/继任(康继袁)", "overlap_org": "中共太原市小店区委", "overlap_period": "2025-08 前后"},
]

if __name__ == "__main__":
    run_build(slug=SLUG, persons=PERSONS, organizations=ORGANIZATIONS,
              positions=POSITIONS, relationships=RELATIONSHIPS,
              db_path=DB_PATH, gexf_path=GEXF_PATH, overwrite=True)
    print("built:", DB_PATH, GEXF_PATH)
    print("row counts:"); _verify_db()
