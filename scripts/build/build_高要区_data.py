#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高要区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 广东省
Parent City: 肇庆市
Region: 高要区
Targets: 区委书记 & 区长

Research Sources:
- 高要区人民政府网站 (www.gaoyao.gov.cn) — 领导之窗
- 高要区人民政府网站 — 新闻资讯（要闻）

Current status (as of 2026-07-22):
- 区委书记: 陈德培（confirmed from official news: 区委全会、常委会等报道）
- 区长: 韦贤康（confirmed from official leadership page: gaoyao.gov.cn/zwgk/ldzc/）

Research Date: 2026-07-22

Note: Due to web access constraints (Exa rate-limited, Baidu 403),
biographical details (birth dates, education, full career timeline)
are limited. These are marked as gaps in person JSONs and open_gaps.md.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "高要区"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # 区委领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "陈德培",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共肇庆市高要区委书记",
        "current_org": "中共肇庆市高要区委员会",
        "source": "高要区人民政府网站新闻（2026-07-17区委全会报道确认）"
    },
    {
        "id": 2,
        "name": "韦贤康",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共肇庆市高要区委副书记、区政府党组书记、区长",
        "current_org": "肇庆市高要区人民政府",
        "source": "高要区人民政府网站领导之窗（www.gaoyao.gov.cn/zwgk/ldzc/）"
    },
    # ════════════════════════════════════════
    # 区政府领导班子
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "李志鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委，区政府党组副书记、副区长",
        "current_org": "肇庆市高要区人民政府",
        "source": "高要区人民政府网站领导之窗（2025-12-12更新）"
    },
    {
        "id": 4,
        "name": "周宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "挂任区委常委，区政府党组成员、副区长",
        "current_org": "肇庆市高要区人民政府",
        "source": "高要区人民政府网站领导之窗（2026-03-03更新）"
    },
    {
        "id": 5,
        "name": "史英泽",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区政府党组成员、副区长人选，市公安局高要分局局长",
        "current_org": "肇庆市高要区人民政府",
        "source": "高要区人民政府网站领导之窗（2026-03-03更新）"
    },
    {
        "id": 6,
        "name": "吴秀雄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区政府党组成员、副区长，兼任区委卫健工委书记",
        "current_org": "肇庆市高要区人民政府",
        "source": "高要区人民政府网站领导之窗（2024-02-01更新）"
    },
    {
        "id": 7,
        "name": "吕文聪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区政府党组成员、副区长",
        "current_org": "肇庆市高要区人民政府",
        "source": "高要区人民政府网站领导之窗（2025-12-12更新）"
    },
    {
        "id": 8,
        "name": "林寿智",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区政府党组成员、副区长",
        "current_org": "肇庆市高要区人民政府",
        "source": "高要区人民政府网站领导之窗（2025-09-30更新）"
    },
    {
        "id": 9,
        "name": "吴世军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区政府党组成员",
        "current_org": "肇庆市高要区人民政府",
        "source": "高要区人民政府网站领导之窗（2025-01-06更新）"
    },
    # ════════════════════════════════════════
    # 前任主要领导
    # ════════════════════════════════════════
    # 前任区委书记（待查）
    # Based on typical district leadership transitions, the predecessor
    # would have left office before 陈德培 assumed the role.
    # This is a gap pending further research.
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共肇庆市高要区委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共肇庆市委员会",
        "location": "肇庆市高要区"
    },
    {
        "id": 2,
        "name": "肇庆市高要区人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "肇庆市人民政府",
        "location": "肇庆市高要区"
    },
    {
        "id": 3,
        "name": "肇庆市高要区人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "肇庆市人民代表大会常务委员会",
        "location": "肇庆市高要区"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议肇庆市高要区委员会",
        "type": "政协",
        "level": "县级",
        "parent": "中国人民政治协商会议肇庆市委员会",
        "location": "肇庆市高要区"
    },
    {
        "id": 5,
        "name": "中共肇庆市高要区纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共肇庆市纪律检查委员会",
        "location": "肇庆市高要区"
    },
    {
        "id": 6,
        "name": "肇庆市高要区监察委员会",
        "type": "党委",
        "level": "县级",
        "parent": "肇庆市监察委员会",
        "location": "肇庆市高要区"
    },
]

# 3. Positions (person_id, org_id, title, start, end, rank, note)
positions = [
    # 陈德培 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "中共肇庆市高要区委书记", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "2026年7月仍在任（第14届区委第11次全会）"},
    # 韦贤康 — 区长
    {"person_id": 2, "org_id": 2, "title": "高要区区长", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "主持区政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "中共肇庆市高要区委副书记", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": ""},
    # 李志鹏 — 常务副区长
    {"person_id": 3, "org_id": 2, "title": "区委常委、区政府党组副书记、副区长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "协助日常事务，分管发改、财政、应急等"},
    # 周宇 — 挂职副区长
    {"person_id": 4, "org_id": 2, "title": "挂任区委常委、区政府党组成员、副区长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "挂职，负责妇女儿童，协管发改财政"},
    # 史英泽 — 副区长兼公安局长
    {"person_id": 5, "org_id": 2, "title": "区政府党组成员、副区长人选，市公安局高要分局局长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "负责公安、司法、综治"},
    # 吴秀雄 — 副区长
    {"person_id": 6, "org_id": 2, "title": "区政府党组成员、副区长，兼任区委卫健工委书记", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "负责外事、民政、交通、卫健等"},
    # 吕文聪 — 副区长
    {"person_id": 7, "org_id": 2, "title": "区政府党组成员、副区长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "负责工信、商务、科技、市场监管等"},
    # 林寿智 — 副区长
    {"person_id": 8, "org_id": 2, "title": "区政府党组成员、副区长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "负责人社、三农、乡村振兴、林业等"},
    # 吴世军 — 区政府党组成员
    {"person_id": 9, "org_id": 2, "title": "区政府党组成员", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "负责双百行动，协管百千万工程、教育"},
]

# 4. Relationships
relationships = [
    # 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "区委书记与区长是区级最重要的党政搭档", "overlap_org": "中共高要区委/高要区人民政府", "overlap_period": "至今"},
    # 区长与常务副区长
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "常务副区长协助区长处理区政府日常事务", "overlap_org": "高要区人民政府", "overlap_period": "至今"},
    # 副区长之间的协作关系
    {"person_a": 3, "person_b": 4, "type": "工作协作", "context": "周宇挂职协管发改财政，与常务副区长有业务重叠", "overlap_org": "高要区人民政府", "overlap_period": "2026-至今"},
    {"person_a": 6, "person_b": 8, "type": "工作协作", "context": "吴秀雄（交通卫健）与林寿智（三农林业）乡镇工作有交叉", "overlap_org": "高要区人民政府", "overlap_period": "至今"},
]

# ── Build ──
if __name__ == "__main__":
    print(f"Building {SLUG} network...")
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
    print("Done.")
