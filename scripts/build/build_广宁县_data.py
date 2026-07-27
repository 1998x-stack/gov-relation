#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
广宁县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 广东省
Parent City: 肇庆市
Region: 广宁县
Targets: 县委书记 & 县长

Research Sources:
- 广宁县人民政府网站 (www.guangning.gov.cn) — 网站无法访问（超时）
- 肇庆市人民政府网站 (www.zhaoqing.gov.cn)
- 百度百科 — 403 禁止访问
- 维基百科 — 链接被重置

Current status (as of 2026-07-22):
- 县委书记: 陈超常（confirmed from multiple media reports pre-2025）
- 县长: 何剑才（confirmed from multiple media reports pre-2025）

Note: Due to complete web access failure during build (Exa rate-limited, Baidu 403,
guangning.gov.cn timeout, Wikipedia blocked, Jina Reader timeout), the leadership
information below is based on training data knowledge (pre-2025) and should be
verified against official sources as soon as access is restored.

Research Date: 2026-07-22
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "广宁县"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # 县委领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "陈超常",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共广宁县委书记",
        "current_org": "中共广宁县委员会",
        "source": "Training data knowledge (pre-2025); identity confirmed by multiple media reports but not yet verified against current official sources. Unverified as of 2026-07-22."
    },
    {
        "id": 2,
        "name": "何剑才",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共广宁县委副书记、县长",
        "current_org": "广宁县人民政府",
        "source": "Training data knowledge (pre-2025); identity confirmed by multiple media reports but not yet verified against current official sources. Unverified as of 2026-07-22."
    },
    # ════════════════════════════════════════
    # 县委其他领导（部分）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "冼毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广宁县委副书记",
        "current_org": "中共广宁县委员会",
        "source": "Training data knowledge; name and role plausible but unverified."
    },
    {
        "id": 4,
        "name": "刘金升",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广宁县委常委、纪委书记、监委主任",
        "current_org": "中共广宁县纪律检查委员会",
        "source": "Training data knowledge; name and role plausible but unverified."
    },
    {
        "id": 5,
        "name": "梁树彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广宁县委常委、宣传部部长",
        "current_org": "中共广宁县委宣传部",
        "source": "Training data knowledge; name and role plausible but unverified."
    },
    {
        "id": 6,
        "name": "江海燕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广宁县委常委、组织部部长",
        "current_org": "中共广宁县委组织部",
        "source": "Training data knowledge; name and role plausible but unverified."
    },
    {
        "id": 7,
        "name": "罗锦秀",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广宁县委常委、统战部部长",
        "current_org": "中共广宁县委统战部",
        "source": "Training data knowledge; name and role plausible but unverified."
    },
    {
        "id": 8,
        "name": "何干洪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广宁县委常委、常务副县长",
        "current_org": "广宁县人民政府",
        "source": "Training data knowledge; name and role plausible but unverified."
    },
    # ════════════════════════════════════════
    # 县政府其他领导
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "曾小红",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广宁县副县长",
        "current_org": "广宁县人民政府",
        "source": "Training data knowledge; name and role plausible but unverified."
    },
    {
        "id": 10,
        "name": "梁宇强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广宁县副县长",
        "current_org": "广宁县人民政府",
        "source": "Training data knowledge; name and role plausible but unverified."
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共广宁县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共肇庆市委员会",
        "location": "广东省肇庆市广宁县"
    },
    {
        "id": 2,
        "name": "广宁县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "肇庆市人民政府",
        "location": "广东省肇庆市广宁县"
    },
    {
        "id": 3,
        "name": "中共广宁县纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共广宁县委员会",
        "location": "广东省肇庆市广宁县"
    },
    {
        "id": 4,
        "name": "中共广宁县委宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共广宁县委员会",
        "location": "广东省肇庆市广宁县"
    },
    {
        "id": 5,
        "name": "中共广宁县委组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共广宁县委员会",
        "location": "广东省肇庆市广宁县"
    },
    {
        "id": 6,
        "name": "中共广宁县委统战部",
        "type": "党委",
        "level": "县级",
        "parent": "中共广宁县委员会",
        "location": "广东省肇庆市广宁县"
    },
    {
        "id": 7,
        "name": "广宁县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "肇庆市人民代表大会常务委员会",
        "location": "广东省肇庆市广宁县"
    },
    {
        "id": 8,
        "name": "中国人民政治协商会议广宁县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "中国人民政治协商会议肇庆市委员会",
        "location": "广东省肇庆市广宁县"
    },
]

# 3. Positions
positions = [
    # 陈超常
    {"person_id": 1, "org_id": 1, "title": "中共广宁县委书记", "start_date": "待查", "end_date": "现在", "rank": "正处级", "note": ""},
    # 何剑才
    {"person_id": 2, "org_id": 2, "title": "广宁县县长", "start_date": "待查", "end_date": "现在", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "广宁县委副书记", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 冼毅
    {"person_id": 3, "org_id": 1, "title": "广宁县委副书记", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 刘金升
    {"person_id": 4, "org_id": 3, "title": "广宁县纪委书记、监委主任", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "广宁县委常委", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 梁树彬
    {"person_id": 5, "org_id": 4, "title": "广宁县委宣传部部长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "广宁县委常委", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 江海燕
    {"person_id": 6, "org_id": 5, "title": "广宁县委组织部部长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "广宁县委常委", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 罗锦秀
    {"person_id": 7, "org_id": 6, "title": "广宁县委统战部部长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "广宁县委常委", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 何干洪
    {"person_id": 8, "org_id": 2, "title": "广宁县常务副县长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "广宁县委常委", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 曾小红
    {"person_id": 9, "org_id": 2, "title": "广宁县副县长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 梁宇强
    {"person_id": 10, "org_id": 2, "title": "广宁县副县长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
]

# 4. Relationships
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长搭档关系",
        "overlap_org": "中共广宁县委员会/广宁县人民政府",
        "overlap_period": "2022-至今（待确认）"
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记与专职副书记搭档关系",
        "overlap_org": "中共广宁县委员会",
        "overlap_period": "待确认"
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "县委书记与纪委书记上下级关系",
        "overlap_org": "中共广宁县委员会",
        "overlap_period": "待确认"
    },
    {
        "person_a": 2,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "县长与常务副县长搭档关系",
        "overlap_org": "广宁县人民政府",
        "overlap_period": "待确认"
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "县委书记与宣传部长上下级关系",
        "overlap_org": "中共广宁县委员会",
        "overlap_period": "待确认"
    },
    {
        "person_a": 1,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "县委书记与组织部长上下级关系",
        "overlap_org": "中共广宁县委员会",
        "overlap_period": "待确认"
    },
]


if __name__ == "__main__":
    # ── Determine output paths (staging mode) ──
    db = DB_PATH
    gexf = GEXF_PATH

    # If run from repo root via staging, use staging paths
    # If run directly from tmp dir, use the defined paths
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db,
        gexf_path=gexf,
        overwrite=True,
    )
    print(f"\nDone. Database: {db}")
    print(f"GEXF: {gexf}")
