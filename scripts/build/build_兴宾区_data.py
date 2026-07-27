#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
兴宾区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 市辖区
Province: 广西壮族自治区
Parent City: 来宾市
Region: 兴宾区
Targets: 区委书记 & 区长

当前在任 (as of 2026-07-23):
- 区委书记: 王轶 (来宾市人大常委会副主任、兴宾区委书记)
- 区长: 管志斌 (兴宾区委副书记、政府区长)
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
SLUG = "兴宾区"
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-23"

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：区委书记
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "王轶",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "来宾市人大常委会副主任、兴宾区委书记",
        "current_org": "中共兴宾区委员会/来宾市人大常委会",
        "source": "http://www.xingbin.gov.cn"
    },
    # ════════════════════════════════════════
    # 核心领导：区长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "管志斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-05",
        "birthplace": "待查",
        "education": "研究生学历，文学博士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴宾区委副书记、政府区长",
        "current_org": "兴宾区人民政府/中共兴宾区委员会",
        "source": "http://www.xingbin.gov.cn/zfxxgk_1/fdzdgknr/ldjj/qz/t27372518.shtml"
    },
    # ════════════════════════════════════════
    # 区委副书记
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "唐彦乐",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴宾区委副书记",
        "current_org": "中共兴宾区委员会",
        "source": "http://www.xingbin.gov.cn/xwzx/xbyw/t27782171.shtml"
    },
    # ════════════════════════════════════════
    # 区委常委：副区长
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "黄大乘",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴宾区委常委、副区长",
        "current_org": "中共兴宾区委员会/兴宾区人民政府",
        "source": "http://www.xingbin.gov.cn/xwzx/xbyw/t27782171.shtml"
    },
    # ════════════════════════════════════════
    # 区委常委：挂职副区长
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "仇兴华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-10",
        "birthplace": "待查",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广西园区发展和投资促进服务中心投资促进三处副处长，兴宾区委常委，区政府党组成员、副区长、驻村工作队队长",
        "current_org": "广西壮族自治区园区发展和投资促进服务中心/中共兴宾区委员会/兴宾区人民政府",
        "source": "http://www.xingbin.gov.cn/zfxxgk_1/fdzdgknr/ldjj/fqz/t21762348.shtml"
    },
    # ════════════════════════════════════════
    # 挂职副区长
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "梁济谞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-12",
        "birthplace": "待查",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "共青团广西来宾市委副书记、兴宾区抓党建促乡村振兴工作队队长，挂任兴宾区委常委、副区长",
        "current_org": "共青团广西来宾市委/中共兴宾区委员会/兴宾区人民政府",
        "source": "http://www.xingbin.gov.cn/zfxxgk_1/fdzdgknr/ldjj/fqz/t9342594.shtml"
    },
    # ════════════════════════════════════════
    # 区委常委：统战部部长
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "潘锦辉",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1987-12",
        "birthplace": "待查",
        "education": "大学，哲学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴宾区委常委、统战部部长，区政府党组成员，区政协党组副书记（兼）",
        "current_org": "中共兴宾区委员会/兴宾区人民政府/兴宾区政协",
        "source": "http://www.xingbin.gov.cn/zfxxgk_1/fdzdgknr/ldjj/fqz/t19381854.shtml"
    },
    # ════════════════════════════════════════
    # 区委常委
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "蓝文钰",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴宾区委常委",
        "current_org": "中共兴宾区委员会",
        "source": "http://www.xingbin.gov.cn/xwzx/xbyw/t27852526.shtml"
    },
    {
        "id": 9,
        "name": "蒙函",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴宾区委常委",
        "current_org": "中共兴宾区委员会",
        "source": "http://www.xingbin.gov.cn/xwzx/xbyw/t27852526.shtml"
    },
    {
        "id": 10,
        "name": "陆彦毓",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴宾区委常委",
        "current_org": "中共兴宾区委员会",
        "source": "http://www.xingbin.gov.cn/xwzx/xbyw/t27852526.shtml"
    },
    {
        "id": 11,
        "name": "韦建红",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴宾区委常委",
        "current_org": "中共兴宾区委员会",
        "source": "http://www.xingbin.gov.cn/xwzx/xbyw/t27852526.shtml"
    },
    # ════════════════════════════════════════
    # 区委常委、办公室主任
    # ════════════════════════════════════════
    {
        "id": 12,
        "name": "梁修田",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴宾区委常委、办公室主任",
        "current_org": "中共兴宾区委员会",
        "source": "http://www.xingbin.gov.cn/xwzx/xbyw/t27852526.shtml"
    },
    {
        "id": 13,
        "name": "邓建宇",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴宾区委常委",
        "current_org": "中共兴宾区委员会",
        "source": "http://www.xingbin.gov.cn/xwzx/xbyw/t27852526.shtml"
    },
    # ════════════════════════════════════════
    # 区政府副区长
    # ════════════════════════════════════════
    {
        "id": 14,
        "name": "黄宁",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1979-10",
        "birthplace": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴宾区人民政府党组成员、副区长，来宾市公安局兴宾分局局长",
        "current_org": "兴宾区人民政府/来宾市公安局兴宾分局",
        "source": "http://www.xingbin.gov.cn/zfxxgk_1/fdzdgknr/ldjj/fqz/t27562385.shtml"
    },
    {
        "id": 15,
        "name": "覃泽毅",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1976-08",
        "birthplace": "待查",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴宾区人民政府党组成员、副区长",
        "current_org": "兴宾区人民政府",
        "source": "http://www.xingbin.gov.cn/zfxxgk_1/fdzdgknr/ldjj/fqz/t18055461.shtml"
    },
    # ════════════════════════════════════════
    # 政府办主任
    # ════════════════════════════════════════
    {
        "id": 16,
        "name": "袁海斌",
        "gender": "男",
        "ethnicity": "瑶族",
        "birth": "1982-04",
        "birthplace": "待查",
        "education": "大学，文学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴宾区人民政府党组成员、办公室党组书记、主任",
        "current_org": "兴宾区人民政府办公室",
        "source": "http://www.xingbin.gov.cn/zfxxgk_1/fdzdgknr/ldjj/zfbzr/t13301202.shtml"
    },
    # ════════════════════════════════════════
    # 人大常委会主任
    # ════════════════════════════════════════
    {
        "id": 17,
        "name": "方革",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴宾区人大常委会主任",
        "current_org": "兴宾区人大常委会",
        "source": "http://www.xingbin.gov.cn/xwzx/xbyw/t27852526.shtml"
    },
    # ════════════════════════════════════════
    # 政协主席
    # ════════════════════════════════════════
    {
        "id": 18,
        "name": "冉纪贵",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "兴宾区政协主席",
        "current_org": "兴宾区政协",
        "source": "http://www.xingbin.gov.cn/xwzx/xbyw/t27852526.shtml"
    },
    # ════════════════════════════════════════
    # 前任区委书记
    # ════════════════════════════════════════
    {
        "id": 19,
        "name": "周灵",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查（原来宾市人大常委会副主任、兴宾区委书记）",
        "current_org": "待查",
        "source": "http://www.xingbin.gov.cn/xwzx/xbyw/t18497447.shtml"
    },
    # ════════════════════════════════════════
    # 前任区长
    # ════════════════════════════════════════
    {
        "id": 20,
        "name": "蓝海鹏",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "待查（原兴宾区区长）",
        "current_org": "待查",
        "source": "https://www.thepaper.cn (人民网报道)"
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共兴宾区委员会", "type": "党委", "level": "县级", "parent": "中共来宾市委员会", "location": "兴宾区"},
    {"id": 2, "name": "兴宾区人民政府", "type": "政府", "level": "县级", "parent": "来宾市人民政府", "location": "兴宾区"},
    {"id": 3, "name": "兴宾区人大常委会", "type": "人大", "level": "县级", "parent": "来宾市人大常委会", "location": "兴宾区"},
    {"id": 4, "name": "兴宾区政协", "type": "政协", "level": "县级", "parent": "来宾市政协", "location": "兴宾区"},
    {"id": 5, "name": "来宾市人大常委会", "type": "人大", "level": "地市级", "parent": "广西壮族自治区人大常委会", "location": "来宾市"},
    {"id": 6, "name": "来宾市公安局兴宾分局", "type": "政府", "level": "县级", "parent": "来宾市公安局", "location": "兴宾区"},
    {"id": 7, "name": "广西壮族自治区园区发展和投资促进服务中心", "type": "事业单位", "level": "自治区级", "parent": "广西壮族自治区", "location": "南宁市"},
    {"id": 8, "name": "共青团广西来宾市委", "type": "群团", "level": "地市级", "parent": "共青团广西区委", "location": "来宾市"},
    {"id": 9, "name": "兴宾区人民政府办公室", "type": "政府", "level": "县级", "parent": "兴宾区人民政府", "location": "兴宾区"},
    {"id": 10, "name": "兴宾区纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共兴宾区委员会", "location": "兴宾区"},
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 王轶
    {"person_id": 1, "org_id": 1, "title": "兴宾区委书记", "start_date": "2024-08前", "end_date": "present", "rank": "副厅级", "note": "兼来宾市人大常委会副主任"},
    {"person_id": 1, "org_id": 5, "title": "来宾市人大常委会副主任", "start_date": "2024", "end_date": "present", "rank": "副厅级", "note": ""},
    # 管志斌
    {"person_id": 2, "org_id": 2, "title": "兴宾区政府区长", "start_date": "2026-04前", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "兴宾区委副书记", "start_date": "2026-04前", "end_date": "present", "rank": "正处级", "note": ""},
    # 唐彦乐
    {"person_id": 3, "org_id": 1, "title": "兴宾区委副书记", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": ""},
    # 黄大乘
    {"person_id": 4, "org_id": 1, "title": "兴宾区委常委", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "兴宾区副区长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 仇兴华
    {"person_id": 5, "org_id": 7, "title": "广西园区发展和投资促进服务中心投资促进三处副处长", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "兴宾区委常委（挂职）", "start_date": "待查", "end_date": "present", "rank": "挂职", "note": "驻村工作队队长"},
    {"person_id": 5, "org_id": 2, "title": "兴宾区副区长（挂职）", "start_date": "待查", "end_date": "present", "rank": "挂职", "note": "驻村工作队队长"},
    # 梁济谞
    {"person_id": 6, "org_id": 8, "title": "共青团广西来宾市委副书记", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "兴宾区委常委（挂职）", "start_date": "待查", "end_date": "present", "rank": "挂职", "note": "抓党建促乡村振兴工作队队长"},
    {"person_id": 6, "org_id": 2, "title": "兴宾区副区长（挂职）", "start_date": "待查", "end_date": "present", "rank": "挂职", "note": ""},
    # 潘锦辉
    {"person_id": 7, "org_id": 1, "title": "兴宾区委常委、统战部部长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "兼区政协党组副书记"},
    {"person_id": 7, "org_id": 4, "title": "兴宾区政协党组副书记（兼）", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 蓝文钰
    {"person_id": 8, "org_id": 1, "title": "兴宾区委常委", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 蒙函
    {"person_id": 9, "org_id": 1, "title": "兴宾区委常委", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 陆彦毓
    {"person_id": 10, "org_id": 1, "title": "兴宾区委常委", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 韦建红
    {"person_id": 11, "org_id": 1, "title": "兴宾区委常委", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 梁修田
    {"person_id": 12, "org_id": 1, "title": "兴宾区委常委、办公室主任", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 邓建宇
    {"person_id": 13, "org_id": 1, "title": "兴宾区委常委", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 黄宁
    {"person_id": 14, "org_id": 2, "title": "兴宾区副区长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 6, "title": "来宾市公安局兴宾分局局长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 覃泽毅
    {"person_id": 15, "org_id": 2, "title": "兴宾区副区长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 袁海斌
    {"person_id": 16, "org_id": 9, "title": "兴宾区人民政府办公室主任", "start_date": "待查", "end_date": "present", "rank": "正科级", "note": "区政府党组成员、办公室党组书记"},
    # 方革
    {"person_id": 17, "org_id": 3, "title": "兴宾区人大常委会主任", "start_date": "2024-02", "end_date": "present", "rank": "正处级", "note": "2024年2月兴宾区五届人大四次会议当选"},
    # 冉纪贵
    {"person_id": 18, "org_id": 4, "title": "兴宾区政协主席", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": ""},
    # 周灵（前任区委书记）
    {"person_id": 19, "org_id": 1, "title": "兴宾区委书记", "start_date": "待查", "end_date": "2024", "rank": "副厅级", "note": "前任，兼市人大常委会副主任"},
    {"person_id": 19, "org_id": 5, "title": "来宾市人大常委会副主任", "start_date": "待查", "end_date": "2024", "rank": "副厅级", "note": ""},
    # 蓝海鹏（前任区长）
    {"person_id": 20, "org_id": 2, "title": "兴宾区区长", "start_date": "待查", "end_date": "2026初", "rank": "正处级", "note": "前任区长"},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 书记-区长（党政一把手）
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "区委书记—区长党政搭档", "overlap_org": "中共兴宾区委员会/兴宾区人民政府", "overlap_period": "2026-"},
    # 书记-副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "区委书记—区委副书记", "overlap_org": "中共兴宾区委员会", "overlap_period": "2024/2025-"},
    # 书记-常委副区长
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "区委书记—区委常委、副区长", "overlap_org": "中共兴宾区委员会", "overlap_period": "2024/2025-"},
    # 书记-各常委
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "区委书记—挂职常委副区长", "overlap_org": "中共兴宾区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "区委书记—挂职常委副区长", "overlap_org": "中共兴宾区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "区委书记—统战部长", "overlap_org": "中共兴宾区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "区委书记—区委常委", "overlap_org": "中共兴宾区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "区委书记—区委常委", "overlap_org": "中共兴宾区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "区委书记—区委常委", "overlap_org": "中共兴宾区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate", "context": "区委书记—区委常委", "overlap_org": "中共兴宾区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate", "context": "区委书记—区委办公室主任", "overlap_org": "中共兴宾区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 13, "type": "superior_subordinate", "context": "区委书记—区委常委", "overlap_org": "中共兴宾区委员会", "overlap_period": ""},
    # 区长-副区长
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "区长—副区长", "overlap_org": "兴宾区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "区长—挂职副区长", "overlap_org": "兴宾区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "区长—挂职副区长", "overlap_org": "兴宾区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "区长—副区长（公安）", "overlap_org": "兴宾区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "区长—副区长", "overlap_org": "兴宾区人民政府", "overlap_period": ""},
    # 前任-现任（书记）
    {"person_a": 19, "person_b": 1, "type": "predecessor_successor", "context": "周灵→王轶 兴宾区委书记交接", "overlap_org": "中共兴宾区委员会", "overlap_period": "2024"},
    # 前任-现任（区长）
    {"person_a": 20, "person_b": 2, "type": "predecessor_successor", "context": "蓝海鹏→管志斌 兴宾区区长交接", "overlap_org": "兴宾区人民政府", "overlap_period": "2026"},
    # 人大-党委
    {"person_a": 17, "person_b": 1, "type": "overlap", "context": "人大常委会主任—区委书记（四套班子）", "overlap_org": "兴宾区", "overlap_period": ""},
    # 政协-党委
    {"person_a": 18, "person_b": 1, "type": "overlap", "context": "政协主席—区委书记（四套班子）", "overlap_org": "兴宾区", "overlap_period": ""},
    # 人大-区长
    {"person_a": 17, "person_b": 2, "type": "overlap", "context": "人大常委会主任—区长", "overlap_org": "兴宾区", "overlap_period": ""},
]


# =========================================================================
# 5. BUILD
# =========================================================================
def make_gexf(persons, orgs, positions, relationships, path):
    """Generate GEXF using string formatting (avoids ElementTree namespace issues)."""
    from datetime import datetime

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color(post):
        post_lower = post.lower() if post else ""
        if "区委书记" in post_lower or "县委书记" in post_lower:
            return "255,50,50"
        elif "区长" in post_lower or "县长" in post_lower:
            return "50,100,255"
        elif "纪委书记" in post_lower or "监委" in post_lower:
            return "255,165,0"
        else:
            return "100,100,100"

    def is_top_leader(post):
        post_lower = post.lower() if post else ""
        return "区委书记" in post_lower or "县委书记" in post_lower or "区长" in post_lower or "县长" in post_lower or "人大" in post_lower or "政协" in post_lower

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append(f'    <description>兴宾区领导班子工作关系网络 (as of {AS_OF})</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p.get("current_post", ""))
        sz = "20.0" if is_top_leader(p.get("current_post", "")) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in orgs:
        oid = o["id"] + 1000
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('        <viz:color r="200" g="200" b="200"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges: person->organization (worked_at)
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        oid = pos["org_id"] + 1000
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Edges: person<->person (relationship)
    for r in relationships:
        eid += 1
        weight = "2.0" if r["type"] in ("overlap", "predecessor_successor") else "1.0"
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF written: {path}")


def build():
    """Main build function."""
    # SQLite
    print(f"Building database: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Create tables
    c.execute("DROP TABLE IF EXISTS relationships")
    c.execute("DROP TABLE IF EXISTS positions")
    c.execute("DROP TABLE IF EXISTS organizations")
    c.execute("DROP TABLE IF EXISTS persons")

    c.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        gender TEXT DEFAULT '',
        ethnicity TEXT DEFAULT '',
        birth TEXT DEFAULT '',
        birthplace TEXT DEFAULT '',
        education TEXT DEFAULT '',
        party_join TEXT DEFAULT '',
        work_start TEXT DEFAULT '',
        current_post TEXT DEFAULT '',
        current_org TEXT DEFAULT '',
        source TEXT DEFAULT ''
    )""")

    c.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT DEFAULT '',
        level TEXT DEFAULT '',
        parent TEXT DEFAULT '',
        location TEXT DEFAULT ''
    )""")

    c.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER NOT NULL,
        org_id INTEGER NOT NULL,
        title TEXT DEFAULT '',
        start_date TEXT DEFAULT '',
        end_date TEXT DEFAULT '',
        rank TEXT DEFAULT '',
        note TEXT DEFAULT '',
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    )""")

    c.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER NOT NULL,
        person_b INTEGER NOT NULL,
        type TEXT DEFAULT '',
        context TEXT DEFAULT '',
        overlap_org TEXT DEFAULT '',
        overlap_period TEXT DEFAULT '',
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    )""")

    # Insert data
    for p in persons:
        c.execute("""INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education,
                    party_join, work_start, current_post, current_org, source)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
                   p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("INSERT INTO positions (person_id, org_id, title, start_date, end_date, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?, ?, ?, ?, ?, ?)",
                  (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()

    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    # GEXF
    print(f"Building GEXF: {GEXF_PATH}")
    make_gexf(persons, organizations, positions, relationships, GEXF_PATH)

    print("Done.")


if __name__ == "__main__":
    build()
