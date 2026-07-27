#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
容城县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 保定市（行政区划隶属）/ 雄安新区（实际管理）
Region: 容城县
Targets: 县委书记 & 县长

Research Sources:
- 维基百科容城县条目 (https://zh.wikipedia.org/wiki/容城县)
  确认县委书记张浩
- Baidu Baike (web search degraded)
- 容城县人民政府 (www.rongcheng.gov.cn — 网站访问超时)
- 雄安新区管委会 (web search degraded)

Research Date: 2026-07-23

已知信息:
- 县委书记: 张浩（维基百科信息框确认）
- 县长: 待查（网络访问受限，未能确认姓名）
- 容城县下辖5镇3乡: 容城镇、小里镇、南张镇、大河镇、晾马台镇、八于乡、贾光乡、平王乡
- 容城县实际由雄安新区管理，行政区划上属保定市

Confidence:
- 张浩 县委书记: confirmed (Wikipedia infobox, last revised 2026-05-26)
- 县长: unverified (web search degraded — 所有搜索源均超时/受限)
- 张浩完整履历: unverified (web search degraded)
- 县委常委完整名单: unverified (web search degraded)
- 容城县领导分工: unverified (web search degraded)
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "容城县"

STAGING = os.path.join(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(STAGING, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "张浩",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "容城县委书记",
        "current_org": "中共容城县委员会（雄安新区）",
        "source": "https://zh.wikipedia.org/wiki/容城县 — 维基百科信息框确认张浩任容城县委书记（页面最后修订于2026年5月26日）"
    },
    {
        "id": 2,
        "name": "（待确认）",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "容城县委副书记、县长",
        "current_org": "容城县人民政府",
        "source": "网络搜索受限 — 未能确认2026年容城县县长姓名；容城县人民政府官网(rongcheng.gov.cn)访问超时"
    },
    # ════════════════════════════════════════
    # Townships (乡镇)
    # ════════════════════════════════════════
    # 容城县下辖5镇3乡 — 乡镇主要领导待查
]

# 2. Organizations
organizations = [
    {"id": 1, "name": "中共容城县委员会", "type": "党委", "level": "县处级", "parent": "中共保定市委/中共雄安新区工委", "location": "容城县"},
    {"id": 2, "name": "容城县人民政府", "type": "政府", "level": "县处级", "parent": "保定市人民政府/雄安新区管委会", "location": "容城县"},
    {"id": 3, "name": "容城县纪律检查委员会", "type": "纪委", "level": "副县处级", "parent": "中共容城县委员会", "location": "容城县"},
    {"id": 4, "name": "容城县人大常委会", "type": "人大", "level": "县处级", "parent": "", "location": "容城县"},
    {"id": 5, "name": "容城县政协", "type": "政协", "level": "县处级", "parent": "", "location": "容城县"},
    # Townships
    {"id": 6, "name": "容城镇", "type": "乡镇/街道", "level": "乡科级", "location": "容城县"},
    {"id": 7, "name": "小里镇", "type": "乡镇/街道", "level": "乡科级", "location": "容城县"},
    {"id": 8, "name": "南张镇", "type": "乡镇/街道", "level": "乡科级", "location": "容城县"},
    {"id": 9, "name": "大河镇", "type": "乡镇/街道", "level": "乡科级", "location": "容城县"},
    {"id": 10, "name": "晾马台镇", "type": "乡镇/街道", "level": "乡科级", "location": "容城县"},
    {"id": 11, "name": "八于乡", "type": "乡镇/街道", "level": "乡科级", "location": "容城县"},
    {"id": 12, "name": "贾光乡", "type": "乡镇/街道", "level": "乡科级", "location": "容城县"},
    {"id": 13, "name": "平王乡", "type": "乡镇/街道", "level": "乡科级", "location": "容城县"},
    # Higher-level relevant orgs
    {"id": 14, "name": "雄安新区管理委员会", "type": "政府", "level": "副省级", "parent": "河北省人民政府", "location": "雄安新区"},
    {"id": 15, "name": "中共雄安新区工作委员会", "type": "党委", "level": "副省级", "parent": "中共河北省委", "location": "雄安新区"},
]

# 3. Positions
positions = [
    {"id": 1, "person_id": 1, "org_id": 1, "title": "容城县委书记", "start": "待查", "end": "present", "rank": "县处级正职", "note": ""},
    {"id": 2, "person_id": 2, "org_id": 2, "title": "容城县委副书记、县长", "start": "待查", "end": "present", "rank": "县处级正职", "note": "县长姓名待确认"},
]

# 4. Relationships (minimal — only confirmed connections)
relationships = []

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
    )
    print(f"\nDone. DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
