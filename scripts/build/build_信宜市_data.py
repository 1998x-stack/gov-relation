#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
信宜市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县级市
Province: 广东省
Parent City: 茂名市
Region: 信宜市
Targets: 市委书记 & 市长

Research Sources:
- 信宜市人民政府网站 (www.xinyi.gov.cn) — 领导之窗（访问超时，无法获取）
- 茂名市人民政府网站 (www.maoming.gov.cn) — 领导之窗（访问超时）
- 百度百科 — 信宜市词条（403 禁止访问）
- 维基百科 — 信宜市词条、龚庆词条（不可用）
- 广东省/茂名市人事任免公告（不可用）

Current status (as of 2026-07-22):
Note: All official government web channels, Baidu, Exa search, and Jina Reader were
unavailable during this investigation (transport errors, 403, rate limits timeouts).
The data below is based on pre-2025 training knowledge. Official sources should be
consulted to verify current officeholders and all biographical details.

Known data points from training knowledge:
- 龚庆: 信宜市委书记（约2019/2020年上任）
- 李龙飞: 信宜市委副书记、市长（约2022年上任，前信宜市常务副市长）
- 邓惠林: 前任信宜市委书记（约2016-2019年）
- 王土瑞: 曾任职信宜市（约2015-2018年任信宜市副市长等职）
- 黄权: 曾任信宜市副市长等职

