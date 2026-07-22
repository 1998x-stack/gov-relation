#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从化区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 广东省
Parent City: 广州市
Region: 从化区
Targets: 区委书记 & 区长

Research Sources:
- 广州市从化区人民政府门户网站 (www.conghua.gov.cn) — 领导之窗/区政府
- 维基百科 (zh.wikipedia.org) — 从化区词条
- 区政府领导个人简介页面（8位领导详细履历）

Current status:
- 区委书记: 董可（任期待核实, 已从维基百科确认）
- 区长: 刘志杰（1976年10月生）

Research Date: 2026-07-22
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "从化区"
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
        "name": "董可",
        "gender": "待查",
        "ethnicity": "汉族（推测）",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员（现任区委书记）",
        "work_start": "待查",
        "current_post": "中共广州市从化区委书记",
        "current_org": "中共广州市从化区委员会",
        "source": "维基百科：从化区词条—区委书记"
    },
    # ════════════════════════════════════════
    # 区政府领导
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "刘志杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生学历，法学硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "从化区委副书记、区长",
        "current_org": "从化区人民政府",
        "source": "www.conghua.gov.cn 领导之窗—区长个人简介"
    },
    {
        "id": 3,
        "name": "阮伟致",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年8月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生学历，农学硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "从化区委常委、常务副区长",
        "current_org": "从化区人民政府",
        "source": "www.conghua.gov.cn 领导之窗—常务副区长个人简介"
    },
    {
        "id": 4,
        "name": "涂家朝",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年9月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职研究生学历，理学硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "从化区副区长",
        "current_org": "从化区人民政府",
        "source": "www.conghua.gov.cn 领导之窗—涂家朝个人简介"
    },
    {
        "id": 5,
        "name": "毛翔",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年11月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "从化区副区长、区公安分局局长",
        "current_org": "从化区人民政府、广州市公安局从化区分局",
        "source": "www.conghua.gov.cn 领导之窗—毛翔个人简介"
    },
    {
        "id": 6,
        "name": "徐东川",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年4月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生学历，工学博士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "从化区副区长",
        "current_org": "从化区人民政府",
        "source": "www.conghua.gov.cn 领导之窗—徐东川个人简介"
    },
    {
        "id": 7,
        "name": "李延波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年5月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生学历，管理学硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "从化区副区长",
        "current_org": "从化区人民政府",
        "source": "www.conghua.gov.cn 领导之窗—李延波个人简介"
    },
    {
        "id": 8,
        "name": "胡香玲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980年6月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历，法学学士",
        "party_join": "民革党员",
        "work_start": "待查",
        "current_post": "从化区副区长",
        "current_org": "从化区人民政府",
        "source": "www.conghua.gov.cn 领导之窗—胡香玲个人简介"
    },
    {
        "id": 9,
        "name": "梁艺威",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年9月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生学历，工学硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "从化区政府党组成员、区政府办公室党组书记",
        "current_org": "从化区人民政府",
        "source": "www.conghua.gov.cn 领导之窗—梁艺威个人简介"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共广州市从化区委员会",
        "type": "党委",
        "level": "副厅级",
        "parent": "中共广州市委员会",
        "location": "广州市从化区"
    },
    {
        "id": 2,
        "name": "从化区人民政府",
        "type": "政府",
        "level": "副厅级",
        "parent": "广州市人民政府",
        "location": "广州市从化区"
    },
    {
        "id": 3,
        "name": "广州市公安局从化区分局",
        "type": "政府",
        "level": "正处级",
        "parent": "广州市公安局、从化区人民政府",
        "location": "广州市从化区"
    },
    {
        "id": 4,
        "name": "中共广州市委员会",
        "type": "党委",
        "level": "副省级",
        "parent": "中共广东省委",
        "location": "广州市"
    },
    {
        "id": 5,
        "name": "广州市人民政府",
        "type": "政府",
        "level": "副省级",
        "parent": "广东省人民政府",
        "location": "广州市"
    },
    {
        "id": 6,
        "name": "广州市从化区人大常委会",
        "type": "人大",
        "level": "副厅级",
        "parent": "广州市人大常委会",
        "location": "广州市从化区"
    },
    {
        "id": 7,
        "name": "广州市从化区政协",
        "type": "政协",
        "level": "副厅级",
        "parent": "广州市政协",
        "location": "广州市从化区"
    },
]

