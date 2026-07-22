#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
封开县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 广东省
Parent City: 肇庆市
Region: 封开县
Targets: 县委书记 & 县长

Research Sources:
- 封开县人民政府网站 (www.fengkai.gov.cn) — 领导之窗
- 封开县人民政府网站 — 领导活动

Current status (as of 2026-07-22):
- 县委书记: 李亚旭（confirmed from official government news reports, 2025-2026 activities）
- 县长: 丘灿辉（confirmed from 封开县人民政府网站 领导之窗 listing）

Research Date: 2026-07-22
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "封开县"
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
        "name": "李亚旭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共封开县委书记",
        "current_org": "中共封开县委员会",
        "source": "封开县政府官网领导活动报道确认（2025-2026年多次报道）；个人详细履历待查。"
    },
    {
        "id": 2,
        "name": "丘灿辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共封开县委副书记、封开县人民政府县长",
        "current_org": "封开县人民政府",
        "source": "封开县政府官网领导之窗页面确认；个人详细履历待查。"
    },
    # ════════════════════════════════════════
    # 县政府领导（副县长）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "邓东尧",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "封开县人民政府副县长",
        "current_org": "封开县人民政府",
        "source": "封开县政府官网领导之窗页面确认；个人详细履历待查。"
    },
    {
        "id": 4,
        "name": "李彦玉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "封开县人民政府副县长",
        "current_org": "封开县人民政府",
        "source": "封开县政府官网领导之窗页面确认；个人详细履历待查。"
    },
    {
        "id": 5,
        "name": "梁积瑜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "封开县人民政府副县长",
        "current_org": "封开县人民政府",
        "source": "封开县政府官网领导之窗页面确认；个人详细履历待查。"
    },
    {
        "id": 6,
        "name": "何浩立",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "封开县人民政府副县长",
        "current_org": "封开县人民政府",
        "source": "封开县政府官网领导之窗页面确认；个人详细履历待查。"
    },
    {
        "id": 7,
        "name": "黄锡河",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "封开县人民政府副县长",
        "current_org": "封开县人民政府",
        "source": "封开县政府官网领导之窗页面确认；个人详细履历待查。"
    },
    {
        "id": 8,
        "name": "庄武军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "封开县人民政府副县长",
        "current_org": "封开县人民政府",
        "source": "封开县政府官网领导之窗页面确认；个人详细履历待查。"
    },
    {
        "id": 9,
        "name": "卢可",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "封开县人民政府副县长",
        "current_org": "封开县人民政府",
        "source": "封开县政府官网领导之窗页面确认；个人详细履历待查。"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共封开县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共肇庆市委员会",
        "location": "广东省肇庆市封开县"
    },
    {
        "id": 2,
        "name": "封开县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "肇庆市人民政府",
        "location": "广东省肇庆市封开县"
    },
    {
        "id": 3,
        "name": "中共封开县纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共封开县委员会",
        "location": "广东省肇庆市封开县"
    },
    {
        "id": 4,
        "name": "封开县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "肇庆市人民代表大会常务委员会",
        "location": "广东省肇庆市封开县"
    },
    {
        "id": 5,
        "name": "中国人民政治协商会议封开县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "中国人民政治协商会议肇庆市委员会",
        "location": "广东省肇庆市封开县"
    },
]

# 3. Positions
positions = [
    # 李亚旭
    {"person_id": 1, "org_id": 1, "title": "中共封开县委书记", "start_date": "待查", "end_date": "现在", "rank": "正处级", "note": "2025-2026年领导活动新闻报道确认现任"},
    # 丘灿辉
    {"person_id": 2, "org_id": 2, "title": "封开县人民政府县长", "start_date": "待查", "end_date": "现在", "rank": "正处级", "note": "领导之窗确认"},
    {"person_id": 2, "org_id": 1, "title": "封开县委副书记", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 邓东尧
    {"person_id": 3, "org_id": 2, "title": "封开县人民政府副县长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 李彦玉
    {"person_id": 4, "org_id": 2, "title": "封开县人民政府副县长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 梁积瑜
    {"person_id": 5, "org_id": 2, "title": "封开县人民政府副县长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 何浩立
    {"person_id": 6, "org_id": 2, "title": "封开县人民政府副县长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 黄锡河
    {"person_id": 7, "org_id": 2, "title": "封开县人民政府副县长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 庄武军
    {"person_id": 8, "org_id": 2, "title": "封开县人民政府副县长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 卢可
    {"person_id": 9, "org_id": 2, "title": "封开县人民政府副县长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
]

# 4. Relationships
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长搭档关系",
        "overlap_org": "中共封开县委员会/封开县人民政府",
        "overlap_period": "待确认"
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记与副县长上下级关系",
        "overlap_org": "封开县人民政府",
        "overlap_period": "待确认"
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "县委书记与副县长上下级关系",
        "overlap_org": "封开县人民政府",
        "overlap_period": "待确认"
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "县委书记与副县长上下级关系",
        "overlap_org": "封开县人民政府",
        "overlap_period": "待确认"
    },
    {
        "person_a": 1,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "县委书记与副县长上下级关系",
        "overlap_org": "封开县人民政府",
        "overlap_period": "待确认"
    },
    {
        "person_a": 1,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "县委书记与副县长上下级关系",
        "overlap_org": "封开县人民政府",
        "overlap_period": "待确认"
    },
    {
        "person_a": 1,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "县委书记与副县长上下级关系",
        "overlap_org": "封开县人民政府",
        "overlap_period": "待确认"
    },
    {
        "person_a": 1,
        "person_b": 9,
        "type": "superior_subordinate",
        "context": "县委书记与副县长上下级关系",
        "overlap_org": "封开县人民政府",
        "overlap_period": "待确认"
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县长与副县长搭档关系",
        "overlap_org": "封开县人民政府",
        "overlap_period": "待确认"
    },
    {
        "person_a": 2,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "县长与副县长搭档关系",
        "overlap_org": "封开县人民政府",
        "overlap_period": "待确认"
    },
    {
        "person_a": 2,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "县长与副县长搭档关系",
        "overlap_org": "封开县人民政府",
        "overlap_period": "待确认"
    },
    {
        "person_a": 2,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "县长与副县长搭档关系",
        "overlap_org": "封开县人民政府",
        "overlap_period": "待确认"
    },
    {
        "person_a": 2,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "县长与副县长搭档关系",
        "overlap_org": "封开县人民政府",
        "overlap_period": "待确认"
    },
    {
        "person_a": 2,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "县长与副县长搭档关系",
        "overlap_org": "封开县人民政府",
        "overlap_period": "待确认"
    },
    {
        "person_a": 2,
        "person_b": 9,
        "type": "superior_subordinate",
        "context": "县长与副县长搭档关系",
        "overlap_org": "封开县人民政府",
        "overlap_period": "待确认"
    },
]


if __name__ == "__main__":
    # ── Determine output paths (staging mode) ──
    db = DB_PATH
    gexf = GEXF_PATH

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
