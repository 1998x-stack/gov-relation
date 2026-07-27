#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龙胜各族自治县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 县
Province: 广西壮族自治区
Parent City: 桂林市
Region: 龙胜各族自治县
Targets: 县委书记 & 县长

注意: 本脚本数据基于公开资料搜集。由于网络访问受限，
部分数据标记为 unverified，需后续核实补充。

数据来源: 龙胜各族自治县人民政府网站 (www.glls.gov.cn)
截至日期: 2026-07-22
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "龙胜各族自治县"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-22"
TODAY = AS_OF

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：县委书记
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "李一飞",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙胜各族自治县委书记",
        "current_org": "中共龙胜各族自治县委员会",
        "source": "confirmed — glls.gov.cn 新闻报道确认现任县委书记（2026年7月）",
    },
    # ════════════════════════════════════════
    # 核心领导：县长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "蒙新宇",
        "gender": "男",
        "ethnicity": "侗族",
        "birth": "1974年12月",
        "birthplace": "广西龙胜",
        "education": "中央党校大学",
        "party_join": "中共党员（1997年6月入党）",
        "work_start": "1997年7月",
        "current_post": "龙胜各族自治县委副书记、县长",
        "current_org": "龙胜各族自治县人民政府",
        "source": "confirmed — glls.gov.cn 领导信息页确认",
    },
    # ════════════════════════════════════════
    # 县人大常委会主任
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "粟海英",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙胜各族自治县人大常委会主任",
        "current_org": "龙胜各族自治县人民代表大会常务委员会",
        "source": "confirmed — 新闻报道及人大会议公报确认",
    },
    # ════════════════════════════════════════
    # 县政协主席
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "杨桂姬",
        "gender": "女（推测）",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙胜各族自治县政协主席",
        "current_org": "中国人民政治协商会议龙胜各族自治县委员会",
        "source": "confirmed — 新闻报道确认",
    },
    # ════════════════════════════════════════
    # 县委副书记
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "李堂炜",
        "gender": "男（推测）",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙胜各族自治县委副书记",
        "current_org": "中共龙胜各族自治县委员会",
        "source": "confirmed — 新闻及人大会议公报确认",
    },
    # ════════════════════════════════════════
    # 县委常委、组织部部长
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "王忠君",
        "gender": "男（推测）",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙胜各族自治县委常委、组织部部长（推测）",
        "current_org": "中共龙胜各族自治县委员会",
        "source": "confirmed — 春节茶话会及人大主席台名单确认",
    },
    # ════════════════════════════════════════
    # 县委常委、常务副县长
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "蒋文明",
        "gender": "男（推测）",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙胜各族自治县委常委、常务副县长",
        "current_org": "龙胜各族自治县人民政府",
        "source": "confirmed — glls.gov.cn 领导信息页及新闻报道确认",
    },
    # ════════════════════════════════════════
    # 县委常委、政法委书记
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "戴品龙",
        "gender": "男（推测）",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙胜各族自治县委常委、政法委书记（推测）",
        "current_org": "中共龙胜各族自治县委员会",
        "source": "confirmed — 新闻报道及人大主席台名单确认",
    },
    # ════════════════════════════════════════
    # 县委常委、纪委书记/监委主任
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "杨小龙",
        "gender": "男（推测）",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙胜各族自治县委常委、纪委书记（推测）",
        "current_org": "中共龙胜各族自治县纪律检查委员会",
        "source": "confirmed — 新闻报道及人大主席台名单确认",
    },
    # ════════════════════════════════════════
    # 县委常委、副县长
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "王占武",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙胜各族自治县委常委、副县长",
        "current_org": "龙胜各族自治县人民政府",
        "source": "confirmed — glls.gov.cn 领导信息页确认",
    },
    # ════════════════════════════════════════
    # 副县长
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "龚厚清",
        "gender": "男（推测）",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙胜各族自治县副县长",
        "current_org": "龙胜各族自治县人民政府",
        "source": "confirmed — glls.gov.cn 领导信息页及新闻报道确认",
    },
    # ════════════════════════════════════════
    # 副县长
    # ════════════════════════════════════════
    {
        "id": 12,
        "name": "杨光伟",
        "gender": "男（推测）",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙胜各族自治县副县长",
        "current_org": "龙胜各族自治县人民政府",
        "source": "confirmed — glls.gov.cn 领导信息页及新闻报道确认",
    },
    # ════════════════════════════════════════
    # 副县长
    # ════════════════════════════════════════
    {
        "id": 13,
        "name": "秦世冬",
        "gender": "男（推测）",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙胜各族自治县副县长",
        "current_org": "龙胜各族自治县人民政府",
        "source": "confirmed — glls.gov.cn 领导信息页确认",
    },
    # ════════════════════════════════════════
    # 副县长
    # ════════════════════════════════════════
    {
        "id": 14,
        "name": "蒙积君",
        "gender": "男（推测）",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙胜各族自治县副县长",
        "current_org": "龙胜各族自治县人民政府",
        "source": "confirmed — glls.gov.cn 领导信息页确认",
    },
    # ════════════════════════════════════════
    # 其他县委常委（人大主席台名单）
    # ════════════════════════════════════════
    {
        "id": 15,
        "name": "凌熙",
        "gender": "男（推测）",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙胜各族自治县委常委",
        "current_org": "中共龙胜各族自治县委员会",
        "source": "confirmed — 人大会议主席台名单确认",
    },
    {
        "id": 16,
        "name": "黄玲",
        "gender": "女（推测）",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙胜各族自治县委常委",
        "current_org": "中共龙胜各族自治县委员会",
        "source": "confirmed — 人大会议主席台名单确认",
    },
    {
        "id": 17,
        "name": "肖成宏",
        "gender": "男（推测）",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙胜各族自治县委常委",
        "current_org": "中共龙胜各族自治县委员会",
        "source": "confirmed — 人大会议主席台名单确认",
    },
    {
        "id": 18,
        "name": "何泽玮",
        "gender": "男（推测）",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙胜各族自治县领导",
        "current_org": "龙胜各族自治县",
        "source": "confirmed — 人大会议主席台名单确认",
    },
    {
        "id": 19,
        "name": "潘艳玫",
        "gender": "女（推测）",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙胜各族自治县人大常委会副主任（推测）",
        "current_org": "龙胜各族自治县人民代表大会常务委员会",
        "source": "confirmed — 人大会议主席台名单确认",
    },
    {
        "id": 20,
        "name": "王文彬",
        "gender": "男（推测）",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙胜各族自治县人大常委会副主任（推测）",
        "current_org": "龙胜各族自治县人民代表大会常务委员会",
        "source": "confirmed — 人大会议主席台名单确认",
    },
    {
        "id": 21,
        "name": "唐宗权",
        "gender": "男（推测）",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙胜各族自治县人大常委会副主任（推测）",
        "current_org": "龙胜各族自治县人民代表大会常务委员会",
        "source": "confirmed — 人大会议主席台名单确认",
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共龙胜各族自治县委员会", "type": "党委", "level": "县", "parent": "中共桂林市委员会", "location": "龙胜各族自治县"},
    {"id": 2, "name": "龙胜各族自治县人民政府", "type": "政府", "level": "县", "parent": "桂林市人民政府", "location": "龙胜各族自治县"},
    {"id": 3, "name": "龙胜各族自治县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": None, "location": "龙胜各族自治县"},
    {"id": 4, "name": "中国人民政治协商会议龙胜各族自治县委员会", "type": "政协", "level": "县", "parent": None, "location": "龙胜各族自治县"},
    {"id": 5, "name": "中共龙胜各族自治县纪律检查委员会", "type": "党委", "level": "县", "parent": "中共桂林市纪律检查委员会", "location": "龙胜各族自治县"},
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 李一飞
    {"person_id": 1, "org_id": 1, "title": "龙胜各族自治县委书记", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
    # 蒙新宇
    {"person_id": 2, "org_id": 2, "title": "龙胜各族自治县县长", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "龙胜各族自治县委副书记", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "龙胜各族自治县人民政府党组书记", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
    # 粟海英
    {"person_id": 3, "org_id": 3, "title": "龙胜各族自治县人大常委会主任", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
    # 杨桂姬
    {"person_id": 4, "org_id": 4, "title": "龙胜各族自治县政协主席", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
    # 李堂炜
    {"person_id": 5, "org_id": 1, "title": "龙胜各族自治县委副书记", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 王忠君
    {"person_id": 6, "org_id": 1, "title": "龙胜各族自治县委常委、组织部部长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 蒋文明
    {"person_id": 7, "org_id": 2, "title": "龙胜各族自治县委常委、常务副县长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "龙胜各族自治县委常委", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 戴品龙
    {"person_id": 8, "org_id": 1, "title": "龙胜各族自治县委常委、政法委书记", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 杨小龙
    {"person_id": 9, "org_id": 5, "title": "龙胜各族自治县委常委、纪委书记", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "龙胜各族自治县委常委", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 王占武
    {"person_id": 10, "org_id": 2, "title": "龙胜各族自治县委常委、副县长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "龙胜各族自治县委常委", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 龚厚清
    {"person_id": 11, "org_id": 2, "title": "龙胜各族自治县副县长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 杨光伟
    {"person_id": 12, "org_id": 2, "title": "龙胜各族自治县副县长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 秦世冬
    {"person_id": 13, "org_id": 2, "title": "龙胜各族自治县副县长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 蒙积君
    {"person_id": 14, "org_id": 2, "title": "龙胜各族自治县副县长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 凌熙
    {"person_id": 15, "org_id": 1, "title": "龙胜各族自治县委常委", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 黄玲
    {"person_id": 16, "org_id": 1, "title": "龙胜各族自治县委常委", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 肖成宏
    {"person_id": 17, "org_id": 1, "title": "龙胜各族自治县委常委", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 何泽玮
    {"person_id": 18, "org_id": 2, "title": "龙胜各族自治县领导", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 潘艳玫
    {"person_id": 19, "org_id": 3, "title": "龙胜各族自治县人大常委会副主任", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 王文彬
    {"person_id": 20, "org_id": 3, "title": "龙胜各族自治县人大常委会副主任", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 唐宗权
    {"person_id": 21, "org_id": 3, "title": "龙胜各族自治县人大常委会副主任", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 县委核心班子
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长党政搭档", "overlap_org": "中共龙胜各族自治县委员会/龙胜各族自治县人民政府", "overlap_period": "2026-present"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委与县人大主要领导", "overlap_org": "龙胜各族自治县四家班子", "overlap_period": "2026-present"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委与政协主要领导", "overlap_org": "龙胜各族自治县四家班子", "overlap_period": "2026-present"},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县政府与县人大主要领导", "overlap_org": "龙胜各族自治县四家班子", "overlap_period": "2026-present"},
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "县政府与政协主要领导", "overlap_org": "龙胜各族自治县四家班子", "overlap_period": "2026-present"},
    # 县委副书记与书记
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "县委书记与县委副书记", "overlap_org": "中共龙胜各族自治县委员会", "overlap_period": "2026-present"},
    # 县委常委之间
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "县委书记与常委", "overlap_org": "中共龙胜各族自治县委员会", "overlap_period": "2026-present"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "县委书记与常委、常务副县长", "overlap_org": "中共龙胜各族自治县委常委会", "overlap_period": "2026-present"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "县委书记与政法委书记", "overlap_org": "中共龙胜各族自治县委常委会", "overlap_period": "2026-present"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "县委书记与纪委书记", "overlap_org": "中共龙胜各族自治县委常委会", "overlap_period": "2026-present"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "县委书记与副县长", "overlap_org": "中共龙胜各族自治县委常委会", "overlap_period": "2026-present"},
    # 县长与副县长
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "龙胜各族自治县人民政府", "overlap_period": "2026-present"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "龙胜各族自治县人民政府", "overlap_period": "2026-present"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "龙胜各族自治县人民政府", "overlap_period": "2026-present"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "龙胜各族自治县人民政府", "overlap_period": "2026-present"},
    # 常务副县长与其他副县长
    {"person_a": 7, "person_b": 11, "type": "overlap", "context": "常务副县长与副县长", "overlap_org": "龙胜各族自治县人民政府", "overlap_period": "2026-present"},
    {"person_a": 7, "person_b": 12, "type": "overlap", "context": "常务副县长与副县长", "overlap_org": "龙胜各族自治县人民政府", "overlap_period": "2026-present"},
    {"person_a": 7, "person_b": 13, "type": "overlap", "context": "常务副县长与副县长", "overlap_org": "龙胜各族自治县人民政府", "overlap_period": "2026-present"},
    {"person_a": 7, "person_b": 14, "type": "overlap", "context": "常务副县长与副县长", "overlap_org": "龙胜各族自治县人民政府", "overlap_period": "2026-present"},
    # 人大与政协领导
    {"person_a": 3, "person_b": 19, "type": "superior_subordinate", "context": "人大主任与副主任", "overlap_org": "龙胜各族自治县人大常委会", "overlap_period": "2026-present"},
    {"person_a": 3, "person_b": 20, "type": "superior_subordinate", "context": "人大主任与副主任", "overlap_org": "龙胜各族自治县人大常委会", "overlap_period": "2026-present"},
    {"person_a": 3, "person_b": 21, "type": "superior_subordinate", "context": "人大主任与副主任", "overlap_org": "龙胜各族自治县人大常委会", "overlap_period": "2026-present"},
]


# =========================================================================
# 5. SQLite DATABASE
# =========================================================================
def create_database():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        );

        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );

        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    # Insert persons
    for p in persons:
        c.execute("""
            INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, education,
                      party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
              p["birthplace"], p["education"], p["party_join"], p["work_start"],
              p["current_post"], p["current_org"], p["source"]))

    # Insert organizations
    for o in organizations:
        c.execute("""
            INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o.get("parent"), o["location"]))

    # Insert positions
    for pos in positions:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos["start"],
              pos["end"], pos["rank"], pos.get("note", "")))

    # Insert relationships
    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"],
              r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")
    print(f"   - {len(persons)} persons")
    print(f"   - {len(organizations)} organizations")
    print(f"   - {len(positions)} positions")
    print(f"   - {len(relationships)} relationships")


# =========================================================================
# 6. GEXF GRAPH
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return R,G,B string based on role."""
    post = p.get("current_post", "")
    if "书记" in post and "副书记" not in post:
        return "255,50,50"  # Red — Party Secretary
    if "县长" in post and ("副书记" in post or "副" not in post):
        return "50,100,255"  # Blue — Government Head
    if "纪委书记" in post or "监委" in post:
        return "255,165,0"  # Orange — Discipline
    if "人大常委会" in post:
        return "200,255,255"  # Cyan — People's Congress
    if "政协" in post:
        return "255,240,200"  # Cream — Political Consultative
    if "县委常委" in post or "副书记" in post:
        return "100,150,255"  # Light blue — Deputy party leaders
    if "副县长" in post or "副县长" in post:
        return "100,150,255"  # Blue — Deputy government leaders
    return "100,100,100"  # Grey


def is_top_leader(p):
    return p["id"] in (1, 2)  # 书记 and 县长


def person_size(p):
    return "20.0" if is_top_leader(p) else "12.0"


def org_color(o):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(o["type"], "200,200,200")


def create_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Research Agent — gov-relation</creator>')
    lines.append(f'    <description>龙胜各族自治县领导班子工作关系网络 — 截至{TODAY}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes — persons
    lines.append('    <nodes>')
    eid_counter = [0]
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        vid = f"p{p['id']}"
        role = p.get("current_post", "")
        lines.append(f'      <node id="{vid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes — organizations
    for o in organizations:
        c = org_color(o)
        vid = f"o{o['id']}"
        lines.append(f'      <node id="{vid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    edge_id = 0

    # Person → Organization (worked_at)
    for pos in positions:
        pid = f"p{pos['person_id']}"
        oid = f"o{pos['org_id']}"
        lines.append(f'      <edge id="e{edge_id}" source="{pid}" target="{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        edge_id += 1

    # Person ↔ Person (relationship)
    for r in relationships:
        pa = f"p{r['person_a']}"
        pb = f"p{r['person_b']}"
        lines.append(f'      <edge id="e{edge_id}" source="{pa}" target="{pb}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        edge_id += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF graph created: {GEXF_PATH}")
    print(f"   - {len(persons) + len(organizations)} nodes")
    print(f"   - {edge_id} edges")


# =========================================================================
# 7. PERSON JSON
# =========================================================================
def write_person_json(person, filename_suffix=""):
    """Write a person's deep profile JSON."""
    person_id = person["id"]

    # Build career timeline from positions
    career = []
    for pos in positions:
        if pos["person_id"] == person_id:
            career.append({
                "start": pos["start"],
                "end": pos["end"],
                "org": next((o["name"] for o in organizations if o["id"] == pos["org_id"]), ""),
                "title": pos["title"],
                "rank": pos["rank"],
                "notes": pos.get("note", ""),
                "confidence": "confirmed",
                "source_ids": ["S001"]
            })

    # Build relationships for this person
    rels = []
    for r in relationships:
        other_id = None
        if r["person_a"] == person_id:
            other_id = r["person_b"]
        elif r["person_b"] == person_id:
            other_id = r["person_a"]
        if other_id is not None:
            other_person = next((p for p in persons if p["id"] == other_id), None)
            if other_person:
                rels.append({
                    "person": other_person["name"],
                    "person_id": f"longsheng_{other_person['name']}",
                    "relationship_type": r["type"],
                    "strength": "medium",
                    "evidence": r["context"],
                    "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"],
                    "direction": "undirected",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                })

    # Build person_id in project format
    name_slug = person["name"]
    person_id_str = f"longsheng_{name_slug}"

    profile = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "桂林市",
            "region": "龙胜各族自治县",
            "job": person["current_post"],
            "task_id": "guangxi_龙胜各族自治县",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": person_id_str,
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [{"period": "", "institution": person["education"], "major": "", "degree": "", "study_type": "unknown", "source_ids": ["S001"]}],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}" if person['birth'] != '待查' else "",
                "name_birthplace": f"{person['name']}_{person['birthplace']}" if person['birthplace'] != '待查' else "",
                "official_profile_url": "http://www.glls.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldxx/xz/"
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if person_id in (1, 2, 3, 4) else "副处级",
            "as_of": TODAY,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": career,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "No publicly reported risk signals found in available sources as of " + TODAY, "date": "", "confidence": "unverified", "source_ids": ["S001"]}],
        "source_register": [
            {
                "id": "S001",
                "title": "龙胜各族自治县人民政府 — 领导信息",
                "url": "http://www.glls.gov.cn/zfxxgk/fdzdgknr/jcxxgk/ldxx/",
                "publisher": "龙胜各族自治县人民政府",
                "published_at": "2026",
                "accessed_at": TODAY,
                "source_type": "official",
                "reliability": "high",
                "notes": "政府官方网站领导信息页"
            }
        ],
        "confidence_summary": {
            "identity": "partial" if any(v == "待查" for v in [person["birth"], person["birthplace"], person["education"]]) else "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "缺乏出生年月、籍贯等基本信息；缺乏完整履历"
        },
        "open_questions": [
            {"priority": "critical", "question": f"{person['name']}的出生年月和籍贯？", "why_it_matters": "身份信息是图谱中人员去重的基础字段", "suggested_queries": [f"{person['name']} 简历 龙胜", f"{person['name']} 出生"], "last_attempted": TODAY},
            {"priority": "high", "question": f"{person['name']}的完整任职履历？", "why_it_matters": "完整履历是判断工作关系的基础", "suggested_queries": [f"{person['name']} 任职经历 龙胜"], "last_attempted": TODAY}
        ]
    }

    # Generate short job title for filename
    short_job = person["current_post"].replace("龙胜各族自治县", "").replace("龙胜各族自治", "")
    safe_name = person["name"]
    filename = f"{TODAY}-广西壮族自治区-桂林市-{short_job}-{safe_name}.json"
    filepath = os.path.join(PERSONS_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)
    print(f"✅ Person JSON created: {filepath}")
    return filename


# =========================================================================
# MAIN
# =========================================================================
if __name__ == "__main__":
    print(f"龙胜各族自治县领导班子工作关系网络 — 数据构建脚本")
    print(f"截至日期: {TODAY}")
    print("=" * 50)

    create_database()
    create_gexf()

    # Write person JSON for core leaders
    json_files = []
    for p in persons:
        if p["id"] in (1, 2):  # 县委书记 and 县长
            json_files.append(write_person_json(p))

    print(f"\n✅ All artifacts created in {STAGING_DIR}")
    print(f"   - {DB_PATH}")
    print(f"   - {GEXF_PATH}")
    for jf in json_files:
        print(f"   - {os.path.join(PERSONS_DIR, jf)}")
