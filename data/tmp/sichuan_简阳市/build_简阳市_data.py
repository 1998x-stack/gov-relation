#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 简阳市 (Jianyang City), Chengdu, Sichuan.

简阳市 is a county-level city under Chengdu, Sichuan Province.
As of July 2026, web access was severely degraded during research,
so many biographical fields are marked as "待查" (to be investigated).

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
DB_PATH = os.path.join(BASE, "简阳市_network.db")
GEXF_PATH = os.path.join(BASE, "简阳市_network.gexf")

# ── PERSONS ──────────────────────────────────────────────────────────
# NOTE: Web research was severely limited. Names marked "待查" indicate
# the current officeholder's identity could not be confirmed from
# publicly accessible sources during this research cycle.
# Implicit: the placeholder ID prefix "unknown_" allows future updates.

persons = [
    # ── Current Top Leaders ──
    {
        "id": 1,
        "name": "待查（简阳市委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "简阳市委书记",
        "current_org": "中共简阳市委员会",
        "source": "web research unavailable",
    },
    {
        "id": 2,
        "name": "待查（简阳市市长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "简阳市市长",
        "current_org": "简阳市人民政府",
        "source": "web research unavailable",
    },
    # ── Key Standing Committee Members (unknown — web access degraded) ──
    {
        "id": 10,
        "name": "待查（简阳市委副书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "简阳市委副书记",
        "current_org": "中共简阳市委员会",
        "source": "web research unavailable",
    },
    {
        "id": 11,
        "name": "待查（简阳市委常委、常务副市长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "简阳市委常委、常务副市长",
        "current_org": "简阳市人民政府",
        "source": "web research unavailable",
    },
    {
        "id": 12,
        "name": "待查（简阳市委常委、组织部部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "简阳市委常委、组织部部长",
        "current_org": "中共简阳市委组织部",
        "source": "web research unavailable",
    },
    {
        "id": 13,
        "name": "待查（简阳市委常委、纪委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "简阳市委常委、纪委书记、监委主任",
        "current_org": "中共简阳市纪律检查委员会",
        "source": "web research unavailable",
    },
    {
        "id": 14,
        "name": "待查（简阳市委常委、政法委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "简阳市委常委、政法委书记",
        "current_org": "中共简阳市委政法委员会",
        "source": "web research unavailable",
    },
    {
        "id": 15,
        "name": "待查（简阳市委常委、宣传部部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "简阳市委常委、宣传部部长",
        "current_org": "中共简阳市委宣传部",
        "source": "web research unavailable",
    },
]

# ── ORGANIZATIONS ───────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共简阳市委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共成都市委员会",
        "location": "四川省成都市简阳市射洪坝街道",
    },
    {
        "id": 2,
        "name": "简阳市人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "成都市人民政府",
        "location": "四川省成都市简阳市射洪坝街道",
    },
    {
        "id": 3,
        "name": "简阳市人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "成都市人民代表大会常务委员会",
        "location": "四川省成都市简阳市射洪坝街道",
    },
    {
        "id": 4,
        "name": "中国共产党简阳市纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共成都市纪律检查委员会",
        "location": "四川省成都市简阳市射洪坝街道",
    },
    {
        "id": 5,
        "name": "中共简阳市委组织部",
        "type": "党委",
        "level": "县处级",
        "location": "四川省成都市简阳市射洪坝街道",
    },
    {
        "id": 6,
        "name": "中共简阳市委宣传部",
        "type": "党委",
        "level": "县处级",
        "location": "四川省成都市简阳市射洪坝街道",
    },
    {
        "id": 7,
        "name": "中共简阳市委政法委员会",
        "type": "党委",
        "level": "县处级",
        "location": "四川省成都市简阳市射洪坝街道",
    },
    {
        "id": 8,
        "name": "简阳市政协",
        "type": "政协",
        "level": "县处级",
        "location": "四川省成都市简阳市射洪坝街道",
    },
    {
        "id": 9,
        "name": "简阳市监察委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "成都市监察委员会",
        "location": "四川省成都市简阳市射洪坝街道",
    },
    {
        "id": 10,
        "name": "简阳市人民政府办公室",
        "type": "政府",
        "level": "县处级",
        "location": "四川省成都市简阳市射洪坝街道",
    },
]

# ── POSITIONS ───────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "简阳市委书记", "start": "", "end": "至今", "rank": "县处级正职", "note": "identity not confirmed during this research cycle"},
    {"person_id": 2, "org_id": 2, "title": "简阳市人民政府市长", "start": "", "end": "至今", "rank": "县处级正职", "note": "identity not confirmed during this research cycle"},
    {"person_id": 10, "org_id": 1, "title": "简阳市委副书记", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "简阳市委常委、常务副市长", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 5, "title": "简阳市委常委、组织部部长", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 13, "org_id": 4, "title": "简阳市委常委、纪委书记、监委主任", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 14, "org_id": 7, "title": "简阳市委常委、政法委书记", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 15, "org_id": 6, "title": "简阳市委常委、宣传部部长", "start": "", "end": "", "rank": "县处级副职", "note": ""},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────────
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "市委书记与市长搭班子",
        "overlap_org": "简阳市",
        "overlap_period": "至今",
    },
    {
        "person_a": 1,
        "person_b": 10,
        "type": "superior_subordinate",
        "context": "市委书记与副书记搭班子",
        "overlap_org": "中共简阳市委员会",
        "overlap_period": "至今",
    },
]

# ── BUILD ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_build(
        slug="简阳市",
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