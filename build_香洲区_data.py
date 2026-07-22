#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
香洲区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 广东省
Parent City: 珠海市
Region: 香洲区
Targets: 区委书记 & 区长

Research Sources:
- 珠海市香洲区人民政府门户网站 (www.zhxz.gov.cn) — 领导之窗
- 维基百科 (zh.wikipedia.org) — 香洲区词条

Current status (as of 2026-07-22):
- 区委书记: 刘力（珠海市委常委，香洲区委书记）
- 区长: 张会洋（区委副书记，区政府党组书记、区长，保税区管委会主任）

Research Date: 2026-07-22
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "香洲区"
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
        "name": "刘力",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员（现任市委常委、区委书记）",
        "work_start": "待查",
        "current_post": "珠海市委常委，香洲区委书记",
        "current_org": "中共珠海市香洲区委员会",
        "source": "www.zhxz.gov.cn 领导之窗—区委书记刘力"
    },
    {
        "id": 2,
        "name": "张会洋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "香洲区委副书记，区政府党组书记、区长，保税区管委会主任",
        "current_org": "香洲区人民政府",
        "source": "www.zhxz.gov.cn 领导之窗—区长张会洋"
    },
    {
        "id": 3,
        "name": "蓝璋",
        "gender": "待查",
        "ethnicity": "汉族（推测）",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "香洲区委副书记（专职）",
        "current_org": "中共珠海市香洲区委员会",
        "source": "www.zhxz.gov.cn 领导之窗—区委副书记蓝璋"
    },
    # ════════════════════════════════════════
    # 区委常委（不含书记、副书记）
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "刘铁兵",
        "gender": "待查",
        "ethnicity": "汉族（推测）",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "香洲区委常委、区委政法委书记",
        "current_org": "中共珠海市香洲区委员会",
        "source": "www.zhxz.gov.cn 领导之窗—区委常委刘铁兵"
    },
    {
        "id": 5,
        "name": "陈祥瑞",
        "gender": "待查",
        "ethnicity": "汉族（推测）",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "香洲区委常委、区纪委书记、区监委主任",
        "current_org": "中共珠海市香洲区纪律检查委员会",
        "source": "www.zhxz.gov.cn 领导之窗—区委常委陈祥瑞"
    },
    {
        "id": 6,
        "name": "高晓燕",
        "gender": "女（推测）",
        "ethnicity": "汉族（推测）",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "香洲区委常委、区委宣传部部长",
        "current_org": "中共珠海市香洲区委员会",
        "source": "www.zhxz.gov.cn 领导之窗—区委常委高晓燕"
    },
    {
        "id": 7,
        "name": "李志刚",
        "gender": "待查",
        "ethnicity": "汉族（推测）",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "香洲区委常委、区委组织部部长",
        "current_org": "中共珠海市香洲区委员会",
        "source": "www.zhxz.gov.cn 领导之窗—区委常委李志刚"
    },
    {
        "id": 8,
        "name": "吴浩涛",
        "gender": "待查",
        "ethnicity": "汉族（推测）",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "香洲区委常委、常务副区长",
        "current_org": "香洲区人民政府",
        "source": "www.zhxz.gov.cn 领导之窗—区委常委吴浩涛"
    },
    {
        "id": 9,
        "name": "梁洪波",
        "gender": "待查",
        "ethnicity": "汉族（推测）",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "香洲区委常委、区委统战部部长",
        "current_org": "中共珠海市香洲区委员会",
        "source": "www.zhxz.gov.cn 领导之窗—区委常委梁洪波"
    },
    {
        "id": 10,
        "name": "罗实",
        "gender": "待查",
        "ethnicity": "汉族（推测）",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "香洲区委常委、区委办主任",
        "current_org": "中共珠海市香洲区委员会",
        "source": "www.zhxz.gov.cn 领导之窗—区委常委罗实"
    },
    # ════════════════════════════════════════
    # 区政府副区长（非区委常委）
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "邓剑虹",
        "gender": "待查",
        "ethnicity": "汉族（推测）",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "香洲区副区长",
        "current_org": "香洲区人民政府",
        "source": "www.zhxz.gov.cn 领导之窗—副区长邓剑虹"
    },
    {
        "id": 12,
        "name": "魏恒",
        "gender": "待查",
        "ethnicity": "汉族（推测）",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "香洲区副区长",
        "current_org": "香洲区人民政府",
        "source": "www.zhxz.gov.cn 领导之窗—副区长魏恒"
    },
    {
        "id": 13,
        "name": "李磊",
        "gender": "待查",
        "ethnicity": "汉族（推测）",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "香洲区副区长",
        "current_org": "香洲区人民政府",
        "source": "www.zhxz.gov.cn 领导之窗—副区长李磊"
    },
    {
        "id": 14,
        "name": "陈继彬",
        "gender": "待查",
        "ethnicity": "汉族（推测）",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "香洲区副区长",
        "current_org": "香洲区人民政府",
        "source": "www.zhxz.gov.cn 领导之窗—副区长陈继彬"
    },
    {
        "id": 15,
        "name": "罗瑜",
        "gender": "待查",
        "ethnicity": "汉族（推测）",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "香洲区副区长",
        "current_org": "香洲区人民政府",
        "source": "www.zhxz.gov.cn 领导之窗—副区长罗瑜"
    },
    # ════════════════════════════════════════
    # 区人大
    # ════════════════════════════════════════
    {
        "id": 16,
        "name": "陈静",
        "gender": "待查",
        "ethnicity": "汉族（推测）",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "香洲区人大常委会主任",
        "current_org": "香洲区人大常委会",
        "source": "www.zhxz.gov.cn 领导之窗—区人大陈静"
    },
    # ════════════════════════════════════════
    # 区政协
    # ════════════════════════════════════════
    {
        "id": 17,
        "name": "容立雄",
        "gender": "待查",
        "ethnicity": "汉族（推测）",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "香洲区政协主席",
        "current_org": "香洲区政协",
        "source": "www.zhxz.gov.cn 领导之窗—区政协容立雄"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共珠海市香洲区委员会",
        "type": "党委",
        "level": "副厅级",
        "parent": "中共珠海市委员会",
        "location": "珠海市香洲区"
    },
    {
        "id": 2,
        "name": "香洲区人民政府",
        "type": "政府",
        "level": "副厅级",
        "parent": "珠海市人民政府",
        "location": "珠海市香洲区"
    },
    {
        "id": 3,
        "name": "中共珠海市香洲区纪律检查委员会",
        "type": "党委",
        "level": "副厅级",
        "parent": "中共珠海市纪律检查委员会、香洲区委",
        "location": "珠海市香洲区"
    },
    {
        "id": 4,
        "name": "香洲区人大常委会",
        "type": "人大",
        "level": "副厅级",
        "parent": "珠海市人大常委会",
        "location": "珠海市香洲区"
    },
    {
        "id": 5,
        "name": "香洲区政协",
        "type": "政协",
        "level": "副厅级",
        "parent": "珠海市政协",
        "location": "珠海市香洲区"
    },
    {
        "id": 6,
        "name": "珠海保税区管委会",
        "type": "政府",
        "level": "正处级",
        "parent": "珠海市人民政府",
        "location": "珠海市香洲区"
    },
    {
        "id": 7,
        "name": "中共珠海市委员会",
        "type": "党委",
        "level": "副省级",
        "parent": "中共广东省委",
        "location": "珠海市"
    },
    {
        "id": 8,
        "name": "珠海市人民政府",
        "type": "政府",
        "level": "副省级",
        "parent": "广东省人民政府",
        "location": "珠海市"
    },
]

