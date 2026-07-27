#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 广元市旺苍县 leadership network.

调查日期: 2026-07-26
信息来源: 公开媒体报道、有限 web 搜索 — 中方县县政府网站 (wangcang.gov.cn) DNS 无法解析，
          广元市市政府 (cngy.gov.cn) 返回 412/SPA 无法爬取。
          本版本保留核心已知事实，标注不确定性。
调查级别: 县
"""

import sqlite3  # noqa: used by gov_relation.runner via schema

import json
import os
import sys
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
sys.path.insert(0, REPO_ROOT)

STAGING_DIR = BASE
DB_PATH = os.path.join(STAGING_DIR, "旺苍县_network.db")  # noqa
GEXF_PATH = os.path.join(STAGING_DIR, "旺苍县_network.gexf")  # noqa
PERSONS_DIR = STAGING_DIR

TODAY = datetime.now().strftime("%Y%m%d")
SLUG = "四川省广元市旺苍县"

# ═══════════════════════════════════════════════════════════════════
# RESEARCH SUMMARY
# ═══════════════════════════════════════════════════════════════════
#
# 旺苍县位于四川省广元市东北部，川陕交界处。
# 广元市下辖：利州区、昭化区、朝天区、剑阁县、苍溪县、旺苍县、青川县。
#
# 已知主要领导序列（来自零散新闻报道）：
#
# 县委书记序列：
#   杨永昌 (约2016前)
#  → 唐涛/唐文辉 (约2016-2023，从县长升任，公开来源中"唐涛"与"唐文辉"可能是同一人，也可能是混淆)
#  → 待确认 (约2023至今 — 已换任但现任姓名未能通过当前 web 访问确认)
#
# 县长序列：
#   余飞吉 (约2016前)
#  → 唐涛 (约2016-2019，后升任县委书记)
#  → 待确认 (2019至今 — 唐文辉由县长调任县委后，继任县长未确认)
#
# ⚠ 由于 Exa rate-limit + 政府站 DNS/SPA 无法访问，
#   核心领导人的最新姓名、出生、籍贯、教育、履职时间均未确认。
#   下属编委、副县长、党常委名录也未找到。
#
# ═══════════════════════════════════════════════════════════════════

# ── PERSONS ────────────────────────────────────────────────────────
persons = [
    # ═══════════════════════════════
    # 县委领导 (County Party Committee)
    # ═══════════════════════════════

    # 县委书记 — 待确认（2023年后可能已换任）
    {
        "id": 1,
        "name": "待确认",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共旺苍县委书记",
        "current_org": "中共旺苍县委员会",
        "source": "官方来源待补充 — web访问受限无法确认现任县委书记姓名",
    },
    # 县长 — 待确认
    {
        "id": 2,
        "name": "待确认",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "旺苍县人民政府县长",
        "current_org": "旺苍县人民政府",
        "source": "官方来源待补充 — web访问受限无法确认现任县长姓名",
    },

    # ═══════════════════════════════
    # 已知前任干部 (来自公开媒体报道，部分信息可能混淆)
    # ═══════════════════════════════

    # 唐涛/唐文辉 — 前任县委书记／县长
    {
        "id": 3,
        "name": "唐涛（或唐文辉）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（疑似已调离）",
        "current_org": "",
        "source": "公开媒体报道提及 — 需确认当前任职；唐涛与唐文辉可能为同一人",
    },
    # 杨永昌 — 前任县委书记
    {
        "id": 4,
        "name": "杨永昌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "公开媒体报道 — 约2016-2019任旺苍县委书记，调离方向待查",
    },
    # 余飞吉 — 前任县长
    {
        "id": 5,
        "name": "余飞吉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "公开媒体报道 — 约2016前曾任旺苍县长，调离/退休待查",
    },
    # 唐涛（单独作为一人，如果与唐文辉为同一人则去重）
    # 已有id=3覆盖，不再重复，备注中说明混淆点
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共旺苍县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共广元市委",
        "location": "四川省广元市旺苍县",
    },
    {
        "id": 2,
        "name": "旺苍县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "广元市人民政府",
        "location": "四川省广元市旺苍县",
    },
    {
        "id": 3,
        "name": "中共广元市委",
        "type": "党委",
        "level": "地厅级",
        "parent": "中共四川省委",
        "location": "四川省广元市",
    },
    {
        "id": 4,
        "name": "广元市人民政府",
        "type": "政府",
        "level": "地厅级",
        "parent": "四川省人民政府",
        "location": "四川省广元市",
    },
]

# ── POSITIONS ──────────────────────────────────────────────────────
positions = [
    # 现任
    {"person_id": 1, "org_id": 1, "title": "县委书记",
     "start_date": "", "end_date": "present",
     "rank": "县处级正职", "note": "待确认 — 2023年后可能已换任"},
    {"person_id": 2, "org_id": 2, "title": "县长",
     "start_date": "", "end_date": "present",
     "rank": "县处级正职", "note": "待确认 — 唐文辉升任县委书记后继任县长未确认"},

    # 前任县委书记/县长
    {"person_id": 3, "org_id": 1, "title": "县委书记（前任）",
     "start_date": "约2019", "end_date": "约2023",
     "rank": "县处级正职", "note": "唐涛/唐文辉，约2019-2023任县委书记，此前曾任旺苍县长"},
    {"person_id": 3, "org_id": 2, "title": "县长（前任）",
     "start_date": "约2016", "end_date": "约2019",
     "rank": "县处级正职", "note": "唐涛，从县长升任县委书记"},

    # 杨永昌
    {"person_id": 4, "org_id": 1, "title": "县委书记（前任）",
     "start_date": "约2016", "end_date": "约2019",
     "rank": "县处级正职", "note": "杨永昌，约2016-2019任旺苍县委书记"},

    # 余飞吉
    {"person_id": 5, "org_id": 2, "title": "县长（前任）",
     "start_date": "", "end_date": "约2016",
     "rank": "县处级正职", "note": "余飞吉，约2016年前任旺苍县长"},
]

# ── RELATIONSHIPS ─────────────────────────────────────────────────
relationships = [
    # 唐涛→现任继任
    {"person_a": 3, "person_b": 1,
     "type": "前任继任",
     "context": "唐涛→现任县委书记（待确认）",
     "overlap_org": "中共旺苍县委员会",
     "overlap_period": "约2023交接"},
    # 杨永昌→唐涛
    {"person_a": 4, "person_b": 3,
     "type": "前任继任",
     "context": "杨永昌→唐涛 旺苍县委书记交接",
     "overlap_org": "中共旺苍县委员会",
     "overlap_period": "约2019交接"},
    # 余飞吉→唐涛（县长交接）
    {"person_a": 5, "person_b": 3,
     "type": "前任继任",
     "context": "余飞吉→唐涛旺苍县长交接",
     "overlap_org": "旺苍县人民政府",
     "overlap_period": "约2016交接"},
    # 唐涛升任县委书记（同一人同时任县长后升书记）
    {"person_a": 3, "person_b": 1,
     "type": "上下级",
     "context": "唐涛从县长升任县委书记—与现任书记为前任继任关系",
     "overlap_org": "中共旺苍县委员会",
     "overlap_period": ""},
]

# ── MAIN ───────────────────────────────────────────────────────────
def main():
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

    print(f"\n✅ Done: {DB_PATH}")
    print(f"✅ Done: {GEXF_PATH}")
    print(f"  - Persons: {len(persons)}")
    print(f"  - Organizations: {len(organizations)}")
    print(f"  - Positions: {len(positions)}")
    print(f"  - Relationships: {len(relationships)}")
    print("⚠ 注意: 大量字段为待确认状态，因 web 访问受限（Exa rate-limit、政府站 412/超时）")
    print("  待 web 恢复后需补充：")
    print("    - 现任县委书记姓名、履历、籍贯、教育")
    print("    - 现任县长姓名、履历、籍贯、教育")
    print("    - 所有县委常委、副县长、部门负责人的完整名录")
    print("    - 广元市委组织部任前公示详细出处")
    print("    - 唐涛/唐文辉的人员去重（同一人还是两人）")

if __name__ == "__main__":
    main()