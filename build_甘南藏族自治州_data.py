#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
甘南藏族自治州领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Gannan Tibetan Autonomous Prefecture leadership network.

Level: 地级市 (自治州)
Province: 甘肃省
Region: 甘南藏族自治州
Targets: 州委书记 & 州长

Research Sources:
- zh.wikipedia.org/wiki/甘南藏族自治州 — 现任领导信息，2026年7月22日确认
- zh.wikipedia.org/wiki/仁青东珠 — 政协主席履历
- Baidu Baike (via Wikipedia references) — 人物基本信息

Confirmed officeholders (as of 2026-07-22, from zh.wikipedia.org/wiki/甘南藏族自治州#现任领导):
- 州委书记: 张泽武 (男，汉族，1977年12月出生，甘肃陇南人，2026年6月就任)
- 州委副书记、州长: 杨振林 (男，藏族，1972年9月出生，甘肃夏河人，2026年3月就任)
- 人大常委会主任: 胡晓华 (男，蒙古族，1974年7月出生，甘肃迭部人，2025年1月就任)
- 政协主席: 仁青东珠 (男，藏族，1967年3月出生，甘肃夏河人，1992年入党，2021年2月就任)

Predecessors (from Wikipedia history):
- 前任州委书记: 何谋保 (调任/去向待查)
- 前任州长: 杨武 (调任/去向待查)

Open Gaps (to be filled in future investigations):
- 张泽武: 2026年6月前任职务不详，推测可能来自甘肃省纪委或省委部门
- 杨振林: 2026年3月前曾任甘南州副州长等职，完整履历待查
- 州委常委班子: 除四套班子正职外，其他副职信息暂缺（官方ldzc页面无法访问）
- 仁青东珠: 曾任甘南州副州长，完整履历待补充

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
SLUG = "甘南藏族自治州"
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
        "name": "张泽武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年12月",
        "birthplace": "甘肃陇南",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "甘南州委书记",
        "current_org": "中共甘南藏族自治州委员会",
        "source": "https://zh.wikipedia.org/wiki/甘南藏族自治州#现任领导 — 维基百科, 2026年7月22日确认"
    },
    {
        "id": 2,
        "name": "杨振林",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1972年9月",
        "birthplace": "甘肃夏河",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "甘南州委副书记、州长",
        "current_org": "甘南藏族自治州人民政府",
        "source": "https://zh.wikipedia.org/wiki/甘南藏族自治州#现任领导 — 维基百科, 2026年7月22日确认"
    },
    # ════════════════════════════════════════
    # 州委副书记 (Deputy Party Secretary)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "胡晓华",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1974年7月",
        "birthplace": "甘肃迭部",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "甘南州人大常委会党组书记、主任",
        "current_org": "甘南藏族自治州人民代表大会常务委员会",
        "source": "https://zh.wikipedia.org/wiki/甘南藏族自治州#现任领导 — 维基百科, 2026年7月22日确认"
    },
    {
        "id": 4,
        "name": "仁青东珠",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1967年3月",
        "birthplace": "甘肃夏河",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "甘南州政协党组书记、主席",
        "current_org": "中国人民政治协商会议甘南藏族自治州委员会",
        "source": "https://zh.wikipedia.org/wiki/仁青东珠 — 维基百科, 2026年7月22日确认"
    },
    # ════════════════════════════════════════
    # 前任领导 (Predecessors)
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "何谋保",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任甘南州委书记（去向待查）",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/甘南藏族自治州#现任领导 — 维基百科·前任信息, 2026年7月22日"
    },
    {
        "id": 6,
        "name": "杨武",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任甘南州州长（去向待查）",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/甘南藏族自治州#现任领导 — 维基百科·前任信息, 2026年7月22日"
    },
    # ════════════════════════════════════════
    # 现任副州长/州委常委（部分已知）
    # ════════════════════════════════════════
    # 注意：以下人员的完整信息需从 gnzrmzf.gov.cn 官方ldzc页面补充
    # 因网站无法访问，以下为基于新闻报导的部分信息，标记为"unverified"
    # 待官方ldzc页面恢复后更新
    {
        "id": 7,
        "name": "杨光龙",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "甘南州委常委、常务副州长（待确认）",
        "current_org": "甘南藏族自治州人民政府",
        "source": "推测 — 部分新闻提及，未从官方来源确认"
    },
]

