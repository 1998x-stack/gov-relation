#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 沿滩区 (Yantan District), 自贡市, 四川省.

Current leadership researched as of 2026-07-26 via Baidu search and news sources:

Confirmed leaders:
- 区委书记: 廖东 (full career timeline known from Baidu AI summary + 人民网 + 自贡日报)
- 区长: 赵德本 (career partially known: 市投资促进局→沿滩区, 2025.03 elected)
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
DB_PATH = os.path.join(BASE, "沿滩区_network.db")
GEXF_PATH = os.path.join(BASE, "沿滩区_network.gexf")

# ── PERSONS ──────────────────────────────────────────────────────────

persons = [
    # ── Top Leader: 区委书记 ──
    {
        "id": 1,
        "name": "廖东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-10",
        "birthplace": "",
        "education": "在职大学、在职硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沿滩区委书记",
        "current_org": "中共沿滩区委员会",
        "source": "Baidu search AI summary; 人民网四川频道 2025-01-17; 自贡日报数字报 2024-12-28 任前公示",
    },
    # ── Top Leader: 区长 ──
    {
        "id": 2,
        "name": "赵德本",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-10",
        "birthplace": "",
        "education": "在职硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沿滩区委副书记、区长",
        "current_org": "沿滩区人民政府",
        "source": "人民网四川频道 2025-03-21; 自贡网 2025-03-26 选举公告; 沿滩区政府工作报告 2026-02-24",
    },
    # ── Key Standing Committee (partially known) ──
    {
        "id": 10,
        "name": "李钢",
        "gender": "男",
        "ethnicity": "羌族",
        "birth": "1987-02",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沿滩区委常委、常务副区长",
        "current_org": "沿滩区人民政府",
        "source": "沿滩区人民政府官网 (2026-05-15)",
    },
    {
        "id": 11,
        "name": "张根祥",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "沿滩区委常委、区纪委书记、区监委主任",
        "current_org": "中共沿滩区纪律检查委员会",
        "source": "廉洁沿滩官网 (lianjie.yantan.gov.cn)",
    },
    {
        "id": 12,
        "name": "待查（沿滩区委副书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "沿滩区委副书记",
        "current_org": "中共沿滩区委员会",
        "source": "not found on official site or via search",
    },
    {
        "id": 13,
        "name": "杨兵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "沿滩区人大常委会主任",
        "current_org": "沿滩区人民代表大会常务委员会",
        "source": "沿滩区党建工作会议新闻报道 (2025-03-31)",
    },
    {
        "id": 14,
        "name": "待查（沿滩区政协主席）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "沿滩区政协主席",
        "current_org": "中国人民政治协商会议沿滩区委员会",
        "source": "待查",
    },
    # ── 廖东's past roles (historical) ──
    # These are represented via the ID 1 person with multiple position entries
    # Former 区委书记 (before 廖东)
    {
        "id": 20,
        "name": "邹天才",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "Baidu near search — 邹天才曾任区委书记，早于廖东",
    },
    # Former 区长 (before 廖东 / before 赵德本)
    {
        "id": 21,
        "name": "待查（沿滩区前任区长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "待查 — 赵德之前任区长未在公开信息查获",
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
    {"id": 1, "name": "中共沿滩区委员会", "type": "党委", "level": "县处级", "parent": "中共自贡市委", "location": "四川省自贡市沿滩区"},
    {"id": 2, "name": "沿滩区人民政府", "type": "政府", "level": "县处级", "parent": "自贡市人民政府", "location": "四川省自贡市沿滩区"},
    {"id": 3, "name": "中共沿滩区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共沿滩区委", "location": "四川省自贡市沿滩区"},
    {"id": 4, "name": "中共沿滩区委组织部", "type": "党委", "level": "乡科级", "parent": "中共沿滩区委", "location": "四川省自贡市沿滩区"},
    {"id": 5, "name": "中共沿滩区委宣传部", "type": "党委", "level": "乡科级", "parent": "中共沿滩区委", "location": "四川省自贡市沿滩区"},
    {"id": 6, "name": "沿滩区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "沿滩区", "location": "四川省自贡市沿滩区"},
    {"id": 7, "name": "中国人民政治协商会议沿滩区委员会", "type": "政协", "level": "县处级", "parent": "沿滩区", "location": "四川省自贡市沿滩区"},
    {"id": 8, "name": "自贡市投资促进局", "type": "政府", "level": "县处级", "parent": "自贡市人民政府", "location": "四川省自贡市"},
    {"id": 9, "name": "自贡市人民检察院", "type": "司法", "level": "地厅级副职", "parent": "四川省人民检察院", "location": "四川省自贡市"},
    {"id": 10, "name": "自流井区舒坪镇", "type": "政府", "level": "乡科级", "parent": "自流井区", "location": "四川省自贡市自流井区"},
    {"id": 11, "name": "自流井区荣边镇", "type": "政府", "level": "乡科级", "parent": "自流井区", "location": "四川省自贡市自流井区"},
    {"id": 12, "name": "中共自流井区委", "type": "党委", "level": "县处级", "parent": "中共自贡市委", "location": "四川省自贡市自流井区"},
    {"id": 13, "name": "富顺县", "type": "政府", "level": "县处级", "parent": "自贡市", "location": "四川省自贡市富顺县"},
]

# ── POSITIONS ────────────────────────────────────────────────────────

positions = [
    # 廖东 career
    {"person_id": 1, "org_id": 13, "title": "富顺县（早期工作）", "start": "~2000", "end": "~2005", "rank": "", "note": "早期在富顺县工作"},
    {"person_id": 1, "org_id": 12, "title": "共青团自流井区委副书记", "start": "~2005", "end": "~2008", "rank": "副科级", "note": ""},
    {"person_id": 1, "org_id": 12, "title": "自流井区农林局副局长", "start": "~2008", "end": "~2010", "rank": "副科级", "note": ""},
    {"person_id": 1, "org_id": 10, "title": "舒坪镇党委副书记、纪委书记", "start": "~2008", "end": "~2012", "rank": "正科级", "note": ""},
    {"person_id": 1, "org_id": 11, "title": "荣边镇镇长", "start": "~2010", "end": "~2013", "rank": "正科级", "note": ""},
    {"person_id": 1, "org_id": 9, "title": "自贡市人民检察院机关党委书记、党组成员", "start": "2013", "end": "2016-09", "rank": "副县级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "沿滩区委常委、组织部部长", "start": "2016-09", "end": "2019", "rank": "副县级", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "沿滩区委常委、常务副区长", "start": "2019", "end": "2021", "rank": "副县级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "沿滩区委副书记、区长", "start": "2021", "end": "2025-01", "rank": "正县级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "沿滩区委书记", "start": "2025-01", "end": "present", "rank": "正县级", "note": "2024年12月任前公示，2025年1月正式任区委书记"},
    # 赵德本 — current
    {"person_id": 2, "org_id": 8, "title": "自贡市投资促进局党组书记、局长", "start": "~2022", "end": "2025-02", "rank": "正县级", "note": "任沿滩区长前职务"},
    {"person_id": 2, "org_id": 1, "title": "沿滩区委副书记、代理区长", "start": "2025-02", "end": "2025-03-26", "rank": "正县级", "note": "2025年2月任代理区长"},
    {"person_id": 2, "org_id": 1, "title": "沿滩区委副书记、区长", "start": "2025-03-26", "end": "present", "rank": "正县级", "note": "2025年3月26日区人大选举正式当选"},
    # 李钢 — 常务副区长
    {"person_id": 10, "org_id": 1, "title": "沿滩区委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "沿滩区人民政府党组副书记、常务副区长", "start": "", "end": "present", "rank": "副县级", "note": "官方页面确认(2026-05-15)"},
    # 张根祥 — 纪委书记
    {"person_id": 11, "org_id": 1, "title": "沿滩区委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 3, "title": "沿滩区纪委书记、监委主任", "start": "", "end": "present", "rank": "副县级", "note": "廉洁沿滩页面确认"},
    # Placeholder positions
    {"person_id": 12, "org_id": 1, "title": "沿滩区委副书记", "start": "", "end": "present", "rank": "副县级", "note": "待查"},
    {"person_id": 13, "org_id": 6, "title": "沿滩区人大常委会主任", "start": "", "end": "present", "rank": "正县级", "note": "新闻报道确认"},
    {"person_id": 14, "org_id": 7, "title": "沿滩区政协主席", "start": "", "end": "present", "rank": "正县级", "note": "待查"},
    # Historical — 前任
    {"person_id": 20, "org_id": 1, "title": "沿滩区委书记（前任）", "start": "", "end": "~2024", "rank": "正县级", "note": "邹天才，为廖东前任"},
]

# ── RELATIONSHIPS ────────────────────────────────────────────────────
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "先后接任",
        "context": "廖东升任书记后，赵德本接任区长",
        "overlap_org": "沿滩区",
        "overlap_period": "2025-至今",
    },
    {
        "person_a": 1,
        "person_b": 20,
        "type": "前任-继任",
        "context": "廖东接替邹天才任沿滩区委书记",
        "overlap_org": "中共沿滩区委",
        "overlap_period": "2025",
    },
]

# ── BUILD ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_build(
        slug="沿滩区",
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
