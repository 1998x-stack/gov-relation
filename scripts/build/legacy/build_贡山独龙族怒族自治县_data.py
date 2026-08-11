#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
贡山独龙族怒族自治县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 云南省
Parent City: 怒江傈僳族自治州
Region: 贡山独龙族怒族自治县
Targets: 县委书记 & 县长

Current Leaders (as of 2026-07-28, from official website www.gongshan.gov.cn):
  县委书记: 杨秀兴 (confirmed by multiple 2026-07 articles)
  县委副书记、代理县长: 张文芳 (confirmed by official resume page, 2026-04-10)
  县委常委、常务副县长: 普云春 (confirmed by 2026-07-16 article)

Previous Leaders:
  前县长: 李勇 (confirmed by 2026-01-09 article — still in office as of Jan 2026)
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "贡山独龙族怒族自治县"
NOW = datetime.now().strftime("%Y-%m-%d")

# ─── PERSONS ──────────────────────────────────────────────────────────

persons = [
    # ── Top Leaders ──
    {
        "id": 1,
        "name": "杨秀兴",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共贡山独龙族怒族自治县委员会",
        "source": "www.gongshan.gov.cn — 2026年7月多篇报道以县委书记身份主持常委会、调研",
    },
    {
        "id": 2,
        "name": "张文芳",
        "gender": "女",
        "ethnicity": "怒族",
        "birth": "1979年9月",
        "birthplace": "",
        "education": "中央党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、代理县长",
        "current_org": "贡山独龙族怒族自治县人民政府",
        "source": "www.gongshan.gov.cn — 2026-04-10 简历页 /html/xzf/ldxx/",
    },

    # ── Predecessors ──
    {
        "id": 3,
        "name": "李勇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原贡山县长（2026年1月仍在任）",
        "current_org": "贡山独龙族怒族自治县人民政府",
        "source": "www.gongshan.gov.cn — 2026-01-09 article: 李勇主持第75次常务会议 / 2025-12-17 article: 李勇主持第74次常务会议",
    },

    # ── County Government Leaders (from /html/xzf page) ──
    {
        "id": 4,
        "name": "普云春",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "贡山独龙族怒族自治县人民政府",
        "source": "www.gongshan.gov.cn — 2026-07-16 article: 普云春以县委常委、常务副县长身份主持会议",
    },
    {
        "id": 5,
        "name": "李俊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "贡山独龙族怒族自治县人民政府",
        "source": "www.gongshan.gov.cn — 政府领导页面 /html/xzf",
    },
    {
        "id": 6,
        "name": "廖琦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "贡山独龙族怒族自治县人民政府",
        "source": "www.gongshan.gov.cn — 政府领导页面 /html/xzf",
    },
    {
        "id": 7,
        "name": "郗磊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "贡山独龙族怒族自治县人民政府",
        "source": "www.gongshan.gov.cn — 政府领导页面 /html/xzf",
    },
    {
        "id": 8,
        "name": "李跃东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "贡山独龙族怒族自治县人民政府",
        "source": "www.gongshan.gov.cn — 政府领导页面 /html/xzf",
    },
    {
        "id": 9,
        "name": "李正平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "贡山独龙族怒族自治县人民政府",
        "source": "www.gongshan.gov.cn — 政府领导页面 /html/xzf",
    },
    {
        "id": 10,
        "name": "和斐",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "贡山独龙族怒族自治县人民政府",
        "source": "www.gongshan.gov.cn — 政府领导页面 /html/xzf",
    },
    {
        "id": 11,
        "name": "密贵才",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "贡山独龙族怒族自治县人民政府",
        "source": "www.gongshan.gov.cn — 政府领导页面 /html/xzf",
    },
    {
        "id": 12,
        "name": "和蓉",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "贡山独龙族怒族自治县人民政府",
        "source": "www.gongshan.gov.cn — 政府领导页面 /html/xzf",
    },
]