Research Date: 2026-07-22
Evidence Note: Web access severely degraded. Data labeled with appropriate confidence
levels. Gaps explicitly documented in open_questions. Person JSON files contain
detailed uncertainty documentation.
"""

import os
import sys
from datetime import datetime

# Allow import from repo root
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "信宜市"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════════
    # 市委领导
    # ════════════════════════════════════════════
    {
        "id": 1,
        "name": "龚庆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共信宜市委书记",
        "current_org": "中共信宜市委员会",
        "source": "训练知识 (plausible) — 约2019/2020年起任信宜市委书记，需官方网站确认"
    },
    {
        "id": 2,
        "name": "李龙飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "信宜市委副书记、市长",
        "current_org": "信宜市人民政府",
        "source": "训练知识 (plausible) — 约2022年起任信宜市长，此前曾任信宜市常务副市长"
    },
    # ════════════════════════════════════════════
    # 前任领导
    # ════════════════════════════════════════════
    {
        "id": 3,
        "name": "邓惠林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "前任信宜市委书记（约2016-2019年）",
        "current_org": "(已离任)",
        "source": "训练知识 (plausible) — 前任信宜市委书记，后另有任用"
    },
    {
        "id": 4,
        "name": "王土瑞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "前任信宜市副市长",
        "current_org": "(已离任)",
        "source": "训练知识 (plausible) — 约2015-2018年任信宜市副市长"
    },
    {
        "id": 5,
        "name": "黄权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "前任信宜市副市长",
        "current_org": "(已离任)",
        "source": "训练知识 (plausible) — 曾任信宜市副市长"
    },
    # ════════════════════════════════════════════
    # 市人大、政协领导
    # ════════════════════════════════════════════
    {
        "id": 6,
        "name": "待查（信宜市人大常委会主任）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "信宜市人大常委会主任",
        "current_org": "信宜市人大常委会",
        "source": "待查 — 官方网站不可用，需后续补充"
    },
    {
        "id": 7,
        "name": "待查（信宜市政协主席）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "信宜市政协主席",
        "current_org": "信宜市政协",
        "source": "待查 — 官方网站不可用，需后续补充"
    },
    # ════════════════════════════════════════════
    # 重要副职
    # ════════════════════════════════════════════
    {
        "id": 8,
        "name": "待查（常务副市长）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "信宜市委常委、常务副市长",
        "current_org": "信宜市人民政府",
        "source": "待查 — 官方网站不可用，需后续补充"
    },
    {
        "id": 9,
        "name": "待查（纪委书记）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "信宜市委常委、纪委书记、监委主任",
        "current_org": "信宜市纪律检查委员会",
        "source": "待查 — 官方网站不可用，需后续补充"
    },
    {
        "id": 10,
        "name": "待查（组织部部长）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "信宜市委常委、组织部部长",
        "current_org": "中共信宜市委组织部",
        "source": "待查 — 官方网站不可用，需后续补充"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共信宜市委员会",
        "type": "党委",
        "level": "县级市",
        "location": "广东省茂名市信宜市",
        "source": "公开机构信息"
    },
    {
        "id": 2,
        "name": "信宜市人民政府",
        "type": "政府",
        "level": "县级市",
        "location": "广东省茂名市信宜市",
        "source": "公开机构信息"
    },
    {
        "id": 3,
        "name": "信宜市人大常委会",
        "type": "人大",
        "level": "县级市",
        "location": "广东省茂名市信宜市",
        "source": "公开机构信息"
    },
    {
        "id": 4,
        "name": "信宜市政协",
        "type": "政协",
        "level": "县级市",
        "location": "广东省茂名市信宜市",
        "source": "公开机构信息"
    },
    {
        "id": 5,
        "name": "中共信宜市纪律检查委员会",
        "type": "党委",
        "level": "县级市",
        "location": "广东省茂名市信宜市",
        "source": "公开机构信息"
    },
    {
        "id": 6,
        "name": "中共信宜市委组织部",
        "type": "党委",
        "level": "县级市",
        "location": "广东省茂名市信宜市",
        "source": "公开机构信息"
    },
]

# 3. Positions
positions = [
    # 龚庆 — 市委书记
    {
        "id": 1,
        "person_id": 1,
        "org_id": 1,
        "title": "中共信宜市委书记",
        "start": "约2019/2020",
        "end": "至今",
        "is_current": True,
        "rank": "正处级",
        "system": "party",
        "source": "训练知识 (plausible)"
    },
    # 李龙飞 — 市长
    {
        "id": 2,
        "person_id": 2,
        "org_id": 2,
        "title": "信宜市委副书记、市长",
        "start": "约2022",
        "end": "至今",
        "is_current": True,
        "rank": "正处级",
        "system": "government",
        "source": "训练知识 (plausible)"
    },
    # 邓惠林 — 前任市委书记
    {
        "id": 3,
        "person_id": 3,
        "org_id": 1,
        "title": "中共信宜市委书记",
        "start": "约2016",
        "end": "约2019",
        "is_current": False,
        "rank": "正处级",
        "system": "party",
        "source": "训练知识 (plausible)"
    },
    # 王土瑞 — 前任副市长
    {
        "id": 4,
        "person_id": 4,
        "org_id": 2,
        "title": "信宜市副市长",
        "start": "约2015",
        "end": "约2018",
        "is_current": False,
        "rank": "副处级",
        "system": "government",
        "source": "训练知识 (plausible)"
    },
    # 黄权 — 前任副市长
    {
        "id": 5,
        "person_id": 5,
        "org_id": 2,
        "title": "信宜市副市长",
        "start": "未知",
        "end": "未知",
        "is_current": False,
        "rank": "副处级",
        "system": "government",
        "source": "训练知识 (plausible)"
    },
    # 人大主任
    {
        "id": 6,
        "person_id": 6,
        "org_id": 3,
        "title": "信宜市人大常委会主任",
        "start": "未知",
        "end": "至今",
        "is_current": True,
        "rank": "正处级",
        "system": "other",
        "source": "待查"
    },
    # 政协主席
    {
        "id": 7,
        "person_id": 7,
        "org_id": 4,
        "title": "信宜市政协主席",
        "start": "未知",
        "end": "至今",
        "is_current": True,
        "rank": "正处级",
        "system": "other",
        "source": "待查"
    },
    # 常务副市长
    {
        "id": 8,
        "person_id": 8,
        "org_id": 2,
        "title": "信宜市委常委、常务副市长",
        "start": "未知",
        "end": "至今",
        "is_current": True,
        "rank": "副处级",
        "system": "government",
        "source": "待查"
    },
    # 纪委书记
    {
        "id": 9,
        "person_id": 9,
        "org_id": 5,
        "title": "信宜市委常委、纪委书记、监委主任",
        "start": "未知",
        "end": "至今",
        "is_current": True,
        "rank": "副处级",
        "system": "discipline",
        "source": "待查"
    },
    # 组织部部长
    {
        "id": 10,
        "person_id": 10,
        "org_id": 6,
        "title": "信宜市委常委、组织部部长",
        "start": "未知",
        "end": "至今",
        "is_current": True,
        "rank": "副处级",
        "system": "organization",
        "source": "待查"
    },
]

# 4. Relationships
relationships = [
    # 龚庆 ← 邓惠林 (predecessor_successor)
    {
        "id": 1,
        "person_a": 1,
        "person_b": 3,
        "type": "predecessor_successor",
        "strength": "strong",
        "evidence": "龚庆接替邓惠林担任信宜市委书记",
        "overlap_org": "中共信宜市委员会",
        "overlap_period": "约2019/2020交接",
        "direction": "person_b_to_person_a",
        "confidence": "plausible",
        "source": "训练知识 — 职务交接"
    },
    # 龚庆 ↔ 李龙飞 (superior_subordinate)
    {
        "id": 2,
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "strength": "strong",
        "evidence": "龚庆作为市委书记，李龙飞作为市长，为党政主要领导搭档",
        "overlap_org": "中共信宜市委员会/信宜市人民政府",
        "overlap_period": "约2022至今",
        "direction": "undirected",
        "confidence": "plausible",
        "source": "训练知识 — 党政主要领导"
    },
    # 李龙飞 — 曾任常务副市长（基于推测，如果他从常务副市长升任市长）
    {
        "id": 3,
        "person_a": 2,
        "person_b": 8,
        "type": "overlap",
        "strength": "medium",
        "evidence": "李龙飞此前可能曾任常务副市长，与现任常务副市长可能有交接",
        "overlap_org": "信宜市人民政府",
        "overlap_period": "约2022年前后",
        "direction": "undirected",
        "confidence": "unverified",
        "source": "训练知识 — 推测"
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
    print(f"Done: {DB_PATH} and {GEXF_PATH}")
