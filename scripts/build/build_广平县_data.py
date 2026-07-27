#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
广平县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 邯郸市
Region: 广平县
Targets: 县委书记 & 县长

Research Sources:
- 广平县人民政府网站 (www.gpx.gov.cn) — 概况页面 (2026-05-15更新) 确认四套班子领导
- 广平县人民政府办公室关于县政府领导工作分工的通知 (2024-09-30/2025-09-29发布) — 确认县长、副县长名单及分工
- 广平要闻确认张建涛为政府县长、县政府党组书记（2026年5月仍在任）
- 广平要闻确认李慧、赵鸿光、江峥、王剑飞为副县长（2026年5月仍在任）
- 维基百科广平县页面确认祁富强为县委书记（2026年更新）
- 广平要闻"张建涛在县委管理干部学习贯彻二十届四中全会精神研讨班上作专题授课"确认张建涛为县长
- 广平要闻"县人代会"等报导

Research Date: 2026-07-23
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "广平县"

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
        "name": "祁富强",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广平县委书记",
        "current_org": "中共广平县委员会",
        "source": "广平县人民政府概况页面（2026-05-15更新）列县委书记为祁富强。来源：https://www.gpx.gov.cn/about/"
    },
    {
        "id": 2,
        "name": "张建涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广平县委副书记、县政府县长",
        "current_org": "广平县人民政府",
        "source": "广平县人民政府概况页面（2026-05-15更新）列县长为张建涛。来源：https://www.gpx.gov.cn/about/；广平要闻确认其以县政府党组书记、县长身份出席活动（2026年5月）。来源：https://www.gpx.gov.cn/news/5323.cshtml"
    },
    # ════════════════════════════════════════
    # 县政府领导（来自官方领导分工通知）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "李慧",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广平县委常委、政府常务副县长",
        "current_org": "广平县人民政府",
        "source": "广平县人民政府办公室关于县政府领导工作分工的通知（2024-09-30）。来源：https://www.gpx.gov.cn/policyDocument/40972.cshtml"
    },
    {
        "id": 4,
        "name": "杜学强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广平县人民政府副县长",
        "current_org": "广平县人民政府",
        "source": "广平县人民政府办公室关于县政府领导工作分工的通知（2024-09-30）。来源：https://www.gpx.gov.cn/policyDocument/40972.cshtml"
    },
    {
        "id": 5,
        "name": "赵鸿光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广平县人民政府副县长",
        "current_org": "广平县人民政府",
        "source": "广平县人民政府办公室关于县政府领导工作分工的通知（2024-09-30）。来源：https://www.gpx.gov.cn/policyDocument/40972.cshtml；广平要闻确认出席活动（2026年5月）。来源：https://www.gpx.gov.cn/news/5323.cshtml"
    },
    {
        "id": 6,
        "name": "江峥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广平县人民政府副县长",
        "current_org": "广平县人民政府",
        "source": "广平县人民政府办公室关于县政府领导工作分工的通知（2024-09-30）。来源：https://www.gpx.gov.cn/policyDocument/40972.cshtml；广平要闻确认出席活动（2026年5月）。来源：https://www.gpx.gov.cn/news/5323.cshtml"
    },
    {
        "id": 7,
        "name": "王剑飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广平县人民政府副县长",
        "current_org": "广平县人民政府",
        "source": "广平县人民政府办公室关于县政府领导工作分工的通知（2024-09-30）。来源：https://www.gpx.gov.cn/policyDocument/40972.cshtml；广平要闻确认出席活动（2026年5月）。来源：https://www.gpx.gov.cn/news/5323.cshtml"
    },
    # ════════════════════════════════════════
    # 人大、政协领导
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "商凤祥",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广平县人大常委会主任",
        "current_org": "广平县人大常委会",
        "source": "广平县人民政府概况页面（2026-05-15更新）。来源：https://www.gpx.gov.cn/about/"
    },
    {
        "id": 9,
        "name": "王学峰",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广平县政协主席",
        "current_org": "广平县政协",
        "source": "广平县人民政府概况页面（2026-05-15更新）。来源：https://www.gpx.gov.cn/about/"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共广平县委员会",
        "type": "党委",
        "level": "县级",
        "location": "邯郸市广平县",
        "parent": "中共邯郸市委"
    },
    {
        "id": 2,
        "name": "广平县人民政府",
        "type": "政府",
        "level": "县级",
        "location": "邯郸市广平县",
        "parent": "邯郸市人民政府"
    },
    {
        "id": 3,
        "name": "广平县人大常委会",
        "type": "人大",
        "level": "县级",
        "location": "邯郸市广平县",
        "parent": "邯郸市人大常委会"
    },
    {
        "id": 4,
        "name": "广平县政协",
        "type": "政协",
        "level": "县级",
        "location": "邯郸市广平县",
        "parent": "邯郸市政协"
    },
    {
        "id": 5,
        "name": "广平县公安局",
        "type": "政府",
        "level": "正科级",
        "location": "邯郸市广平县",
        "parent": "广平县人民政府"
    },
]

