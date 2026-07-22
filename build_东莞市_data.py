#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
东莞市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 地级市
Province: 广东省
Parent City:
Region: 东莞市
Targets: 市委书记 & 市长

Research Sources:
- 东莞市人民政府门户网站 (www.dg.gov.cn) — 领导信息版块
- 东莞市政府新闻动态（确认韦皓为市委书记活动）
- 维基百科/公开资料——东莞市词条

Current status (as of 2026-07-22):
- 市委书记: 韦皓（2024年－）
- 市长: 吕成蹊（2022年1月－）

Research Date: 2026-07-22
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "东莞市"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # 市委领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "韦皓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共东莞市委书记",
        "current_org": "中共东莞市委员会",
        "source": "东莞市人民政府门户网站(dg.gov.cn)新闻报道确认"
    },
    {
        "id": 2,
        "name": "吕成蹊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查（约1969年）",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共东莞市委副书记、市长",
        "current_org": "东莞市人民代表大会",
        "source": "公开资料：东莞市市长（2022年1月至今）"
    },
    # ════════════════════════════════════════
    # 市政府领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "曾坚朋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "东莞市委常委、副市长",
        "current_org": "东莞市人民政府",
        "source": "dg.gov.cn 领导信息"
    },
    {
        "id": 4,
        "name": "黎军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "东莞市人民政府副市长",
        "current_org": "东莞市人民政府",
        "source": "dg.gov.cn 领导信息"
    },
    {
        "id": 5,
        "name": "卢建军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "东莞市人民政府副市长",
        "current_org": "东莞市人民政府",
        "source": "dg.gov.cn 领导信息"
    },
    {
        "id": 6,
        "name": "陈海波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "东莞市人民政府副市长",
        "current_org": "东莞市人民政府",
        "source": "dg.gov.cn 领导信息"
    },
    {
        "id": 7,
        "name": "陈庆松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "东莞市人民政府副市长",
        "current_org": "东莞市人民政府",
        "source": "dg.gov.cn 领导信息"
    },
    {
        "id": 8,
        "name": "杨宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "东莞市人民政府副市长",
        "current_org": "东莞市人民政府",
        "source": "dg.gov.cn 领导信息"
    },
    {
        "id": 9,
        "name": "袁仕望",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "东莞市人民政府秘书长",
        "current_org": "东莞市人民政府办公室",
        "source": "dg.gov.cn 领导信息"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共东莞市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共广东省委员会",
        "location": "东莞市南城区"
    },
    {
        "id": 2,
        "name": "东莞市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "广东省人民政府",
        "location": "东莞市南城区"
    },
    {
        "id": 3,
        "name": "东莞市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级市",
        "parent": "广东省人民代表大会常务委员会",
        "location": "东莞市南城区"
    },
    {
        "id": 4,
        "name": "东莞市人民政府办公室",
        "type": "政府",
        "level": "地级市",
        "parent": "东莞市人民政府",
        "location": "东莞市南城区"
    },
    {
        "id": 5,
        "name": "广东省人民政府",
        "type": "政府",
        "level": "省级",
        "parent": "",
        "location": "广州市"
    },
    {
        "id": 6,
        "name": "中共广东省委员会",
        "type": "党委",
        "level": "省级",
        "parent": "",
        "location": "广州市"
    },
]

# 3. Positions (person_id, org_id, title, start, end, rank, note)
positions = [
    # 韦皓
    {"person_id": 1, "org_id": 1, "title": "中共东莞市委书记", "start_date": "2024", "end_date": "present", "rank": "正厅级", "note": "东莞市委书记，兼任东莞军分区党委第一书记"},
    # 吕成蹊
    {"person_id": 2, "org_id": 2, "title": "东莞市市长", "start_date": "2022-01", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "中共东莞市委副书记", "start_date": "2022-01", "end_date": "present", "rank": "正厅级", "note": "市委副书记兼市长"},
    # 曾坚朋
    {"person_id": 3, "org_id": 2, "title": "东莞市委常委、副市长", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": "dg.gov.cn确认在任"},
    # 黎军
    {"person_id": 4, "org_id": 2, "title": "东莞市副市长", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": "dg.gov.cn确认在任"},
    # 卢建军
    {"person_id": 5, "org_id": 2, "title": "东莞市副市长", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": "dg.gov.cn确认在任"},
    # 陈海波
    {"person_id": 6, "org_id": 2, "title": "东莞市副市长", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": "dg.gov.cn确认在任"},
    # 陈庆松
    {"person_id": 7, "org_id": 2, "title": "东莞市副市长", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": "dg.gov.cn确认在任"},
    # 杨宇
    {"person_id": 8, "org_id": 2, "title": "东莞市副市长", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": "dg.gov.cn确认在任"},
    # 袁仕望
    {"person_id": 9, "org_id": 4, "title": "东莞市人民政府秘书长", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "dg.gov.cn确认在任"},
]

# 4. Relationships
relationships = [
    # 现任党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "市委书记与市长是地级市最重要的党政搭档", "overlap_org": "中共东莞市委员会/东莞市人民政府", "overlap_period": "2024至今"},
    # 韦皓与副市长们（上下级关系）
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "市委书记与常务副市长", "overlap_org": "中共东莞市委员会/东莞市人民政府", "overlap_period": "2024至今"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "市委书记与副市长", "overlap_org": "东莞市人民政府", "overlap_period": "2024至今"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "市委书记与副市长", "overlap_org": "东莞市人民政府", "overlap_period": "2024至今"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "市委书记与副市长", "overlap_org": "东莞市人民政府", "overlap_period": "2024至今"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "市委书记与副市长", "overlap_org": "东莞市人民政府", "overlap_period": "2024至今"},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "市委书记与副市长", "overlap_org": "东莞市人民政府", "overlap_period": "2024至今"},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "市委书记与市政府秘书长", "overlap_org": "中共东莞市委员会/东莞市人民政府", "overlap_period": "2024至今"},
    # 吕成蹊与副市长们
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "市长与常务副市长", "overlap_org": "东莞市人民政府", "overlap_period": "2022至今"},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "市长与副市长", "overlap_org": "东莞市人民政府", "overlap_period": "2022至今"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "市长与副市长", "overlap_org": "东莞市人民政府", "overlap_period": "2022至今"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "市长与副市长", "overlap_org": "东莞市人民政府", "overlap_period": "2022至今"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "市长与副市长", "overlap_org": "东莞市人民政府", "overlap_period": "2022至今"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "市长与副市长", "overlap_org": "东莞市人民政府", "overlap_period": "2022至今"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "市长与市政府秘书长", "overlap_org": "东莞市人民政府", "overlap_period": "2022至今"},
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
