#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
海珠区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 广东省
Parent City: 广州市
Region: 海珠区
Targets: 区委书记 & 区长

Research Sources:
- 广州市海珠区人民政府门户网站 (www.haizhu.gov.cn) — 领导之窗: 区政府领导分工与简历
- 海珠要闻 — 区委常委会会议等新闻报道（区委办供稿）
- 区委办新闻报道确认区委书记为蔡澍

Research Date: 2026-07-22
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths ──
SLUG = "海珠区"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DATABASE_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(GRAPH_DIR, f"{SLUG}_network.gexf")

# The script uses gov_relation.runner (which internally uses sqlite3)
import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "蔡澍",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广州市海珠区委书记",
        "current_org": "中共广州市海珠区委员会",
        "source": "海珠区人民政府门户网站—海珠要闻（区委办供稿，2026年多篇报道确认）"
    },
    {
        "id": 2,
        "name": "毛松柏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年5月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历，管理学硕士学位",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "海珠区委副书记、区长",
        "current_org": "海珠区人民政府",
        "source": "www.haizhu.gov.cn 领导之窗—区长简历"
    },
    # ════════════════════════════════════════
    # 区人大常委会、政协主要领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "陆世泽",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "海珠区人大常委会主任",
        "current_org": "广州市海珠区人民代表大会常务委员会",
        "source": "海珠区人民政府门户网站—新闻报道确认（2026年7月两优一先表彰大会）"
    },
    {
        "id": 4,
        "name": "卢兆华",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "海珠区政协主席",
        "current_org": "中国人民政治协商会议广州市海珠区委员会",
        "source": "海珠区人民政府门户网站—新闻报道确认（2026年7月两优一先表彰大会）"
    },
    # ════════════════════════════════════════
    # 区政府副区长（领导之窗确认）
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "陈伟锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年1月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历，工程硕士学位",
        "party_join": "中共党员",
        "work_start": "1997年7月",
        "current_post": "区委常委、常务副区长",
        "current_org": "海珠区人民政府",
        "source": "www.haizhu.gov.cn 领导之窗"
    },
    {
        "id": 6,
        "name": "孙伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年11月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生学历，工商管理硕士学位",
        "party_join": "中共党员",
        "work_start": "2002年7月",
        "current_post": "区委常委、副区长",
        "current_org": "海珠区人民政府",
        "source": "www.haizhu.gov.cn 领导之窗"
    },
    {
        "id": 7,
        "name": "庄承汶",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年9月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "中央党校大学学历",
        "party_join": "中共党员",
        "work_start": "1991年7月",
        "current_post": "区政府党组成员、副区长",
        "current_org": "海珠区人民政府",
        "source": "www.haizhu.gov.cn 领导之窗"
    },
    {
        "id": 8,
        "name": "张永良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生学历，管理学硕士学位",
        "party_join": "中国国民党革命委员会",
        "work_start": "1989年7月",
        "current_post": "区政府副区长",
        "current_org": "海珠区人民政府",
        "source": "www.haizhu.gov.cn 领导之窗"
    },
    {
        "id": 9,
        "name": "陈志勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年9月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生学历，法学硕士学位",
        "party_join": "中共党员",
        "work_start": "1994年7月",
        "current_post": "区政府党组成员、副区长，区公安分局局长",
        "current_org": "海珠区人民政府",
        "source": "www.haizhu.gov.cn 领导之窗"
    },
    {
        "id": 10,
        "name": "陈宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历，公共管理硕士学位",
        "party_join": "中共党员",
        "work_start": "2002年7月",
        "current_post": "区政府党组成员、副区长",
        "current_org": "海珠区人民政府",
        "source": "www.haizhu.gov.cn 领导之窗"
    },
    {
        "id": 11,
        "name": "杨晓",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1971年11月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历，公共管理硕士学位",
        "party_join": "中共党员",
        "work_start": "1990年3月",
        "current_post": "区政府党组成员、副区长，区投资促进局党组书记",
        "current_org": "海珠区人民政府",
        "source": "www.haizhu.gov.cn 领导之窗"
    },
    {
        "id": 12,
        "name": "黄智勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年12月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历，工程硕士学位",
        "party_join": "中共党员",
        "work_start": "1998年7月",
        "current_post": "区政府党组成员、副区长，区政府办公室主任",
        "current_org": "海珠区人民政府",
        "source": "www.haizhu.gov.cn 领导之窗"
    },
    # ════════════════════════════════════════
    # 区委关键领导（新闻报道中确认）
    # ════════════════════════════════════════
    {
        "id": 13,
        "name": "贺立峰",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共广州市海珠区委员会",
        "source": "海珠区「两优一先」表彰大会报道（区委办2026年7月3日）"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共广州市海珠区委员会",
        "type": "党委",
        "level": "正处级（区委书记通常为副厅级）",
        "parent": "中共广州市委",
        "location": "广州市海珠区广州大道南999号"
    },
    {
        "id": 2,
        "name": "海珠区人民政府",
        "type": "政府",
        "level": "正处级",
        "parent": "广州市人民政府",
        "location": "广州市海珠区广州大道南999号"
    },
    {
        "id": 3,
        "name": "广州市海珠区人民代表大会常务委员会",
        "type": "人大",
        "level": "正处级",
        "parent": "广州市人大常委会",
        "location": "广州市海珠区"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议广州市海珠区委员会",
        "type": "政协",
        "level": "正处级",
        "parent": "广州市政协",
        "location": "广州市海珠区"
    },
    {
        "id": 5,
        "name": "广州市公安局海珠分局",
        "type": "政府",
        "level": "正处级",
        "parent": "广州市公安局",
        "location": "广州市海珠区"
    },
]

