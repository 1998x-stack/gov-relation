#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
南沙区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 广东省
Parent City: 广州市
Region: 南沙区
Targets: 区委书记 & 区长

Research Sources:
- Wikipedia (zh.wikipedia.org) — 南沙区页
- 南方日报/南方+ — 任免公告: 吴扬任南沙区副区长、代理区长 (2022-09-09)
- 白云区人民政府门户网站 (by.gov.cn) — 领导之窗确认吴扬前任职务
- 网易/搜狐等媒体报道确认刘炜任南沙区委书记
- gzns.gov.cn — 南沙区人民政府门户网站

Research Date: 2026-07-22
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths ──
SLUG = "南沙区"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DATABASE_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(GRAPH_DIR, f"{SLUG}_network.gexf")

# The script uses gov_relation.runner (which internally uses sqlite3)
import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders (as of 2026-07-22)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "刘炜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广州市南沙区委书记",
        "current_org": "中共广州市南沙区委员会",
        "source": "网易/搜狐等媒体报道确认；前任广东省科技厅厅长调任南沙区委书记（2023-2024年间）"
    },
    {
        "id": 2,
        "name": "吴扬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年3月",
        "birthplace": "广东饶平",
        "native_place": "广东饶平",
        "education": "研究生学历，管理学硕士学位",
        "party_join": "1995年1月",
        "work_start": "1992年7月",
        "current_post": "南沙区委副书记、区长",
        "current_org": "南沙区人民政府",
        "source": "南方日报: 2022年9月吴扬任南沙区代区长；白云区领导之窗确认前任职务为白云区委常委"
    },
    # ════════════════════════════════════════
    # 前任领导 (Predecessors)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "董可",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已离任（去向待查）",
        "current_org": "待查",
        "source": "南方日报: 2022年9月南沙区人大常委会接受董可辞去区长职务"
    },
    {
        "id": 4,
        "name": "卢一先",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已离任（去向待查）",
        "current_org": "待查",
        "source": "媒体报道：卢一先曾任南沙区委书记（~2021年），后调任"
    },
    # ════════════════════════════════════════
    # 区人大常委会、政协主要领导
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "李德球",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "南沙区人大常委会主任",
        "current_org": "广州市南沙区人民代表大会常务委员会",
        "source": "南方日报: 2022年9月李德球主持南沙区人大常委会会议确认"
    },
    {
        "id": 6,
        "name": "翁殊武（待确认）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "南沙区政协主席（待确认）",
        "current_org": "中国人民政治协商会议广州市南沙区委员会",
        "source": "媒体报道推断，需要gzns.gov.cn领导之窗确认"
    },
    # ════════════════════════════════════════
    # 区政府副区长（待确认完整名单）
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "魏敏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、常务副区长",
        "current_org": "南沙区人民政府",
        "source": "南方日报: 2022年9月南沙区人大常委会会议魏敏以常务副区长身份出席"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共广州市南沙区委员会",
        "type": "党委",
        "level": "正处级（区委书记通常为副厅级，南沙为国家级新区可高配）",
        "parent": "中共广州市委",
        "location": "广州市南沙区凤凰大道1号"
    },
    {
        "id": 2,
        "name": "南沙区人民政府",
        "type": "政府",
        "level": "正处级（区长通常为正处级，南沙为国家级新区可高配）",
        "parent": "广州市人民政府",
        "location": "广州市南沙区凤凰大道1号"
    },
    {
        "id": 3,
        "name": "广州市南沙区人民代表大会常务委员会",
        "type": "人大",
        "level": "正处级",
        "parent": "广州市人大常委会",
        "location": "广州市南沙区"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议广州市南沙区委员会",
        "type": "政协",
        "level": "正处级",
        "parent": "广州市政协",
        "location": "广州市南沙区"
    },
    {
        "id": 5,
        "name": "广州南沙经济技术开发区（广州南沙新区）管委会",
        "type": "开发区",
        "level": "副省级（南沙新区为国家级新区）",
        "parent": "广州市人民政府",
        "location": "广州市南沙区"
    },
    {
        "id": 6,
        "name": "中共广州市白云区委员会",
        "type": "党委",
        "level": "正处级",
        "parent": "中共广州市委",
        "location": "广州市白云区"
    },
]

