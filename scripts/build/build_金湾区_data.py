#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
金湾区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 广东省
Parent City: 珠海市
Region: 金湾区
Targets: 区委书记 & 区长

Research Sources:
- 珠海市金湾区人民政府门户网站 (www.jinwan.gov.cn) — 领导之窗
- 维基百科 (zh.wikipedia.org) — 金湾区词条

Current status (as of 2026-07-22):
- 区委书记: 梁耀斌（区委书记）
- 区长: 刘军（区委副书记，区政府党组书记、区长）

Research Date: 2026-07-22
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "金湾区"
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
        "name": "梁耀斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年12月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职研究生学历、历史学硕士学位",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "金湾区委书记",
        "current_org": "中共珠海市金湾区委员会",
        "source": "www.jinwan.gov.cn 领导之窗—区委书记梁耀斌"
    },
    {
        "id": 2,
        "name": "刘军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年6月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职研究生学历，经济学硕士学位",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "金湾区委副书记，区政府党组书记、区长",
        "current_org": "金湾区人民政府",
        "source": "www.jinwan.gov.cn 领导之窗—区长刘军"
    },
    {
        "id": 3,
        "name": "庞前聪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生学历，工学博士学位",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "金湾区委副书记（挂任），西城街道党工委书记",
        "current_org": "中共珠海市金湾区委员会",
        "source": "www.jinwan.gov.cn 领导之窗—区委副书记庞前聪"
    },
    # ════════════════════════════════════════
    # 区委常委（不含书记、副书记）
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "姜学勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年11月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历，工学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "金湾区委常委",
        "current_org": "中共珠海市金湾区委员会",
        "source": "www.jinwan.gov.cn 领导之窗—区委常委姜学勇"
    },
    {
        "id": 5,
        "name": "梁永森",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年12月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "金湾区委常委、区纪委书记、区监委主任",
        "current_org": "中共珠海市金湾区纪律检查委员会",
        "source": "www.jinwan.gov.cn 领导之窗—区委常委梁永森"
    },
    {
        "id": 6,
        "name": "李邦耀",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年9月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生学历，公共管理硕士学位",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "金湾区委常委、区委组织部部长、区委党校校长",
        "current_org": "中共珠海市金湾区委员会",
        "source": "www.jinwan.gov.cn 领导之窗—区委常委李邦耀"
    },
    {
        "id": 7,
        "name": "高禄林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年1月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职研究生学历，公共管理硕士学位",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "金湾区委常委、区委宣传部部长",
        "current_org": "中共珠海市金湾区委员会",
        "source": "www.jinwan.gov.cn 领导之窗—区委常委高禄林"
    },
    {
        "id": 8,
        "name": "朱荣新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年1月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历，文学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "金湾区委常委、区委政法委书记",
        "current_org": "中共珠海市金湾区委员会",
        "source": "www.jinwan.gov.cn 领导之窗—区委常委朱荣新"
    },
    {
        "id": 9,
        "name": "苗奇峰",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982年8月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历，法学硕士学位",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "金湾区委常委，区政府党组副书记、副区长",
        "current_org": "金湾区人民政府",
        "source": "www.jinwan.gov.cn 领导之窗—区委常委苗奇峰"
    },
    {
        "id": 10,
        "name": "张涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年9月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历，工学学士学位",
        "party_join": "中共党员（2002年4月入党）",
        "work_start": "待查",
        "current_post": "金湾区委常委、区人民武装部上校部长",
        "current_org": "珠海市金湾区人民武装部",
        "source": "www.jinwan.gov.cn 领导之窗—区委常委张涛"
    },
    # ════════════════════════════════════════
    # 区人大
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "（待查）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "金湾区人大常委会主任",
        "current_org": "金湾区人大常委会",
        "source": "待查"
    },
    # ════════════════════════════════════════
    # 区政协
    # ════════════════════════════════════════
    {
        "id": 12,
        "name": "（待查）",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "金湾区政协主席",
        "current_org": "金湾区政协",
        "source": "待查"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共珠海市金湾区委员会",
        "type": "党委",
        "level": "副厅级",
        "parent": "中共珠海市委员会",
        "location": "珠海市金湾区"
    },
    {
        "id": 2,
        "name": "金湾区人民政府",
        "type": "政府",
        "level": "副厅级",
        "parent": "珠海市人民政府",
        "location": "珠海市金湾区"
    },
    {
        "id": 3,
        "name": "中共珠海市金湾区纪律检查委员会",
        "type": "党委",
        "level": "副厅级",
        "parent": "中共珠海市纪律检查委员会、金湾区委",
        "location": "珠海市金湾区"
    },
    {
        "id": 4,
        "name": "金湾区人大常委会",
        "type": "人大",
        "level": "副厅级",
        "parent": "珠海市人大常委会",
        "location": "珠海市金湾区"
    },
    {
        "id": 5,
        "name": "金湾区政协",
        "type": "政协",
        "level": "副厅级",
        "parent": "珠海市政协",
        "location": "珠海市金湾区"
    },
    {
        "id": 6,
        "name": "珠海市金湾区人民武装部",
        "type": "政府",
        "level": "正团级",
        "parent": "珠海警备区",
        "location": "珠海市金湾区"
    },
    {
        "id": 7,
        "name": "西城街道党工委",
        "type": "党委",
        "level": "正科级",
        "parent": "中共珠海市金湾区委员会",
        "location": "珠海市金湾区"
    },
    {
        "id": 8,
        "name": "中共珠海市委员会",
        "type": "党委",
        "level": "副省级",
        "parent": "中共广东省委",
        "location": "珠海市"
    },
    {
        "id": 9,
        "name": "珠海市人民政府",
        "type": "政府",
        "level": "副省级",
        "parent": "广东省人民政府",
        "location": "珠海市"
    },
    {
        "id": 10,
        "name": "珠海经济技术开发区管委会",
        "type": "政府",
        "level": "正厅级（推测）",
        "parent": "珠海市人民政府",
        "location": "珠海市金湾区"
    },
]

