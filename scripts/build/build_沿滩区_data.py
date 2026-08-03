#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 沿滩区 (Yantan District), 自贡市, 四川省.

Research as of 2026-08-03 based on:
- 人民网四川频道 (2025-01-17) — 廖东任沿滩区委书记
- 封面新闻 (2021-09-27) — 刘军当选沿滩区委书记 (前任)
- 自贡日报数字报 (2024-12-28) — 廖东任前公示
- 沿滩区人民政府官网 — 李钢、张根祥等常委信息
- 自贡网 (2025-03-26) — 赵德本当选区长公告
- 沿滩区政府工作报告 (2026-02-24) — 赵德本作报告
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
        "work_start": "约2000年",
        "current_post": "沿滩区委书记",
        "current_org": "中共沿滩区委员会",
        "source": "人民网四川频道 2025-01-17; 自贡日报数字报 2024-12-28 任前公示; 封面新闻 2021-09-27",
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
    # ── Key Standing Committee ──
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
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沿滩区委常委、区纪委书记、区监委主任",
        "current_org": "中共沿滩区纪律检查委员会",
        "source": "廉洁沿滩官网 (lianjie.yantan.gov.cn)",
    },
    {
        "id": 12,
        "name": "张东明",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沿滩区委副书记",
        "current_org": "中共沿滩区委员会",
        "source": "沿滩区党建工作报道 (2025-03-31)",
    },
    {
        "id": 13,
        "name": "杨兵",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沿滩区人大常委会主任",
        "current_org": "沿滩区人民代表大会常务委员会",
        "source": "沿滩区党建工作会议新闻报道 (2025-03-31)",
    },
    # ── Historical Leaders ──
    {
        "id": 20,
        "name": "刘军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "封面新闻 2021-09-27 — 刘军当选沿滩区委书记",
    },
    {
        "id": 21,
        "name": "邹天才",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "百度搜索 — 邹天才曾任沿滩区委书记，早于廖东",
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
    {"id": 10, "name": "自流井区舒坪镇", "type": "乡镇/街道", "level": "乡科级", "parent": "自流井区", "location": "四川省自贡市自流井区"},
    {"id": 11, "name": "自流井区荣边镇", "type": "乡镇/街道", "level": "乡科级", "parent": "自流井区", "location": "四川省自贡市自流井区"},
    {"id": 12, "name": "中共自流井区委", "type": "党委", "level": "县处级", "parent": "中共自贡市委", "location": "四川省自贡市自流井区"},
    {"id": 13, "name": "富顺县", "type": "政府", "level": "县处级", "parent": "自贡市", "location": "四川省自贡市富顺县"},
    {"id": 14, "name": "共青团自流井区委", "type": "群团", "level": "乡科级", "parent": "共青团自贡市委", "location": "四川省自贡市自流井区"},
    {"id": 15, "name": "自流井区农林局", "type": "政府", "level": "乡科级", "parent": "自流井区人民政府", "location": "四川省自贡市自流井区"},
]

# ── POSITIONS ────────────────────────────────────────────────────────

