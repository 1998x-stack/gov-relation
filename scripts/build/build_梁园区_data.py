#!/usr/bin/env python3
"""商丘市梁园区领导班子工作关系网络 — 数据构建脚本。

等级: 市辖区
调查日期: 2026-07-24
信息来源:
  - 梁园区人民政府网站 (liangyuan.gov.cn)
  - 新闻动态及政府会议报道
"""

from __future__ import annotations

import json
import sqlite3  # noqa
import sys
from datetime import datetime
from pathlib import Path

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Config ────────────────────────────────────────────────────────────────────
SLUG = "梁园区"
TODAY = "2026-07-24"
STAGING = Path(__file__).resolve().parent

DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────────
# Person IDs: 1xxx = party committee, 2xxx = government, 3xxx = other leaders

persons = [
    # ═══════════════════════════════════════════════════════════════════════
    # 1. 张亚光 — 区委书记
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1001,
        "name": "张亚光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "梁园区委书记",
        "current_org": "中共商丘市梁园区委员会",
        "source": "https://www.liangyuan.gov.cn/ （新闻：张亚光主持召开全区重点项目调度会 2026-07-17；张亚光带队调研防汛备汛 2026-07-14）",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 2. 魏宏志 — 区委副书记、区长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1002,
        "name": "魏宏志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "梁园区委副书记、区人民政府党组书记、区长",
        "current_org": "梁园区人民政府",
        "source": "https://www.liangyuan.gov.cn/ （新闻：魏宏志主持召开六届政府第69次常务会议 2026-07-02）",
    },
]

# ── Organizations ────────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共商丘市梁园区委员会",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共商丘市委员会",
        "location": "河南省商丘市梁园区",
    },
    {
        "id": 2,
        "name": "梁园区人民政府",
        "type": "政府",
        "level": "市辖区",
        "parent": "商丘市人民政府",
        "location": "河南省商丘市梁园区",
    },
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 张亚光 — 梁园区委书记
    {"person_id": 1001, "org_id": 1, "title": "梁园区委书记",
     "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 魏宏志 — 梁园区委副书记、区长
    {"person_id": 1002, "org_id": 1, "title": "梁园区委副书记",
     "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 1002, "org_id": 2, "title": "区长",
     "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────────
relationships = [
    {
        "person_a": 1001,
        "person_b": 1002,
        "type": "党政搭档",
        "context": "区委书记—区长搭班工作关系",
        "overlap_org": "梁园区",
        "overlap_period": "2026",
    },
]

# ═════════════════════════════════════════════════════════════════════════════
#  Run
# ═════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    # Use staging paths
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
    print("=" * 50)
    print("Build complete!")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")