# ─── ORGANIZATIONS ────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共贡山独龙族怒族自治县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共怒江傈僳族自治州委员会",
        "location": "云南省怒江傈僳族自治州贡山独龙族怒族自治县",
    },
    {
        "id": 2,
        "name": "贡山独龙族怒族自治县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "怒江傈僳族自治州人民政府",
        "location": "云南省怒江傈僳族自治州贡山独龙族怒族自治县",
    },
    {
        "id": 3,
        "name": "贡山独龙族怒族自治县人大常委会",
        "type": "人大",
        "level": "县",
        "parent": "怒江傈僳族自治州",
        "location": "云南省怒江傈僳族自治州贡山独龙族怒族自治县",
    },
    {
        "id": 4,
        "name": "贡山独龙族怒族自治县政协委员会",
        "type": "政协",
        "level": "县",
        "parent": "怒江傈僳族自治州",
        "location": "云南省怒江傈僳族自治州贡山独龙族怒族自治县",
    },
]

# ─── POSITIONS ────────────────────────────────────────────────────────

positions = [
    # Top leaders at county party committee
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "unknown", "end": "present", "rank": "正处级", "note": "十四届县委，2026年7月主持第3次常委会"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "代理县长", "start": "2026年初", "end": "present", "rank": "正处级", "note": "县人民政府党组书记、副县长、代理县长"},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "常务副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},

    # Previous leaders
    {"person_id": 3, "org_id": 2, "title": "县长", "start": "unknown", "end": "2026年初", "rank": "正处级", "note": "2025年12月-2026年1月仍在任，后去职"},

    # County government deputies
    {"person_id": 5, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
]

# ─── RELATIONSHIPS ────────────────────────────────────────────────────

relationships = [
    # Top leadership core
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与代理县长，党政一把手", "overlap_org": "中共贡山独龙族怒族自治县委员会", "overlap_period": "2026（推定）"},

    # Party committee leadership
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记与常务副县长，县委常委班子", "overlap_org": "中共贡山独龙族怒族自治县委员会", "overlap_period": "2026（推定）"},

    # Government team
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "代理县长与常务副县长，政府领导", "overlap_org": "贡山独龙族怒族自治县人民政府", "overlap_period": "2026（推定）"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "代理县长与副县长，政府领导", "overlap_org": "贡山独龙族怒族自治县人民政府", "overlap_period": "2026（推定）"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "代理县长与副县长，政府领导", "overlap_org": "贡山独龙族怒族自治县人民政府", "overlap_period": "2026（推定）"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "代理县长与副县长，政府领导", "overlap_org": "贡山独龙族怒族自治县人民政府", "overlap_period": "2026（推定）"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "代理县长与副县长，政府领导", "overlap_org": "贡山独龙族怒族自治县人民政府", "overlap_period": "2026（推定）"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "代理县长与副县长，政府领导", "overlap_org": "贡山独龙族怒族自治县人民政府", "overlap_period": "2026（推定）"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "代理县长与副县长，政府领导", "overlap_org": "贡山独龙族怒族自治县人民政府", "overlap_period": "2026（推定）"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "代理县长与副县长，政府领导", "overlap_org": "贡山独龙族怒族自治县人民政府", "overlap_period": "2026（推定）"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "代理县长与副县长，政府领导", "overlap_org": "贡山独龙族怒族自治县人民政府", "overlap_period": "2026（推定）"},

    # Predecessor-successor
    {"person_a": 3, "person_b": 2, "type": "predecessor_successor", "context": "前县长李勇与代理县长张文芳交接", "overlap_org": "贡山独龙族怒族自治县人民政府", "overlap_period": "2026年初"},

    # County government peers
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "副县长之间同级共事", "overlap_org": "贡山独龙族怒族自治县人民政府", "overlap_period": "2026（推定）"},
    {"person_a": 5, "person_b": 7, "type": "overlap", "context": "副县长之间同级共事", "overlap_org": "贡山独龙族怒族自治县人民政府", "overlap_period": "2026（推定）"},
    {"person_a": 8, "person_b": 9, "type": "overlap", "context": "副县长之间同级共事", "overlap_org": "贡山独龙族怒族自治县人民政府", "overlap_period": "2026（推定）"},
    {"person_a": 10, "person_b": 11, "type": "overlap", "context": "副县长之间同级共事", "overlap_org": "贡山独龙族怒族自治县人民政府", "overlap_period": "2026（推定）"},
]

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
STAGING_DIR = os.path.join(REPO_ROOT, "data/tmp/yunnan_贡山独龙族怒族自治县")
DB_PATH = os.path.join(STAGING_DIR, "贡山独龙族怒族自治县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "贡山独龙族怒族自治县_network.gexf")

if __name__ == "__main__":
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

    print("\n=== Build Complete ===")
    print(f"Database: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"Persons: {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")