# 3. Positions
positions = [
    # 刘力 — 区委书记
    {"person_id": 1, "org_id": 7, "title": "珠海市委常委", "start": "待查", "end": "present", "rank": "正厅级", "note": "刘力兼任珠海市委常委"},
    {"person_id": 1, "org_id": 1, "title": "香洲区委书记", "start": "待查", "end": "present", "rank": "副厅级", "note": "主持区委全面工作"},
    # 张会洋 — 区长
    {"person_id": 2, "org_id": 1, "title": "香洲区委副书记", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "香洲区政府党组书记、区长", "start": "待查", "end": "present", "rank": "副厅级", "note": "主持区政府全面工作"},
    {"person_id": 2, "org_id": 6, "title": "保税区管委会主任", "start": "待查", "end": "present", "rank": "正处级", "note": "兼保税区管委会主任"},
    # 蓝璋 — 区委副书记（专职）
    {"person_id": 3, "org_id": 1, "title": "香洲区委副书记（专职）", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    # 刘铁兵 — 政法委书记
    {"person_id": 4, "org_id": 1, "title": "香洲区委常委、政法委书记", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    # 陈祥瑞 — 纪委书记
    {"person_id": 5, "org_id": 1, "title": "香洲区委常委", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "香洲区纪委书记、区监委主任", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    # 高晓燕 — 宣传部部长
    {"person_id": 6, "org_id": 1, "title": "香洲区委常委、宣传部部长", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    # 李志刚 — 组织部部长
    {"person_id": 7, "org_id": 1, "title": "香洲区委常委、组织部部长", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    # 吴浩涛 — 常务副区长
    {"person_id": 8, "org_id": 1, "title": "香洲区委常委", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "香洲区常务副区长", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    # 梁洪波 — 统战部部长
    {"person_id": 9, "org_id": 1, "title": "香洲区委常委、统战部部长", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    # 罗实 — 区委办主任
    {"person_id": 10, "org_id": 1, "title": "香洲区委常委、区委办主任", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    # 副区长
    {"person_id": 11, "org_id": 2, "title": "香洲区副区长", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "香洲区副区长", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "香洲区副区长", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "香洲区副区长", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "香洲区副区长", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
    # 人大
    {"person_id": 16, "org_id": 4, "title": "香洲区人大常委会主任", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    # 政协
    {"person_id": 17, "org_id": 5, "title": "香洲区政协主席", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
]

# 4. Relationships
relationships = [
    # 刘力 ↔ 张会洋 — 党政搭档
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "香洲区委书记与区长党政搭档（刘力任市委常委屈高位配置）",
        "overlap_org": "香洲区",
        "overlap_period": "刘力任区委书记、张会洋任区长期间",
    },
    # 刘力 → 蓝璋 — 上下级
    {
        "person_a": 1, "person_b": 3, "type": "superior_subordinate",
        "context": "区委书记与专职副书记",
        "overlap_org": "中共香洲区委", "overlap_period": "当前"
    },
    # 刘力 → 各常委 — 上级
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "区委书记与政法委书记", "overlap_org": "中共香洲区委", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "区委书记与纪委书记", "overlap_org": "中共香洲区委", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "区委书记与宣传部部长", "overlap_org": "中共香洲区委", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "区委书记与组织部部长", "overlap_org": "中共香洲区委", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "区委书记与常务副区长", "overlap_org": "中共香洲区委", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "区委书记与统战部部长", "overlap_org": "中共香洲区委", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "区委书记与区委办主任", "overlap_org": "中共香洲区委", "overlap_period": "当前"},
    # 张会洋 → 各副区长 — 上下级
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "区长与常务副区长", "overlap_org": "香洲区人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "香洲区人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "香洲区人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "香洲区人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "香洲区人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "香洲区人民政府", "overlap_period": "当前"},
    # 吴浩涛（常务副区长）→ 各副区长 — 班子同僚
    {"person_a": 8, "person_b": 11, "type": "overlap", "context": "常务副区长与副区长（班子同僚）", "overlap_org": "香洲区人民政府", "overlap_period": "当前"},
    {"person_a": 8, "person_b": 12, "type": "overlap", "context": "常务副区长与副区长（班子同僚）", "overlap_org": "香洲区人民政府", "overlap_period": "当前"},
    {"person_a": 8, "person_b": 13, "type": "overlap", "context": "常务副区长与副区长（班子同僚）", "overlap_org": "香洲区人民政府", "overlap_period": "当前"},
    {"person_a": 8, "person_b": 14, "type": "overlap", "context": "常务副区长与副区长（班子同僚）", "overlap_org": "香洲区人民政府", "overlap_period": "当前"},
    {"person_a": 8, "person_b": 15, "type": "overlap", "context": "常务副区长与副区长（班子同僚）", "overlap_org": "香洲区人民政府", "overlap_period": "当前"},
    # 党委委员之间 — 常委会同僚
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "区委常委同僚（政法+纪委）", "overlap_org": "中共香洲区委", "overlap_period": "当前"},
    {"person_a": 6, "person_b": 7, "type": "overlap", "context": "区委常委同僚（宣传+组织）", "overlap_org": "中共香洲区委", "overlap_period": "当前"},
    {"person_a": 9, "person_b": 10, "type": "overlap", "context": "区委常委同僚（统战+区委办）", "overlap_org": "中共香洲区委", "overlap_period": "当前"},
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
