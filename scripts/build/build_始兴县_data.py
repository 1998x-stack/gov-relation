#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
始兴县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 广东省
Parent City: 韶关市
Region: 始兴县
Targets: 县委书记 & 县长

Research Sources:
- 维基百科 (zh.wikipedia.org) — 始兴县词条
- Web search limited — see open_gaps.md for access constraints

Current status (as of 2026-07-22):
- 县委书记: [待查 — 已知历任: 黄令遥(～2021)、华关(2021～2024?)；2024年后待查]
- 县长: [待查]

Research Date: 2026-07-22
Web Access Status: Degraded (Exa rate-limited, Baidu 403, gov sites timeout)
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../"))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "始兴县"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──
# Note: All data below is based on limited web access.
# Confidence levels and sources are marked explicitly.
# Web access was degraded during this research (July 2026):
# Exa rate-limited, Baidu 403, gov.cn timeouts.
# Fields marked "待查" are unknown.

# 1. Persons
persons = [
    # ── 县委领导 ──
    # Note: 始兴县县委书记和县长的人选在2024-2026年间可能有变更。
    # 根据已知信息：黄令遥(2016-2021)、华关(2021-)曾任县委书记。
    # 当前(2026年7月)的县委书记和县长信息无法确认。
    {
        "id": 1,
        "name": "待查_县委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共始兴县委书记",
        "current_org": "中共始兴县委员会",
        "source": "公开资料无法确认当前在任者"
    },
    {
        "id": 2,
        "name": "待查_县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "始兴县人民政府县长",
        "current_org": "始兴县人民政府",
        "source": "公开资料无法确认当前在任者"
    },
    # ── 已知历任县委书记 ──
    {
        "id": 3,
        "name": "黄令遥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "曾任中共始兴县委书记（～2021年）",
        "current_org": "中共始兴县委员会",
        "source": "Wikipedia:始兴县；维基百科页面列举黄令遥为县委书记"
    },
    {
        "id": 4,
        "name": "华关",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "曾任始兴县委书记（2021年－？）",
        "current_org": "中共始兴县委员会",
        "source": "公开新闻报道；华关曾任始兴县委书记，此前任始兴县长"
    },
    # ── 已知历任县长 ──
    {
        "id": 5,
        "name": "叶洪番",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "曾任始兴县人民政府县长（～2021年）",
        "current_org": "始兴县人民政府",
        "source": "公开新闻报道：叶洪番曾任始兴县长，后调任"
    },
    # ── 县委副书记 ──
    {
        "id": 6,
        "name": "待查_县委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共始兴县委副书记",
        "current_org": "中共始兴县委员会",
        "source": "公开资料无法确认当前在任者"
    },
    # ── 县委常委、常务副县长 ──
    {
        "id": 7,
        "name": "待查_常务副县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "始兴县委常委、常务副县长",
        "current_org": "始兴县人民政府",
        "source": "公开资料无法确认当前在任者"
    },
    # ── 县纪委 ──
    {
        "id": 8,
        "name": "待查_纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "始兴县委常委、纪委书记、监委主任",
        "current_org": "中共始兴县纪律检查委员会",
        "source": "公开资料无法确认当前在任者"
    },
    # ── 县委组织部 ──
    {
        "id": 9,
        "name": "待查_组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "始兴县委常委、组织部部长",
        "current_org": "中共始兴县委组织部",
        "source": "公开资料无法确认当前在任者"
    },
    # ── 县委宣传部 ──
    {
        "id": 10,
        "name": "待查_宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "始兴县委常委、宣传部部长",
        "current_org": "中共始兴县委宣传部",
        "source": "公开资料无法确认当前在任者"
    },
    # ── 县委政法委 ──
    {
        "id": 11,
        "name": "待查_政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "始兴县委常委、政法委书记",
        "current_org": "中共始兴县委政法委员会",
        "source": "公开资料无法确认当前在任者"
    },
    # ── 人武部 ──
    {
        "id": 12,
        "name": "待查_人武部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "始兴县委常委、人武部部长",
        "current_org": "始兴县人民武装部",
        "source": "公开资料无法确认当前在任者"
    },
    # ── 副县长 ──
    {
        "id": 13,
        "name": "待查_副县长1",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "始兴县人民政府副县长",
        "current_org": "始兴县人民政府",
        "source": "公开资料无法确认当前在任者"
    },
    {
        "id": 14,
        "name": "待查_副县长2",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "始兴县人民政府副县长",
        "current_org": "始兴县人民政府",
        "source": "公开资料无法确认当前在任者"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共始兴县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共韶关市委员会",
        "location": "广东省韶关市始兴县"
    },
    {
        "id": 2,
        "name": "始兴县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "韶关市人民政府",
        "location": "广东省韶关市始兴县"
    },
    {
        "id": 3,
        "name": "中共始兴县纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共韶关市纪律检查委员会",
        "location": "广东省韶关市始兴县"
    },
    {
        "id": 4,
        "name": "中共始兴县委组织部",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共始兴县委员会",
        "location": "广东省韶关市始兴县"
    },
    {
        "id": 5,
        "name": "中共始兴县委宣传部",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共始兴县委员会",
        "location": "广东省韶关市始兴县"
    },
    {
        "id": 6,
        "name": "中共始兴县委政法委员会",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共始兴县委员会",
        "location": "广东省韶关市始兴县"
    },
    {
        "id": 7,
        "name": "始兴县人民武装部",
        "type": "政府",
        "level": "县处级",
        "parent": "韶关军分区",
        "location": "广东省韶关市始兴县"
    },
    {
        "id": 8,
        "name": "始兴县人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "韶关市人民代表大会常务委员会",
        "location": "广东省韶关市始兴县"
    },
    {
        "id": 9,
        "name": "中国人民政治协商会议始兴县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协韶关市委员会",
        "location": "广东省韶关市始兴县"
    },
]

