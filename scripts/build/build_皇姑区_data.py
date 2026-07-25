#!/usr/bin/env python3
"""Build script for 沈阳市皇姑区 government personnel network."""

import sqlite3
from datetime import datetime
from pathlib import Path

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "皇姑区"
STAGING = Path("data/tmp/liaoning_皇姑区")

# Tokens required by process_tmp validation
DB_PATH = STAGING / "皇姑区_network.db"
GEXF_PATH = STAGING / "皇姑区_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────

persons = [
    # ── Party Secretary (区委书记) ──
    {
        "id": 1,
        "name": "牛群",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "区委书记",
        "current_org": "中共沈阳市皇姑区委员会",
        "source": "syhg.gov.cn政府网站新闻报道/政府常务会议记录",
    },
    # ── District Mayor (区长) ──
    {
        "id": 2,
        "name": "赵宇旭",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "区委副书记、区长",
        "current_org": "皇姑区人民政府",
        "source": "syhg.gov.cn政府网站政府常务会议记录",
    },
    # ── Predecessor Party Secretary (前任区委书记, now 沈河区委书记) ──
    {
        "id": 3,
        "name": "李盛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-01",
        "birthplace": "待查",
        "education": "研究生学历，公共管理硕士（清华大学机械工程系硕士研究生，美国伊利诺伊理工学院公共管理硕士）",
        "party_join": "1996-06",
        "work_start": "2001-08",
        "current_post": "区委书记",
        "current_org": "中共沈阳市沈河区委员会",
        "source": "百度百科/沈阳日报/沈河区调查报告",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共沈阳市皇姑区委员会",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共沈阳市委",
        "location": "沈阳市皇姑区",
    },
    {
        "id": 2,
        "name": "皇姑区人民政府",
        "type": "政府",
        "level": "市辖区",
        "parent": "沈阳市人民政府",
        "location": "沈阳市皇姑区",
    },
    {
        "id": 3,
        "name": "中共沈阳市沈河区委员会",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共沈阳市委",
        "location": "沈阳市沈河区",
    },
]

# ── Positions ─────────────────────────────────────────────────────────────

positions = [
    # 牛群 - current区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "2025-11", "end": "present", "rank": "正局级（副省级城市辖区）", "note": "从区长转任区委书记"},
    # 牛群 - previous区长
    {"person_id": 1, "org_id": 2, "title": "区长", "start": "待查", "end": "2025-11", "rank": "", "note": "后转任区委书记"},
    # 赵宇旭 - current区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "2026-01", "end": "present", "rank": "", "note": "原代区长，2025年12月任代区长"},
    # 赵宇旭 - 代区长
    {"person_id": 2, "org_id": 2, "title": "代区长", "start": "2025-12", "end": "2026-01", "rank": "", "note": ""},
    # 李盛 - previous皇姑区委书记
    {"person_id": 3, "org_id": 1, "title": "区委书记", "start": "2021", "end": "2025", "rank": "", "note": "后调任沈河区委书记"},
    # 李盛 - previous皇姑区区长
    {"person_id": 3, "org_id": 2, "title": "区长", "start": "2019", "end": "2021", "rank": "", "note": "最初为代区长"},
    # 李盛 - current沈河区委书记
    {"person_id": 3, "org_id": 3, "title": "区委书记", "start": "2025", "end": "present", "rank": "正局级（副省级城市辖区）", "note": "从皇姑区平调沈河区"},
]

# ── Relationships ─────────────────────────────────────────────────────────

relationships = [
    {
        "person_a": 1,  # 牛群
        "person_b": 3,  # 李盛
        "type": "predecessor_successor",
        "context": "牛群接替李盛任皇姑区委书记（李盛调任沈河区委书记）",
        "overlap_org": "中共沈阳市皇姑区委员会",
        "overlap_period": "",
    },
    {
        "person_a": 1,  # 牛群
        "person_b": 2,  # 赵宇旭
        "type": "predecessor_successor",
        "context": "牛群原为区长，后转任区委书记；赵宇旭接任区长",
        "overlap_org": "皇姑区人民政府",
        "overlap_period": "2025-2026",
    },
    {
        "person_a": 3,  # 李盛
        "person_b": 2,  # 赵宇旭
        "type": "superior_subordinate",
        "context": "李盛曾任皇姑区委书记（赵宇旭前任的前任），与赵宇旭不直接搭班",
        "overlap_org": "中共沈阳市皇姑区委员会/皇姑区人民政府",
        "overlap_period": "",
    },
]

# ── Build ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
