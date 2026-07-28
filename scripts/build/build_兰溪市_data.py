#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 兰溪市 (Lanxi City, Zhejiang) leadership network.

归口地区: 浙江省金华市代管县级市
"""

import sqlite3
import os
import sys
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))
print(f"sys.path adjusted to reach repo root from: {os.path.dirname(__file__)}")

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "兰溪市"
PROVINCE = "浙江省"
PARENT_CITY = "金华市"
TODAY = "2026-07-28"

DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"

# ═══════════════════════════════════════════════════════════════════════════
# DATA — hardcoded research data
# Sources: Official 兰溪市政府网站, Baidu Baike, appointment notices
# ═══════════════════════════════════════════════════════════════════════════

persons = [
    # (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
    {
        "id": 1,
        "name": "戴翀",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年（推测）",
        "birthplace": "待查",
        "education": "大学（推测）",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兰溪市委书记",
        "current_org": "中共兰溪市委员会",
    },
    {
        "id": 2,
        "name": "朱俊华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兰溪市委副书记、市长",
        "current_org": "兰溪市人民政府",
    },
    {
        "id": 3,
        "name": "张群环",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年（推测）",
        "birthplace": "浙江金东（推测）",
        "education": "大学（推测）",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "金华市金东区委书记（前任兰溪市委书记）",
        "current_org": "中共金华市金东区委员会",
    },
    {
        "id": 4,
        "name": "王新锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查（前任兰溪市长）",
        "current_org": "待查",
    },
    {
        "id": 5,
        "name": "傅兢",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兰溪市委常委、常务副市长",
        "current_org": "兰溪市人民政府",
    },
    {
        "id": 6,
        "name": "厉昂",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兰溪市委常委、组织部部长",
        "current_org": "中共兰溪市委组织部",
    },
    {
        "id": 7,
        "name": "孙东升",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兰溪市委常委、市纪委书记、市监委主任",
        "current_org": "中共兰溪市纪委/兰溪市监委",
    },
]

organizations = [
    {"id": 1, "name": "中共兰溪市委员会", "type": "党委", "level": "县级", "parent": PARENT_CITY, "location": PROVINCE},
    {"id": 2, "name": "兰溪市人民政府", "type": "政府", "level": "县级", "parent": PARENT_CITY, "location": PROVINCE},
    {"id": 3, "name": "中共兰溪市委组织部", "type": "党委", "level": "县级", "parent": "中共兰溪市委员会", "location": PROVINCE},
    {"id": 4, "name": "中共兰溪市纪委/兰溪市监委", "type": "党委", "level": "县级", "parent": "中共兰溪市委员会", "location": PROVINCE},
    {"id": 5, "name": "中共金华市金东区委员会", "type": "党委", "level": "县级", "parent": "中共金华市委员会", "location": PROVINCE},
    {"id": 6, "name": "中共金华市委员会", "type": "党委", "level": "地市级", "parent": PROVINCE, "location": PROVINCE},
]

positions = [
    # -- 戴翀 --
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2023年（推测）", "end_date": "至今", "rank": "正处级"},
    # -- 朱俊华 --
    {"person_id": 2, "org_id": 2, "title": "市委副书记、市长", "start_date": "2022年（推测）", "end_date": "至今", "rank": "正处级"},
    # -- 张群环 (前任市委书记) --
    {"person_id": 3, "org_id": 1, "title": "市委书记", "start_date": "约2021", "end_date": "2023", "rank": "正处级"},
    {"person_id": 3, "org_id": 5, "title": "区委副书记", "start_date": "2023", "end_date": "至今", "rank": "正处级"},
    # -- 王新锋 (前任市长) --
    {"person_id": 4, "org_id": 2, "title": "市长", "start_date": "约2019", "end_date": "约2022", "rank": "正处级"},
    # -- 傅兢 --
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    {"person_id": 5, "org_id": 2, "title": "常务副市长", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    # -- 陆昂 --
    {"person_id": 6, "org_id": 1, "title": "市委常委", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    {"person_id": 6, "org_id": 3, "title": "组织部部长", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    # -- 孙建升 --
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    {"person_id": 7, "org_id": 4, "title": "市纪委书记、市监委主任", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
]

relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "市委书记与市长搭班子",
        "overlap_org": "中共兰溪市委员会/兰溪市人民政府",
        "overlap_period": "2022至今",
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "predecessor_successor",
        "context": "戴翀接替张群环担任兰溪市委书记",
        "overlap_org": "中共兰溪市委员会",
        "overlap_period": "2023",
    },
    {
        "person_a": 2,
        "person_b": 4,
        "type": "predecessor_successor",
        "context": "朱俊华接替王新锋担任兰溪市市长",
        "overlap_org": "兰溪市人民政府",
        "overlap_period": "约2022",
    },
    {
        "person_a": 5,
        "person_b": 1,
        "type": "superior_subordinate",
        "context": "常务副市长为市委书记下级",
        "overlap_org": "中共兰溪市委员会",
        "overlap_period": "待查",
    },
    {
        "person_a": 6,
        "person_b": 1,
        "type": "superior_subordinate",
        "context": "组织部长为市委书记下级",
        "overlap_org": "中共兰溪市委员会",
        "overlap_period": "待查",
    },
    {
        "person_a": 7,
        "person_b": 1,
        "type": "superior_subordinate",
        "context": "市纪委书记为市委书记下级",
        "overlap_org": "中共兰溪市委员会",
        "overlap_period": "待查",
    },
]

# ═══════════════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    # Manual GEXF extension using string formatting for viz namespace safety
    # (GEXFBuilder handles this, but verify output exists)
    db_size = os.path.getsize(DB_PATH) if os.path.exists(DB_PATH) else 0
    gexf_size = os.path.getsize(GEXF_PATH) if os.path.exists(GEXF_PATH) else 0
    print(f"Database: {DB_PATH} ({db_size} bytes)")
    print(f"GEXF graph: {GEXF_PATH} ({gexf_size} bytes)")
    print(f"Persons: {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")
    print("Build complete.")