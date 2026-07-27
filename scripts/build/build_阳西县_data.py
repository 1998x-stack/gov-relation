#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阳西县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 广东省
Parent City: 阳江市
Region: 阳西县
Targets: 县委书记 & 县长

Research Sources:
- 阳西县人民政府网站 (www.yangxi.gov.cn) — 不可达
- 阳江市人民政府网站 (www.yangjiang.gov.cn) — 不可达
- 百度百科 — 不可达（403）
- Wikipedia — 不可达（超时）
- Jina Reader — 不可达
- Exa Search — 超限

Web access was completely unavailable during this investigation (government sites timeout,
Baidu 403, Wikipedia blocked, Exa rate-limited, Jina Reader transport errors).
Data is based on training knowledge and labeled plausible/unverified.

Current status (as of 2026-07-22 estimates):
- 县委书记: 待确认（需官方来源验证）
- 县长: 待确认（需官方来源验证）

Research Date: 2026-07-22
Evidence Note: All leadership info is unverified due to total web access failure.
Every field should be verified against official sources before use.
"""

import os
import sys
from datetime import datetime

# Allow import from repo root
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "阳西县"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──
# NOTE: All data is based on training knowledge and could not be verified
# against current official sources due to total web access failure.
# Open questions are documented in person JSON and report/open_gaps.md.

# 1. Persons
persons = [
    {
        "id": 1,
        "name": "待确认（县委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共阳西县委书记",
        "current_org": "中共阳西县委员会",
        "source": "需官方来源验证"
    },
    {
        "id": 2,
        "name": "待确认（县长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共阳西县委副书记、县长",
        "current_org": "阳西县人民政府",
        "source": "需官方来源验证"
    },
    # ════════════════════════════════════════
    # 县人大常委会
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "待确认（县人大常委会主任）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "阳西县人大常委会主任",
        "current_org": "阳西县人民代表大会常务委员会",
        "source": "待查"
    },
    # ════════════════════════════════════════
    # 县政协
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "待确认（县政协主席）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "阳西县政协主席",
        "current_org": "中国人民政治协商会议阳西县委员会",
        "source": "待查"
    },
    # ════════════════════════════════════════
    # 县委常委 — 常规配置
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "待确认（常务副县长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "阳西县委常委、常务副县长",
        "current_org": "阳西县人民政府",
        "source": "待查"
    },
    {
        "id": 6,
        "name": "待确认（县纪委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "阳西县委常委、县纪委书记、县监委主任",
        "current_org": "中共阳西县纪律检查委员会",
        "source": "待查"
    },
    {
        "id": 7,
        "name": "待确认（县委组织部部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "阳西县委常委、组织部部长",
        "current_org": "中共阳西县委组织部",
        "source": "待查"
    },
    {
        "id": 8,
        "name": "待确认（县委宣传部部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "阳西县委常委、宣传部部长",
        "current_org": "中共阳西县委宣传部",
        "source": "待查"
    },
    {
        "id": 9,
        "name": "待确认（县委政法委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "阳西县委常委、政法委书记",
        "current_org": "中共阳西县委政法委员会",
        "source": "待查"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共阳西县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共阳江市委员会",
        "location": "阳江市阳西县"
    },
    {
        "id": 2,
        "name": "阳西县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "阳江市人民政府",
        "location": "阳江市阳西县"
    },
    {
        "id": 3,
        "name": "阳西县人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "阳江市人民代表大会常务委员会",
        "location": "阳江市阳西县"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议阳西县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "中国人民政治协商会议阳江市委员会",
        "location": "阳江市阳西县"
    },
    {
        "id": 5,
        "name": "中共阳西县纪律检查委员会",
        "type": "纪律检查",
        "level": "县处级",
        "parent": "中共阳江市纪律检查委员会",
        "location": "阳江市阳西县"
    },
    {
        "id": 6,
        "name": "中共阳西县委组织部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共阳西县委员会",
        "location": "阳江市阳西县"
    },
    {
        "id": 7,
        "name": "中共阳西县委宣传部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共阳西县委员会",
        "location": "阳江市阳西县"
    },
    {
        "id": 8,
        "name": "中共阳西县委政法委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共阳西县委员会",
        "location": "阳江市阳西县"
    },
    {
        "id": 9,
        "name": "中共阳江市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共广东省委员会",
        "location": "阳江市江城区"
    },
    {
        "id": 10,
        "name": "阳江市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "广东省人民政府",
        "location": "阳江市江城区"
    },
]

# 3. Positions
positions = [
    # 县委书记 — 待确认
    {"person_id": 1, "org_id": 1, "title": "中共阳西县委书记", "start_date": "待查", "end_date": "present", "rank": "县处级正职", "note": "待确认"},
    # 县长 — 待确认
    {"person_id": 2, "org_id": 2, "title": "阳西县县长", "start_date": "待查", "end_date": "present", "rank": "县处级正职", "note": "待确认，兼任县委副书记"},
    {"person_id": 2, "org_id": 1, "title": "中共阳西县委副书记", "start_date": "待查", "end_date": "present", "rank": "县处级正职", "note": "待确认"},
    # 县人大常委会主任
    {"person_id": 3, "org_id": 3, "title": "阳西县人大常委会主任", "start_date": "待查", "end_date": "present", "rank": "县处级正职", "note": "待确认"},
    # 县政协主席
    {"person_id": 4, "org_id": 4, "title": "阳西县政协主席", "start_date": "待查", "end_date": "present", "rank": "县处级正职", "note": "待确认"},
    # 常务副县长
    {"person_id": 5, "org_id": 2, "title": "阳西县委常委、常务副县长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "待确认"},
    # 县纪委书记
    {"person_id": 6, "org_id": 5, "title": "阳西县委常委、县纪委书记、县监委主任", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "待确认"},
    # 县委组织部部长
    {"person_id": 7, "org_id": 6, "title": "阳西县委常委、组织部部长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "待确认"},
    # 县委宣传部部长
    {"person_id": 8, "org_id": 7, "title": "阳西县委常委、宣传部部长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "待确认"},
    # 县委政法委书记
    {"person_id": 9, "org_id": 8, "title": "阳西县委常委、政法委书记", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "待确认"},
]

# 4. Relationships (minimal — core团队结构关系)
relationships = [
    # 党政正职
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "县委书记与县长是阳西县最重要的党政搭档", "overlap_org": "中共阳西县委员会/阳西县人民政府", "overlap_period": "待查", "strength": "strong", "confidence": "unverified"},
    # 县委班子
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "县委书记与常务副县长为上下级关系，均为县委常委", "overlap_org": "中共阳西县委员会", "overlap_period": "待查", "strength": "strong", "confidence": "unverified"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "县委书记与县纪委书记为上下级关系，均为县委常委", "overlap_org": "中共阳西县委员会", "overlap_period": "待查", "strength": "strong", "confidence": "unverified"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "县委书记与组织部部长为上下级关系，均为县委常委", "overlap_org": "中共阳西县委员会", "overlap_period": "待查", "strength": "strong", "confidence": "unverified"},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "县委书记与宣传部部长为上下级关系，均为县委常委", "overlap_org": "中共阳西县委员会", "overlap_period": "待查", "strength": "strong", "confidence": "unverified"},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "县委书记与政法委书记为上下级关系，均为县委常委", "overlap_org": "中共阳西县委员会", "overlap_period": "待查", "strength": "strong", "confidence": "unverified"},
    # 县长与常务副县长
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "县长与常务副县长为政府班子上下级关系", "overlap_org": "阳西县人民政府", "overlap_period": "待查", "strength": "strong", "confidence": "unverified"},
]

# ── Build ──
if __name__ == "__main__":
    print(f"Building {SLUG} network...")
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
    print("Done.")
    print("NOTE: All person data is unverified due to total web access failure.")
    print("See open_gaps.md for details on what needs verification.")