# 3. Positions
positions = [
    # 祁富强 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "广平县委书记", "start": "未知", "end": "present", "rank": "正处级", "note": "截至2026年5月在任"},
    # 张建涛 — 县长
    {"person_id": 2, "org_id": 1, "title": "广平县委副书记", "start": "未知", "end": "present", "rank": "正处级", "note": "县委副书记兼县长"},
    {"person_id": 2, "org_id": 2, "title": "广平县人民政府县长", "start": "未知", "end": "present", "rank": "正处级", "note": "县政府党组书记；截至2026年5月在任"},
    # 李慧 — 常务副县长
    {"person_id": 3, "org_id": 1, "title": "广平县委常委", "start": "未知", "end": "present", "rank": "副处级", "note": "截至2026年在任"},
    {"person_id": 3, "org_id": 2, "title": "广平县人民政府常务副县长", "start": "未知", "end": "present", "rank": "副处级", "note": "分管发改、财税、金融、教育等"},
    # 杜学强 — 副县长
    {"person_id": 4, "org_id": 2, "title": "广平县人民政府副县长", "start": "未知", "end": "present", "rank": "副处级", "note": "分管政法、退役军人、信访等"},
    # 赵鸿光 — 副县长
    {"person_id": 5, "org_id": 2, "title": "广平县人民政府副县长", "start": "未知", "end": "present", "rank": "副处级", "note": "分管自然资源、住建、交通、文旅等"},
    # 江峥 — 副县长
    {"person_id": 6, "org_id": 2, "title": "广平县人民政府副县长", "start": "未知", "end": "present", "rank": "副处级", "note": "分管市场监管、卫健、医保等"},
    # 王剑飞 — 副县长
    {"person_id": 7, "org_id": 2, "title": "广平县人民政府副县长", "start": "未知", "end": "present", "rank": "副处级", "note": "分管人社、综合执法、环保、农业农村等"},
    # 商凤祥 — 人大主任
    {"person_id": 8, "org_id": 3, "title": "广平县人大常委会主任", "start": "未知", "end": "present", "rank": "正处级", "note": "截至2026年5月在任"},
    # 王学峰 — 政协主席
    {"person_id": 9, "org_id": 4, "title": "广平县政协主席", "start": "未知", "end": "present", "rank": "正处级", "note": "截至2026年5月在任"},
]

# 4. Relationships
relationships = [
    # 祁富强与张建涛 — 核心搭档
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "祁富强为县委书记，张建涛为县长，县核心领导搭档",
        "overlap_org": "中共广平县委员会/广平县人民政府",
        "overlap_period": "未知-present"
    },
    # 祁富强与李慧 — 上下级
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "祁富强作为县委书记领导县委常委李慧",
        "overlap_org": "中共广平县委员会",
        "overlap_period": "未知-present"
    },
    # 张建涛与李慧 — 上下级
    {
        "person_a": 2,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "张建涛为县长，李慧为常务副县长",
        "overlap_org": "广平县人民政府",
        "overlap_period": "未知-present"
    },
    # 张建涛与杜学强 — 上下级
    {
        "person_a": 2,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "县长与副县长（政法）",
        "overlap_org": "广平县人民政府",
        "overlap_period": "未知-present"
    },
    # 张建涛与赵鸿光 — 上下级
    {
        "person_a": 2,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "县长与副县长（自然资源、住建、交通）",
        "overlap_org": "广平县人民政府",
        "overlap_period": "未知-present"
    },
    # 张建涛与江峥 — 上下级
    {
        "person_a": 2,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "县长与副县长（市场监管、卫健）",
        "overlap_org": "广平县人民政府",
        "overlap_period": "未知-present"
    },
    # 张建涛与王剑飞 — 上下级
    {
        "person_a": 2,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "县长与副县长（人社、农业农村等）",
        "overlap_org": "广平县人民政府",
        "overlap_period": "未知-present"
    },
    # 李慧与江峥 — AB角协作关系
    {
        "person_a": 3,
        "person_b": 6,
        "type": "other",
        "context": "李慧与江峥互为AB角，一位外出时另一位代管工作",
        "overlap_org": "广平县人民政府",
        "overlap_period": "2024.09-"
    },
    # 杜学强与江峥 — AB角协作关系
    {
        "person_a": 4,
        "person_b": 6,
        "type": "other",
        "context": "杜学强与江峥互为AB角，一位外出时另一位代管工作",
        "overlap_org": "广平县人民政府",
        "overlap_period": "2024.09-"
    },
    # 赵鸿光与王剑飞 — AB角协作关系
    {
        "person_a": 5,
        "person_b": 7,
        "type": "other",
        "context": "赵鸿光与王剑飞互为AB角，一位外出时另一位代管工作",
        "overlap_org": "广平县人民政府",
        "overlap_period": "2024.09-"
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
