#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
惠城区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 广东省
Parent City: 惠州市
Region: 惠城区
Targets: 区委书记 & 区长

Research Sources:
- 惠城区人民政府门户网站 (www.hcq.gov.cn) — 领导之窗页面 (2026-07-22)
- 惠州市人民政府门户网站 (www.huizhou.gov.cn) — 领导之窗页面 (2026-07-22)

Research Date: 2026-07-22

网络环境限制说明:
- Exa搜索达到速率限制
- Baidu/Google/Bing搜索被验证码或超时拦截
- Wikipedia超时
- 基于惠城区政府官网和惠州市政府官网确认领导班子

Current State:
- 区委书记: 空缺 (Vacant as of 2026-07-22)
- 区委副书记、区长: 田胜思
- 前区委书记信息不可获取（曹洪彬现任惠州市副市长，但无法确认其是否为前任惠城区委书记）
"""

import os
import sys
from pathlib import Path

# Add repo root to path
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

# Staging paths
STAGING_DIR = Path(__file__).parent
DB_PATH = STAGING_DIR / "惠城区_network.db"
GEXF_PATH = STAGING_DIR / "惠城区_network.gexf"

import sqlite3

# Use absolute paths for canonical promotion later
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ════════════════════════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════════════════════════

persons = [
    # ── 1. Current Top Leaders ──
    # 区委书记: 空缺 (vacant as of 2026-07-22)
    # 曹洪彬 is currently 惠州市副市长, could not confirm if he was 惠城区委书记

    # ── 1a. Party Committee (区委常委会) ──
    {
        "id": 1,
        "name": "田胜思",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠城区委副书记、区长",
        "current_org": "中共惠州市惠城区委员会/惠城区人民政府",
        "source": "www.hcq.gov.cn — 领导之窗 (2026-07-22)"
    },
    {
        "id": 2,
        "name": "邹运章",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠城区委副书记",
        "current_org": "中共惠州市惠城区委员会",
        "source": "www.hcq.gov.cn — 领导之窗 (2026-07-22)"
    },
    {
        "id": 3,
        "name": "何碧光",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠城区委常委",
        "current_org": "中共惠州市惠城区委员会",
        "source": "www.hcq.gov.cn — 领导之窗 (2026-07-22)"
    },
    {
        "id": 4,
        "name": "朱昆智",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠城区委常委",
        "current_org": "中共惠州市惠城区委员会",
        "source": "www.hcq.gov.cn — 领导之窗 (2026-07-22)"
    },
    {
        "id": 5,
        "name": "余育灵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠城区委常委、副区长",
        "current_org": "中共惠州市惠城区委员会/惠城区人民政府",
        "source": "www.hcq.gov.cn — 领导之窗 (2026-07-22)"
    },
    {
        "id": 6,
        "name": "张琪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠城区委常委",
        "current_org": "中共惠州市惠城区委员会",
        "source": "www.hcq.gov.cn — 领导之窗 (2026-07-22)"
    },
    {
        "id": 7,
        "name": "董江涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠城区委常委、副区长",
        "current_org": "中共惠州市惠城区委员会/惠城区人民政府",
        "source": "www.hcq.gov.cn — 领导之窗 (2026-07-22)"
    },
    {
        "id": 8,
        "name": "周文超",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠城区委常委",
        "current_org": "中共惠州市惠城区委员会",
        "source": "www.hcq.gov.cn — 领导之窗 (2026-07-22)"
    },
    {
        "id": 9,
        "name": "李晓敏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠城区委常委",
        "current_org": "中共惠州市惠城区委员会",
        "source": "www.hcq.gov.cn — 领导之窗 (2026-07-22)"
    },
    # ── 1b. District Government (区政府) ──
    {
        "id": 10,
        "name": "何东文",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠城区副区长",
        "current_org": "惠城区人民政府",
        "source": "www.hcq.gov.cn — 领导之窗 (2026-07-22)"
    },
    {
        "id": 11,
        "name": "何铭",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠城区副区长",
        "current_org": "惠城区人民政府",
        "source": "www.hcq.gov.cn — 领导之窗 (2026-07-22)"
    },
    {
        "id": 12,
        "name": "巫南辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠城区副区长",
        "current_org": "惠城区人民政府",
        "source": "www.hcq.gov.cn — 领导之窗 (2026-07-22)"
    },
    {
        "id": 13,
        "name": "翟金华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠城区副区长",
        "current_org": "惠城区人民政府",
        "source": "www.hcq.gov.cn — 领导之窗 (2026-07-22)"
    },
    {
        "id": 14,
        "name": "张贤",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠城区副区长",
        "current_org": "惠城区人民政府",
        "source": "www.hcq.gov.cn — 领导之窗 (2026-07-22)"
    },
    # ── 1c. People's Congress (区人大常委会) ──
    {
        "id": 15,
        "name": "林月云",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠城区人大常委会主任",
        "current_org": "惠城区人民代表大会常务委员会",
        "source": "www.hcq.gov.cn — 领导之窗 (2026-07-22)"
    },
    {
        "id": 16,
        "name": "余道方",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠城区人大常委会副主任",
        "current_org": "惠城区人民代表大会常务委员会",
        "source": "www.hcq.gov.cn — 领导之窗 (2026-07-22)"
    },
    {
        "id": 17,
        "name": "周国静",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠城区人大常委会副主任",
        "current_org": "惠城区人民代表大会常务委员会",
        "source": "www.hcq.gov.cn — 领导之窗 (2026-07-22)"
    },
    {
        "id": 18,
        "name": "田勇辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠城区人大常委会副主任",
        "current_org": "惠城区人民代表大会常务委员会",
        "source": "www.hcq.gov.cn — 领导之窗 (2026-07-22)"
    },
    {
        "id": 19,
        "name": "黄友良",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠城区人大常委会副主任",
        "current_org": "惠城区人民代表大会常务委员会",
        "source": "www.hcq.gov.cn — 领导之窗 (2026-07-22)"
    },
    {
        "id": 20,
        "name": "李雪松",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠城区人大常委会副主任",
        "current_org": "惠城区人民代表大会常务委员会",
        "source": "www.hcq.gov.cn — 领导之窗 (2026-07-22)"
    },
    {
        "id": 21,
        "name": "梁日洪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠城区人大常委会副主任",
        "current_org": "惠城区人民代表大会常务委员会",
        "source": "www.hcq.gov.cn — 领导之窗 (2026-07-22)"
    },
    # ── 1d. Political Consultative Conference (区政协) ──
    {
        "id": 22,
        "name": "彭华君",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠城区政协主席",
        "current_org": "政协惠城区委员会",
        "source": "www.hcq.gov.cn — 领导之窗 (2026-07-22)"
    },
    {
        "id": 23,
        "name": "占必佑",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠城区政协副主席",
        "current_org": "政协惠城区委员会",
        "source": "www.hcq.gov.cn — 领导之窗 (2026-07-22)"
    },
    {
        "id": 24,
        "name": "刘红光",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠城区政协副主席",
        "current_org": "政协惠城区委员会",
        "source": "www.hcq.gov.cn — 领导之窗 (2026-07-22)"
    },
    {
        "id": 25,
        "name": "邹忠平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠城区政协副主席",
        "current_org": "政协惠城区委员会",
        "source": "www.hcq.gov.cn — 领导之窗 (2026-07-22)"
    },
    {
        "id": 26,
        "name": "殷琼",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠城区政协副主席",
        "current_org": "政协惠城区委员会",
        "source": "www.hcq.gov.cn — 领导之窗 (2026-07-22)"
    },
    {
        "id": 27,
        "name": "甄红",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠城区政协副主席",
        "current_org": "政协惠城区委员会",
        "source": "www.hcq.gov.cn — 领导之窗 (2026-07-22)"
    },
    {
        "id": 28,
        "name": "翁少芳",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠城区政协副主席",
        "current_org": "政协惠城区委员会",
        "source": "www.hcq.gov.cn — 领导之窗 (2026-07-22)"
    },
    # ── 1e. Discipline Inspection (区纪委) ──
    {
        "id": 29,
        "name": "梁强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠城区纪委书记",
        "current_org": "中共惠城区纪律检查委员会",
        "source": "www.hcq.gov.cn — 领导之窗 (2026-07-22)"
    },
    {
        "id": 30,
        "name": "林雪梅",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠城区纪委副书记",
        "current_org": "中共惠城区纪律检查委员会",
        "source": "www.hcq.gov.cn — 领导之窗 (2026-07-22)"
    },
    {
        "id": 31,
        "name": "王力涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠城区纪委副书记",
        "current_org": "中共惠城区纪律检查委员会",
        "source": "www.hcq.gov.cn — 领导之窗 (2026-07-22)"
    },
]

# ── Organizations ──

organizations = [
    {
        "id": 1,
        "name": "中共惠州市惠城区委员会",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共惠州市委",
        "location": "惠州市惠城区"
    },
    {
        "id": 2,
        "name": "惠城区人民政府",
        "type": "政府",
        "level": "市辖区",
        "parent": "惠州市人民政府",
        "location": "惠州市惠城区"
    },
    {
        "id": 3,
        "name": "中共惠城区纪律检查委员会",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共惠州市惠城区委员会",
        "location": "惠州市惠城区"
    },
    {
        "id": 4,
        "name": "惠城区人民代表大会常务委员会",
        "type": "人大",
        "level": "市辖区",
        "parent": "惠州市人民代表大会常务委员会",
        "location": "惠州市惠城区"
    },
    {
        "id": 5,
        "name": "中国人民政治协商会议惠城区委员会",
        "type": "政协",
        "level": "市辖区",
        "parent": "政协惠州市委员会",
        "location": "惠州市惠城区"
    },
]

# ── Positions (Person → Organization mappings) ──

positions = [
    # Party Committee
    {"person_id": 1, "org_id": 1, "title": "惠城区委副书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "惠城区委副书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "惠城区委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "惠城区委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "惠城区委常委", "start": "", "end": "present", "rank": "副厅级", "note": "兼副区长"},
    {"person_id": 6, "org_id": 1, "title": "惠城区委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "惠城区委常委", "start": "", "end": "present", "rank": "副厅级", "note": "兼副区长"},
    {"person_id": 8, "org_id": 1, "title": "惠城区委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "惠城区委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # District Government
    {"person_id": 1, "org_id": 2, "title": "惠城区区长", "start": "", "end": "present", "rank": "副厅级", "note": "区委副书记、区长"},
    {"person_id": 5, "org_id": 2, "title": "惠城区副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "惠城区副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "惠城区副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "惠城区副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "惠城区副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "惠城区副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "惠城区副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # People's Congress
    {"person_id": 15, "org_id": 4, "title": "惠城区人大常委会主任", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 16, "org_id": 4, "title": "惠城区人大常委会副主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 17, "org_id": 4, "title": "惠城区人大常委会副主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 18, "org_id": 4, "title": "惠城区人大常委会副主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 19, "org_id": 4, "title": "惠城区人大常委会副主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 20, "org_id": 4, "title": "惠城区人大常委会副主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 21, "org_id": 4, "title": "惠城区人大常委会副主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # CPPCC
    {"person_id": 22, "org_id": 5, "title": "惠城区政协主席", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 23, "org_id": 5, "title": "惠城区政协副主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 24, "org_id": 5, "title": "惠城区政协副主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 25, "org_id": 5, "title": "惠城区政协副主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 26, "org_id": 5, "title": "惠城区政协副主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 27, "org_id": 5, "title": "惠城区政协副主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 28, "org_id": 5, "title": "惠城区政协副主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # Discipline Inspection
    {"person_id": 29, "org_id": 3, "title": "惠城区纪委书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 30, "org_id": 3, "title": "惠城区纪委副书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 31, "org_id": 3, "title": "惠城区纪委副书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
]

# ── Relationships ──

relationships = [
    # ── Party-Government Core ──
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "区委副书记班子搭档",
        "overlap_org": "中共惠州市惠城区委员会",
        "overlap_period": "现任（2026-07-22）",
        "confidence": "confirmed"
    },
    {
        "person_a": 1, "person_b": 5,
        "type": "superior_subordinate",
        "context": "区长与副区长",
        "overlap_org": "惠城区人民政府",
        "overlap_period": "现任（2026-07-22）",
        "confidence": "confirmed"
    },
    {
        "person_a": 1, "person_b": 7,
        "type": "superior_subordinate",
        "context": "区长与副区长",
        "overlap_org": "惠城区人民政府",
        "overlap_period": "现任（2026-07-22）",
        "confidence": "confirmed"
    },
    {
        "person_a": 1, "person_b": 10,
        "type": "superior_subordinate",
        "context": "区长与副区长",
        "overlap_org": "惠城区人民政府",
        "overlap_period": "现任（2026-07-22）",
        "confidence": "confirmed"
    },
    {
        "person_a": 1, "person_b": 11,
        "type": "superior_subordinate",
        "context": "区长与副区长",
        "overlap_org": "惠城区人民政府",
        "overlap_period": "现任（2026-07-22）",
        "confidence": "confirmed"
    },
    {
        "person_a": 1, "person_b": 12,
        "type": "superior_subordinate",
        "context": "区长与副区长",
        "overlap_org": "惠城区人民政府",
        "overlap_period": "现任（2026-07-22）",
        "confidence": "confirmed"
    },
    {
        "person_a": 1, "person_b": 13,
        "type": "superior_subordinate",
        "context": "区长与副区长",
        "overlap_org": "惠城区人民政府",
        "overlap_period": "现任（2026-07-22）",
        "confidence": "confirmed"
    },
    {
        "person_a": 1, "person_b": 14,
        "type": "superior_subordinate",
        "context": "区长与副区长",
        "overlap_org": "惠城区人民政府",
        "overlap_period": "现任（2026-07-22）",
        "confidence": "confirmed"
    },
    # ── Party Standing Committee Overlaps ──
    {
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "区委常委会班子成员",
        "overlap_org": "中共惠州市惠城区委员会",
        "overlap_period": "现任（2026-07-22）",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 4,
        "type": "overlap",
        "context": "区委常委会班子成员",
        "overlap_org": "中共惠州市惠城区委员会",
        "overlap_period": "现任（2026-07-22）",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 8,
        "type": "overlap",
        "context": "区委常委会班子成员",
        "overlap_org": "中共惠州市惠城区委员会",
        "overlap_period": "现任（2026-07-22）",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 9,
        "type": "overlap",
        "context": "区委常委会班子成员",
        "overlap_org": "中共惠州市惠城区委员会",
        "overlap_period": "现任（2026-07-22）",
        "confidence": "confirmed"
    },
    # ── Government Team Overlaps ──
    {
        "person_a": 5, "person_b": 7,
        "type": "overlap",
        "context": "副区长班子搭档",
        "overlap_org": "惠城区人民政府",
        "overlap_period": "现任（2026-07-22）",
        "confidence": "confirmed"
    },
    {
        "person_a": 10, "person_b": 11,
        "type": "overlap",
        "context": "副区长班子搭档",
        "overlap_org": "惠城区人民政府",
        "overlap_period": "现任（2026-07-22）",
        "confidence": "confirmed"
    },
    # ── Discipline Inspection ──
    {
        "person_a": 29, "person_b": 30,
        "type": "superior_subordinate",
        "context": "纪委书记与副书记",
        "overlap_org": "中共惠城区纪律检查委员会",
        "overlap_period": "现任（2026-07-22）",
        "confidence": "confirmed"
    },
    {
        "person_a": 29, "person_b": 31,
        "type": "superior_subordinate",
        "context": "纪委书记与副书记",
        "overlap_org": "中共惠城区纪律检查委员会",
        "overlap_period": "现任（2026-07-22）",
        "confidence": "confirmed"
    },
]


# ════════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════════

def main():
    print(f"=== 惠城区网络数据构建 ===")
    print(f"Research date: 2026-07-22")
    print(f"Source: www.hcq.gov.cn — 领导之窗 (official)")
    print(f"区委书记: 空缺 (vacant as of 2026-07-22)")
    print(f"区委副书记、区长: 田胜思")
    print(f"")
    print(f"人员: {len(persons)} 人")
    print(f"组织机构: {len(organizations)} 个")
    print(f"任职记录: {len(positions)} 条")
    print(f"关系: {len(relationships)} 条")

    run_build(
        slug="惠城区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print(f"\n=== 完成 ===")


if __name__ == "__main__":
    main()
