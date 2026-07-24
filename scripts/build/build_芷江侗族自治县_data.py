#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
芷江侗族自治县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 湖南省
Parent City: 怀化市
Region: 芷江侗族自治县
Targets: 县委书记 & 县长

Research Sources:
- 芷江侗族自治县人民政府网站 (www.zhijiang.gov.cn) — 超时无法访问
- 怀化市人民政府网站 (www.huaihua.gov.cn) — 超时无法访问
- 百度百科 — 403 被拦截
- 搜索工具 — Exa 被限流
- 公开媒体报道 — 网络不可用

Research Date: 2026-07-24
Web Access: Degraded — 所有外部网站超时/被拦截
Evidence Status: Partial — 基于训练数据中的已知信息
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "芷江侗族自治县"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons (use IDs 1-100 for persons)
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders (芷江侗族自治县)
    # ════════════════════════════════════════
    # 梁志平 — 芷江侗族自治县委书记
    # Evidence: 曾任洪江市委书记，2022年调任芷江县委书记
    # 来源：公开新闻报道（训练数据），无法在线验证
    # 注意：2026年是否仍在任需要确认
    {
        "id": 1,
        "name": "梁志平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共芷江侗族自治县委书记",
        "current_org": "中共芷江侗族自治县委员会",
        "source": "公开新闻报道（训练数据）— 网络不可用，待在线验证",
    },
    # 梁元和 — 芷江侗族自治县县长
    # Evidence: 曾任芷江县委副书记、县长，约2021年起任职
    # 来源：公开新闻报道（训练数据），无法在线验证
    # 注意：2026年是否仍在任需要确认
    {
        "id": 2,
        "name": "梁元和",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "芷江侗族自治县人民政府县长",
        "current_org": "芷江侗族自治县人民政府",
        "source": "公开新闻报道（训练数据）— 网络不可用，待在线验证",
    },
    # ════════════════════════════════════════
    # Key Deputies (信息待验证)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "待查（常务副县长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "芷江侗族自治县委常委、常务副县长",
        "current_org": "芷江侗族自治县人民政府",
        "source": "信息待确认 — 网站不可用",
    },
    {
        "id": 4,
        "name": "待查（组织部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "芷江侗族自治县委常委、组织部长",
        "current_org": "中共芷江侗族自治县委组织部",
        "source": "信息待确认 — 网站不可用",
    },
    {
        "id": 5,
        "name": "待查（纪委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "芷江侗族自治县委常委、县纪委书记",
        "current_org": "中共芷江侗族自治县纪律检查委员会",
        "source": "信息待确认 — 网站不可用",
    },
    {
        "id": 6,
        "name": "待查（政法委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "芷江侗族自治县委常委、政法委书记",
        "current_org": "中共芷江侗族自治县委政法委员会",
        "source": "信息待确认 — 网站不可用",
    },
    {
        "id": 7,
        "name": "待查（宣传部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "芷江侗族自治县委常委、宣传部长",
        "current_org": "中共芷江侗族自治县委宣传部",
        "source": "信息待确认 — 网站不可用",
    },
    # ════════════════════════════════════════
    # Previous Leaders
    # ════════════════════════════════════════
    # 前任县委书记 — 梁志平的前任
    # 梁志平约2022年接任，前任需要确认
    {
        "id": 8,
        "name": "待查（前任县委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任芷江侗族自治县委书记（已调离）",
        "current_org": "",
        "source": "信息待确认 — 网站不可用",
    },
]

