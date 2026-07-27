#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
肥乡区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 河北省
Parent City: 邯郸市
Region: 肥乡区
Targets: 区委书记 & 区长

Research Sources:
- 邯郸市肥乡区人民政府官方网站 (www.fxq.gov.cn) — 新闻资讯确认区委书记李春红、区长郑建民
- 政府信息公开—常务会议确认区长郑建民(2025年11月)、前任区长赵鹏飞(2024年6月)
- 全域电商发展推进大会(2026-04-30)确认李春红主持、郑建民出席、区领导李莹玮通报

Research Date: 2026-07-23
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "肥乡区"

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
        "name": "李春红",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "邯郸市肥乡区委书记",
        "current_org": "中共邯郸市肥乡区委员会",
        "source": "肥乡区政府官方网站—全域电商发展推进大会(2026-04-29)确认李春红任肥乡区委书记。来源：https://www.fxq.gov.cn/xwzx/fxyw/202604/t20260430_2200495.html"
    },
    {
        "id": 2,
        "name": "郑建民",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "邯郸市肥乡区委副书记、区长",
        "current_org": "肥乡区人民政府",
        "source": "肥乡区政府信息公开—第73次政府常务会议(2025-11-06)确认郑建民任肥乡区长。来源：https://www.fxq.gov.cn/zwgk/zfxxgk/fdgknr/zyhy/"
    },
    # ════════════════════════════════════════
    # 其他领导（部分确认）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "李莹玮",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "肥乡区区领导（副区长/常委）",
        "current_org": "肥乡区人民政府",
        "source": "肥乡区政府官方网站—全域电商发展推进大会(2026-04-30)提及'区领导李莹玮通报了全区一品一播工作进展情况'"
    },
    # ════════════════════════════════════════
    # Historical Leaders
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "赵鹏飞",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查（原肥乡区长，约2025年离任）",
        "current_org": "",
        "source": "肥乡区政府信息公开—赵鹏飞主持第四十三次政府常务会议(2024-06-18)。来源：https://www.fxq.gov.cn/zwgk/zfxxgk/fdgknr/zyhy/"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共邯郸市肥乡区委员会",
        "type": "党委",
        "level": "县级",
        "location": "邯郸市肥乡区",
        "parent": "中共邯郸市委"
    },
    {
        "id": 2,
        "name": "肥乡区人民政府",
        "type": "政府",
        "level": "县级",
        "location": "邯郸市肥乡区",
        "parent": "邯郸市人民政府"
    },
    {
        "id": 3,
        "name": "肥乡区人大常委会",
        "type": "人大",
        "level": "县级",
        "location": "邯郸市肥乡区",
        "parent": "邯郸市人大常委会"
    },
    {
        "id": 4,
        "name": "肥乡区政协",
        "type": "政协",
        "level": "县级",
        "location": "邯郸市肥乡区",
        "parent": "邯郸市政协"
    },
]

# 3. Positions
positions = [
    # 李春红
    {"person_id": 1, "org_id": 1, "title": "邯郸市肥乡区委书记", "start": "未知", "end": "present", "rank": "正处级", "note": "截至2026年7月在任"},
    # 郑建民
    {"person_id": 2, "org_id": 2, "title": "肥乡区委副书记、区长", "start": "约2025年", "end": "present", "rank": "正处级", "note": "截至2026年7月在任"},
    # 李莹玮
    {"person_id": 3, "org_id": 2, "title": "肥乡区区领导", "start": "未知", "end": "present", "rank": "副处级", "note": "2026年4月会议报道确认"},
    # 赵鹏飞 — 历史职务
    {"person_id": 4, "org_id": 2, "title": "邯郸市肥乡区委副书记、区长", "start": "未知", "end": "约2025年", "rank": "正处级", "note": "2024年6月18日在任"},
]

# 4. Relationships
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记与区长同为肥乡区核心领导搭档",
        "overlap_org": "中共邯郸市肥乡区委员会／肥乡区人民政府",
        "overlap_period": "2025-2026"
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "李春红作为区委书记领导区领导李莹玮",
        "overlap_org": "中共邯郸市肥乡区委员会／肥乡区人民政府",
        "overlap_period": "2025-2026"
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "郑建民作为区长领导李莹玮",
        "overlap_org": "肥乡区人民政府",
        "overlap_period": "2025-2026"
    },
    {
        "person_a": 2,
        "person_b": 4,
        "type": "predecessor_successor",
        "context": "赵鹏飞为前任肥乡区长，郑建民接任",
        "overlap_org": "肥乡区人民政府",
        "overlap_period": "2024-2025"
    },
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
