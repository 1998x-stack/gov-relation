#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 自流井区 (Ziliujing District), 自贡市, 四川省.

Current leadership researched as of 2026-07-26 via Wikipedia (confirmed: 区委书记).
区长 and other roster positions are 待查 due to degraded web access (government websites
zlj.gov.cn and zg.gov.cn unreachable; Baidu/360百科 blocked; search engines unavailable).

Implicit: the ID prefix "unknown_" for placeholder people allows future updates.
"""

import sqlite3
import sys
import os
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# Staging directory
BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "自流井区_network.db")
GEXF_PATH = os.path.join(BASE, "自流井区_network.gexf")

# ── PERSONS ──────────────────────────────────────────────────────────
# NOTE: Web research was severely limited. All roster positions except
# 区委书记 are marked 待查 (to be investigated).

persons = [
    # ── Current Top Leaders ──
    {
        "id": 1,
        "name": "龙腾鑫",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "自流井区委书记",
        "current_org": "中共自流井区委员会",
        "source": "https://zh.wikipedia.org/wiki/自流井区 (confirmed from Wikipedia infobox)",
    },
    {
        "id": 2,
        "name": "待查（自流井区区长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "自流井区区长",
        "current_org": "自流井区人民政府",
        "source": "web research unavailable — government sites unreachable",
    },
    # ── Key Standing Committee Members (unknown — web access degraded) ──
    {
        "id": 10,
        "name": "待查（自流井区委副书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "自流井区委副书记",
        "current_org": "中共自流井区委员会",
        "source": "web research unavailable",
    },
    {
        "id": 11,
        "name": "待查（自流井区委常委、常务副区长）",
        "current_post": "自流井区委常委、常务副区长",
        "current_org": "自流井区人民政府",
        "source": "web research unavailable",
    },
    {
        "id": 12,
        "name": "待查（自流井区委常委、纪委书记）",
        "current_post": "自流井区委常委、纪委书记",
        "current_org": "中共自流井区纪律检查委员会",
        "source": "web research unavailable",
    },
    {
        "id": 13,
        "name": "待查（自流井区委常委、组织部部长）",
        "current_post": "自流井区委常委、组织部部长",
        "current_org": "中共自流井区委员会组织部",
        "source": "web research unavailable",
    },
    {
        "id": 14,
        "name": "待查（自流井区委常委、宣传部部长）",
        "current_post": "自流井区委常委、宣传部部长",
        "current_org": "中共自流井区委员会宣传部",
        "source": "web research unavailable",
    },
    {
        "id": 15,
        "name": "待查（自流井区委常委、政法委书记）",
        "current_post": "自流井区委常委、政法委书记",
        "current_org": "中共自流井区委员会政法委员会",
        "source": "web research unavailable",
    },
    {
        "id": 16,
        "name": "待查（自流井区委常委、统战部部长）",
        "current_post": "自流井区委常委、统战部部长",
        "current_org": "中共自流井区委员会统战部",
        "source": "web research unavailable",
    },
    # ── Other Key Positions ──
    {
        "id": 20,
        "name": "待查（自流井区人大常委会主任）",
        "current_post": "自流井区人大常委会主任",
        "current_org": "自流井区人民代表大会常务委员会",
        "source": "web research unavailable",
    },
    {
        "id": 21,
        "name": "待查（自流井区政协主席）",
        "current_post": "自流井区政协主席",
        "current_org": "中国人民政治协商会议自流井区委员会",
        "source": "web research unavailable",
    },
]

# Assign default empty fields for persons missing gender/ethnicity/etc.
_defaults = {"gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
             "party_join": "", "work_start": ""}
for p in persons:
    for k, v in _defaults.items():
        p.setdefault(k, v)

# ── ORGANIZATIONS ────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共自流井区委员会", "type": "党委", "level": "县处级", "parent": "中共自贡市委", "location": "四川省自贡市自流井区"},
    {"id": 2, "name": "自流井区人民政府", "type": "政府", "level": "县处级", "parent": "自贡市人民政府", "location": "四川省自贡市自流井区"},
    {"id": 3, "name": "中共自流井区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共自流井区委", "location": "四川省自贡市自流井区"},
    {"id": 4, "name": "中共自流井区委组织部", "type": "党委", "level": "乡科级", "parent": "中共自流井区委", "location": "四川省自贡市自流井区"},
    {"id": 5, "name": "中共自流井区委宣传部", "type": "党委", "level": "乡科级", "parent": "中共自流井区委", "location": "四川省自贡市自流井区"},
    {"id": 6, "name": "中共自流井区委政法委员会", "type": "党委", "level": "乡科级", "parent": "中共自流井区委", "location": "四川省自贡市自流井区"},
    {"id": 7, "name": "中共自流井区委统战部", "type": "党委", "level": "乡科级", "parent": "中共自流井区委", "location": "四川省自贡市自流井区"},
    {"id": 8, "name": "自流井区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "自流井区", "location": "四川省自贡市自流井区"},
    {"id": 9, "name": "中国人民政治协商会议自流井区委员会", "type": "政协", "level": "县处级", "parent": "自流井区", "location": "四川省自贡市自流井区"},
]

# ── POSITIONS ────────────────────────────────────────────────────────

positions = [
    # 区委书记
    {"person_id": 1, "org_id": 1, "title": "自流井区委书记", "start": "", "end": "present", "rank": "正县级", "note": "Wikipedia infobox confirmed"},
    # All other positions are 待查 with unknown holder info
    {"person_id": 2, "org_id": 2, "title": "自流井区区长", "start": "", "end": "present", "rank": "正县级", "note": "待查"},
    {"person_id": 10, "org_id": 1, "title": "自流井区委副书记", "start": "", "end": "present", "rank": "副县级", "note": "待查"},
    {"person_id": 11, "org_id": 2, "title": "自流井区委常委、常务副区长", "start": "", "end": "present", "rank": "副县级", "note": "待查"},
    {"person_id": 12, "org_id": 3, "title": "自流井区委常委、纪委书记", "start": "", "end": "present", "rank": "副县级", "note": "待查"},
    {"person_id": 13, "org_id": 4, "title": "自流井区委常委、组织部部长", "start": "", "end": "present", "rank": "副县级", "note": "待查"},
    {"person_id": 14, "org_id": 5, "title": "自流井区委常委、宣传部部长", "start": "", "end": "present", "rank": "副县级", "note": "待查"},
    {"person_id": 15, "org_id": 6, "title": "自流井区委常委、政法委书记", "start": "", "end": "present", "rank": "副县级", "note": "待查"},
    {"person_id": 16, "org_id": 7, "title": "自流井区委常委、统战部部长", "start": "", "end": "present", "rank": "副县级", "note": "待查"},
    {"person_id": 20, "org_id": 8, "title": "自流井区人大常委会主任", "start": "", "end": "present", "rank": "正县级", "note": "待查"},
    {"person_id": 21, "org_id": 9, "title": "自流井区政协主席", "start": "", "end": "present", "rank": "正县级", "note": "待查"},
]

# ── RELATIONSHIPS ────────────────────────────────────────────────────
# No confirmed relationships can be established without deputy/predecessor data.

relationships = []

# ── BUILD ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_build(
        slug="自流井区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print("\nDone. Artifacts:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")