#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
麻阳苗族自治县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 湖南省
Parent City: 怀化市
Region: 麻阳苗族自治县
Targets: 县委书记 & 县长

Research Sources:
- 麻阳苗族自治县人民政府网站 (www.mayang.gov.cn) — 首页可访问，深层页面无法访问
- 怀化市人民政府网站 (www.huaihua.gov.cn) — 超时无法访问
- 百度百科 — 403 被拦截
- 搜索工具 — Exa 被限流
- 公开媒体报道 — 网络不可用

Research Date: 2026-07-24
Web Access: Degraded — 大部分外部网站超时/被拦截
Evidence Status: Partial — 基于政府网站首页新闻中提取的信息和训练数据中的已知信息

Known from mayang.gov.cn homepage news (2026-07-24):
- 廖园熙: 主持县委理论学习中心组集体学习、主持召开米墅清淼温泉度假村二期规划汇报会
- 胡宏林: 主持召开县人民政府常务会议 (2026年1月、3月、4月)
- 麻学清: 主持召开县人民政府常务会议 (2026年6月)
- "宣布麻阳苗族自治县人武部党委第一书记任职大会" — 县委书记兼任人武部党委第一书记
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "麻阳苗族自治县"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons (use IDs 1-100 for persons)
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders (麻阳苗族自治县)
    # ════════════════════════════════════════
    # 廖园熙 — 麻阳县委书记
    # Evidence: 主持县委理论学习中心组2026年第七次集体学习 (2026-07-17 news)
    #          主持召开麻阳米墅清淼温泉度假村二期规划汇报会 (2026-07-21 news)
    #          人武部党委第一书记任职大会 (县委书记兼任)
    {
        "id": 1,
        "name": "廖园熙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共麻阳苗族自治县委书记",
        "current_org": "中共麻阳苗族自治县委员会",
        "source": "麻阳苗族自治县人民政府官网新闻 (2026-07)",
    },
    # 胡宏林 — 麻阳苗族自治县县长
    # Evidence: 主持召开县人民政府常务会议(1月23日、3月27日、4月29日)
    # 最新一条为4月29日，此后6月26日常务会议由麻学清主持
    {
        "id": 2,
        "name": "胡宏林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "麻阳苗族自治县人民政府县长",
        "current_org": "麻阳苗族自治县人民政府",
        "source": "麻阳苗族自治县人民政府官网新闻 (2026-01至2026-04)",
    },
    # ════════════════════════════════════════
    # Key Deputies and Leadership Team
    # ════════════════════════════════════════
    # 麻学清 — 县委常委、常务副县长(推测)
    # Evidence: 主持召开县人民政府常务会议(6月26日), 在胡宏林之后
    {
        "id": 3,
        "name": "麻学清",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "麻阳苗族自治县委常委、县人民政府常务副县长(推测)",
        "current_org": "麻阳苗族自治县人民政府",
        "source": "麻阳苗族自治县人民政府官网新闻 (2026-06)",
    },
    # ════════════════════════════════════════
    # Previous Leaders
    # ════════════════════════════════════════
    # 前任县委书记 — 需要确认具体人选
    {
        "id": 4,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任麻阳苗族自治县委书记（已调离）",
        "current_org": "",
        "source": "信息待确认 — 网站不可用",
    },
]

# 2. Organizations
organizations = [
    {"id": 1, "name": "中共麻阳苗族自治县委员会", "type": "党委", "level": "县级", "location": "湖南省怀化市麻阳苗族自治县"},
    {"id": 2, "name": "麻阳苗族自治县人民政府", "type": "政府", "level": "县级", "location": "湖南省怀化市麻阳苗族自治县"},
    {"id": 3, "name": "中共麻阳苗族自治县纪律检查委员会", "type": "纪委", "level": "县级", "location": "湖南省怀化市麻阳苗族自治县"},
    {"id": 4, "name": "麻阳苗族自治县监察委员会", "type": "纪委", "level": "县级", "location": "湖南省怀化市麻阳苗族自治县"},
    {"id": 5, "name": "中共麻阳苗族自治县委组织部", "type": "党委", "level": "县级", "location": "湖南省怀化市麻阳苗族自治县"},
    {"id": 6, "name": "中共麻阳苗族自治县委宣传部", "type": "党委", "level": "县级", "location": "湖南省怀化市麻阳苗族自治县"},
    {"id": 7, "name": "中共麻阳苗族自治县委政法委员会", "type": "党委", "level": "县级", "location": "湖南省怀化市麻阳苗族自治县"},
    {"id": 8, "name": "麻阳苗族自治县人民代表大会常务委员会", "type": "人大", "level": "县级", "location": "湖南省怀化市麻阳苗族自治县"},
    {"id": 9, "name": "中国人民政治协商会议麻阳苗族自治县委员会", "type": "政协", "level": "县级", "location": "湖南省怀化市麻阳苗族自治县"},
    {"id": 10, "name": "麻阳苗族自治县人民武装部", "type": "政府", "level": "县级", "location": "湖南省怀化市麻阳苗族自治县"},
]

# 3. Positions: person_id -> org_id with title and dates
positions = [
    # 廖园熙
    {"person_id": 1, "org_id": 1, "title": "中共麻阳苗族自治县委书记", "start": "", "end": "至今", "note": "兼任县人武部党委第一书记"},
    {"person_id": 1, "org_id": 10, "title": "麻阳苗族自治县人武部党委第一书记", "start": "", "end": "至今", "note": "县委书记兼任"},

    # 胡宏林
    {"person_id": 2, "org_id": 2, "title": "麻阳苗族自治县人民政府县长", "start": "", "end": "至今", "note": "主持县政府全面工作"},

    # 麻学清
    {"person_id": 3, "org_id": 2, "title": "麻阳苗族自治县委常委、常务副县长(推测)", "start": "", "end": "至今", "note": "2026年6月起主持县政府常务会议"},
]

# 4. Relationships
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长搭班",
        "overlap_org": "麻阳苗族自治县",
        "overlap_period": "2026-至今",
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记与常务副县长上下级关系",
        "overlap_org": "麻阳苗族自治县",
        "overlap_period": "2026-至今",
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县长与常务副县长工作搭档",
        "overlap_org": "麻阳苗族自治县人民政府",
        "overlap_period": "2026-至今",
    },
]

# ── Build ──

if __name__ == "__main__":
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
    print("Done!")