# 2. Organizations
organizations = [
    {"id": 1, "name": "中共芷江侗族自治县委员会", "type": "党委", "level": "县级", "location": "湖南省怀化市芷江侗族自治县"},
    {"id": 2, "name": "芷江侗族自治县人民政府", "type": "政府", "level": "县级", "location": "湖南省怀化市芷江侗族自治县"},
    {"id": 3, "name": "中共芷江侗族自治县纪律检查委员会", "type": "纪委", "level": "县级", "location": "湖南省怀化市芷江侗族自治县"},
    {"id": 4, "name": "芷江侗族自治县监察委员会", "type": "纪委", "level": "县级", "location": "湖南省怀化市芷江侗族自治县"},
    {"id": 5, "name": "中共芷江侗族自治县委组织部", "type": "党委", "level": "县级", "location": "湖南省怀化市芷江侗族自治县"},
    {"id": 6, "name": "中共芷江侗族自治县委宣传部", "type": "党委", "level": "县级", "location": "湖南省怀化市芷江侗族自治县"},
    {"id": 7, "name": "中共芷江侗族自治县委政法委员会", "type": "党委", "level": "县级", "location": "湖南省怀化市芷江侗族自治县"},
    {"id": 8, "name": "芷江侗族自治县人民代表大会常务委员会", "type": "人大", "level": "县级", "location": "湖南省怀化市芷江侗族自治县"},
    {"id": 9, "name": "中国人民政治协商会议芷江侗族自治县委员会", "type": "政协", "level": "县级", "location": "湖南省怀化市芷江侗族自治县"},
    {"id": 10, "name": "芷江侗族自治县人民武装部", "type": "政府", "level": "县级", "location": "湖南省怀化市芷江侗族自治县"},
]

# 3. Positions: person_id -> org_id with title and dates
positions = [
    # 梁志平
    {"person_id": 1, "org_id": 1, "title": "中共芷江侗族自治县委书记", "start": "", "end": "至今", "note": "兼任县人武部党委第一书记（推定）"},
    {"person_id": 1, "org_id": 10, "title": "芷江侗族自治县人武部党委第一书记", "start": "", "end": "至今", "note": "县委书记兼任（推定）"},

    # 梁元和
    {"person_id": 2, "org_id": 2, "title": "芷江侗族自治县人民政府县长", "start": "", "end": "至今", "note": "主持县政府全面工作"},

    # 常务副县长
    {"person_id": 3, "org_id": 2, "title": "芷江侗族自治县委常委、常务副县长", "start": "", "end": "至今", "note": "姓名待确认"},

    # 组织部长
    {"person_id": 4, "org_id": 5, "title": "芷江侗族自治县委常委、组织部长", "start": "", "end": "至今", "note": "姓名待确认"},

    # 纪委书记
    {"person_id": 5, "org_id": 3, "title": "芷江侗族自治县委常委、纪委书记", "start": "", "end": "至今", "note": "姓名待确认"},
    {"person_id": 5, "org_id": 4, "title": "芷江侗族自治县监委主任", "start": "", "end": "至今", "note": "姓名待确认"},

    # 政法委书记
    {"person_id": 6, "org_id": 7, "title": "芷江侗族自治县委常委、政法委书记", "start": "", "end": "至今", "note": "姓名待确认"},

    # 宣传部长
    {"person_id": 7, "org_id": 6, "title": "芷江侗族自治县委常委、宣传部长", "start": "", "end": "至今", "note": "姓名待确认"},
]

# 4. Relationships
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长搭班",
        "overlap_org": "芷江侗族自治县",
        "overlap_period": "推定至今",
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记与常务副县长上下级关系",
        "overlap_org": "芷江侗族自治县",
        "overlap_period": "推定至今",
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县长与常务副县长工作搭档",
        "overlap_org": "芷江侗族自治县人民政府",
        "overlap_period": "推定至今",
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "县委书记与组织部长",
        "overlap_org": "中共芷江侗族自治县委员会",
        "overlap_period": "推定至今",
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "县委书记与纪委书记",
        "overlap_org": "中共芷江侗族自治县委员会",
        "overlap_period": "推定至今",
    },
    {
        "person_a": 1,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "县委书记与政法委书记",
        "overlap_org": "中共芷江侗族自治县委员会",
        "overlap_period": "推定至今",
    },
    {
        "person_a": 1,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "县委书记与宣传部长",
        "overlap_org": "中共芷江侗族自治县委员会",
        "overlap_period": "推定至今",
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