# 3. Positions
positions = [
    # 梁耀斌 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "金湾区委书记", "start": "待查", "end": "present", "rank": "副厅级", "note": "主持区委全面工作"},
    # 刘军 — 区长
    {"person_id": 2, "org_id": 1, "title": "金湾区委副书记", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "金湾区政府党组书记、区长", "start": "待查", "end": "present", "rank": "副厅级", "note": "主持区政府全面工作，负责审计工作"},
    # 庞前聪 — 区委副书记（挂任）
    {"person_id": 3, "org_id": 1, "title": "金湾区委副书记（挂任）", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 7, "title": "西城街道党工委书记", "start": "待查", "end": "present", "rank": "正科级", "note": "负责西部城市中心建设开发"},
    # 姜学勇 — 区委常委
    {"person_id": 4, "org_id": 1, "title": "金湾区委常委", "start": "待查", "end": "present", "rank": "副厅级", "note": "负责对口帮扶协作阳江市阳东区"},
    # 梁永森 — 纪委书记
    {"person_id": 5, "org_id": 1, "title": "金湾区委常委", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "金湾区纪委书记、区监委主任", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    # 李邦耀 — 组织部部长
    {"person_id": 6, "org_id": 1, "title": "金湾区委常委、组织部部长", "start": "待查", "end": "present", "rank": "副厅级", "note": "兼区委党校校长"},
    # 高禄林 — 宣传部部长
    {"person_id": 7, "org_id": 1, "title": "金湾区委常委、宣传部部长", "start": "待查", "end": "present", "rank": "副厅级", "note": "代管统战、民族宗教等工作"},
    # 朱荣新 — 政法委书记
    {"person_id": 8, "org_id": 1, "title": "金湾区委常委、政法委书记", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    # 苗奇峰 — 常务副区长
    {"person_id": 9, "org_id": 1, "title": "金湾区委常委", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "金湾区政府党组副书记、副区长", "start": "待查", "end": "present", "rank": "副厅级", "note": "协助区长负责区政府日常工作"},
    # 张涛 — 人武部长
    {"person_id": 10, "org_id": 1, "title": "金湾区委常委", "start": "待查", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 6, "title": "金湾区人民武装部上校部长", "start": "待查", "end": "present", "rank": "正团级", "note": ""},
    # 人大、政协
    {"person_id": 11, "org_id": 4, "title": "金湾区人大常委会主任", "start": "待查", "end": "present", "rank": "副厅级", "note": "待查"},
    {"person_id": 12, "org_id": 5, "title": "金湾区政协主席", "start": "待查", "end": "present", "rank": "副厅级", "note": "待查"},
]

# 4. Relationships
relationships = [
    # 梁耀斌 ↔ 刘军 — 党政搭档
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "金湾区委书记与区长党政搭档",
        "overlap_org": "金湾区",
        "overlap_period": "梁耀斌任区委书记、刘军任区长期间",
    },
    # 梁耀斌 → 庞前聪 — 上下级
    {
        "person_a": 1, "person_b": 3, "type": "superior_subordinate",
        "context": "区委书记与挂任副书记", "overlap_org": "中共金湾区委", "overlap_period": "当前"
    },
    # 梁耀斌 → 各常委 — 上级
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "区委书记与区委常委", "overlap_org": "中共金湾区委", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "区委书记与纪委书记", "overlap_org": "中共金湾区委", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "区委书记与组织部部长", "overlap_org": "中共金湾区委", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "区委书记与宣传部部长", "overlap_org": "中共金湾区委", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "区委书记与政法委书记", "overlap_org": "中共金湾区委", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "区委书记与常务副区长", "overlap_org": "中共金湾区委", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "区委书记与人武部长", "overlap_org": "中共金湾区委", "overlap_period": "当前"},
    # 刘军 → 苗奇峰 — 上下级 (政府系统)
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "区长与常务副区长", "overlap_org": "金湾区人民政府", "overlap_period": "当前"},
    # 梁耀斌 — 过往工作关系（从佛山高明区调任）
    {
        "person_a": 1, "person_b": 5,
        "type": "past_colleague",
        "context": "梁耀斌曾任佛山市高明区区长，梁永森曾任珠海市香洲区纪委书记—无直接共事证据，但香洲与金湾同属珠海市",
        "overlap_org": "珠海市",
        "overlap_period": "推测",
    },
    # 苗奇峰 — 过往曾任香洲区副区长，与梁永森曾在香洲共事
    {
        "person_a": 9, "person_b": 5,
        "type": "past_colleague",
        "context": "苗奇峰曾任香洲区副区长，梁永森曾任香洲区委常委、纪委书记，二人在香洲区存在工作交集可能",
        "overlap_org": "香洲区",
        "overlap_period": "推测（苗奇峰任香洲副区长、梁永森任香洲纪委书记期间）",
    },
    # 庞前聪 — 过往曾任香洲区委常委、副区长，与苗奇峰在香洲区有交集
    {
        "person_a": 3, "person_b": 9,
        "type": "past_colleague",
        "context": "庞前聪曾任香洲区委常委、副区长，苗奇峰曾任香洲区副区长，二人在香洲区政府班子有交集",
        "overlap_org": "香洲区",
        "overlap_period": "庞前聪任香洲区委常委、苗奇峰任香洲副区长期间",
    },
    # 刘军 — 曾任珠海经济技术开发区党工委副书记、管委会主任
    {
        "person_a": 2, "person_b": 4,
        "type": "past_colleague",
        "context": "刘军曾任珠海经济技术开发区党工委副书记、管委会主任，姜学勇曾任珠海经济技术开发区党工委委员、管委会副主任，二人在开发区有工作交集",
        "overlap_org": "珠海经济技术开发区",
        "overlap_period": "刘军任开发区党工委副书记、姜学勇任开发区党工委委员期间",
    },
    # 梁耀斌 — 曾任珠海经济技术开发区党工委书记
    {
        "person_a": 1, "person_b": 2,
        "type": "past_colleague",
        "context": "梁耀斌曾任珠海经济技术开发区党工委书记，刘军曾任开发区党工委副书记、管委会主任，二人在开发区已建立党政搭档关系",
        "overlap_org": "珠海经济技术开发区",
        "overlap_period": "梁耀斌任开发区党工委书记、刘军任开发区党工委副书记期间",
    },
    {
        "person_a": 1, "person_b": 4,
        "type": "past_colleague",
        "context": "梁耀斌曾任珠海经济技术开发区党工委书记，姜学勇曾任开发区党工委委员、管委会副主任",
        "overlap_org": "珠海经济技术开发区",
        "overlap_period": "梁耀斌任开发区党工委书记期间",
    },
    # 高禄林 — 曾任市纪委监委宣传部部长，与梁永森（区纪委书记）可能有系统交集
    {
        "person_a": 7, "person_b": 5,
        "type": "past_colleague",
        "context": "高禄林曾任珠海市纪委监委宣传部部长，梁永森现任金湾区纪委书记，同在珠海纪检监察系统工作",
        "overlap_org": "珠海市纪检监察系统",
        "overlap_period": "推测",
    },
    # 常委同僚关系
    {"person_a": 6, "person_b": 7, "type": "overlap", "context": "区委组织部部长与宣传部部长同僚", "overlap_org": "中共金湾区委", "overlap_period": "当前"},
    {"person_a": 8, "person_b": 6, "type": "overlap", "context": "政法委书记与组织部部长同僚", "overlap_org": "中共金湾区委", "overlap_period": "当前"},
    {"person_a": 8, "person_b": 5, "type": "overlap", "context": "政法委书记与纪委书记同僚", "overlap_org": "中共金湾区委", "overlap_period": "当前"},
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