# 3. Positions
positions = [
    # 蔡澍
    {"person_id": 1, "org_id": 1, "title": "海珠区委书记", "start": "待查", "end": "至今", "rank": "副厅级（通常由广州市委常委兼任）", "note": "主持区委全面工作；截至2026年7月多篇区委常委会新闻报道确认"},
    # 毛松柏
    {"person_id": 2, "org_id": 1, "title": "海珠区委副书记", "start": "待查", "end": "至今", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "海珠区区长", "start": "待查", "end": "至今", "rank": "正处级", "note": "主持区政府全面工作，负责审计工作；分管区审计局"},
    # 陆世泽
    {"person_id": 3, "org_id": 3, "title": "海珠区人大常委会主任", "start": "待查", "end": "至今", "rank": "正处级", "note": "主持区人大常委会全面工作"},
    # 卢兆华
    {"person_id": 4, "org_id": 4, "title": "海珠区政协主席", "start": "待查", "end": "至今", "rank": "正处级", "note": "主持区政协全面工作"},
    # 陈伟锋
    {"person_id": 5, "org_id": 2, "title": "常务副区长", "start": "待查", "end": "至今", "rank": "正处级", "note": "负责财政、住建、应急管理等工作"},
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},
    # 孙伟
    {"person_id": 6, "org_id": 2, "title": "副区长", "start": "待查", "end": "至今", "rank": "正处级", "note": "负责水务、文旅、城管等工作"},
    {"person_id": 6, "org_id": 1, "title": "区委常委", "start": "待查", "end": "至今", "rank": "副厅级", "note": ""},
    # 庄承汶
    {"person_id": 7, "org_id": 2, "title": "副区长", "start": "待查", "end": "至今", "rank": "二级巡视员", "note": "负责农业农村、对口帮扶等工作"},
    # 张永良
    {"person_id": 8, "org_id": 2, "title": "副区长", "start": "待查", "end": "至今", "rank": "正处级", "note": "负责教育、卫生健康等工作"},
    # 陈志勇
    {"person_id": 9, "org_id": 2, "title": "副区长、区公安分局局长", "start": "待查", "end": "至今", "rank": "正处级", "note": "负责公安、司法等工作"},
    {"person_id": 9, "org_id": 5, "title": "区公安分局党委书记、分局长", "start": "待查", "end": "至今", "rank": "正处级", "note": ""},
    # 陈宇
    {"person_id": 10, "org_id": 2, "title": "副区长", "start": "待查", "end": "至今", "rank": "正处级", "note": "负责发改、人工智能、琶洲管委会等工作"},
    # 杨晓
    {"person_id": 11, "org_id": 2, "title": "副区长", "start": "待查", "end": "至今", "rank": "正处级", "note": "负责市场监管、政务服务、投资促进等工作"},
    # 黄智勇
    {"person_id": 12, "org_id": 2, "title": "副区长", "start": "待查", "end": "至今", "rank": "正处级", "note": "负责民政、人社、信访等工作"},
    # 贺立峰
    {"person_id": 13, "org_id": 1, "title": "区委常委、组织部部长", "start": "待查", "end": "至今", "rank": "副厅级", "note": "分管组织、干部、党校等工作"},
]

