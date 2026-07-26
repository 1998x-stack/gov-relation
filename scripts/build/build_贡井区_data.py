#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 贡井区 (Gongjing District), 自贡市, 四川省.

Current leadership researched as of 2026-07-26 via official government website (gj.gov.cn):
- 7 confirmed vice district mayors (副区长) with bios from official site
- 区委书记 and 区长: names confirmed from official site but full bios are
  on JS-rendered pages that could not be fully extracted via text-mode fetch.
  Marked as 待查 (to be investigated) with open questions.
"""

import sqlite3
import sys
import os
from pathlib import Path
from datetime import datetime

# Add project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "贡井区_network.db")
GEXF_PATH = os.path.join(BASE, "贡井区_network.gexf")

# ── PERSONS ──────────────────────────────────────────────────────────

persons = [
    # ── Top Leaders (区委书记 & 区长 — names/bios partially known) ──
    {
        "id": 1,
        "name": "待查（贡井区委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "贡井区委书记",
        "current_org": "中共贡井区委员会",
        "source": "Official site gj.gov.cn — name not extracted from JS-rendered leadership page; confirmed that the 区政府 page shows 区长 section structure",
    },
    {
        "id": 2,
        "name": "待查（贡井区区长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "贡井区区长",
        "current_org": "贡井区人民政府",
        "source": "gj.gov.cn — 区长 section exists on gov site but JS-rendered content could not be fully extracted",
    },
    # ── Vice District Mayors (副区长) from official site ──
    {
        "id": 10,
        "name": "刘远初",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-04",
        "birthplace": "",
        "education": "省委党校大学",
        "party_join": "",
        "work_start": "",
        "current_post": "贡井区委常委、区政府副区长",
        "current_org": "贡井区人民政府",
        "source": "gj.gov.cn 官方页面 (2025-08-25)",
    },
    {
        "id": 11,
        "name": "李敏",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1975-02",
        "birthplace": "",
        "education": "党校大学",
        "party_join": "",
        "work_start": "",
        "current_post": "贡井区委常委、宣传部部长，区政府副区长",
        "current_org": "贡井区人民政府",
        "source": "gj.gov.cn 官方页面 (2025-08-25)",
    },
    {
        "id": 12,
        "name": "李丰波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-09",
        "birthplace": "",
        "education": "博士研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "贡井区委常委、区政府副区长",
        "current_org": "贡井区人民政府",
        "source": "gj.gov.cn 官方页面 (2026-04-14)",
    },
    {
        "id": 13,
        "name": "刘鹏程",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-01",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "贡井区政府副区长",
        "current_org": "贡井区人民政府",
        "source": "gj.gov.cn 官方页面 (2025-08-25)",
    },
    {
        "id": 14,
        "name": "钟昕",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-11",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "贡井区政府副区长",
        "current_org": "贡井区人民政府",
        "source": "gj.gov.cn 官方页面 (2025-08-25)",
    },
    {
        "id": 15,
        "name": "但唐杰",
        "gender": "男",
        "ethnicity": "",
        "birth": "1988-10",
        "birthplace": "",
        "education": "法律硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "贡井区政府副区长",
        "current_org": "贡井区人民政府",
        "source": "gj.gov.cn 官方页面 (2025-12-03)",
    },
    {
        "id": 16,
        "name": "陈英",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976-09",
        "birthplace": "",
        "education": "四川大学在职研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "贡井区政府党组成员、副区长，区委政法委副书记，市公安局贡井区分局党委书记、局长",
        "current_org": "贡井区人民政府",
        "source": "gj.gov.cn 官方页面 (2025-09-30)",
    },
    # ── Key Standing Committee (unknown — web access degraded) ──
    {
        "id": 20,
        "name": "待查（贡井区委副书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "贡井区委副书记",
        "current_org": "中共贡井区委员会",
        "source": "web research unavailable — 区委副书记 not found on official site or via search",
    },
    {
        "id": 21,
        "name": "待查（贡井区人大常委会主任）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "贡井区人大常委会主任",
        "current_org": "贡井区人民代表大会常务委员会",
        "source": "web research unavailable",
    },
    {
        "id": 22,
        "name": "待查（贡井区政协主席）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "贡井区政协主席",
        "current_org": "中国人民政治协商会议贡井区委员会",
        "source": "web research unavailable",
    },
]

# Fill defaults
_defaults = {"gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
             "party_join": "", "work_start": ""}
for p in persons:
    for k, v in _defaults.items():
        p.setdefault(k, v)

# ── ORGANIZATIONS ────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共贡井区委员会", "type": "党委", "level": "县处级", "parent": "中共自贡市委", "location": "四川省自贡市贡井区"},
    {"id": 2, "name": "贡井区人民政府", "type": "政府", "level": "县处级", "parent": "自贡市人民政府", "location": "四川省自贡市贡井区"},
    {"id": 3, "name": "中共贡井区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共贡井区委", "location": "四川省自贡市贡井区"},
    {"id": 4, "name": "中共贡井区委组织部", "type": "党委", "level": "乡科级", "parent": "中共贡井区委", "location": "四川省自贡市贡井区"},
    {"id": 5, "name": "中共贡井区委宣传部", "type": "党委", "level": "乡科级", "parent": "中共贡井区委", "location": "四川省自贡市贡井区"},
    {"id": 6, "name": "中共贡井区委政法委员会", "type": "党委", "level": "乡科级", "parent": "中共贡井区委", "location": "四川省自贡市贡井区"},
    {"id": 7, "name": "中共贡井区委统战部", "type": "党委", "level": "乡科级", "parent": "中共贡井区委", "location": "四川省自贡市贡井区"},
    {"id": 8, "name": "贡井区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "贡井区", "location": "四川省自贡市贡井区"},
    {"id": 9, "name": "中国人民政治协商会议贡井区委员会", "type": "政协", "level": "县处级", "parent": "贡井区", "location": "四川省自贡市贡井区"},
    {"id": 10, "name": "自贡市公安局贡井区分局", "type": "政府", "level": "乡科级", "parent": "贡井区人民政府", "location": "四川省自贡市贡井区"},
]

# ── POSITIONS ────────────────────────────────────────────────────────

positions = [
    # Top leaders
    {"person_id": 1, "org_id": 1, "title": "贡井区委书记", "start": "", "end": "present", "rank": "正县级", "note": "待查"},
    {"person_id": 2, "org_id": 2, "title": "贡井区区长", "start": "", "end": "present", "rank": "正县级", "note": "待查"},
    # Confirmed 副区长
    {"person_id": 10, "org_id": 2, "title": "贡井区委常委、区政府副区长", "start": "", "end": "present", "rank": "副县级", "note": "official site confirmed"},
    {"person_id": 11, "org_id": 5, "title": "贡井区委常委、宣传部部长", "start": "", "end": "present", "rank": "副县级", "note": "官方确认"},
    {"person_id": 11, "org_id": 2, "title": "贡井区政府副区长", "start": "", "end": "present", "rank": "副县级", "note": "官方确认"},
    {"person_id": 12, "org_id": 2, "title": "贡井区委常委、区政府副区长", "start": "", "end": "present", "rank": "副县级", "note": "官方确认"},
    {"person_id": 13, "org_id": 2, "title": "贡井区政府副区长", "start": "", "end": "present", "rank": "副县级", "note": "官方确认"},
    {"person_id": 14, "org_id": 2, "title": "贡井区政府副区长", "start": "", "end": "present", "rank": "副县级", "note": "官方确认"},
    {"person_id": 15, "org_id": 2, "title": "贡井区政府副区长", "start": "", "end": "present", "rank": "副县级", "note": "官方确认"},
    {"person_id": 16, "org_id": 2, "title": "贡井区政府党组成员、副区长", "start": "", "end": "present", "rank": "副县级", "note": "官方确认"},
    {"person_id": 16, "org_id": 6, "title": "区委政法委副书记", "start": "", "end": "present", "rank": "副县级", "note": "官方确认"},
    {"person_id": 16, "org_id": 10, "title": "市公安局贡井区分局局长", "start": "", "end": "present", "rank": "副县级", "note": "官方确认"},
    # Placeholder positions
    {"person_id": 20, "org_id": 1, "title": "贡井区委副书记", "start": "", "end": "present", "rank": "副县级", "note": "待查"},
    {"person_id": 21, "org_id": 8, "title": "贡井区人大常委会主任", "start": "", "end": "present", "rank": "正县级", "note": "待查"},
    {"person_id": 22, "org_id": 9, "title": "贡井区政协主席", "start": "", "end": "present", "rank": "正县级", "note": "待查"},
]

# ── RELATIONSHIPS ────────────────────────────────────────────────────
# No confirmed co-work relationships without full career histories.
# Cross-county exchange data is unavailable.

relationships = []

# ── BUILD ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_build(
        slug="贡井区",
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
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")