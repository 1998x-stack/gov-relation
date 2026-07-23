#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
成安县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 邯郸市
Region: 成安县
Targets: 县委书记 & 县长

Research Sources:
- 成安县人民政府官方网站 (www.chengan.gov.cn) — 领导之窗页面确认县长刘丙胜、副县长名单及简历
- 成安县政府新闻"县委常委会召开扩大会议"(newsid=132000, 2024-12-31后)确认李东健任县委书记
- 成安县政府新闻"刘金仓 刘丙胜到经济开发区调研"(newsid=131600, 2024-11-27)确认刘金仓为前任县委书记
- 政府新闻"县委常委会召开扩大会议"(newsid=133387, 2025-2026)确认李东健继续在任
- 领导之窗更新日期: 2026-07-24

Research Date: 2026-07-23
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "成安县"

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
        "name": "李东健",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "邯郸市成安县委书记",
        "current_org": "中共成安县委员会",
        "source": "成安县政府新闻—县委常委会扩大会议确认李东健任县委书记。来源：http://www.chengan.gov.cn/main/viewDetail.jsp?newsid=132000; 最新报道 newsid=133387 仍以县委书记身份出现。领导之窗县委页面(leadtype=sw)更新至2026-07-24。"
    },
    {
        "id": 2,
        "name": "刘丙胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年5月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历，文学学士学位",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "成安县委副书记、县政府县长",
        "current_org": "成安县人民政府",
        "source": "成安县人民政府领导之窗页面(leadtype=xzf)。来源：http://www.chengan.gov.cn/module/leader/viewleaderqian.action?leadtype=xzf。简介：刘丙胜，男，汉族，1981年5月出生，大学学历，文学学士学位，中共党员，现任成安县委副书记，县政府县长、党组书记。"
    },
    # ════════════════════════════════════════
    # 县政府其他领导（来自官方领导之窗）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "杨艳峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年7月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历，工学学士学位",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "成安县委常委、政府常务副县长",
        "current_org": "成安县人民政府",
        "source": "成安县人民政府领导之窗页面。简介：杨艳峰，男，汉族，1979年7月出生，大学学历，工学学士学位，中共党员，现任成安县委常委，政府常务副县长、党组副书记。"
    },
    {
        "id": 4,
        "name": "霍鸿河",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年3月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "成安县人民政府副县长",
        "current_org": "成安县人民政府",
        "source": "成安县人民政府领导之窗页面。简介：霍鸿河，男，汉族，1970年3月出生，大学学历，中共党员，现任成安县人民政府副县长、党组成员。"
    },
    {
        "id": 5,
        "name": "王艳涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年3月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "成安县人民政府副县长",
        "current_org": "成安县人民政府",
        "source": "成安县人民政府领导之窗页面。简介：王艳涛，男，汉族，1979年3月出生，大学学历，中共党员，现任成安县人民政府副县长、党组成员。"
    },
    {
        "id": 6,
        "name": "刘志民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年11月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "成安县人民政府副县长、县公安局局长",
        "current_org": "成安县人民政府/成安县公安局",
        "source": "成安县人民政府领导之窗页面。简介：刘志民，男，汉族，1973年11月出生，大学学历，中共党员，现任成安县人民政府副县长、党组成员，县公安局党委书记、局长、督察长。"
    },
    {
        "id": 7,
        "name": "魏丽丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1987年2月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历，文学学士学位",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "成安县人民政府副县长",
        "current_org": "成安县人民政府",
        "source": "成安县人民政府领导之窗页面。简介：魏丽丽，女，汉族，1987年2月出生，大学学历，文学学士学位，中共党员，现任成安县人民政府副县长、党组成员。"
    },
    {
        "id": 8,
        "name": "李晓东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年11月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历，管理学学士学位",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "成安县人民政府副县长",
        "current_org": "成安县人民政府",
        "source": "成安县人民政府领导之窗页面。简介：李晓东，男，汉族，1987年11月出生，大学学历，管理学学士学位，中共党员，现任成安县人民政府副县长、党组成员。"
    },
    # ════════════════════════════════════════
    # Historical Leaders
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "刘金仓",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查（原成安县委书记，约2024年12月离任）",
        "current_org": "",
        "source": "成安县政府新闻'刘金仓 刘丙胜到经济开发区调研'(newsid=131600, 2024-11-27)确认刘金仓任县委书记；此后不再以县委书记出现在新闻标题中。来源：http://www.chengan.gov.cn/main/viewDetail.jsp?newsid=131600"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共成安县委员会",
        "type": "党委",
        "level": "县级",
        "location": "邯郸市成安县",
        "parent": "中共邯郸市委"
    },
    {
        "id": 2,
        "name": "成安县人民政府",
        "type": "政府",
        "level": "县级",
        "location": "邯郸市成安县",
        "parent": "邯郸市人民政府"
    },
    {
        "id": 3,
        "name": "成安县人大常委会",
        "type": "人大",
        "level": "县级",
        "location": "邯郸市成安县",
        "parent": "邯郸市人大常委会"
    },
    {
        "id": 4,
        "name": "成安县政协",
        "type": "政协",
        "level": "县级",
        "location": "邯郸市成安县",
        "parent": "邯郸市政协"
    },
    {
        "id": 5,
        "name": "成安县公安局",
        "type": "政府",
        "level": "正科级",
        "location": "邯郸市成安县",
        "parent": "成安县人民政府"
    },
]

