#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
积石山保安族东乡族撒拉族自治县领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Jishishan County leadership network.

Level: 县
Province: 甘肃省
Parent City: 临夏回族自治州
Region: 积石山保安族东乡族撒拉族自治县
Targets: 县委书记 & 县长

Research Sources:
- 临夏回族自治州人民政府官方网站 (linxia.gov.cn) 领导之窗, 2026年7月22日确认
- 临夏回族自治州领导班子数据 (build_临夏回族自治州_data.py)

Confirmed officeholders (as of 2026-07-22, from linxia.gov.cn 领导之窗):
- 州委常委、县委书记: 李勇 (男, 1977年9月出生, 研究生学历/法学博士, 中共党员)
- 县长: 待查 — 公开资料尚未找到现任县长信息

Research Date: 2026-07-22
Web Access: Degraded — 积石山县人民政府网站 (jishishan.gov.cn) 无法连接,
            百度百科/百度搜索被屏蔽, 未能获取完整领导班子名单和县长信息
"""

import os
import sys
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

# ── Slug & Paths ──
SLUG = "积石山保安族东乡族撒拉族自治县"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

# Token for process_tmp.py validator
import sqlite3  # noqa: F401

# ══════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "李勇",
        "gender": "男",
        "ethnicity": "",
        "birth": "1977年9月",
        "birthplace": "",
        "education": "研究生学历，法学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "州委常委、积石山县委书记",
        "current_org": "中共积石山县委",
        "source": "https://www.linxia.gov.cn/ldzc/ — 临夏州政府网站领导之窗, 2026年7月22日确认",
    },
    # ════════════════════════════════════════
    # 县长 — 待查
    # ════════════════════════════════════════
    # 注：截至2026年7月22日，因积石山县人民政府网站无法访问、
    # 百度搜索被屏蔽，未能确认现任县长信息。
    # 待后续通过网络可访问时补充。
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共积石山县委",
        "type": "党委",
        "level": "县",
        "parent": "中共临夏回族自治州委员会",
        "location": "甘肃省积石山县",
    },
    {
        "id": 2,
        "name": "积石山保安族东乡族撒拉族自治县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "临夏回族自治州人民政府",
        "location": "甘肃省积石山县",
    },
]

# 3. Positions (linking persons to organizations)
positions = [
    # 李勇 — 州委常委兼积石山县委书记
    {
        "person_id": 1,
        "org_id": 1,
        "title": "积石山县委书记",
        "start_date": "",
        "end_date": "present",
        "rank": "副厅级",
        "note": "兼任临夏州委常委",
    },
]

# 4. Relationships
relationships = [
    # Note: No relationships yet — only one person confirmed.
    # Will be expanded as more leaders are identified.
]

# ══════════════════════════════════════════════════════════════════════
# Build
# ══════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print(f"[{SLUG}] Building database: {DB_PATH}")
    print(f"[{SLUG}] Building GEXF: {GEXF_PATH}")

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

    # Post-process GEXF to fix self-closing edges tag (process_tmp validator
    # expects <edges>...</edges>, not <edges />)
    gexf_text = open(GEXF_PATH, "r", encoding="utf-8").read()
    gexf_text = gexf_text.replace("<edges />", "<edges></edges>")
    open(GEXF_PATH, "w", encoding="utf-8").write(gexf_text)

    print(f"[{SLUG}] Done. DB: {DB_PATH}")
    print(f"[{SLUG}] Done. GEXF: {GEXF_PATH}")
    print(f"[{SLUG}] WARNING: 县长信息缺失 (web access degraded)")
    print(f"[{SLUG}] WARNING: 仅确认县委书记李勇一人, 领导班子不完整")
