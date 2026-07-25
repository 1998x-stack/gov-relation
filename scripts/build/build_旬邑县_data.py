#!/usr/bin/env python3
"""Build script for 旬邑县 (咸阳市, 陕西省) government network.

Research date: 2026-07-25
Sources:
  - https://www.snxunyi.gov.cn/ (official website)
  - News articles from 旬邑县融媒体中心 2025-2026
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.gexf import GEXFBuilder
from gov_relation.schema import create_tables, insert_organizations, insert_persons, insert_positions, insert_relationships

SLUG = "旬邑县"
DB_PATH = REPO_ROOT / "data/database" / f"{SLUG}_network.db"
GEXF_PATH = REPO_ROOT / "data/graph" / f"{SLUG}_network.gexf"

PERSONS = [
    {"id": 1, "name": "师虎", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "县委书记", "current_org": "中共旬邑县委员会", "source": "https://www.snxunyi.gov.cn/xwzx/jrxw/202607/t20260721_2102946.html"},
    {"id": 2, "name": "陈永胜", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "县长", "current_org": "旬邑县人民政府", "source": "https://www.snxunyi.gov.cn/xwzx/jrxw/202607/t20260724_2103665.html"},
    {"id": 3, "name": "党英群", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "县委常委、常务副县长", "current_org": "旬邑县人民政府", "source": "https://www.snxunyi.gov.cn/xwzx/jrxw/202607/t20260716_2101935.html"},
    {"id": 4, "name": "党飞", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "", "current_post": "副县长", "current_org": "旬邑县人民政府", "source": "https://www.snxunyi.gov.cn/zfxxgk/fdzdgknr_21212/gzjh_21218/202603/t20260306_2063488.html"},
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共旬邑县委员会", "type": "党委", "level": "县处级", "parent": "中共咸阳市委", "location": "陕西省咸阳市旬邑县"},
    {"id": 2, "name": "旬邑县人民政府", "type": "政府", "level": "县处级", "parent": "咸阳市人民政府", "location": "陕西省咸阳市旬邑县"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "截至2026年7月21日在任"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "截至2026年7月22日在任"},
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "常务副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记与县长党政主要领导搭档", "overlap_org": "中共旬邑县委员会/旬邑县人民政府", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记与县委常委、常务副县长", "overlap_org": "中共旬邑县委员会", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县长与常务副县长（政府领导班子共同工作）", "overlap_org": "旬邑县人民政府", "overlap_period": "2025-2026"},
]


def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    GEXF_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    try:
        create_tables(conn, overwrite=True)
        insert_persons(conn, PERSONS)
        insert_organizations(conn, ORGANIZATIONS)
        insert_positions(conn, POSITIONS)
        insert_relationships(conn, RELATIONSHIPS)
        print(f"DB ready: {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, {len(POSITIONS)} positions, {len(RELATIONSHIPS)} relationships")
    finally:
        conn.close()
    builder = GEXFBuilder(title=SLUG)
    for p in PERSONS:
        builder.add_person(id=p["id"], name=p["name"], current_post=p.get("current_post",""), current_org=p.get("current_org",""), gender=p.get("gender",""), ethnicity=p.get("ethnicity",""), birth=p.get("birth",""), source=p.get("source",""))
    for o in ORGANIZATIONS:
        builder.add_organization(id=o["id"] + 100000, name=o.get("name",""), org_type=o.get("type",""), level=o.get("level",""), location=o.get("location",""))
    for r in RELATIONSHIPS:
        builder.add_relationship(source=r["person_a"], target=r["person_b"], rel_type=r.get("type",""), context=r.get("context",""), overlap_org=r.get("overlap_org",""), overlap_period=r.get("overlap_period",""))
    builder.write(GEXF_PATH)
    print(f"GEXF ready: {GEXF_PATH}")
    print(f"Done: {DB_PATH}, {GEXF_PATH}")


if __name__ == "__main__":
    main()