# 3. Positions
positions = [
    # 董可 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "从化区委书记", "start": "待查", "end": "present", "rank": "副厅级", "note": "维基百科确认"},
    # 刘志杰 — 区长
    {"person_id": 2, "org_id": 1, "title": "从化区委副书记", "start": "待查", "end": "present", "rank": "副厅级", "note": "官方简介确认"},
    {"person_id": 2, "org_id": 2, "title": "从化区区长", "start": "待查", "end": "present", "rank": "副厅级", "note": "区政府党组书记"},
    # 阮伟致 — 常务副区长
    {"person_id": 3, "org_id": 1, "title": "从化区委常委", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "从化区常务副区长", "start": "待查", "end": "present", "rank": "副厅级", "note": "区政府党组副书记"},
    # 涂家朝 — 副区长
    {"person_id": 4, "org_id": 2, "title": "从化区副区长", "start": "待查", "end": "present", "rank": "正处级", "note": "区政府党组成员"},
    # 毛翔 — 副区长/公安局长
    {"person_id": 5, "org_id": 2, "title": "从化区副区长", "start": "待查", "end": "present", "rank": "正处级", "note": "区政府党组成员"},
    {"person_id": 5, "org_id": 3, "title": "从化区公安分局局长", "start": "待查", "end": "present", "rank": "正处级", "note": "区委政法委第一副书记"},
    # 徐东川 — 副区长
    {"person_id": 6, "org_id": 2, "title": "从化区副区长", "start": "待查", "end": "present", "rank": "正处级", "note": "区政府党组成员"},
    # 李延波 — 副区长
    {"person_id": 7, "org_id": 2, "title": "从化区副区长", "start": "待查", "end": "present", "rank": "正处级", "note": "区政府党组成员"},
    # 胡香玲 — 副区长（非中共）
    {"person_id": 8, "org_id": 2, "title": "从化区副区长", "start": "待查", "end": "present", "rank": "正处级", "note": "民革党员"},
    # 梁艺威 — 党组成员
    {"person_id": 9, "org_id": 2, "title": "从化区政府党组成员、办公室主任", "start": "待查", "end": "present", "rank": "正处级", "note": "区政府办党组书记"},
]

# 4. Relationships
relationships = [
    # 董可 ↔ 刘志杰 — 党政搭档
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "从化区委书记与区长党政搭档",
        "overlap_org": "从化区",
        "overlap_period": "董可任区委书记、刘志杰任区长期间",
    },
    # 刘志杰 → 各副区长 — 上下级
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "区长与常务副区长", "overlap_org": "从化区人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "从化区人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "区长与副区长（公安局长）", "overlap_org": "从化区人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "从化区人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "从化区人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "从化区人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "区长与党组成员/办公室主任", "overlap_org": "从化区人民政府", "overlap_period": "当前"},
    # 阮伟致（常务副区长）→ 各副区长 — 协调关系
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "常务副区长与副区长（班子同僚）", "overlap_org": "从化区人民政府", "overlap_period": "当前"},
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "常务副区长与副区长（班子同僚）", "overlap_org": "从化区人民政府", "overlap_period": "当前"},
    {"person_a": 3, "person_b": 6, "type": "overlap", "context": "常务副区长与副区长（班子同僚）", "overlap_org": "从化区人民政府", "overlap_period": "当前"},
    {"person_a": 3, "person_b": 7, "type": "overlap", "context": "常务副区长与副区长（班子同僚）", "overlap_org": "从化区人民政府", "overlap_period": "当前"},
    {"person_a": 3, "person_b": 8, "type": "overlap", "context": "常务副区长与副区长（班子同僚）", "overlap_org": "从化区人民政府", "overlap_period": "当前"},
    # 毛翔（公安局长）↔ 其他副区长 — 政法系统连接
    {"person_a": 5, "person_b": 4, "type": "overlap", "context": "政法系统副区长与班子同僚", "overlap_org": "从化区人民政府", "overlap_period": "当前"},
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "政法系统副区长与班子同僚", "overlap_org": "从化区人民政府", "overlap_period": "当前"},
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
    print(f"✅ Build complete: {SLUG}")
    print(f"   DB:   {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
