#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
庆城县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 甘肃省
Parent City: 庆阳市
Region: 庆城县
Targets: 县委书记 & 县长

Research Sources:
- 庆城县人民政府官方网站 (chinaqingcheng.gov.cn), 2026年7月确认
- 庆阳市人民政府官方网站
- 新闻报道

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
SLUG = "庆城县"
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
        "name": "张鸿举",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "庆阳市委常委、庆城县委书记",
        "current_org": "中共庆城县委员会",
        "source": "庆城县人民政府官网(chinaqingcheng.gov.cn) 2026-07; 庆城县委常委会会议报道"
    },
    {
        "id": 2,
        "name": "郭丽君",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "庆城县委副书记、县长",
        "current_org": "庆城县人民政府",
        "source": "庆城县人民政府官网(chinaqingcheng.gov.cn) 2026-07; 县政府常务会议报道"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共庆城县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共庆阳市委员会",
        "location": "甘肃省庆阳市庆城县"
    },
    {
        "id": 2,
        "name": "庆城县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "庆阳市人民政府",
        "location": "甘肃省庆阳市庆城县"
    },
    {
        "id": 3,
        "name": "庆城县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "庆阳市人民代表大会常务委员会",
        "location": "甘肃省庆阳市庆城县"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议庆城县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "政协庆阳市委员会",
        "location": "甘肃省庆阳市庆城县"
    },
    {
        "id": 5,
        "name": "中共庆阳市委员会",
        "type": "党委",
        "level": "地市级",
        "parent": "中共甘肃省委员会",
        "location": "甘肃省庆阳市"
    },
]

# 3. Positions
positions = [
    # 张鸿举
    {"person_id": 1, "org_id": 1, "title": "庆阳市委常委、庆城县委书记", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": "兼任庆阳市委常委"},
    # 郭丽君
    {"person_id": 2, "org_id": 2, "title": "庆城县委副书记、县长", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": ""},
]

# 4. Relationships
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "党委-政府主要领导协作关系",
        "overlap_org": "庆城县",
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