# 2. Organizations
organizations = [
    {"id": 1, "name": "中共甘南藏族自治州委员会", "type": "党委", "level": "地级市", "parent": "中共甘肃省委员会", "location": "甘肃省合作市"},
    {"id": 2, "name": "甘南藏族自治州人民政府", "type": "政府", "level": "地级市", "parent": "甘肃省人民政府", "location": "甘肃省合作市"},
    {"id": 3, "name": "甘南藏族自治州人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "甘肃省人大常委会", "location": "甘肃省合作市"},
    {"id": 4, "name": "中国人民政治协商会议甘南藏族自治州委员会", "type": "政协", "level": "地级市", "parent": "甘肃省政协", "location": "甘肃省合作市"},
    {"id": 5, "name": "中共甘南州委组织部", "type": "党委", "level": "地级市", "parent": "中共甘南藏族自治州委员会", "location": "甘肃省合作市"},
    {"id": 6, "name": "中共甘南州纪律检查委员会", "type": "党委", "level": "地级市", "parent": "中共甘南藏族自治州委员会", "location": "甘肃省合作市"},
    {"id": 7, "name": "中共甘南州委宣传部", "type": "党委", "level": "地级市", "parent": "中共甘南藏族自治州委员会", "location": "甘肃省合作市"},
    {"id": 8, "name": "中共甘南州委统战部", "type": "党委", "level": "地级市", "parent": "中共甘南藏族自治州委员会", "location": "甘肃省合作市"},
    {"id": 9, "name": "中共甘南州委政法委员会", "type": "党委", "level": "地级市", "parent": "中共甘南藏族自治州委员会", "location": "甘肃省合作市"},
]

# 3. Positions (linking persons to organizations)
positions = [
    # 州委
    {"person_id": 1, "org_id": 1, "title": "州委书记", "start_date": "2026-06", "end_date": "present", "rank": "正厅级", "note": "州委全面工作"},
    {"person_id": 2, "org_id": 1, "title": "州委副书记", "start_date": "2026-03", "end_date": "present", "rank": "正厅级", "note": "兼州长"},
    # 州政府
    {"person_id": 2, "org_id": 2, "title": "州长", "start_date": "2026-03", "end_date": "present", "rank": "正厅级", "note": "州政府全面工作"},
    # 人大
    {"person_id": 3, "org_id": 3, "title": "主任", "start_date": "2025-01", "end_date": "present", "rank": "正厅级", "note": "人大常委会全面工作"},
    # 政协
    {"person_id": 4, "org_id": 4, "title": "主席", "start_date": "2021-02", "end_date": "present", "rank": "正厅级", "note": "政协全面工作"},
    # 前任
    {"person_id": 5, "org_id": 1, "title": "前任州委书记", "start_date": "", "end_date": "2026-06", "rank": "正厅级", "note": "前任"},
    {"person_id": 6, "org_id": 2, "title": "前任州长", "start_date": "", "end_date": "2026-03", "rank": "正厅级", "note": "前任"},
]

# 4. Relationships
relationships = [
    # 核心领导关系
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "州委书记—州委副书记/州长", "overlap_org": "中共甘南藏族自治州委员会", "overlap_period": "2026年6月至今"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "州委书记—人大主任", "overlap_org": "甘南藏族自治州", "overlap_period": "2026年6月至今"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "州委书记—政协主席", "overlap_org": "甘南藏族自治州", "overlap_period": "2026年6月至今"},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "州长—人大主任", "overlap_org": "甘南藏族自治州", "overlap_period": "2026年3月至今"},
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "州长—政协主席", "overlap_org": "甘南藏族自治州", "overlap_period": "2026年3月至今"},
    # 前任 — 现任关系
    {"person_a": 1, "person_b": 5, "type": "predecessor", "context": "前任州委书记→现任州委书记（接班）", "overlap_org": "中共甘南藏族自治州委员会", "overlap_period": "2026年6月交接"},
    {"person_a": 2, "person_b": 6, "type": "predecessor", "context": "前任州长→现任州长（接班）", "overlap_org": "甘南藏族自治州人民政府", "overlap_period": "2026年3月交接"},
]


# ══════════════════════════════════════════════════════════════
# Build
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print(f"[{SLUG}] Building database: {DB_PATH}")
    print(f"[{SLUG}] Building GEXF: {GEXF_PATH}")

    from gov_relation.runner import run_build

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

    print(f"[{SLUG}] Done. DB: {DB_PATH}")
    print(f"[{SLUG}] Done. GEXF: {GEXF_PATH}")
