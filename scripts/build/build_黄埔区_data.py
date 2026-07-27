#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
黄埔区（广州开发区）领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区 (与广州开发区合署办公)
Province: 广东省
Parent City: 广州市
Region: 黄埔区
Targets: 区委书记 & 区长

Note: 黄埔区与广州经济技术开发区（广州开发区）合署办公，
区委书记通常同时担任广州开发区党工委书记，
区长同时担任广州开发区管委会常务副主任。

Research Sources:
- 广州市黄埔区人民政府门户网站 (www.hp.gov.cn) — 领导之窗
- 维基百科 (zh.wikipedia.org) — 黄埔区词条
- 维基百科消歧义页 — 陈杰 (1970年)

Current status of区委书记:
- 陈杰 (1970年生) 曾任黄埔区委书记，已于2025/2026年调任中共江门市委书记
- 现任区委书记待确认（可能空缺或由新任命人选担任）

Research Date: 2026-07-22
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths ──
SLUG = "黄埔区"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DATABASE_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(GRAPH_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Former & Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "陈杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共江门市委书记（原黄埔区委书记）",
        "current_org": "中共江门市委员会",
        "source": "维基百科消歧义页：陈杰(1970年)—现任中共江门市委书记，曾任中共广州市委常委、常务副市长、黄埔区委书记"
    },
    {
        "id": 2,
        "name": "冼银崧",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "黄埔区区长、广州开发区管委会常务副主任",
        "current_org": "黄埔区人民政府、广州开发区管委会",
        "source": "www.hp.gov.cn 领导之窗—区长/管委会常务副主任"
    },
    # ════════════════════════════════════════
    # 区政府副区长
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "董彦君",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "黄埔区副区长",
        "current_org": "黄埔区人民政府",
        "source": "www.hp.gov.cn 领导之窗—副区长"
    },
    {
        "id": 4,
        "name": "黎信坤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "黄埔区副区长",
        "current_org": "黄埔区人民政府",
        "source": "www.hp.gov.cn 领导之窗—副区长"
    },
    {
        "id": 5,
        "name": "徐丹",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "黄埔区副区长",
        "current_org": "黄埔区人民政府",
        "source": "www.hp.gov.cn 领导之窗—副区长"
    },
    {
        "id": 6,
        "name": "何宇鸿",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "黄埔区副区长",
        "current_org": "黄埔区人民政府",
        "source": "www.hp.gov.cn 领导之窗—副区长"
    },
    {
        "id": 7,
        "name": "杨峻岭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "黄埔区副区长",
        "current_org": "黄埔区人民政府",
        "source": "www.hp.gov.cn 领导之窗—副区长"
    },
    # ════════════════════════════════════════
    # 广州开发区管委会
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "顾晓斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广州开发区管委会副主任",
        "current_org": "广州开发区管委会",
        "source": "www.hp.gov.cn 领导之窗—广州开发区管委会"
    },
    {
        "id": 9,
        "name": "姚锦全",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广州开发区管委会副主任",
        "current_org": "广州开发区管委会",
        "source": "www.hp.gov.cn 领导之窗—广州开发区管委会"
    },
    {
        "id": 10,
        "name": "代新祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广州开发区管委会副主任",
        "current_org": "广州开发区管委会",
        "source": "www.hp.gov.cn 领导之窗—广州开发区管委会"
    },
    {
        "id": 11,
        "name": "陈超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广州开发区管委会秘书长",
        "current_org": "广州开发区管委会",
        "source": "www.hp.gov.cn 领导之窗—广州开发区管委会"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共广州市黄埔区委员会",
        "type": "党委",
        "level": "副厅级",
        "parent": "中共广州市委员会",
        "location": "广州市黄埔区"
    },
    {
        "id": 2,
        "name": "黄埔区人民政府",
        "type": "政府",
        "level": "副厅级",
        "parent": "广州市人民政府",
        "location": "广州市黄埔区"
    },
    {
        "id": 3,
        "name": "广州开发区管委会",
        "type": "开发区",
        "level": "副厅级（合并后实质副省级）",
        "parent": "广州市人民政府",
        "location": "广州市黄埔区"
    },
    {
        "id": 4,
        "name": "广州开发区党工委",
        "type": "党委",
        "level": "副厅级",
        "parent": "中共广州市委员会",
        "location": "广州市黄埔区"
    },
    {
        "id": 5,
        "name": "中共江门市委员会",
        "type": "党委",
        "level": "正厅级",
        "parent": "中共广东省委",
        "location": "江门市"
    },
    {
        "id": 6,
        "name": "中共广州市委员会",
        "type": "党委",
        "level": "副省级",
        "parent": "中共广东省委",
        "location": "广州市"
    },
    {
        "id": 7,
        "name": "广州市人民政府",
        "type": "政府",
        "level": "副省级",
        "parent": "广东省人民政府",
        "location": "广州市"
    },
]

# 3. Positions
positions = [
    # 陈杰 — 曾任黄埔区委书记
    {"person_id": 1, "org_id": 1, "title": "黄埔区委书记（原任）", "start": "待查", "end": "2025-2026", "rank": "副厅级", "note": "已调任江门市委书记"},
    {"person_id": 1, "org_id": 5, "title": "江门市委书记（现任）", "start": "2025-2026", "end": "present", "rank": "正厅级", "note": "升任"},
    {"person_id": 1, "org_id": 6, "title": "广州市委常委、常务副市长", "start": "待查", "end": "2025-2026", "rank": "副省级城市副职", "note": "兼任"},
    # 冼银崧 — 区长/开发区常务副主任
    {"person_id": 2, "org_id": 2, "title": "黄埔区区长", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 3, "title": "广州开发区管委会常务副主任", "start": "待查", "end": "present", "rank": "副厅级", "note": "兼任"},
    # 副区长
    {"person_id": 3, "org_id": 2, "title": "黄埔区副区长", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "黄埔区副区长", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "黄埔区副区长", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "黄埔区副区长", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "黄埔区副区长", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
    # 开发区管委会
    {"person_id": 8, "org_id": 3, "title": "广州开发区管委会副主任", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 3, "title": "广州开发区管委会副主任", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 3, "title": "广州开发区管委会副主任", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 11, "org_id": 3, "title": "广州开发区管委会秘书长", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
]

# 4. Relationships
relationships = [
    # 陈杰与冼银崧 — 党政搭档（共事于黄埔区/广州开发区）
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "黄埔区委书记与区长党政搭档，共事于黄埔区",
        "overlap_org": "黄埔区",
        "overlap_period": "陈杰任黄埔区委书记期间",
    },
    # 冼银崧与副区长们 — 上下级
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "黄埔区人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "黄埔区人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "黄埔区人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "黄埔区人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "黄埔区人民政府", "overlap_period": "当前"},
    # 开发区管委会 — 冼银崧为主管
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "管委会常务副主任与副主任", "overlap_org": "广州开发区管委会", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "管委会常务副主任与副主任", "overlap_org": "广州开发区管委会", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "管委会常务副主任与副主任", "overlap_org": "广州开发区管委会", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "管委会常务副主任与秘书长", "overlap_org": "广州开发区管委会", "overlap_period": "当前"},
    # 陈杰与广州市委/市政府
    {"person_a": 1, "person_b": 11, "type": "same_system", "context": "陈杰曾任广州市委常委、常务副市长", "overlap_org": "中共广州市委员会、广州市人民政府", "overlap_period": "任广州市委常委、常务副市长期间"},
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