# 3. Positions
positions = [
    # 现任县委领导
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "待查", "end_date": "present", "rank": "县处级正职", "note": "当前在任者信息待查"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "待查", "end_date": "present", "rank": "县处级正职", "note": "当前在任者信息待查"},

    # 历任县委书记
    {"person_id": 3, "org_id": 1, "title": "县委书记", "start_date": "2016年", "end_date": "2021年", "rank": "县处级正职", "note": "黄令遥任始兴县委书记"},
    {"person_id": 4, "org_id": 1, "title": "县委书记", "start_date": "2021年", "end_date": "待查", "rank": "县处级正职", "note": "华关任始兴县委书记"},

    # 历任县长
    {"person_id": 5, "org_id": 2, "title": "县长", "start_date": "待查", "end_date": "2021年", "rank": "县处级正职", "note": "叶洪番任始兴县长"},

    # 华关曾任县长
    {"person_id": 4, "org_id": 2, "title": "县长", "start_date": "待查", "end_date": "2021年", "rank": "县处级正职", "note": "华关曾任始兴县长后升任县委书记"},

    # 其他班子成员
    {"person_id": 6, "org_id": 1, "title": "县委副书记", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "当前在任者信息待查"},
    {"person_id": 7, "org_id": 2, "title": "常务副县长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "当前在任者信息待查"},
    {"person_id": 8, "org_id": 3, "title": "纪委书记、监委主任", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "当前在任者信息待查"},
    {"person_id": 9, "org_id": 4, "title": "组织部部长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "当前在任者信息待查"},
    {"person_id": 10, "org_id": 5, "title": "宣传部部长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "当前在任者信息待查"},
    {"person_id": 11, "org_id": 6, "title": "政法委书记", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "当前在任者信息待查"},
    {"person_id": 12, "org_id": 7, "title": "人武部部长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "当前在任者信息待查"},
    {"person_id": 13, "org_id": 2, "title": "副县长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "当前在任者信息待查"},
    {"person_id": 14, "org_id": 2, "title": "副县长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "当前在任者信息待查"},
]

# 4. Relationships
relationships = [
    # 华关—叶洪番：前后任关系（华关接替叶洪番任县长）
    {
        "person_a": 4,
        "person_b": 5,
        "type": "predecessor_successor",
        "context": "华关接替叶洪番担任始兴县长",
        "overlap_org": "始兴县人民政府",
        "overlap_period": "待查"
    },
    # 黄令遥—华关：前后任关系（华关接替黄令遥任县委书记）
    {
        "person_a": 3,
        "person_b": 4,
        "type": "predecessor_successor",
        "context": "华关接替黄令遥担任始兴县委书记",
        "overlap_org": "中共始兴县委员会",
        "overlap_period": "2021年"
    },
    # 华关—待查县长：上下级关系
    {
        "person_a": 4,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "华关任县委书记期间与现任县长的领导关系",
        "overlap_org": "中共始兴县委员会",
        "overlap_period": "待查"
    },
]

# ── Build ──
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

print(f"✅ Build complete: {DB_PATH}")
print(f"✅ Build complete: {GEXF_PATH}")
print(f"   Persons: {len(persons)}")
print(f"   Organizations: {len(organizations)}")
print(f"   Positions: {len(positions)}")
print(f"   Relationships: {len(relationships)}")
print("⚠️  Many person records contain '待查' due to degraded web access.")
print("   See report/open_gaps.md for details.")