positions = [
    # 廖东 career timeline
    {"person_id": 1, "org_id": 13, "title": "富顺县工作（基层）", "start": "约2000", "end": "约2005", "rank": "", "note": "早期在富顺县基层工作"},
    {"person_id": 1, "org_id": 14, "title": "共青团自流井区委副书记", "start": "约2005", "end": "约2008", "rank": "副科级", "note": ""},
    {"person_id": 1, "org_id": 15, "title": "自流井区农林局副局长", "start": "约2008", "end": "约2010", "rank": "副科级", "note": ""},
    {"person_id": 1, "org_id": 10, "title": "舒坪镇党委副书记、纪委书记", "start": "约2008", "end": "约2012", "rank": "正科级", "note": ""},
    {"person_id": 1, "org_id": 11, "title": "荣边镇镇长", "start": "约2010", "end": "约2013", "rank": "正科级", "note": ""},
    {"person_id": 1, "org_id": 9, "title": "自贡市人民检察院机关党委书记、党组成员", "start": "2013", "end": "2016-09", "rank": "副县级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "沿滩区委常委、组织部部长", "start": "2016-09", "end": "2019", "rank": "副县级", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "沿滩区委常委、常务副区长", "start": "2019", "end": "2021", "rank": "副县级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "沿滩区委副书记、区长", "start": "2021", "end": "2025-01", "rank": "正县级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "沿滩区委书记", "start": "2025-01", "end": "present", "rank": "正县级", "note": "2024年12月任前公示，2025年1月正式任区委书记"},
    # 赵德本
    {"person_id": 2, "org_id": 8, "title": "自贡市投资促进局党组书记、局长", "start": "约2022", "end": "2025-02", "rank": "正县级", "note": "任沿滩区长前职务"},
    {"person_id": 2, "org_id": 1, "title": "沿滩区委副书记、代理区长", "start": "2025-02", "end": "2025-03-26", "rank": "正县级", "note": "2025年2月任代理区长"},
    {"person_id": 2, "org_id": 2, "title": "沿滩区委副书记、区长", "start": "2025-03-26", "end": "present", "rank": "正县级", "note": "2025年3月26日区人大选举正式当选"},
    # 李钢
    {"person_id": 10, "org_id": 1, "title": "沿滩区委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "沿滩区人民政府党组副书记、常务副区长", "start": "", "end": "present", "rank": "副县级", "note": "官方页面确认(2026-05-15)"},
    # 张根祥
    {"person_id": 11, "org_id": 1, "title": "沿滩区委常委", "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 3, "title": "沿滩区纪委书记、监委主任", "start": "", "end": "present", "rank": "副县级", "note": "廉洁沿滩页面确认"},
    # 张东明
    {"person_id": 12, "org_id": 1, "title": "沿滩区委副书记", "start": "", "end": "present", "rank": "副县级", "note": "新闻确认"},
    # 杨兵
    {"person_id": 13, "org_id": 6, "title": "沿滩区人大常委会主任", "start": "", "end": "present", "rank": "正县级", "note": "新闻报道确认"},
    # Historical
    {"person_id": 20, "org_id": 1, "title": "沿滩区委书记（前任）", "start": "", "end": "约2021", "rank": "正县级", "note": "刘军，2021年9月当选"},
    {"person_id": 21, "org_id": 1, "title": "沿滩区委书记（前任）", "start": "", "end": "约2020", "rank": "正县级", "note": "邹天才，早于刘军"},
]

# ── RELATIONSHIPS ────────────────────────────────────────────────────

relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "党政搭档",
        "context": "廖东任区委书记，赵德本任区长，党政正职配合",
        "overlap_org": "沿滩区",
        "overlap_period": "2025-至今",
    },
    {
        "person_a": 1,
        "person_b": 20,
        "type": "前任-继任",
        "context": "廖东接替刘军任沿滩区委书记（刘军2021年9月当选，廖东2025年1月接任）",
        "overlap_org": "中共沿滩区委",
        "overlap_period": "2025",
    },
    {
        "person_a": 1,
        "person_b": 21,
        "type": "前任-继任",
        "context": "廖东的前任之一邹天才，早于刘军",
        "overlap_org": "中共沿滩区委",
        "overlap_period": "2025",
    },
    {
        "person_a": 1,
        "person_b": 10,
        "type": "上下级",
        "context": "廖东（区委书记）与李钢（常委、常务副区长）在沿滩区委班子共事",
        "overlap_org": "中共沿滩区委",
        "overlap_period": "2019-至今",
    },
    {
        "person_a": 1,
        "person_b": 11,
        "type": "上下级",
        "context": "廖东（区委书记）与张根祥（纪委书记）在沿滩区委班子共事",
        "overlap_org": "中共沿滩区委",
        "overlap_period": "2025-至今",
    },
    {
        "person_a": 1,
        "person_b": 12,
        "type": "上下级",
        "context": "廖东（区委书记）与张东明（区委副书记）在沿滩区委班子共事",
        "overlap_org": "中共沿滩区委",
        "overlap_period": "2025-至今",
    },
    {
        "person_a": 2,
        "person_b": 10,
        "type": "党政搭档",
        "context": "赵德本（区长）与李钢（常务副区长）在政府班子搭档",
        "overlap_org": "沿滩区人民政府",
        "overlap_period": "2025-至今",
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