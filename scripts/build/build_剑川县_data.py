#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
剑川县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 县
Province: 云南省
Parent City: 大理白族自治州
Region: 剑川县
Targets: 县委书记 & 县长

Current Leaders (as of 2026-07-28, from official website www.jianchuan.gov.cn):
   县委书记: 李增堂 (白族, 1972.02生, 来源: 百度百科/剑川县人民政府2023年通报)
   县委副书记、县长: 郑巍黎 (1978.08, 湖北当阳, 研究生, 2000.10入党, 2005.08工作)
   县委常委、常务副县长: 赵盛海 (1983.06, 云南剑川, 省委党校研究生, 2007.01入党, 2007.12工作)
   副县长(公安局长): 陈绩 (1980.09, 云南南涧, 省委党校研究生)
   副县长: 代磊 (1988.03, 云南宾川, 大学)
   副县长: 杨福堂 (1981.01, 云南剑川, 无党派, 中国地质大学)
   副县长: 李红宇 (1981.05, 云南大理, 拉祜族, 女, 省委党校研究生)
   副县长: 李志军 (1979.12, 云南剑川, 研究生, 2004.11入党, 2000.12工作)
   副县长(挂职): 陆伟 (1985.07, 上海浦东)
   副县长(挂职): 门永强 (1970.10, 甘肃宁县)
   县人大常委会主任: 张益儒 (来源: 剑川县第十八届人民代表大会)
   政协主席: 苏育新 (来源: 剑川县政协)
Predecessor chain:
   聂金辉 (剑川县委书记 ~2016.03-2021.08) → 怒江州纪委书记 → 丽江市委副书记、市长
   李增堂 succeeded 聂金辉 as 县委书记 (sometime 2021-2023)
   张韬 (former 县长, received 党内严重警告 2023.03, replaced)
   郑巍黎 succeeded 张韬 as 县长 (2026.05 appointed)

