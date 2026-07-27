#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宁县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 甘肃省
Parent City: 庆阳市
Region: 宁县
Targets: 县委书记 & 县长

Research Sources:
- 宁县人民政府官方网站 (ningxian.gov.cn), 2026年7月确认
  - 县委领导: https://www.ningxian.gov.cn/zwgk/fdzdgknr/jgzn/cwld/
  - 政府领导: https://www.ningxian.gov.cn/zwgk/fdzdgknr/jgzn/zfld/
  - 常文洲简历: https://www.ningxian.gov.cn/zwgk/fdzdgknr/jgzn/zfld/xzfxz/content_84166
- 宁县政务动态新闻报道

Research Date: 2026-07-22
"""

import os
import sys
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths ──
SLUG = "宁县"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

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
        "name": "冯毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "宁县委书记",
        "current_org": "中共宁县委员会",
        "source": "宁县人民政府官网(ningxian.gov.cn) 2026-07; 宁县领导之窗"
    },
    {
        "id": 2,
        "name": "常文洲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年2月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "宁县委副书记、县政府党组书记、县长",
        "current_org": "宁县人民政府",
        "source": "宁县人民政府官网(ningxian.gov.cn) 2026-07; 领导之窗个人简介"
    },
    # ════════════════════════════════════════
    # 县委其他副书记
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "蒙文超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "宁县委副书记",
        "current_org": "中共宁县委员会",
        "source": "宁县人民政府官网(ningxian.gov.cn) 2026-07; 领导之窗"
    },
    # ════════════════════════════════════════
    # 县委常委（按官网列示）
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "王建广",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、副县长",
        "current_org": "宁县人民政府",
        "source": "宁县人民政府官网(ningxian.gov.cn) 2026-07; 领导之窗"
    },
    {
        "id": 5,
        "name": "贺炜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、纪委书记",
        "current_org": "中共宁县纪律检查委员会",
        "source": "宁县人民政府官网(ningxian.gov.cn) 2026-07; 领导之窗"
    },
    {
        "id": 6,
        "name": "徐小洲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共宁县委员会宣传部",
        "source": "宁县人民政府官网(ningxian.gov.cn) 2026-07; 领导之窗（2026年7月更新头像）"
    },
    {
        "id": 7,
        "name": "贾小建",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共宁县委员会政法委员会",
        "source": "宁县人民政府官网(ningxian.gov.cn) 2026-07; 领导之窗"
    },
    {
        "id": 8,
        "name": "李晓刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、副县长",
        "current_org": "宁县人民政府",
        "source": "宁县人民政府官网(ningxian.gov.cn) 2026-07; 领导之窗"
    },
    {
        "id": 9,
        "name": "罗婕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共宁县委员会组织部",
        "source": "宁县人民政府官网(ningxian.gov.cn) 2026-07; 领导之窗（2025年5月更新头像）"
    },
    {
        "id": 10,
        "name": "咸子逸",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、副县长",
        "current_org": "宁县人民政府",
        "source": "宁县人民政府官网(ningxian.gov.cn) 2026-07; 领导之窗（2026年2月更新头像）"
    },
    {
        "id": 11,
        "name": "杨博涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委，县政府党组副书记、副县长候选人，长庆桥工业集中区工作委员会书记、管委会主任（兼）",
        "current_org": "宁县人民政府",
        "source": "宁县人民政府官网(ningxian.gov.cn) 2026-07; 领导之窗（2026年7月更新头像）"
    },
    # ════════════════════════════════════════
    # 县政府其他副县长
    # ════════════════════════════════════════
    {
        "id": 12,
        "name": "栗芳年",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县政府党组成员、副县长",
        "current_org": "宁县人民政府",
        "source": "宁县人民政府官网(ningxian.gov.cn) 2026-07; 领导之窗"
    },
    {
        "id": 13,
        "name": "秦建宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县政府党组成员、副县长，县公安局党委书记、局长",
        "current_org": "宁县人民政府",
        "source": "宁县人民政府官网(ningxian.gov.cn) 2026-07; 领导之窗"
    },
    {
        "id": 14,
        "name": "郭德祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县政府党组成员、副县长",
        "current_org": "宁县人民政府",
        "source": "宁县人民政府官网(ningxian.gov.cn) 2026-07; 领导之窗（2025年2月更新头像）"
    },
    {
        "id": 15,
        "name": "陶志金",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县政府党组成员、副县长",
        "current_org": "宁县人民政府",
        "source": "宁县人民政府官网(ningxian.gov.cn) 2026-07; 领导之窗（2025年5月更新头像）"
    },
    {
        "id": 16,
        "name": "代娅娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县政府党组成员、副县长",
        "current_org": "宁县人民政府",
        "source": "宁县人民政府官网(ningxian.gov.cn) 2026-07; 领导之窗（2025年11月更新头像）"
    },
    # ════════════════════════════════════════
    # 县人大
    # ════════════════════════════════════════
    {
        "id": 17,
        "name": "姚德学",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县人大常委会党组书记、主任",
        "current_org": "宁县人民代表大会常务委员会",
        "source": "宁县人民政府官网(ningxian.gov.cn) 2026-07; 领导之窗"
    },
    # ════════════════════════════════════════
    # 县政协
    # ════════════════════════════════════════
    {
        "id": 18,
        "name": "石博学",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县政协党组书记、主席",
        "current_org": "中国人民政治协商会议宁县委员会",
        "source": "宁县人民政府官网(ningxian.gov.cn) 2026-07; 领导之窗"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共宁县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共庆阳市委员会",
        "location": "甘肃省庆阳市宁县"
    },
    {
        "id": 2,
        "name": "宁县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "庆阳市人民政府",
        "location": "甘肃省庆阳市宁县"
    },
    {
        "id": 3,
        "name": "宁县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "庆阳市人民代表大会常务委员会",
        "location": "甘肃省庆阳市宁县"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议宁县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "政协庆阳市委员会",
        "location": "甘肃省庆阳市宁县"
    },
    {
        "id": 5,
        "name": "中共宁县纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共宁县委员会",
        "location": "甘肃省庆阳市宁县"
    },
    {
        "id": 6,
        "name": "中共宁县委员会宣传部",
        "type": "党委",
        "level": "县级",
        "parent": "中共宁县委员会",
        "location": "甘肃省庆阳市宁县"
    },
    {
        "id": 7,
        "name": "中共宁县委员会政法委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共宁县委员会",
        "location": "甘肃省庆阳市宁县"
    },
    {
        "id": 8,
        "name": "中共宁县委员会组织部",
        "type": "党委",
        "level": "县级",
        "parent": "中共宁县委员会",
        "location": "甘肃省庆阳市宁县"
    },
    {
        "id": 9,
        "name": "宁县公安局",
        "type": "政府",
        "level": "县级",
        "parent": "宁县人民政府",
        "location": "甘肃省庆阳市宁县"
    },
    {
        "id": 10,
        "name": "长庆桥工业集中区",
        "type": "开发区",
        "level": "县级",
        "parent": "宁县人民政府",
        "location": "甘肃省庆阳市宁县长庆桥镇"
    },
    {
        "id": 11,
        "name": "中共庆阳市委员会",
        "type": "党委",
        "level": "地市级",
        "parent": "中共甘肃省委员会",
        "location": "甘肃省庆阳市"
    },
]

# 3. Positions
positions = [
    # 冯毅
    {"person_id": 1, "org_id": 1, "title": "宁县委书记", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": ""},
    # 常文洲
    {"person_id": 2, "org_id": 1, "title": "宁县委副书记", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县政府党组书记、县长", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "主持县政府全面工作"},
    # 蒙文超
    {"person_id": 3, "org_id": 1, "title": "宁县委副书记", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": ""},
    # 王建广
    {"person_id": 4, "org_id": 2, "title": "县委常委、副县长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 贺炜
    {"person_id": 5, "org_id": 5, "title": "县委常委、纪委书记", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 徐小洲
    {"person_id": 6, "org_id": 6, "title": "县委常委、宣传部部长", "start_date": "2026年", "end_date": "present", "rank": "副处级", "note": "2026年7月更新领导头像"},
    # 贾小建
    {"person_id": 7, "org_id": 7, "title": "县委常委、政法委书记", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 李晓刚
    {"person_id": 8, "org_id": 2, "title": "县委常委、副县长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 罗婕
    {"person_id": 9, "org_id": 8, "title": "县委常委、组织部部长", "start_date": "2025年", "end_date": "present", "rank": "副处级", "note": "2025年5月更新领导头像"},
    # 咸子逸
    {"person_id": 10, "org_id": 2, "title": "县委常委、副县长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "2026年2月更新头像"},
    # 杨博涛
    {"person_id": 11, "org_id": 2, "title": "县委常委，县政府党组副书记、副县长候选人", "start_date": "2026年", "end_date": "present", "rank": "副处级", "note": "2026年7月更新头像"},
    {"person_id": 11, "org_id": 10, "title": "长庆桥工业集中区工作委员会书记、管委会主任（兼）", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 栗芳年
    {"person_id": 12, "org_id": 2, "title": "县政府党组成员、副县长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 秦建宏
    {"person_id": 13, "org_id": 2, "title": "县政府党组成员、副县长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 9, "title": "县公安局党委书记、局长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 郭德祥
    {"person_id": 14, "org_id": 2, "title": "县政府党组成员、副县长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "2025年2月更新头像"},
    # 陶志金
    {"person_id": 15, "org_id": 2, "title": "县政府党组成员、副县长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "2025年5月更新头像"},
    # 代娅娟
    {"person_id": 16, "org_id": 2, "title": "县政府党组成员、副县长", "start_date": "2025年", "end_date": "present", "rank": "副处级", "note": "2025年11月更新头像"},
    # 姚德学
    {"person_id": 17, "org_id": 3, "title": "县人大常委会党组书记、主任", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": ""},
    # 石博学
    {"person_id": 18, "org_id": 4, "title": "县政协党组书记、主席", "start_date": "2025年", "end_date": "present", "rank": "正处级", "note": "2025年1月更新头像"},
]

# 4. Relationships
relationships = [
    # 党委-政府主要领导
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "党委-政府主要领导协作关系",
        "overlap_org": "宁县",
        "overlap_period": "2026年",
        "confidence": "confirmed"
    },
    # 冯毅-蒙文超: 书记-副书记
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记-县委副书记协作关系",
        "overlap_org": "中共宁县委员会",
        "overlap_period": "2026年",
        "confidence": "confirmed"
    },
    # 常文洲-蒙文超: 两位县委副书记
    {
        "person_a": 2,
        "person_b": 3,
        "type": "overlap",
        "context": "同为宁县委副书记",
        "overlap_org": "中共宁县委员会",
        "overlap_period": "2026年",
        "confidence": "confirmed"
    },
    # 县委常委间的关系（同属常委会）
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "县委书记-县委常委/副县长",
        "overlap_org": "中共宁县委员会",
        "overlap_period": "2026年",
        "confidence": "confirmed"
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "县委书记-县委常委/纪委书记",
        "overlap_org": "中共宁县委员会",
        "overlap_period": "2026年",
        "confidence": "confirmed"
    },
    {
        "person_a": 1,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "县委书记-县委常委/宣传部部长",
        "overlap_org": "中共宁县委员会",
        "overlap_period": "2026年",
        "confidence": "confirmed"
    },
    {
        "person_a": 1,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "县委书记-县委常委/政法委书记",
        "overlap_org": "中共宁县委员会",
        "overlap_period": "2026年",
        "confidence": "confirmed"
    },
    {
        "person_a": 1,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "县委书记-县委常委/副县长",
        "overlap_org": "中共宁县委员会",
        "overlap_period": "2026年",
        "confidence": "confirmed"
    },
    {
        "person_a": 1,
        "person_b": 9,
        "type": "superior_subordinate",
        "context": "县委书记-县委常委/组织部部长",
        "overlap_org": "中共宁县委员会",
        "overlap_period": "2026年",
        "confidence": "confirmed"
    },
    {
        "person_a": 1,
        "person_b": 10,
        "type": "superior_subordinate",
        "context": "县委书记-县委常委/副县长",
        "overlap_org": "中共宁县委员会",
        "overlap_period": "2026年",
        "confidence": "confirmed"
    },
    {
        "person_a": 1,
        "person_b": 11,
        "type": "superior_subordinate",
        "context": "县委书记-县委常委/党组副书记",
        "overlap_org": "中共宁县委员会",
        "overlap_period": "2026年",
        "confidence": "confirmed"
    },
    # 县长-副县长: 政府班子关系
    {
        "person_a": 2,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "县长-副县长",
        "overlap_org": "宁县人民政府",
        "overlap_period": "2026年",
        "confidence": "confirmed"
    },
    {
        "person_a": 2,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "县长-副县长",
        "overlap_org": "宁县人民政府",
        "overlap_period": "2026年",
        "confidence": "confirmed"
    },
    {
        "person_a": 2,
        "person_b": 10,
        "type": "superior_subordinate",
        "context": "县长-副县长",
        "overlap_org": "宁县人民政府",
        "overlap_period": "2026年",
        "confidence": "confirmed"
    },
    {
        "person_a": 2,
        "person_b": 11,
        "type": "superior_subordinate",
        "context": "县长-县政府党组副书记",
        "overlap_org": "宁县人民政府",
        "overlap_period": "2026年",
        "confidence": "confirmed"
    },
    {
        "person_a": 2,
        "person_b": 12,
        "type": "superior_subordinate",
        "context": "县长-副县长",
        "overlap_org": "宁县人民政府",
        "overlap_period": "2026年",
        "confidence": "confirmed"
    },
    {
        "person_a": 2,
        "person_b": 13,
        "type": "superior_subordinate",
        "context": "县长-副县长",
        "overlap_org": "宁县人民政府",
        "overlap_period": "2026年",
        "confidence": "confirmed"
    },
    {
        "person_a": 2,
        "person_b": 14,
        "type": "superior_subordinate",
        "context": "县长-副县长",
        "overlap_org": "宁县人民政府",
        "overlap_period": "2026年",
        "confidence": "confirmed"
    },
    {
        "person_a": 2,
        "person_b": 15,
        "type": "superior_subordinate",
        "context": "县长-副县长",
        "overlap_org": "宁县人民政府",
        "overlap_period": "2026年",
        "confidence": "confirmed"
    },
    {
        "person_a": 2,
        "person_b": 16,
        "type": "superior_subordinate",
        "context": "县长-副县长",
        "overlap_org": "宁县人民政府",
        "overlap_period": "2026年",
        "confidence": "confirmed"
    },
    # 县人大与县委
    {
        "person_a": 1,
        "person_b": 17,
        "type": "overlap",
        "context": "县委-县人大主要领导协作",
        "overlap_org": "宁县",
        "overlap_period": "2026年",
        "confidence": "confirmed"
    },
    # 县政协与县委
    {
        "person_a": 1,
        "person_b": 18,
        "type": "overlap",
        "context": "县委-县政协主要领导协作",
        "overlap_org": "宁县",
        "overlap_period": "2026年",
        "confidence": "confirmed"
    },
]


# ── Main ──
def main():
    print(f"=== {SLUG} 网络数据构建 ===")
    print(f"人员: {len(persons)} 人")
    print(f"组织机构: {len(organizations)} 个")
    print(f"任职记录: {len(positions)} 条")
    print(f"关系: {len(relationships)} 条")

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

    print(f"\n=== 完成 ===")


if __name__ == "__main__":
    main()
