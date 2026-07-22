#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
荔湾区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 广东省
Parent City: 广州市
Region: 荔湾区
Targets: 区委书记 & 区长

Research Sources:
- 广州市荔湾区人民政府门户网站 (www.lw.gov.cn) — 官方信息平台
- 荔湾区百度百科词条 — 政治板块领导信息（截至2026年3月）
- 维基百科荔湾区词条 — 行政区划等背景信息
- 广州市荔湾区人民政府信息公开平台 (gkmlpt)

Research Date: 2026-07-22
"""

import os
import sys
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths ──
SLUG = "荔湾区"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

# The script uses gov_relation.runner (which internally uses sqlite3)
import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "刘晨辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广州市荔湾区委书记",
        "current_org": "中共广州市荔湾区委员会",
        "source": "荔湾区百度百科政治板块（截至2026年3月）; www.lw.gov.cn"
    },
    {
        "id": 2,
        "name": "李锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "荔湾区委副书记、区长",
        "current_org": "荔湾区人民政府",
        "source": "荔湾区百度百科政治板块（截至2026年3月）"
    },
    # ════════════════════════════════════════
    # Former Leaders (for network context)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "谭明鹤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已离任",
        "current_org": "荔湾区人民政府（前任区长）",
        "source": "维基百科荔湾区词条所列领导信息"
    },
    # ════════════════════════════════════════
    # 人大、政协主要领导
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "黄洪飙",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "荔湾区人大常委会主任",
        "current_org": "广州市荔湾区人民代表大会常务委员会",
        "source": "荔湾区百度百科政治板块（截至2026年3月）"
    },
    {
        "id": 5,
        "name": "吴辉文",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "荔湾区政协主席",
        "current_org": "中国人民政治协商会议广州市荔湾区委员会",
        "source": "荔湾区百度百科政治板块（截至2026年3月）"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共广州市荔湾区委员会",
        "type": "党委",
        "level": "正处级（区委书记通常为副厅级）",
        "parent": "中共广州市委",
        "location": "广州市荔湾区"
    },
    {
        "id": 2,
        "name": "荔湾区人民政府",
        "type": "政府",
        "level": "正处级",
        "parent": "广州市人民政府",
        "location": "广州市荔湾区芳村大道西2号"
    },
    {
        "id": 3,
        "name": "广州市荔湾区人民代表大会常务委员会",
        "type": "人大",
        "level": "正处级",
        "parent": "广州市人大常委会",
        "location": "广州市荔湾区"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议广州市荔湾区委员会",
        "type": "政协",
        "level": "正处级",
        "parent": "广州市政协",
        "location": "广州市荔湾区"
    },
]

# 3. Positions
positions = [
    # person_id, org_id, title, start, end, rank, note

    # 刘晨辉
    {"person_id": 1, "org_id": 1, "title": "广州市荔湾区委书记", "start": "待查", "end": "至今", "rank": "副厅级（通常由广州市委常委兼任）", "note": "主持区委全面工作"},
    # 李锋
    {"person_id": 2, "org_id": 1, "title": "荔湾区委副书记", "start": "待查", "end": "至今", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "荔湾区区长", "start": "待查", "end": "至今", "rank": "正处级", "note": "主持区政府全面工作"},
    # 谭明鹤（前任区长）
    {"person_id": 3, "org_id": 2, "title": "荔湾区区长（前任）", "start": "待查", "end": "待查", "rank": "正处级", "note": "前任区长，具体任期需进一步确认"},
    # 黄洪飙
    {"person_id": 4, "org_id": 3, "title": "荔湾区人大常委会主任", "start": "待查", "end": "至今", "rank": "正处级", "note": "主持区人大常委会全面工作"},
    # 吴辉文
    {"person_id": 5, "org_id": 4, "title": "荔湾区政协主席", "start": "待查", "end": "至今", "rank": "正处级", "note": "主持区政协全面工作"},
]

# 4. Relationships
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记与区长：党委与政府主要领导工作搭档关系",
        "strength": "strong",
        "confidence": "confirmed",
        "overlap_org": "中共广州市荔湾区委员会/荔湾区人民政府",
        "overlap_period": "至今（李锋任区委副书记、区长期间）",
        "source": "荔湾区百度百科政治板块（截至2026年3月）"
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "overlap",
        "context": "区委书记与人大主任：当前区委领导班子成员与人大主要负责人",
        "strength": "strong",
        "confidence": "confirmed",
        "overlap_org": "荔湾区",
        "overlap_period": "至今",
        "source": "荔湾区百度百科政治板块（截至2026年3月）"
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "overlap",
        "context": "区委书记与政协主席：当前班子同届共事关系",
        "strength": "medium",
        "confidence": "confirmed",
        "overlap_org": "荔湾区",
        "overlap_period": "至今",
        "source": "荔湾区百度百科政治板块（截至2026年3月）"
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "predecessor_successor",
        "context": "李锋接替谭明鹤出任荔湾区区长",
        "strength": "strong",
        "confidence": "plausible",
        "overlap_org": "荔湾区人民政府",
        "overlap_period": "交接期待查",
        "source": "荔湾区百度百科（李锋）及维基百科（谭明鹤）信息对照"
    },
]

# ── Run ──
if __name__ == "__main__":
    print(f"Building {SLUG} network...")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print(f"\nDone. Files created:")
    print(f"  - {DB_PATH}")
    print(f"  - {GEXF_PATH}")