Data Date: 2026-07-28
"""

import json
import os
import sqlite3  # used via runner internally
import sys
from datetime import datetime
from pathlib import Path

# ── Ensure gov_relation is importable ──
_REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# ── Paths ──
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "剑川县"
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR / "persons"

AS_OF = "2026-07-28"
TODAY = AS_OF

# ═══════════════════════════════════════════════════════════════
# 1. PERSONS
# ═══════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 核心领导：县委书记
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "李增堂",
        "gender": "男",
        "ethnicity": "白族",
        "birth": "1972.02",
        "birthplace": "云南省",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "剑川县委书记",
        "current_org": "中共剑川县委",
        "source": "百度百科; 剑川县2023年培训违规饮酒通报; 剑川县第十八届委员会",
    },
    # ════════════════════════════════════════
    # 核心领导：县长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "郑巍黎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978.08",
        "birthplace": "湖北当阳",
        "education": "研究生学历",
        "party_join": "2000.10",
        "work_start": "2005.08",
        "current_post": "县委副书记、县人民政府县长",
        "current_org": "剑川县人民政府",
        "source": "https://www.jianchuan.gov.cn/jcxrmzf/c00001/pc/content/2056987605382254592/content_2056987605382254592.html",
    },
    # ════════════════════════════════════════
    # 常务副县长
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "赵盛海",
        "gender": "男",
        "ethnicity": "白族",
        "birth": "1983.06",
        "birthplace": "云南剑川",
        "education": "云南省委党校研究生学历",
        "party_join": "2007.01",
        "work_start": "2007.12",
        "current_post": "县委常委、常务副县长",
        "current_org": "剑川县人民政府",
        "source": "https://www.jianchuan.gov.cn/jcxrmzf/c00002/pc/content/2044960950157631488/content_2044960950157631488.html",
    },
    # ════════════════════════════════════════
    # 副县长
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "陈绩",
        "gender": "男",
        "ethnicity": "",
        "birth": "1980.09",
        "birthplace": "云南南涧",
        "education": "省委党校研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "剑川县人民政府",
        "source": "https://www.jianchuan.gov.cn/jcxrmzf/c102073/pc/list.html",
    },
    {
        "id": 5,
        "name": "代磊",
        "gender": "男",
        "ethnicity": "",
        "birth": "1988.03",
        "birthplace": "云南宾川",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "剑川县人民政府",
        "source": "https://www.jianchuan.gov.cn/jcxrmzf/c102073/pc/list.html",
    },
    {
        "id": 6,
        "name": "杨福堂",
        "gender": "男",
        "ethnicity": "",
        "birth": "1981.01",
        "birthplace": "云南剑川",
        "education": "中国地质大学本科",
        "party_join": "",  # 无党派
        "work_start": "",
        "current_post": "副县长",
        "current_org": "剑川县人民政府",
        "source": "https://www.jianchuan.gov.cn/jcxrmzf/c102073/pc/list.html",
    },
    {
        "id": 7,
        "name": "李红宇",
        "gender": "女",
        "ethnicity": "拉祜族",
        "birth": "1981.05",
        "birthplace": "云南大理",
        "education": "省委党校研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "剑川县人民政府",
        "source": "https://www.jianchuan.gov.cn/jcxrmzf/c102073/pc/list.html",
    },
    {
        "id": 8,
        "name": "李志军",
        "gender": "男",
        "ethnicity": "白族",
        "birth": "1979.12",
        "birthplace": "云南剑川",
        "education": "研究生学历",
        "party_join": "2004.11",
        "work_start": "2000.12",
        "current_post": "副县长",
        "current_org": "剑川县人民政府",
        "source": "https://www.jianchuan.gov.cn/jcxrmzf/c00003/pc/content/1993917074123100160/content_1993917074123100160.html",
    },
    {
        "id": 9,
        "name": "陆伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "1985.07",
        "birthplace": "上海市浦东新区",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长（挂职）",
        "current_org": "剑川县人民政府",
        "source": "https://www.jianchuan.gov.cn/jcxrmzf/c102073/pc/list.html",
    },
    {
        "id": 10,
        "name": "门永强",
        "gender": "男",
        "ethnicity": "",
        "birth": "1970.10",
        "birthplace": "甘肃宁县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长（挂职）",
        "current_org": "剑川县人民政府",
        "source": "https://www.jianchuan.gov.cn/jcxrmzf/c102073/pc/list.html",
    },
    # ════════════════════════════════════════
    # 人大、政协
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "张益儒",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "剑川县人大常委会",
        "source": "百度百科剑川县词条",
    },
    {
        "id": 12,
        "name": "苏育新",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "政协剑川县委员会",
        "source": "百度百科剑川县词条",
    },
    # ════════════════════════════════════════
    # 前任领导
    # ════════════════════════════════════════
    {
        "id": 13,
        "name": "聂金辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "丽江市委副书记、市长",  # current position
        "current_org": "中共丽江市委",
        "source": "百度百科; 丽江市政府网站",
    },
    {
        "id": 14,
        "name": "张韬",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（原剑川县县长，2023年受处分）",
        "current_org": "",
        "source": "云南省纪委监委通报 2023.03",
    },
]

# ═══════════════════════════════════════════════════════════════
# 2. ORGANIZATIONS
# ═══════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共剑川县委",
        "type": "党委",
        "level": "县",
        "parent": "中共大理州委",
        "location": "云南省大理白族自治州剑川县",
    },
    {
        "id": 2,
        "name": "剑川县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "大理白族自治州人民政府",
        "location": "云南省大理白族自治州剑川县",
    },
    {
        "id": 3,
        "name": "剑川县人大常委会",
        "type": "人大",
        "level": "县",
        "parent": "大理州人大常委会",
        "location": "云南省大理白族自治州剑川县",
    },
    {
        "id": 4,
        "name": "政协剑川县委员会",
        "type": "政协",
        "level": "县",
        "parent": "政协大理州委员会",
        "location": "云南省大理白族自治州剑川县",
    },
    {
        "id": 5,
        "name": "剑川县公安局",
        "type": "政府",
        "level": "县",
        "parent": "剑川县人民政府",
        "location": "云南省大理白族自治州剑川县",
    },
    {
        "id": 6,
        "name": "中共鹤庆县委",
        "type": "党委",
        "level": "县",
        "parent": "中共大理州委",
        "location": "云南省大理白族自治州鹤庆县",
    },
    {
        "id": 7,
        "name": "中共怒江州纪律检查委员会",
        "type": "党委",
        "level": "地市",
        "parent": "中共怒江州委",
        "location": "云南省怒江傈僳族自治州",
    },
    {
        "id": 8,
        "name": "中共丽江市委",
        "type": "党委",
        "level": "地市",
        "parent": "中共云南省委",
        "location": "云南省丽江市",
    },
    {
        "id": 9,
        "name": "大理白族自治州委组织部",
        "type": "党委",
        "level": "地市",
        "parent": "中共大理州委",
        "location": "云南省大理白族自治州",
    },
]

# ═══════════════════════════════════════════════════════════════
# 3. POSITIONS
# ═══════════════════════════════════════════════════════════════

positions = [
    # 李增堂
    {"person_id": 1, "org_id": 1, "title": "剑川县委书记", "start": "~2021", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 6, "title": "鹤庆县副县长/县委副书记", "start": "", "end": "", "rank": "", "note": "据百度百科"},
    {"person_id": 1, "org_id": 9, "title": "大理州委组织部常务副部长", "start": "", "end": "", "rank": "", "note": "据百度百科"},

    # 郑巍黎
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县人民政府县长", "start": "2026.05", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 6, "title": "鹤庆县委常委、常务副县长", "start": "", "end": "2026.05", "rank": "", "note": "升任剑川县县长"},

    # 赵盛海
    {"person_id": 3, "org_id": 2, "title": "县委常委、常务副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 陈绩
    {"person_id": 4, "org_id": 2, "title": "副县长、县公安局局长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 5, "title": "县公安局局长", "start": "", "end": "present", "rank": "", "note": "兼"},

    # 代磊
    {"person_id": 5, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 杨福堂
    {"person_id": 6, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "无党派"},

    # 李红宇
    {"person_id": 7, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "女, 拉祜族"},

    # 李志军
    {"person_id": 8, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 陆伟
    {"person_id": 9, "org_id": 2, "title": "副县长（挂职）", "start": "", "end": "present", "rank": "副处级", "note": "中国电建集团挂职"},

    # 门永强
    {"person_id": 10, "org_id": 2, "title": "副县长（挂职）", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 张益儒
    {"person_id": 11, "org_id": 3, "title": "县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},

    # 苏育新
    {"person_id": 12, "org_id": 4, "title": "县政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},

    # 聂金辉 - predecessor 县委书记
    {"person_id": 13, "org_id": 1, "title": "剑川县委书记", "start": "2016.03", "end": "2021.08", "rank": "正处级", "note": "全国优秀县委书记(2021)"},
    {"person_id": 13, "org_id": 7, "title": "怒江州县委常委、纪委书记", "start": "2021.08", "end": "", "rank": "副厅级", "note": ""},
    {"person_id": 13, "org_id": 8, "title": "丽江市委副书记、市长", "start": "2025.12", "end": "present", "rank": "正厅级", "note": ""},

    # 张韬 - predecessor 县长
    {"person_id": 14, "org_id": 2, "title": "剑川县县长", "start": "", "end": "2023", "rank": "正处级", "note": "2023.03因违规聚餐饮酒受党内严重警告"},
]

# ═══════════════════════════════════════════════════════════════
# 4. RELATIONSHIPS
# ═══════════════════════════════════════════════════════════════

relationships = [
    # 李增堂与郑巍黎 - 当前县委书记与县长 (上下级)
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "李增堂任县委书记时，郑巍黎任县长",
        "overlap_org": "剑川县",
        "overlap_period": "2026.05-",
    },
    # 李增堂与赵盛海 (上下级: 县委书记与县委常委)
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "李增堂任县委书记，赵盛海任县委常委",
        "overlap_org": "中共剑川县委",
        "overlap_period": "",
    },
    # 郑巍黎与赵盛海 (搭档 - 县长与常务副县长)
    {
        "person_a": 2,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "郑巍黎任县长，赵盛海任常务副县长",
        "overlap_org": "剑川县人民政府",
        "overlap_period": "2026.05-",
    },
    # 聂金辉与鞠增堂 - 前任后继任 (县委书记)
    {
        "person_a": 13,
        "person_b": 1,
        "type": "predecessor_successor",
        "context": "聂金辉离任剑川县委书记后，李增堂接任",
        "overlap_org": "中共剑川县委",
        "overlap_period": "2021-2022",
    },
    # 张韬与郑巍黎 - 前任后继任 (县长)
    {
        "person_a": 14,
        "person_b": 2,
        "type": "predecessor_successor",
        "context": "张韬受处分去职后，郑巍黎接任县长",
        "overlap_org": "剑川县人民政府",
        "overlap_period": "2023-2026",
    },
    # 郑巍黎与聂金辉 - 曾共同在中共大理州委工作过
    {
        "person_a": 2,
        "person_b": 13,
        "type": "overlap",
        "context": "郑巍黎与聂金辉先后在剑川县任职，时间上有交叉可能",
        "overlap_org": "剑川县",
        "overlap_period": "2021-2026",
        "strength": "weak",
    },
    # 赵盛海与李志军 - 同乡同在剑川任职
    {
        "person_a": 3,
        "person_b": 8,
        "type": "same_native_place",
        "context": "同为云南剑川人",
        "overlap_org": "",
        "overlap_period": "",
        "strength": "weak",
    },
    # 李增堂曾经担任的鹤庆县职务与郑巍黎的鹤庆县职务重叠
    {
        "person_a": 1,
        "person_b": 2,
        "type": "same_org_different_period",
        "context": "李增堂曾任鹤庆县领导，郑巍黎来自鹤庆县常务副县长",
        "overlap_org": "鹤庆县",
        "overlap_period": "",
        "strength": "weak",
    },
]

# ═══════════════════════════════════════════════════════════════
# 5. BUILD
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Building 剑川县 network database and graph...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")

    # Use the shared runner
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print(f"\n=== Build complete ===")
    print(f"  Persons:         {len(persons)}")
    print(f"  Organizations:   {len(organizations)}")
    print(f"  Positions:       {len(positions)}")
    print(f"  Relationships:   {len(relationships)}")
    print(f"  Database:        {DB_PATH}")
    print(f"  GEXF:            {GEXF_PATH}")

    # Verify outputs exist
    assert DB_PATH.exists(), f"Database not found: {DB_PATH}"
    assert GEXF_PATH.exists(), f"GEXF not found: {GEXF_PATH}"
    print("\n  ✅ Database and GEXF verified!")