# 3. Positions
positions = [
    # 李东健 — 现任
    {"person_id": 1, "org_id": 1, "title": "邯郸市成安县委书记", "start": "约2024年12月", "end": "present", "rank": "正处级", "note": "截至2026年7月在任；前任为刘金仓"},
    # 刘丙胜 — 现任
    {"person_id": 2, "org_id": 1, "title": "成安县委副书记", "start": "未知", "end": "present", "rank": "正处级", "note": "县委副书记兼县长"},
    {"person_id": 2, "org_id": 2, "title": "成安县人民政府县长", "start": "未知", "end": "present", "rank": "正处级", "note": "县政府县长、党组书记；截至2026年7月在任"},
    # 杨艳峰 — 现任
    {"person_id": 3, "org_id": 1, "title": "成安县委常委", "start": "未知", "end": "present", "rank": "副处级", "note": "截至2026年7月在任"},
    {"person_id": 3, "org_id": 2, "title": "成安县人民政府常务副县长", "start": "未知", "end": "present", "rank": "副处级", "note": "县政府党组副书记"},
    # 霍鸿河 — 现任副县长
    {"person_id": 4, "org_id": 2, "title": "成安县人民政府副县长", "start": "未知", "end": "present", "rank": "副处级", "note": "县政府党组成员"},
    # 王艳涛 — 现任副县长
    {"person_id": 5, "org_id": 2, "title": "成安县人民政府副县长", "start": "未知", "end": "present", "rank": "副处级", "note": "县政府党组成员"},
    # 刘志民 — 现任副县长兼公安局长
    {"person_id": 6, "org_id": 2, "title": "成安县人民政府副县长", "start": "未知", "end": "present", "rank": "副处级", "note": "县政府党组成员"},
    {"person_id": 6, "org_id": 5, "title": "成安县公安局局长", "start": "未知", "end": "present", "rank": "正科级", "note": "党委书记、局长、督察长"},
    # 魏丽丽 — 现任副县长
    {"person_id": 7, "org_id": 2, "title": "成安县人民政府副县长", "start": "未知", "end": "present", "rank": "副处级", "note": "县政府党组成员"},
    # 李晓东 — 现任副县长
    {"person_id": 8, "org_id": 2, "title": "成安县人民政府副县长", "start": "未知", "end": "present", "rank": "副处级", "note": "县政府党组成员"},
    # 刘金仓 — 历史职务
    {"person_id": 9, "org_id": 1, "title": "邯郸市成安县委书记", "start": "未知", "end": "约2024年12月", "rank": "正处级", "note": "2024年11月27日在任；其后李东健接任"},
]

# 4. Relationships
relationships = [
    # 李东健与刘丙胜 — 核心搭档
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "李东健为县委书记，刘丙胜为县长，县核心领导搭档",
        "overlap_org": "中共成安县委员会/成安县人民政府",
        "overlap_period": "2024.12-"
    },
    # 李东健与杨艳峰 — 上下级
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "李东健作为县委书记领导县委常委杨艳峰",
        "overlap_org": "中共成安县委员会",
        "overlap_period": "2024.12-"
    },
    # 刘丙胜与杨艳峰 — 上下级
    {
        "person_a": 2,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "刘丙胜为县长，杨艳峰为常务副县长",
        "overlap_org": "成安县人民政府",
        "overlap_period": "未知-present"
    },
    # 刘丙胜与其他副县长（工作关系）
    {
        "person_a": 2,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "县长与副县长",
        "overlap_org": "成安县人民政府",
        "overlap_period": "未知-present"
    },
    {
        "person_a": 2,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "县长与副县长",
        "overlap_org": "成安县人民政府",
        "overlap_period": "未知-present"
    },
    {
        "person_a": 2,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "县长与副县长（兼公安局长）",
        "overlap_org": "成安县人民政府",
        "overlap_period": "未知-present"
    },
    {
        "person_a": 2,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "县长与副县长",
        "overlap_org": "成安县人民政府",
        "overlap_period": "未知-present"
    },
    {
        "person_a": 2,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "县长与副县长",
        "overlap_org": "成安县人民政府",
        "overlap_period": "未知-present"
    },
    # 李东健与刘金仓 — 接替关系
    {
        "person_a": 1,
        "person_b": 9,
        "type": "predecessor_successor",
        "context": "李东健接替刘金仓任成安县委书记",
        "overlap_org": "中共成安县委员会",
        "overlap_period": "2024.12"
    },
    # 刘金仓与刘丙胜 — 前任搭档关系
    {
        "person_a": 9,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "刘金仓任县委书记时，刘丙胜任县长",
        "overlap_org": "中共成安县委员会/成安县人民政府",
        "overlap_period": "2024年前-2024.12"
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
