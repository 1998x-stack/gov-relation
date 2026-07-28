#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 福海县 (Fuhai County) leadership network.

福海县 — 新疆维吾尔自治区阿勒泰地区下辖县。
位于新疆北部、阿勒泰地区中部，总面积3.24万平方公里，辖3乡3镇，总人口6.5万人。

Research conducted: 2026-07-28
Data sources: 福海县人民政府网站 (www.xjfhx.gov.cn) — official government leadership pages,
news articles ("福海零距离"), and public announcements.
Data currency: 2026-07 (current as of July 2026)
"""

import json
import os
import sqlite3  # noqa: used by gov_relation.schema via runner
import sys
from datetime import datetime

# Ensure gov_relation package is importable
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Paths ──────────────────────────────────────────────────────────────
TMP = os.path.join(BASE, "data/tmp/xinjiang_福海县")
DB_PATH = os.path.join(TMP, "福海县_network.db")
GEXF_PATH = os.path.join(TMP, "福海县_network.gexf")

# ── DATA ──────────────────────────────────────────────────────────────
# Person ID convention used in this build: fuhai_<pinyin>
# Source: www.xjfhx.gov.cn leadership page, accessed 2026-07-28.

persons = [
    # ═══════════════ Core Leaders ═══════════════════════════════════════
    {
        "id": 1,
        "name": "岳龙",
        "gender": "男",
        "ethnicity": "unverified",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "福海县委书记",
        "current_org": "中共福海县委员会",
        "source": "confirmed — cited as 县委书记 in article '薪火相传庆华诞 砥砺奋进新征程——福海县举办七一升国旗' (xjfhx.gov.cn, 2026-07-02). Full biography unavailable on government website."
    },
    {
        "id": 2,
        "name": "叶尔江·库依西拜",
        "gender": "男",
        "ethnicity": "哈萨克族",
        "birth": "1977年3月",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "福海县委副书记、政府县长",
        "current_org": "福海县人民政府",
        "source": "confirmed — 福海县政府领导之窗 (xjfhx.gov.cn/ldzc/) as of 2026-07-21"
    },
    # ═══════════════ Government Leadership ══════════════════════════════
    {
        "id": 3,
        "name": "耿志权",
        "gender": "男",
        "ethnicity": "锡伯族",
        "birth": "1985年3月",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "福海县委常委、政府常务副县长",
        "current_org": "福海县人民政府",
        "source": "confirmed — 福海县政府领导页 (xjfhx.gov.cn/ldzc, 2026-07-21)"
    },
    {
        "id": 4,
        "name": "闫伟峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年5月",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "福海县委常委、政府副县长",
        "current_org": "福海县人民政府",
        "source": "confirmed — 福海县政府领导页 (xjfhx.gov.cn/ldzc, 2026-07-21)"
    },
    {
        "id": 5,
        "name": "张希钦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年2月",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "福海县人民政府副县长、公安局局长",
        "current_org": "福海县人民政府",
        "source": "confirmed — 福海县政府领导页 (xjfh.gov.cn/ldzc, 2026-07-21)"
    },
    {
        "id": 6,
        "name": "卡孜依娜·哈乌汉",
        "gender": "女",
        "ethnicity": "哈萨克族",
        "birth": "1987年8月",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "福海县人民政府副县长",
        "current_org": "福海县人民政府",
        "source": "confirmed — 福海县政府领导页 (xjfhx.gov.cn/ldzc, 2026-07-21)"
    },
    {
        "id": 7,
        "name": "哈伦别克·海诺拉",
        "gender": "男",
        "ethnicity": "哈萨克族",
        "birth": "1988年7月",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "福海县人民政府副县长",
        "current_org": "福海县人民政府",
        "source": "confirmed — 福海县政府领导页 (xjfhx.gov.cn/ldzc, 2026-07-21)"
    },
    {
        "id": 8,
        "name": "李大荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年9月",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "福海县人民政府党组成员",
        "current_org": "福海县人民政府",
        "source": "confirmed — 福海县政府领导页 (xjfhx.gov.cn/ldzc, 2026-07-21)"
    },
    # ═══════════════ County Party Committee Deputies ═══════════════════
    # Note: County party committee leadership (副书记, 纪委书记, 组织部, 宣传部等)
    # is not published on the government website. These names are unverified.
    {
        "id": 9,
        "name": "待查_县委副书记",
        "gender": "unverified",
        "ethnicity": "unverified",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "福海县委副书记（专职）",
        "current_org": "中共福海县委员会",
        "source": "unverified — name not found on government website; may be listed on xinjiang party website"
    },
    {
        "id": 10,
        "name": "待查_纪委书记",
        "gender": "unverified",
        "ethnicity": "unverified",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "福海县委常委、纪委书记、监委主任",
        "current_org": "中共福海县纪律检查委员会",
        "source": "unverified — need to identify from 12388 or discipline website"
    },
    {
        "id": 11,
        "name": "待查_组织部部长",
        "gender": "unverified",
        "ethnicity": "unverified",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "福海县委常委、组织部部长",
        "current_org": "中共福海县委员会组织部",
        "source": "unverified — need to identify"
    },
    {
        "id": 12,
        "name": "待查_宣传部部长",
        "gender": "unverified",
        "ethnicity": "unverified",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "福海县委常委、宣传部部长",
        "current_org": "中共福海县委员会宣传部",
        "source": "unverified — need to identify"
    },
    {
        "id": 13,
        "name": "高鹏",
        "gender": "unverified",
        "ethnicity": "unverified",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "审核人员（新闻署名）",
        "current_org": "福海县融媒体中心",
        "source": "confirmed — appears as 审核/审核人 on multiple xjfhx.gov.cn news articles (2026-06 to 2026-07)"
    },
    {
        "id": 14,
        "name": "郭小虎",
        "gender": "unverified",
        "ethnicity": "unverified",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "终审人员（新闻署名）",
        "current_org": "福海县融媒体中心",
        "source": "confirmed — appears as 终审 on multiple xjfhx.gov.cn news articles (2026-06 to 2026-07)"
    },
]

# ── Organizations ──────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共福海县委员会", "type": "党委", "level": "县级", "parent": "中共阿勒泰地区委员会", "location": "福海县"},
    {"id": 2, "name": "福海县人民政府", "type": "政府", "level": "县级", "parent": "阿勒泰地区行政公署", "location": "福海县"},
    {"id": 3, "name": "中共福海县纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共阿勒泰地区纪律检查委员会", "location": "福海县"},
    {"id": 4, "name": "福海县监察委员会", "type": "监察", "level": "县级", "parent": "阿勒泰地区监察委员会", "location": "福海县"},
    {"id": 5, "name": "中共福海县委员会组织部", "type": "党委部门", "level": "县级", "parent": "中共福海县委员会", "location": "福海县"},
    {"id": 6, "name": "中共福海县委员会宣传部", "type": "党委部门", "level": "县级", "parent": "中共福海县委员会", "location": "福海县"},
    {"id": 7, "name": "福海县人大常委会", "type": "人大", "level": "县级", "parent": "福海县", "location": "福海县"},
    {"id": 8, "name": "政协福海县委员会", "type": "政协", "level": "县级", "parent": "福海县", "location": "福海县"},
    {"id": 9, "name": "福海县公安局", "type": "政府", "level": "县级", "parent": "福海县人民政府", "location": "福海县"},
    {"id": 10, "name": "福海县融媒体中心", "type": "事业单位", "level": "县级", "parent": "中共福海县委员会", "location": "福海县"},
]

# ── Positions ──────────────────────────────────────────────────────────
positions = [
    # 岳龙 — party secretary
    {"person_id": 1, "org_id": 1, "title": "福海县委书记", "start_date": "unverified", "end_date": "", "rank": "正处级", "note": "现任；2026年7月新闻确认其职务"},
    # 叶尔江·库依西拜 — mayor
    {"person_id": 2, "org_id": 2, "title": "福海县委副书记、政府县长", "start_date": "unverified", "end_date": "", "rank": "正处级", "note": "现任；主持政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "福海县委副书记", "start_date": "unverified", "end_date": "", "rank": "副处级", "note": "县委副书记"},
    # Government leadership
    {"person_id": 3, "org_id": 2, "title": "福海县委常委、政府常务副县长", "start_date": "unverified", "end_date": "", "rank": "副处级", "note": "负责政府常务工作、发改、财政等"},
    {"person_id": 3, "org_id": 1, "title": "福海县委常委", "start_date": "unverified", "end_date": "", "rank": "副处级", "note": "县委常委"},
    {"person_id": 4, "org_id": 2, "title": "福海县委常委、政府副县长", "start_date": "unverified", "end_date": "", "rank": "副处级", "note": "负责招商引资、工业、文旅等"},
    {"person_id": 4, "org_id": 1, "title": "福海县委常委", "start_date": "unverified", "end_date": "", "rank": "副处级", "note": "县委常委"},
    {"person_id": 5, "org_id": 2, "title": "福海县人民政府副县长、公安局局长", "start_date": "unverified", "end_date": "", "rank": "副处级", "note": "负责公安、司法、边境等"},
    {"person_id": 5, "org_id": 9, "title": "福海县公安局党委书记、局长", "start_date": "unverified", "end_date": "", "rank": "副处级", "note": "二级高级警长"},
    {"person_id": 6, "org_id": 2, "title": "福海县人民政府副县长", "start_date": "unverified", "end_date": "", "rank": "副处级", "note": "负责教育、民政、卫健、医保等"},
    {"person_id": 7, "org_id": 2, "title": "福海县人民政府副县长", "start_date": "unverified", "end_date": "", "rank": "副处级", "note": "负责环保、林草、自然资源、住建等"},
    {"person_id": 8, "org_id": 2, "title": "福海县人民政府党组成员", "start_date": "unverified", "end_date": "", "rank": "副处级", "note": "负责农业农村、水利、交通等"},
    # Party committee deputies
    {"person_id": 9, "org_id": 1, "title": "福海县委副书记（专职）", "start_date": "", "end_date": "", "rank": "副处级", "note": "待确认身份"},
    {"person_id": 10, "org_id": 3, "title": "福海县委常委、纪委书记、监委主任", "start_date": "", "end_date": "", "rank": "副处级", "note": "待确认身份"},
    {"person_id": 11, "org_id": 5, "title": "福海县委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "待确认身份"},
    {"person_id": 12, "org_id": 6, "title": "福海县委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "待确认身份"},
    # Media center
    {"person_id": 13, "org_id": 10, "title": "审核人员", "start_date": "", "end_date": "", "rank": "", "note": "新闻审核署名"},
    {"person_id": 14, "org_id": 10, "title": "终审人员", "start_date": "", "end_date": "", "rank": "", "note": "新闻终审署名"},
]

# ── Relationships ──────────────────────────────────────────────────────
relationships = [
    # Core duo — party secretary and mayor
    {"person_a": 1, "person_b": 2, "type": "work_duo", "context": "书记与县长搭档", "overlap_org": "福海县", "overlap_period": "unverified"},
    # Party committee - government linkages
    {"person_a": 1, "person_b": 3, "type": "leadership_chain", "context": "书记与常务副县长", "overlap_org": "中共福海县委员会", "overlap_period": "unverified"},
    {"person_a": 1, "person_b": 4, "type": "leadership_chain", "context": "书记与副县长（县委常委）", "overlap_org": "中共福海县委员会", "overlap_period": "unverified"},
    {"person_a": 1, "person_b": 9, "type": "leadership_chain", "context": "书记与专职副书记", "overlap_org": "中共福海县委员会", "overlap_period": "unverified"},
    # Mayor - deputy relationships
    {"person_a": 2, "person_b": 3, "type": "leadership_chain", "context": "县长与常务副县长", "overlap_org": "福海县人民政府", "overlap_period": "unverified"},
    {"person_a": 2, "person_b": 4, "type": "leadership_chain", "context": "县长与副县长", "overlap_org": "福海县人民政府", "overlap_period": "unverified"},
    {"person_a": 2, "person_b": 5, "type": "leadership_chain", "context": "县长与副县长兼公安局长", "overlap_org": "福海县人民政府", "overlap_period": "unverified"},
    {"person_a": 2, "person_b": 6, "type": "leadership_chain", "context": "县长与副县长", "overlap_org": "福海县人民政府", "overlap_period": "unverified"},
    {"person_a": 2, "person_b": 7, "type": "leadership_chain", "context": "县长与副县长", "overlap_org": "福海县人民政府", "overlap_period": "unverified"},
    {"person_a": 2, "person_b": 8, "type": "leadership_chain", "context": "县长与党组成员", "overlap_org": "福海县人民政府", "overlap_period": "unverified"},
    # Discipline supervision
    {"person_a": 1, "person_b": 10, "type": "supervision", "context": "书记领导纪委工作", "overlap_org": "中共福海县委员会", "overlap_period": "unverified"},
    # Organization department
    {"person_a": 1, "person_b": 11, "type": "leadership_chain", "context": "书记与组织部长", "overlap_org": "中共福海县委员会", "overlap_period": "unverified"},
    # Party committee - government cross relations
    {"person_a": 3, "person_b": 4, "type": "colleague", "context": "两位县委常委兼副县长同班共事", "overlap_org": "福海县人民政府", "overlap_period": "unverified"},
    {"person_a": 3, "person_b": 5, "type": "colleague", "context": "常务副县长与副县长", "overlap_org": "福海县人民政府", "overlap_period": "unverified"},
    {"person_a": 6, "person_b": 7, "type": "colleague", "context": "同为少数民族副县长", "overlap_org": "福海县人民政府", "overlap_period": "unverified"},
]

# ── Main ────────────────────────────────────────────────────────────────
def main() -> None:
    os.makedirs(TMP, exist_ok=True)

    # Use the shared runner for DB + GEXF
    run_build(
        slug="福海县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    # Print summary
    print("\n── Build complete ──")
    print(f"  Persons: {len(persons)} ({len([p for p in persons if '待查' not in p['name']])} confirmed names)")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print("\nNote: 4 party committee deputy positions (副书记/纪委书记/组织部长/宣传部长)")
    print("  are unverified. Also, 岳龙's biography is minimal — only his name")
    print("  and role confirmed from news. 叶尔江·库依西拜's bio has birth+ethnicity")
    print("  but no career timeline. All deputy bios have name+ethnicity+birth only.")


if __name__ == "__main__":
    main()