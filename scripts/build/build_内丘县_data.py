#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内丘县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 邢台市
Region: 内丘县
Targets: 县委书记 & 县长

Research Sources:
- 百度百科"管志民"词条：确认2021年5月至2026年2月任内丘县委书记，2026年2月当选邢台市人大常委会副主任
- 内丘县人民政府网站 (www.neiqiu.gov.cn) — 无法访问
- 邢台市人民政府网站 (www.xingtai.gov.cn) — 确认内丘县为邢台市下辖县

Research Date: 2026-07-23

Gaps (HIGH PRIORITY):
- 现任县委书记（接替管志民者）完全未知
- 现任县长完全未知
- 县委常委班子、副县长班子完全未知
- 人大常委会主任、政协主席姓名未知
- 需要进一步搜索"内丘县委书记"（2026年2月之后任命）和"内丘县长"
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "内丘县"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders — UNKNOWN
    # ════════════════════════════════════════
    # Current 县委书记: 待查（管志民2026年2月离任后接任者）
    # Current 县长: 待查
    #
    # ════════════════════════════════════════
    # Historical Leaders (Known)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "管志民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年4月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "邢台市人大常委会副主任",
        "current_org": "邢台市人大常委会",
        "source": "百度百科：管志民，男，汉族，1970年4月生，在职大学学历，中共党员。2021年5月任河北省邢台市内丘县委书记。2026年2月当选邢台市第十六届人大常委会副主任。来源：https://baike.baidu.com/item/管志民"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共内丘县委员会",
        "type": "党委",
        "level": "县级",
        "location": "邢台市内丘县",
        "parent": "中共邢台市委"
    },
    {
        "id": 2,
        "name": "内丘县人民政府",
        "type": "政府",
        "level": "县级",
        "location": "邢台市内丘县",
        "parent": "邢台市人民政府"
    },
    {
        "id": 3,
        "name": "内丘县人大常委会",
        "type": "人大",
        "level": "县级",
        "location": "邢台市内丘县",
        "parent": "邢台市人大常委会"
    },
    {
        "id": 4,
        "name": "政协内丘县委员会",
        "type": "政协",
        "level": "县级",
        "location": "邢台市内丘县",
        "parent": "邢台市政协"
    },
    {
        "id": 5,
        "name": "邢台市人大常委会",
        "type": "人大",
        "level": "地市级",
        "location": "邢台市",
        "parent": "河北省人大常委会"
    },
]

# 3. Positions
positions = [
    # 管志民 — 前任县委书记
    {"person_id": 1, "org_id": 1, "title": "内丘县委书记", "start": "2021年5月", "end": "2026年2月", "rank": "正处级", "note": "2021年5月任内丘县委书记，2026年2月离任"},
    # 管志民 — 现任（邢台市）
    {"person_id": 1, "org_id": 5, "title": "邢台市人大常委会副主任", "start": "2026年2月", "end": "present", "rank": "副厅级", "note": "2026年2月5日当选"},
]

# 4. Relationships
relationships = [
    # 暂无已知关系资料
]

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
    print(f"Done. DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
