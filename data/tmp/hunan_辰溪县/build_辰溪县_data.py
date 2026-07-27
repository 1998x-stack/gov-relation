#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
辰溪县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 湖南省
Parent City: 怀化市
Region: 辰溪县
Targets: 县委书记 & 县长

Research Sources:
- 辰溪县人民政府网站 (www.chenxi.gov.cn) — 超时无法访问
- 怀化市人民政府网站 (www.huaihua.gov.cn) — 超时无法访问
- 百度百科 — 超时无法访问 (403)
- 公开媒体报道 — 网络不可用
- 搜索工具 — Exa 被限流

Research Date: 2026-07-24
Web Access: Degraded — 所有外部网站超时/被拦截
Evidence Status: Partial — 基于训练数据中的已知信息
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "辰溪县"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons (use IDs 1-100 for persons)
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders (辰溪县)
    # ════════════════════════════════════════
    # 丁热平 — 辰溪县委书记
    # Previously served as 辰溪县长, appointed 县委书记 around 2022
    {
        "id": 1,
        "name": "丁热平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共辰溪县委书记",
        "current_org": "中共辰溪县委员会",
        "source": "https://www.chenxi.gov.cn (unreachable)",
    },
    # 县长 — 需要确认具体人选
    # 丁热平原任县长 (至2022年前后), 接任者需核实
    {
        "id": 2,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "辰溪县人民政府县长",
        "current_org": "辰溪县人民政府",
        "source": "信息待确认 — 网站不可用",
    },
    # ════════════════════════════════════════
    # Previous Leaders (Predecessors)
    # ════════════════════════════════════════
    # 谢建军 — 前任辰溪县委书记 (2021年前后任职), 后调任
    {
        "id": 3,
        "name": "谢建军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "已调离辰溪县",
        "current_org": "",
        "source": "公开报道 — 需核实",
    },
    # ════════════════════════════════════════
    # Key Deputies (Standing Committee Members)
    # ════════════════════════════════════════
    # 常务副县长 (待确认具体人选)
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
        "current_post": "辰溪县委常委、常务副县长",
        "current_org": "辰溪县人民政府",
        "source": "信息待确认 — 网站不可用",
    },
    # 县纪委书记 (待确认具体人选)
    {
        "id": 5,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "辰溪县委常委、纪委书记、监委主任",
        "current_org": "中共辰溪县纪律检查委员会",
        "source": "信息待确认 — 网站不可用",
    },
    # 县委组织部部长 (待确认具体人选)
    {
        "id": 6,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "辰溪县委常委、组织部部长",
        "current_org": "中共辰溪县委组织部",
        "source": "信息待确认 — 网站不可用",
    },
    # 县委宣传部部长 (待确认具体人选)
    {
        "id": 7,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "辰溪县委常委、宣传部部长",
        "current_org": "中共辰溪县委宣传部",
        "source": "信息待确认 — 网站不可用",
    },
    # 县委政法委书记 (待确认具体人选)
    {
        "id": 8,
        "name": "待查",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "辰溪县委常委、政法委书记",
        "current_org": "中共辰溪县委政法委员会",
        "source": "信息待确认 — 网站不可用",
    },
]

# 2. Organizations
organizations = [
    {"id": 1, "name": "中共辰溪县委员会", "type": "党委", "level": "县级", "location": "湖南省怀化市辰溪县"},
    {"id": 2, "name": "辰溪县人民政府", "type": "政府", "level": "县级", "location": "湖南省怀化市辰溪县"},
    {"id": 3, "name": "中共辰溪县纪律检查委员会", "type": "纪委", "level": "县级", "location": "湖南省怀化市辰溪县"},
    {"id": 4, "name": "辰溪县监察委员会", "type": "纪委", "level": "县级", "location": "湖南省怀化市辰溪县"},
    {"id": 5, "name": "中共辰溪县委组织部", "type": "党委", "level": "县级", "location": "湖南省怀化市辰溪县"},
    {"id": 6, "name": "中共辰溪县委宣传部", "type": "党委", "level": "县级", "location": "湖南省怀化市辰溪县"},
    {"id": 7, "name": "中共辰溪县委政法委员会", "type": "党委", "level": "县级", "location": "湖南省怀化市辰溪县"},
    {"id": 8, "name": "辰溪县人民代表大会常务委员会", "type": "人大", "level": "县级", "location": "湖南省怀化市辰溪县"},
    {"id": 9, "name": "中国人民政治协商会议辰溪县委员会", "type": "政协", "level": "县级", "location": "湖南省怀化市辰溪县"},
    {"id": 10, "name": "中共怀化市委员会", "type": "党委", "level": "地市级", "location": "湖南省怀化市"},
    {"id": 11, "name": "怀化市人民政府", "type": "政府", "level": "地市级", "location": "湖南省怀化市"},
]

# 3. Positions: person_id -> org_id with title and dates
positions = [
    # 丁热平
    {"person_id": 1, "org_id": 1, "title": "中共辰溪县委书记", "start": "2022?", "end": "至今", "note": "前为辰溪县长"},
    {"person_id": 1, "org_id": 2, "title": "辰溪县人民政府县长", "start": "?", "end": "2022?", "note": "升任县委书记前担任"},

    # 县长 (待查)
    {"person_id": 2, "org_id": 2, "title": "辰溪县人民政府县长", "start": "?", "end": "至今", "note": "接替丁热平"},

    # 谢建军 (前任书记)
    {"person_id": 3, "org_id": 1, "title": "中共辰溪县委书记", "start": "?", "end": "2021?", "note": "前任县委书记"},
]

# 4. Relationships
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长搭班",
        "overlap_org": "辰溪县",
        "overlap_period": "2022-至今",
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "predecessor_successor",
        "context": "丁热平接替谢建军任县委书记",
        "overlap_org": "中共辰溪县委员会",
        "overlap_period": "2021-2022",
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