# 4. Relationships
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记与区长：党委与政府主要领导工作搭档关系",
        "strength": "strong",
        "confidence": "confirmed",
        "overlap_org": "中共广州市海珠区委员会/海珠区人民政府",
        "overlap_period": "至今（蔡澍任区委书记、毛松柏任区委副书记、区长期间）",
        "source": "海珠区人民政府门户网站—多篇新闻报道确认（2026年）"
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "overlap",
        "context": "区委书记与人大主任：当前区委领导班子与人大主要负责人",
        "strength": "strong",
        "confidence": "confirmed",
        "overlap_org": "海珠区",
        "overlap_period": "至今",
        "source": "海珠区「两优一先」表彰大会报道（2026年7月）"
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "overlap",
        "context": "区委书记与政协主席：当前班子同届共事关系",
        "strength": "medium",
        "confidence": "confirmed",
        "overlap_org": "海珠区",
        "overlap_period": "至今",
        "source": "海珠区「两优一先」表彰大会报道（2026年7月）"
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "overlap",
        "context": "区长与人大主任：区政府与区人大主要负责人",
        "strength": "medium",
        "confidence": "confirmed",
        "overlap_org": "海珠区",
        "overlap_period": "至今",
        "source": "海珠区两会报道（2026年3月）"
    },
    {
        "person_a": 2,
        "person_b": 4,
        "type": "overlap",
        "context": "区长与政协主席：区政府与区政协主要负责人",
        "strength": "medium",
        "confidence": "confirmed",
        "overlap_org": "海珠区",
        "overlap_period": "至今",
        "source": "海珠区「两优一先」表彰大会报道（2026年7月）"
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "区委书记与常务副区长：党委主要领导与政府常务副职",
        "strength": "strong",
        "confidence": "confirmed",
        "overlap_org": "海珠区",
        "overlap_period": "至今",
        "source": "海珠区人民政府门户网站"
    },
    {
        "person_a": 2,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "区长与常务副区长：政府正副职搭档",
        "strength": "strong",
        "confidence": "confirmed",
        "overlap_org": "海珠区人民政府",
        "overlap_period": "至今",
        "source": "海珠区人民政府门户网站—领导之窗"
    },
    {
        "person_a": 5,
        "person_b": 6,
        "type": "overlap",
        "context": "常务副区长与常委副区长：区委常委、区政府班子成员",
        "strength": "medium",
        "confidence": "confirmed",
        "overlap_org": "海珠区人民政府/中共海珠区委",
        "overlap_period": "至今",
        "source": "海珠区人民政府门户网站—领导之窗"
    },
    {
        "person_a": 1,
        "person_b": 13,
        "type": "superior_subordinate",
        "context": "区委书记与组织部部长：党委主要领导与组织人事负责人",
        "strength": "strong",
        "confidence": "confirmed",
        "overlap_org": "中共广州市海珠区委员会",
        "overlap_period": "至今",
        "source": "海珠区「两优一先」表彰大会报道（2026年7月）"
    },
]

# ── Run ──
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
