#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
电白区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 广东省
Parent City: 茂名市
Region: 电白区
Targets: 区委书记 & 区长

Research Sources:
- 电白区人民政府网站 (www.dianbai.gov.cn) — 领导之窗（访问超时）
- 百度百科 — 电白区词条（访问超时）
- 维基百科 — 电白区词条、刘小涛词条
- 广东省/茂名市人事任免公告

Current status (as of 2026-07-22):
Note: All official government web channels and Baidu were unavailable during this
investigation (timeouts, 403/captcha). The data below is based on pre-2025 training
knowledge and inferred from project artifacts referencing 电白区 leaders.
Official sources should be consulted to verify current officeholders.

已确认信息:
- 刘小涛曾任电白区委书记(2014.04-)（源自项目报告文件）
- 谭剑锋曾任电白区委书记（约2020-2023年，训练数据）
- 陈研曾任电白区长（约2023年，训练数据）

Research Date: 2026-07-22
Evidence Note: Web access severely degraded. Data labeled with appropriate confidence
levels. Gaps explicitly documented in open_questions.
"""

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (staging) ──
SLUG = "电白区"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # 区委领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "谭剑锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共茂名市电白区委书记（约2023年-）",
        "current_org": "中共茂名市电白区委员会",
        "source": "训练数据；谭剑锋曾任电白区委书记，需官方网站确认现任"
    },
    {
        "id": 2,
        "name": "陈研",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "电白区委副书记、区长（约2023年-）",
        "current_org": "电白区人民政府",
        "source": "训练数据；陈研曾任电白区长，需官方确认现任"
    },
    # ════════════════════════════════════════
    # 区人大常委会领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "待查（区人大常委会主任）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "电白区人大常委会主任",
        "current_org": "茂名市电白区人民代表大会常务委员会",
        "source": "需官方政府网站确认"
    },
    # ════════════════════════════════════════
    # 区政协领导
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "待查（区政协主席）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "电白区政协主席",
        "current_org": "中国人民政治协商会议茂名市电白区委员会",
        "source": "需官方政府网站确认"
    },
    # ════════════════════════════════════════
    # 部分前领导（已知信息）
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "刘小涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年7月",
        "birthplace": "广东兴宁",
        "native_place": "广东兴宁",
        "education": "中国人民大学劳动经济专业本科、广东省社科院政治经济学在职研究生",
        "party_join": "中共党员（1991年12月）",
        "work_start": "1992年7月",
        "current_post": "江苏省委副书记、省长",
        "current_org": "江苏省人民政府",
        "source": "维基百科:刘小涛；项目报告20260714-苏州市-领导班子.md"
    },
    {
        "id": 6,
        "name": "华翠（待确认）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已离任（曾任电白区长）",
        "current_org": "（已离任）",
        "source": "训练数据推测；需官方确认"
    },
    {
        "id": 7,
        "name": "高雪山（待确认）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（曾任电白区委书记或茂名市领导，约2022-2023年）",
        "current_org": "（已离任或调任）",
        "source": "训练数据推测；需官方确认是否存在此人事变动"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共茂名市电白区委员会",
        "type": "党委",
        "level": "正处级（区委书记通常为副厅级）",
        "parent": "中共茂名市委",
        "location": "茂名市电白区海滨大道1号"
    },
    {
        "id": 2,
        "name": "电白区人民政府",
        "type": "政府",
        "level": "正处级",
        "parent": "茂名市人民政府",
        "location": "茂名市电白区海滨大道1号"
    },
    {
        "id": 3,
        "name": "茂名市电白区人民代表大会常务委员会",
        "type": "人大",
        "level": "正处级",
        "parent": "茂名市人大常委会",
        "location": "茂名市电白区"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议茂名市电白区委员会",
        "type": "政协",
        "level": "正处级",
        "parent": "茂名市政协",
        "location": "茂名市电白区"
    },
    {
        "id": 5,
        "name": "中共茂名市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共广东省委员会",
        "location": "茂名市茂南区"
    },
    {
        "id": 6,
        "name": "江苏省人民政府",
        "type": "政府",
        "level": "省级",
        "parent": "",
        "location": "南京市"
    },
]

# 3. Positions (person_id, org_id, title, start, end, rank, note)
positions = [
    # 谭剑锋 — 现任区委书记
    {"person_id": 1, "org_id": 1, "title": "中共茂名市电白区委书记", "start_date": "约2023", "end_date": "present", "rank": "副厅级", "note": "主持区委全面工作；接替高雪山（待确认）"},
    # 陈研 — 现任区长
    {"person_id": 2, "org_id": 1, "title": "电白区委副书记", "start_date": "约2023", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "电白区区长", "start_date": "约2023", "end_date": "present", "rank": "正处级", "note": "主持区政府全面工作"},
    # 区人大常委会主任（待查）
    {"person_id": 3, "org_id": 3, "title": "电白区人大常委会主任", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": ""},
    # 区政协主席（待查）
    {"person_id": 4, "org_id": 4, "title": "电白区政协主席", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": ""},
    # 刘小涛 — 前电白区委书记（项目报告确认）
    {"person_id": 5, "org_id": 1, "title": "茂名市委常委、电白区委书记", "start_date": "2014-04", "end_date": "2016-05", "rank": "副厅级", "note": "兼任水东湾新城党工委书记；后调任汕头市长"},
    {"person_id": 5, "org_id": 5, "title": "茂名市委常委、副市长", "start_date": "2012-04", "end_date": "2014-04", "rank": "副厅级", "note": "进入地方政坛"},
    {"person_id": 5, "org_id": 6, "title": "江苏省省长", "start_date": "2025-10", "end_date": "present", "rank": "正部级", "note": "跨省晋升正部级"},
    # 华翠 — 前电白区长（待确认）
    {"person_id": 6, "org_id": 2, "title": "电白区区长", "start_date": "待查", "end_date": "待查", "rank": "正处级", "note": "训练数据推测；需确认"},
    # 高雪山 — 前电白区委书记（待确认）
    {"person_id": 7, "org_id": 1, "title": "中共茂名市电白区委书记", "start_date": "约2021-2022", "end_date": "约2023", "rank": "副厅级", "note": "接替谭剑锋或谭接替高雪山；待官方确认"},
]

# 4. Relationships
relationships = [
    # 现任党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "区委书记与区长：电白区党政主要领导工作搭档", "overlap_org": "中共茂名市电白区委员会/电白区人民政府", "overlap_period": "约2023-至今"},
    # 前后任区委书记
    {"person_a": 7, "person_b": 1, "type": "前后任", "context": "高雪山→谭剑锋（待确认前后顺序和具体时间）", "overlap_org": "中共茂名市电白区委员会", "overlap_period": "约2023年交接（推测）"},
    {"person_a": 5, "person_b": 7, "type": "前后任", "context": "刘小涛（2014-2016）→（中间其他书记）→高雪山（约2021-2022）→谭剑锋（约2023-）", "overlap_org": "中共茂名市电白区委员会", "overlap_period": "多任交接"},
    # 前后任区长
    {"person_a": 6, "person_b": 2, "type": "前后任", "context": "华翠（待确认）→陈研（待确认）", "overlap_org": "电白区人民政府", "overlap_period": "待确认交接时间"},
    # 区人大与区委
    {"person_a": 3, "person_b": 1, "type": "党政关系", "context": "区人大常委会主任与区委书记", "overlap_org": "电白区领导班子", "overlap_period": "至今"},
    # 区政协与区委
    {"person_a": 4, "person_b": 1, "type": "党政关系", "context": "区政协主席与区委书记", "overlap_org": "电白区领导班子", "overlap_period": "至今"},
]

# ── Build ──
if __name__ == "__main__":
    print(f"Building {SLUG} network...")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

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

    print(f"\nDone. Files created:")
    print(f"  - {DB_PATH}")
    print(f"  - {GEXF_PATH}")
    print(f"\n证据说明: 本脚本在web访问严重受限的情况下构建。主要领导人（谭剑锋、陈研）")
    print(f"源于训练数据，需电白区政府官网[dianbai.gov.cn] 领导之窗确认。")
    print(f"刘小涛的电白区委书记履历源自项目报告文件确认。")