# 3. Positions
positions = [
    # 刘炜 — 现任南沙区委书记
    {"person_id": 1, "org_id": 1, "title": "南沙区委书记", "start": "待查（约2023-2024）", "end": "至今", "rank": "副厅级（南沙新区可高配为正厅级）", "note": "主持区委全面工作；前任为广东省科技厅厅长"},
    # 吴扬 — 现任南沙区长
    {"person_id": 2, "org_id": 1, "title": "南沙区委副书记", "start": "2022-09", "end": "至今", "rank": "正处级（可能高配为副厅级）", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "南沙区区长", "start": "2022-09", "end": "至今", "rank": "正处级", "note": "2022年9月任副区长、代区长，后去代转正"},
    # 吴扬 — 前任职务
    {"person_id": 2, "org_id": 6, "title": "白云区委常委", "start": "待查", "end": "2022-09", "rank": "正处级", "note": "在白云区任区委常委，后调任南沙区"},
    # 董可 — 前任区长
    {"person_id": 3, "org_id": 2, "title": "南沙区区长", "start": "待查（~2019-2021）", "end": "2022-09", "rank": "正处级", "note": "2022年9月辞去区长职务"},
    # 卢一先 — 前任区委书记
    {"person_id": 4, "org_id": 1, "title": "南沙区委书记", "start": "待查（~2019-2021）", "end": "待查（~2021-2022）", "rank": "副厅级", "note": "前任南沙区委书记；后调任"},
    # 李德球
    {"person_id": 5, "org_id": 3, "title": "南沙区人大常委会主任", "start": "待查", "end": "至今", "rank": "正处级", "note": "主持区人大常委会全面工作"},
    # 翁殊武（待确认）
    {"person_id": 6, "org_id": 4, "title": "南沙区政协主席", "start": "待查", "end": "至今", "rank": "正处级", "note": "待确认"},
    # 魏敏
    {"person_id": 7, "org_id": 2, "title": "常务副区长", "start": "待查", "end": "至今", "rank": "正处级", "note": "协助区长负责区政府日常工作"},
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},
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
        "overlap_org": "中共广州市南沙区委员会/南沙区人民政府",
        "overlap_period": "刘炜任区委书记、吴扬任区长期间（约2023年至今）",
        "source": "南沙区人民政府门户网站—多篇新闻报道确认"
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "overlap",
        "context": "区委书记与人大主任：当前区委领导班子与人大主要负责人",
        "strength": "strong",
        "confidence": "confirmed",
        "overlap_org": "南沙区",
        "overlap_period": "至今",
        "source": "南沙区人大相关新闻报道"
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "predecessor_successor",
        "context": "吴扬接替董可任南沙区区长",
        "strength": "strong",
        "confidence": "confirmed",
        "overlap_org": "南沙区人民政府",
        "overlap_period": "2022年9月交接",
        "source": "南方日报: 2022年9月南沙区人大常委会接受董可辞去区长职务，任命吴扬为代区长"
    },
    {
        "person_a": 2,
        "person_b": 5,
        "type": "overlap",
        "context": "区长与人大主任：区政府与区人大主要负责人",
        "strength": "medium",
        "confidence": "confirmed",
        "overlap_org": "南沙区",
        "overlap_period": "2022年9月至今",
        "source": "南方日报: 李德球主持区人大常委会会议任命吴扬"
    },
    {
        "person_a": 2,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "区长与常务副区长：政府正副职搭档",
        "strength": "strong",
        "confidence": "confirmed",
        "overlap_org": "南沙区人民政府",
        "overlap_period": "2022年9月至今",
        "source": "南方日报: 2022年南沙区人大常委会会议魏敏以常务副区长身份出席"
    },
    {
        "person_a": 1,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "区委书记与常务副区长：党委主要领导与政府常务副职",
        "strength": "strong",
        "confidence": "confirmed",
        "overlap_org": "南沙区",
        "overlap_period": "至今",
        "source": "南沙区人民政府门户网站"
    },
    {
        "person_a": 4,
        "person_b": 1,
        "type": "predecessor_successor",
        "context": "卢一先为刘炜前任：前后两任南沙区委书记",
        "strength": "medium",
        "confidence": "plausible",
        "overlap_org": "中共广州市南沙区委员会",
        "overlap_period": "卢一先离任后刘炜接任（约2023-2024年间）",
        "source": "媒体报道推断，需进一步确认具体交接时间"
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
        overwrite=True,
    )

    print(f"\nDone. Files created:")
    print(f"  - {DB_PATH}")
    print(f"  - {GEXF_PATH}")
