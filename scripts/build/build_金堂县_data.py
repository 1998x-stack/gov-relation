#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 金堂县 (Jintang County), Chengdu, Sichuan.

Current leadership researched as of July 2026.
"""

import sqlite3
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# Staging directory
BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "金堂县_network.db")
GEXF_PATH = os.path.join(BASE, "金堂县_network.gexf")

# ── PERSONS ──────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    {
        "id": 1,
        "name": "钟静远",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "金堂县委书记",
        "current_org": "中共金堂县委员会",
        "source": "https://zh.wikipedia.org/wiki/金堂县",
    },
    {
        "id": 2,
        "name": "王安寧",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "金堂县县长",
        "current_org": "金堂县人民政府",
        "source": "https://zh.wikipedia.org/wiki/金堂县",
    },
    # ── Key Standing Committee Members (partial - web access degraded) ──
    {
        "id": 10,
        "name": "姜克锦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "金堂县委常委、金堂县人民政府常务副县长",
        "current_org": "金堂县人民政府",
        "source": "https://www.jintang.gov.cn/",
    },
    {
        "id": 11,
        "name": "曹波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "金堂县委常委、组织部部长",
        "current_org": "中共金堂县委组织部",
        "source": "https://www.jintang.gov.cn/",
    },
    {
        "id": 12,
        "name": "罗勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "金堂县委常委、政法委书记",
        "current_org": "中共金堂县委政法委员会",
        "source": "https://www.jintang.gov.cn/",
    },
    {
        "id": 13,
        "name": "何兴轩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "金堂县委常委、宣传部部长",
        "current_org": "中共金堂县委宣传部",
        "source": "https://www.jintang.gov.cn/",
    },
    # ── Predecessors ──
    {
        "id": 20,
        "name": "古建桥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任金堂县县长（2019-2023）",
        "current_org": "",
        "source": "https://zh.wikipedia.org/zh-cn/金堂县",
    },
    {
        "id": 21,
        "name": "辜学斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任金堂县委书记",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/金堂县",
    },
]

# ── ORGANIZATIONS ───────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共金堂县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共成都市委员会",
        "location": "四川省成都市金堂县赵镇街道",
    },
    {
        "id": 2,
        "name": "金堂县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "成都市人民政府",
        "location": "四川省成都市金堂县赵镇街道",
    },
    {
        "id": 3,
        "name": "金堂县人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "成都市人民代表大会常务委员会",
        "location": "四川省成都市金堂县赵镇街道",
    },
    {
        "id": 4,
        "name": "中国共产党金堂县纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共成都市纪律检查委员会",
        "location": "四川省成都市金堂县赵镇街道",
    },
    {
        "id": 5,
        "name": "金堂县委组织部",
        "type": "党委",
        "level": "县处级",
        "location": "四川省成都市金堂县赵镇街道",
    },
    {
        "id": 6,
        "name": "金堂县委宣传部",
        "type": "党委",
        "level": "县处级",
        "location": "四川省成都市金堂县赵镇街道",
    },
    {
        "id": 7,
        "name": "金堂县委政法委",
        "type": "党委",
        "level": "县处级",
        "location": "四川省成都市金堂县赵镇街道",
    },
    {
        "id": 8,
        "name": "金堂县政协",
        "type": "政协",
        "level": "县处级",
        "location": "四川省成都市金堂县赵镇街道",
    },
]

# ── POSITIONS ───────────────────────────────────────────────────────────
positions = [
    # Current
    {"person_id": 1, "org_id": 1, "title": "金堂县委书记", "start": "2021", "end": "至今", "rank": "县处级正职", "note": "confirmed by Wikipedia"},
    {"person_id": 2, "org_id": 2, "title": "金堂县人民政府县长", "start": "2023-10", "end": "至今", "rank": "县处级正职", "note": "confirmed by Wikipedia infobox"},
    {"person_id": 10, "org_id": 2, "title": "金堂县委常委、常务副县长", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 5, "title": "金堂县委常委、组织部部长", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 7, "title": "金堂县委常委、政法委书记", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 13, "org_id": 6, "title": "金堂县委常委、宣传部部长", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    # Predecessors
    {"person_id": 20, "org_id": 2, "title": "金堂县县长", "start": "2019", "end": "2023", "rank": "县处级正职", "note": "predecessor to 王安寧"},
    {"person_id": 21, "org_id": 1, "title": "金堂县委书记", "start": "2018", "end": "2021", "rank": "县处级正职", "note": "predecessor to 钟静远"},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────────
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "钟静远作为县委书记与县长王安寧搭班子",
        "overlap_org": "金堂县",
        "overlap_period": "2023至今",
    },
    {
        "person_a": 1,
        "person_b": 21,
        "type": "predecessor_successor",
        "context": "钟静远接替晏学斌任金堂县委书记",
        "overlap_org": "中共金堂县委员会",
        "overlap_period": "2021",
    },
    {
        "person_a": 2,
        "person_b": 20,
        "type": "predecessor_successor",
        "context": "王安寧接替古建桥任金堂县县长",
        "overlap_org": "金堂县人民政府",
        "overlap_period": "2023",
    },
]

# ── BUILD ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_build(
        slug="金堂县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("Done. Files written to staging:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")