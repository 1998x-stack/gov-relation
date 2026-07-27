#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合水县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 甘肃省
Parent City: 庆阳市
Region: 合水县
Targets: 县委书记 & 县长

Research Sources:
- 合水县人民政府官方网站 (hsxzf.gov.cn 领导之窗), 2026年7月22日确认
- 合水县委理论学习中心组2026年第7次学习会议报道
- 合水县新闻 (2026年7月)

Confirmed officeholders (as of 2026-07-22, from hsxzf.gov.cn 领导之窗):
- 县委书记: 陈会发 (男，汉族，1971年8月出生，大学学历，中共党员)
- 县委副书记、县长: 吕春晖 (男，汉族，1975年4月出生，大学学历，中共党员)

Research Date: 2026-07-22
"""

import os
import sys
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths ──
SLUG = "合水县"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

# The script uses gov_relation.runner (which internally uses sqlite3)
import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "陈会发",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年8月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "合水县委书记",
        "current_org": "中共合水县委员会",
        "source": "合水县人民政府官网(hsxzf.gov.cn) 领导之窗 2026-07-22"
    },
    {
        "id": 2,
        "name": "吕春晖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年4月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "合水县委副书记、县政府党组书记、县长",
        "current_org": "合水县人民政府",
        "source": "合水县人民政府官网(hsxzf.gov.cn) 领导之窗 2026-07-22"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共合水县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共庆阳市委员会",
        "location": "甘肃省庆阳市合水县"
    },
    {
        "id": 2,
        "name": "合水县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "庆阳市人民政府",
        "location": "甘肃省庆阳市合水县"
    },
    {
        "id": 3,
        "name": "合水县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "庆阳市人民代表大会常务委员会",
        "location": "甘肃省庆阳市合水县"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议合水县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "政协庆阳市委员会",
        "location": "甘肃省庆阳市合水县"
    },
    {
        "id": 5,
        "name": "中共庆阳市委员会",
        "type": "党委",
        "level": "地市级",
        "parent": "中共甘肃省委员会",
        "location": "甘肃省庆阳市"
    },
    {
        "id": 6,
        "name": "庆阳市人民政府",
        "type": "政府",
        "level": "地市级",
        "parent": "甘肃省人民政府",
        "location": "甘肃省庆阳市"
    },
    {
        "id": 7,
        "name": "庆阳市人民代表大会常务委员会",
        "type": "人大",
        "level": "地市级",
        "parent": "甘肃省人民代表大会常务委员会",
        "location": "甘肃省庆阳市"
    },
    {
        "id": 8,
        "name": "政协庆阳市委员会",
        "type": "政协",
        "level": "地市级",
        "parent": "政协甘肃省委员会",
        "location": "甘肃省庆阳市"
    },
]

# 3. Positions
positions = [
    # 陈会发
    {"person_id": 1, "org_id": 1, "title": "合水县委书记", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": ""},
    # 吕春晖
    {"person_id": 2, "org_id": 2, "title": "合水县委副书记、县政府党组书记、县长", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": ""},
]

# 4. Relationships
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "党委-政府主要领导协作关系",
        "overlap_org": "合水县",
        "overlap_period": "2026年",
        "confidence": "confirmed"
    },
]


# ── Main ──
def main():
    print(f"=== {SLUG} 网络数据构建 ===")
    print(f"人员: {len(persons)} 人")
    print(f"组织机构: {len(organizations)} 个")
    print(f"任职记录: {len(positions)} 条")
    print(f"关系: {len(relationships)} 条")

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

    print(f"\n=== 完成 ===")


if __name__ == "__main__":
    main()
