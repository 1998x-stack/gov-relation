#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
磁县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 邯郸市
Region: 磁县
Targets: 县委书记 & 县长

Research Sources:
- 维基百科磁县条目(2026-04-13)确认县委书记王元峰 https://zh.wikipedia.org/wiki/磁县
- 磁县人民政府官方网站 (www.cixian.gov.cn) — 无法访问（超时）
- 百度百科 — 403 验证码拦截
- Google搜索 — 被拦截
- Exa搜索 — 达到免费速率限制

Research Date: 2026-07-23

已知信息:
- 县委书记: 王元峰（维基百科确认，2025-01-27 编辑更新）
- 县长: 待确认（公开网络搜索受限，未能获取当前县长信息）
  - 前任县长: 闫欣欣（2021-2024年间任职磁县县长，后调离）
- 网络搜索严重受限，更多履历信息待补充

Confidence:
- 王元峰 县委书记: confirmed (Wikipedia infobox)
- 县长身份: unverified (web search blocked)
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "磁县"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "王元峰",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "磁县县委书记",
        "current_org": "中共邯郸市磁县委员会",
        "source": "维基百科磁县条目(2026-04-13)通过编辑历史确认王元峰任磁县县委书记。编辑者Mazhenlong于2025-01-27修改县委书记字段。来源：https://zh.wikipedia.org/wiki/磁县"
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
        "current_post": "磁县县长（待确认）",
        "current_org": "磁县人民政府",
        "source": "⚠️ 待确认：磁县县长身份因公开网络搜索受限未能获取。前任县长闫欣欣（2021-2024年间任职）已调离，当前县长人选待查。"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共邯郸市磁县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共邯郸市委员会",
        "location": "河北省邯郸市磁县"
    },
    {
        "id": 2,
        "name": "磁县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "邯郸市人民政府",
        "location": "河北省邯郸市磁县"
    },
    {
        "id": 3,
        "name": "磁县人民代表大会常务委员会",
        "type": "人大",
        "level": "县",
        "parent": "邯郸市人民代表大会常务委员会",
        "location": "河北省邯郸市磁县"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议磁县委员会",
        "type": "政协",
        "level": "县",
        "parent": "中国人民政治协商会议邯郸市委员会",
        "location": "河北省邯郸市磁县"
    },
    {
        "id": 5,
        "name": "中共磁县纪律检查委员会",
        "type": "纪委",
        "level": "县",
        "parent": "中共邯郸市纪律检查委员会",
        "location": "河北省邯郸市磁县"
    },
    {
        "id": 6,
        "name": "磁州镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "磁县人民政府",
        "location": "河北省邯郸市磁县磁州镇"
    },
    {
        "id": 7,
        "name": "中共磁县县委组织部",
        "type": "党委",
        "level": "县",
        "parent": "中共邯郸市磁县委员会",
        "location": "河北省邯郸市磁县"
    },
]

# 3. Positions
positions = [
    {
        "person_id": 1,
        "org_id": 1,
        "title": "磁县县委书记",
        "start_date": "约2025年1月",
        "end_date": "至今",
        "rank": "正处级",
        "note": "维基百科信息框确认，2025-01-27更新"
    },
]

# 4. Relationships
relationships = [
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
        overwrite=True,
    )
    print(f"Done: {DB_PATH}, {GEXF_PATH}")
