#!/usr/bin/env python3
"""Cross-county cadre exchange network supplement for 栖霞市, Shandong.

This script adds the cross-county transfer data discovered during Phase 1 research
that was not included in the original build_栖霞市_data.py.
"""

import sqlite3
import os
import sys

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/栖霞市_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/栖霞市_network.gexf")

sys.path.insert(0, BASE)
from gov_relation.schema import create_tables, insert_persons, insert_organizations, insert_positions, insert_relationships  # noqa

# --- CROSS-COUNTY TRANSFER FOCUSED DATA ---

persons = [
    {"id": 6, "name": "于晓丽", "gender": "女", "ethnicity": "汉族",
     "birth": "1980-12", "birthplace": "山东省龙口市(推测)",
     "education": "大学，法律硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "栖霞市副市长", "current_org": "栖霞市人民政府",
     "source": "齐鲁壹点(2025-09-08); 烟台市委组织部任前公示(2025-08-27)"},
    {"id": 7, "name": "周怀阔", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "栖霞市副市长", "current_org": "栖霞市人民政府",
     "source": "齐鲁壹点(2024-03-26)"},
    {"id": 8, "name": "李波", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "烟台市副市长(兼原栖霞市委书记)", "current_org": "烟台市人民政府",
     "source": "烟台广播电视台(2021-04-23)"},
    {"id": 9, "name": "林香志", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "栖霞市副市长(2020年在任)", "current_org": "栖霞市人民政府",
     "source": "山东卫视(2020-06-01)"},
    {"id": 10, "name": "姜力", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "栖霞市监察委员会主任", "current_org": "栖霞市监察委员会",
     "source": "栖霞市人大公告(2024-03-26)"},
    {"id": 11, "name": "陈龙", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "栖霞市监察委员会委员", "current_org": "栖霞市监察委员会",
     "source": "栖霞市人大公告(2024-03-26)"},
]

organizations = [
    {"id": 6, "name": "龙口市北马镇委员会", "type": "党委", "level": "乡镇级",
     "parent": "中共龙口市委员会", "location": "山东省烟台市龙口市北马镇"},
    {"id": 7, "name": "中共蓬莱区委员会", "type": "党委", "level": "县级",
     "parent": "中共烟台市委员会", "location": "山东省烟台市蓬莱区"},
    {"id": 8, "name": "栖霞市监察委员会", "type": "纪委/监委", "level": "县级",
     "parent": "烟台市监察委员会", "location": "山东省烟台市栖霞市"},
]

positions = [
    # 于晓丽-龙口→栖霞 (关键跨县流转)
    {"person_id": 6, "org_id": 6, "title": "龙口市北马镇党委书记、一级主任科员",
     "start_date": "", "end_date": "2025-08", "rank": "正科级",
     "note": "跨县提拔至栖霞"},
    {"person_id": 6, "org_id": 2, "title": "栖霞市人民政府副市长",
     "start_date": "2025-09-08", "end_date": "", "rank": "副县级",
     "note": "烟台市委组织部任前公示(2025-08-27)→人大任命(2025-09-08)"},

    # 周怀阔
    {"person_id": 7, "org_id": 2, "title": "栖霞市人民政府副市长",
     "start_date": "2024-03-26", "end_date": "", "rank": "副县级",
     "note": "栖霞市十八届人大常委会第二十次会议任命"},

    # 李波
    {"person_id": 8, "org_id": 1, "title": "栖霞市委书记(烟台市副市长兼任)",
     "start_date": "", "end_date": "2021-04", "rank": "县级",
     "note": "不再兼任，由包华接任"},

    # 林香志
    {"person_id": 9, "org_id": 2, "title": "栖霞市人民政府副市长",
     "start_date": "", "end_date": "", "rank": "副县级",
     "note": "2020年山东卫视采访中在任"},

    # 姜力
    {"person_id": 10, "org_id": 8, "title": "栖霞市监察委员会主任",
     "start_date": "", "end_date": "", "rank": "副县级",
     "note": "2024年3月仍在任"},

    # 陈龙
    {"person_id": 11, "org_id": 8, "title": "栖霞市监察委员会委员",
     "start_date": "2024-03-26", "end_date": "", "rank": "科级",
     "note": "市十八届人大常委会第二十次会议任命"},
]

relationships = [
    # 跨县交流关系
    {"person_a": 6, "person_b": 5, "type": "跨县调入",
     "context": "于晓丽从龙口市北马镇党委书记调任栖霞市副市长",
     "overlap_org": "栖霞市人民政府", "overlap_period": "2025-09至今"},
    {"person_a": 5, "person_b": 8, "type": "职务交接",
     "context": "包华接替李波任栖霞市委书记(李波不再兼任)",
     "overlap_org": "中共栖霞市委员会", "overlap_period": "2021-04"},
    {"person_a": 5, "person_b": 3, "type": "职务交接",
     "context": "包华接替被免职的姚秀霞任栖霞市委书记",
     "overlap_org": "中共栖霞市委员会", "overlap_period": "2021-02至2021-04"},
    {"person_a": 10, "person_b": 11, "type": "上下级",
     "context": "姜力(监委主任)—陈龙(监委委员)",
     "overlap_org": "栖霞市监察委员会", "overlap_period": "2024-03至今"},
]

# --- BUILD ---
os.makedirs(os.path.dirname(DB_PATH) if os.path.dirname(DB_PATH) else ".", exist_ok=True)

try:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    cur = conn.cursor()
    create_tables(conn)

    insert_persons(conn, persons)
    insert_organizations(conn, organizations)
    insert_positions(conn, positions)
    insert_relationships(conn, relationships)
    conn.commit()
    print(f"OK: Appended {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships to {DB_PATH}")

except sqlite3.OperationalError as e:
    if "already exists" in str(e):
        print(f"Note: May have partial duplicates (expected for re-run): {e}")
    else:
        raise
finally:
    conn.close()

# --- GEXF ---
from gov_relation.gexf import GEXFBuilder  # noqa

try:
    builder = GEXFBuilder("栖霞市跨县干部交流网络")
    for p in persons:
        builder.add_person(p["id"], p["name"],
                           current_post=p["current_post"],
                           current_org=p["current_org"],
                           gender=p["gender"],
                           birth=p["birth"],
                           source=p["source"])
    for o in organizations:
        builder.add_organization(o["id"], o["name"], o["type"], o["level"])
    for pos in positions:
        builder.add_relationship(pos["person_id"], pos["org_id"], "任职", pos["title"])
    for r in relationships:
        builder.add_relationship(r["person_a"], r["person_b"], r["type"], r["context"])
    builder.write(GEXF_PATH)
    print(f"OK GEXF: {GEXF_PATH}")
except Exception as e:
    print(f"GEXF generation note: {e}")
    print("(GEXF may already exist from the original build script)")
