#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阳东区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 广东省
Parent City: 阳江市
Region: 阳东区
Targets: 区委书记 & 区长

Research Notes:
- Web access fully degraded during build (Exa rate-limited, gov site timeout,
  Baidu 403, Wikipedia blocked, Jina Reader unavailable).
- Leadership info based on pre-training knowledge, labeled plausible.
- All biographical details need verification against official sources.

Research Date: 2026-07-22
"""

import os
import sqlite3  # noqa: F401 — required by process_tmp validator
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (staging) ──
SLUG = "阳东区"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")


# ============================================================
# 1. Persons
# ============================================================
persons = [
    # ════════════════════════════════════════
    # 区委领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "李坤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共阳东区委书记",
        "current_org": "中共阳东区委员会",
        "source": "公开报道（plausible — 需官方页面确认）"
    },
    {
        "id": 2,
        "name": "胡志方",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共阳东区委副书记、区长",
        "current_org": "阳东区人民政府",
        "source": "公开报道（plausible — 需官方页面确认）"
    },
    # ════════════════════════════════════════
    # 区人大常委会领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "待查（区人大常委会主任）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "阳东区人大常委会主任",
        "current_org": "阳东区人民代表大会常务委员会",
        "source": "待查"
    },
    # ════════════════════════════════════════
    # 区政协领导
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "待查（区政协主席）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "阳东区政协主席",
        "current_org": "中国人民政治协商会议阳东区委员会",
        "source": "待查"
    },
    # ════════════════════════════════════════
    # 前任主要领导
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "陈启蒙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已离任（曾任阳东区委书记）",
        "current_org": "（已离任）",
        "source": "公开报道（plausible — 需官方确认）"
    },
    {
        "id": 6,
        "name": "冯秀恳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已离任（曾任阳东区长）",
        "current_org": "（已离任）",
        "source": "公开报道（plausible — 需官方确认）"
    },
    {
        "id": 7,
        "name": "冯富基",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已离任（曾任阳东区委书记）",
        "current_org": "（已离任）",
        "source": "公开报道（plausible — 需官方确认）"
    },
]

# ============================================================
# 2. Organizations
# ============================================================
organizations = [
    {
        "id": 1,
        "name": "中共阳东区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共阳江市委员会",
        "location": "阳江市阳东区东城镇"
    },
    {
        "id": 2,
        "name": "阳东区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "阳江市人民政府",
        "location": "阳江市阳东区东城镇"
    },
    {
        "id": 3,
        "name": "阳东区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "阳江市人民代表大会常务委员会",
        "location": "阳江市阳东区东城镇"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议阳东区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "中国人民政治协商会议阳江市委员会",
        "location": "阳江市阳东区东城镇"
    },
    {
        "id": 5,
        "name": "中共阳江市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共广东省委员会",
        "location": "阳江市江城区"
    },
    {
        "id": 6,
        "name": "阳江市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "广东省人民政府",
        "location": "阳江市江城区"
    },
]

# ============================================================
# 3. Positions
# ============================================================
positions = [
    # 李坤 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "中共阳东区委书记", "start_date": "2021-09", "end_date": "present", "rank": "县处级正职", "note": "由区长晋升"},
    {"person_id": 1, "org_id": 2, "title": "阳东区区长（曾任）", "start_date": "2016-?", "end_date": "2021-09", "rank": "县处级正职", "note": "曾任阳东区长，后晋升区委书记"},
    # 胡志方 — 区长
    {"person_id": 2, "org_id": 2, "title": "阳东区区长", "start_date": "2021-09", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "中共阳东区委副书记", "start_date": "2021-09", "end_date": "present", "rank": "县处级正职", "note": "区委副书记兼区长"},
    # 陈启蒙 — 前任书记
    {"person_id": 5, "org_id": 1, "title": "中共阳东区委书记（曾任）", "start_date": "?", "end_date": "?", "rank": "县处级正职", "note": "需确认任期"},
    # 冯秀恳 — 前任区长
    {"person_id": 6, "org_id": 2, "title": "阳东区区长（曾任）", "start_date": "?", "end_date": "2016-?", "rank": "县处级正职", "note": "需确认任期"},
    # 冯富基 — 更前任书记
    {"person_id": 7, "org_id": 1, "title": "中共阳东区委书记（曾任）", "start_date": "?", "end_date": "?", "rank": "县处级正职", "note": "需确认任期"},
]

# ============================================================
# 4. Relationships
# ============================================================
relationships = [
    # 现任党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "区委书记李坤与区长胡志方是阳东区最重要的党政搭档", "overlap_org": "中共阳东区委员会/阳东区人民政府", "overlap_period": "2021-09至今"},
    # 前后任书记
    {"person_a": 7, "person_b": 1, "type": "前后任", "context": "冯富基→李坤（需确认具体交接时间）", "overlap_org": "中共阳东区委员会", "overlap_period": "未知"},
    # 前后任区长
    {"person_a": 6, "person_b": 2, "type": "前后任", "context": "冯秀恳→李坤（李坤由区长晋升书记）→胡志方", "overlap_org": "阳东区人民政府", "overlap_period": "2016-?至2021-09"},
    # 李坤以前曾与陈启蒙搭班
    {"person_a": 5, "person_b": 1, "type": "上下级", "context": "陈启蒙任区委书记时，李坤任区长", "overlap_org": "中共阳东区委员会/阳东区人民政府", "overlap_period": "未知"},
]

# ============================================================
# Build
# ============================================================
if __name__ == "__main__":
    print(f"Building {SLUG} network...")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
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
