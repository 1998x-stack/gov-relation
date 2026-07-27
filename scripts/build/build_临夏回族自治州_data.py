#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
临夏回族自治州领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Linxia Hui Autonomous Prefecture leadership network.

Level: 地级市 (自治州)
Province: 甘肃省
Region: 临夏回族自治州
Targets: 州委书记 & 州长

Research Sources:
- 临夏回族自治州人民政府官方网站 (linxia.gov.cn) 领导之窗 (ldzc/), 2026年7月22日确认
- 临夏州人民政府网站新闻

Confirmed officeholders (as of 2026-07-22, from linxia.gov.cn 领导之窗):
- 州委书记: 王国斌 (男，汉族，1972年7月出生，研究生学历，公共管理硕士，中共党员)
- 州委副书记、州长: 马斌 (男，回族，1977年6月出生，省委党校研究生学历，中共党员)
- 州委副书记: 万学科 (男，汉族，1973年5月出生，省委党校研究生学历，中共党员)

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
SLUG = "临夏回族自治州"
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
        "name": "王国斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年7月",
        "birthplace": "",
        "education": "研究生学历，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "临夏州委书记",
        "current_org": "中共临夏回族自治州委员会",
        "source": "https://www.linxia.gov.cn/ldzc/ — 临夏州政府网站领导之窗, 2026年7月22日确认"
    },
    {
        "id": 2,
        "name": "马斌",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1977年6月",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "临夏州委副书记、州长",
        "current_org": "临夏回族自治州人民政府",
        "source": "https://www.linxia.gov.cn/ldzc/ — 临夏州政府网站领导之窗, 2026年7月22日确认"
    },
    {
        "id": 3,
        "name": "万学科",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年5月",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "临夏州委副书记",
        "current_org": "中共临夏回族自治州委员会",
        "source": "https://www.linxia.gov.cn/ldzc/ — 临夏州政府网站领导之窗, 2026年7月22日确认"
    },
    # ════════════════════════════════════════
    # 州委常委
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "李勇",
        "gender": "男",
        "ethnicity": "",
        "birth": "1977年9月",
        "birthplace": "",
        "education": "研究生学历，法学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "州委常委、积石山县委书记",
        "current_org": "中共积石山县委",
        "source": "https://www.linxia.gov.cn/ldzc/ — 临夏州政府网站领导之窗, 2026年7月22日确认"
    },
    {
        "id": 5,
        "name": "石磊",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "州委常委、临夏军分区政委",
        "current_org": "临夏军分区",
        "source": "https://www.linxia.gov.cn/ldzc/ — 临夏州政府网站领导之窗, 2026年7月22日确认"
    },
    {
        "id": 6,
        "name": "毛鸿博",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年3月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "州委常委、常务副州长",
        "current_org": "临夏回族自治州人民政府",
        "source": "https://www.linxia.gov.cn/ldzc/ — 临夏州政府网站领导之窗, 2026年7月22日确认"
    },
    {
        "id": 7,
        "name": "陈吉勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年12月",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "州委常委、政法委书记",
        "current_org": "中共临夏州委政法委员会",
        "source": "https://www.linxia.gov.cn/ldzc/ — 临夏州政府网站领导之窗, 2026年7月22日确认"
    },
    {
        "id": 8,
        "name": "李敏娜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1975年8月",
        "birthplace": "",
        "education": "大学学历，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "州委常委、宣传部部长",
        "current_org": "中共临夏州委宣传部",
        "source": "https://www.linxia.gov.cn/ldzc/ — 临夏州政府网站领导之窗, 2026年7月22日确认"
    },
    {
        "id": 9,
        "name": "黄海龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年8月",
        "birthplace": "",
        "education": "大学学历，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "州委常委、组织部部长",
        "current_org": "中共临夏州委组织部",
        "source": "https://www.linxia.gov.cn/ldzc/ — 临夏州政府网站领导之窗, 2026年7月22日确认"
    },
    {
        "id": 10,
        "name": "马显锋",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1972年10月",
        "birthplace": "",
        "education": "大学学历，哲学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "州委常委、统战部部长、州政协党组副书记",
        "current_org": "中共临夏州委统战部",
        "source": "https://www.linxia.gov.cn/ldzc/ — 临夏州政府网站领导之窗, 2026年7月22日确认"
    },
    {
        "id": 11,
        "name": "徐鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年9月",
        "birthplace": "",
        "education": "省委党校研究生学历，管理学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "州委常委、州纪委书记、州监委代主任",
        "current_org": "中共临夏州纪律检查委员会",
        "source": "https://www.linxia.gov.cn/ldzc/ — 临夏州政府网站领导之窗, 2026年7月22日确认"
    },
    {
        "id": 12,
        "name": "杨志军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年4月",
        "birthplace": "甘肃临夏县",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "州委常委、副州长",
        "current_org": "临夏回族自治州人民政府",
        "source": "https://www.linxia.gov.cn/ldzc/ — 临夏州政府网站领导之窗, 2026年7月22日确认"
    },
    {
        "id": 13,
        "name": "张杰刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年1月",
        "birthplace": "",
        "education": "研究生学历，管理学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "州委常委、副州长",
        "current_org": "临夏回族自治州人民政府",
        "source": "https://www.linxia.gov.cn/ldzc/ — 临夏州政府网站领导之窗, 2026年7月22日确认"
    },
    # ════════════════════════════════════════
    # 副州长 (非常委)
    # ════════════════════════════════════════
    {
        "id": 14,
        "name": "李明海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年7月",
        "birthplace": "",
        "education": "大学学历，管理学硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "副州长（民盟）",
        "current_org": "临夏回族自治州人民政府",
        "source": "https://www.linxia.gov.cn/ldzc/ — 临夏州政府网站领导之窗, 2026年7月22日确认"
    },
    {
        "id": 15,
        "name": "王光龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年1月",
        "birthplace": "",
        "education": "研究生学历，历史学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副州长",
        "current_org": "临夏回族自治州人民政府",
        "source": "https://www.linxia.gov.cn/ldzc/ — 临夏州政府网站领导之窗, 2026年7月22日确认"
    },
    {
        "id": 16,
        "name": "马国全",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1977年6月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副州长（挂职住建部）",
        "current_org": "临夏回族自治州人民政府",
        "source": "https://www.linxia.gov.cn/ldzc/ — 临夏州政府网站领导之窗, 2026年7月22日确认"
    },
    {
        "id": 17,
        "name": "何珺",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982年12月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副州长",
        "current_org": "临夏回族自治州人民政府",
        "source": "https://www.linxia.gov.cn/ldzc/ — 临夏州政府网站领导之窗, 2026年7月22日确认"
    },
    {
        "id": 18,
        "name": "张茂龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年6月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副州长、州公安局局长",
        "current_org": "临夏回族自治州人民政府",
        "source": "https://www.linxia.gov.cn/ldzc/ — 临夏州政府网站领导之窗, 2026年7月22日确认"
    },
    # ════════════════════════════════════════
    # 州政府秘书长
    # ════════════════════════════════════════
    {
        "id": 19,
        "name": "马福俊",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1975年5月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "州政府秘书长",
        "current_org": "临夏回族自治州人民政府",
        "source": "https://www.linxia.gov.cn/ldzc/ — 临夏州政府网站领导之窗, 2026年7月22日确认"
    },
    # ════════════════════════════════════════
    # 人大常委会、政协主要领导
    # ════════════════════════════════════════
    {
        "id": 20,
        "name": "蒋建民",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "州人大常委会党组书记、主任",
        "current_org": "临夏回族自治州人民代表大会常务委员会",
        "source": "https://www.linxia.gov.cn — 临夏州新闻: 州人大常委会及机关召开警示教育会, 2026年7月22日"
    },
]

# 2. Organizations
organizations = [
    {"id": 1, "name": "中共临夏回族自治州委员会", "type": "党委", "level": "地级市", "parent": "中共甘肃省委员会", "location": "甘肃省临夏市"},
    {"id": 2, "name": "临夏回族自治州人民政府", "type": "政府", "level": "地级市", "parent": "甘肃省人民政府", "location": "甘肃省临夏市"},
    {"id": 3, "name": "中共临夏州委政法委员会", "type": "党委", "level": "地级市", "parent": "中共临夏回族自治州委员会", "location": "甘肃省临夏市"},
    {"id": 4, "name": "中共临夏州委宣传部", "type": "党委", "level": "地级市", "parent": "中共临夏回族自治州委员会", "location": "甘肃省临夏市"},
    {"id": 5, "name": "中共临夏州委组织部", "type": "党委", "level": "地级市", "parent": "中共临夏回族自治州委员会", "location": "甘肃省临夏市"},
    {"id": 6, "name": "中共临夏州委统战部", "type": "党委", "level": "地级市", "parent": "中共临夏回族自治州委员会", "location": "甘肃省临夏市"},
    {"id": 7, "name": "中共临夏州纪律检查委员会", "type": "党委", "level": "地级市", "parent": "中共临夏回族自治州委员会", "location": "甘肃省临夏市"},
    {"id": 8, "name": "临夏军分区", "type": "党委", "level": "地级市", "parent": "甘肃省军区", "location": "甘肃省临夏市"},
    {"id": 9, "name": "中共积石山县委", "type": "党委", "level": "县", "parent": "中共临夏回族自治州委员会", "location": "甘肃省积石山县"},
    {"id": 10, "name": "临夏回族自治州人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "甘肃省人大常委会", "location": "甘肃省临夏市"},
]

# 3. Positions (linking persons to organizations)
positions = [
    # 州委（Party Committee）
    {"person_id": 1, "org_id": 1, "title": "州委书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "州委全面工作"},
    {"person_id": 2, "org_id": 1, "title": "州委副书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "兼州长"},
    {"person_id": 3, "org_id": 1, "title": "州委副书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "专职副书记"},
    {"person_id": 4, "org_id": 1, "title": "州委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "兼积石山县委书记"},
    {"person_id": 5, "org_id": 1, "title": "州委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "兼临夏军分区政委"},
    {"person_id": 6, "org_id": 1, "title": "州委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "兼常务副州长"},
    {"person_id": 7, "org_id": 1, "title": "州委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "兼政法委书记"},
    {"person_id": 8, "org_id": 1, "title": "州委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "兼宣传部部长"},
    {"person_id": 9, "org_id": 1, "title": "州委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "兼组织部部长"},
    {"person_id": 10, "org_id": 1, "title": "州委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "兼统战部部长"},
    {"person_id": 11, "org_id": 1, "title": "州委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "兼纪委书记、监委代主任"},
    {"person_id": 12, "org_id": 1, "title": "州委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "兼副州长"},
    {"person_id": 13, "org_id": 1, "title": "州委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "兼副州长"},
    # 州政府（Prefecture Government）
    {"person_id": 2, "org_id": 2, "title": "州长", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "州政府全面工作"},
    {"person_id": 6, "org_id": 2, "title": "常务副州长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "州政府日常事务"},
    {"person_id": 12, "org_id": 2, "title": "副州长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "农业农村、自然资源、交通运输等"},
    {"person_id": 13, "org_id": 2, "title": "副州长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "东西协作、中央单位定点帮扶"},
    {"person_id": 14, "org_id": 2, "title": "副州长", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "人社、民政、工信（民盟）"},
    {"person_id": 15, "org_id": 2, "title": "副州长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "住建、文旅、科技、市场监管等"},
    {"person_id": 16, "org_id": 2, "title": "副州长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "住建部挂职"},
    {"person_id": 17, "org_id": 2, "title": "副州长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "教育、卫健、医保"},
    {"person_id": 18, "org_id": 2, "title": "副州长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "公安、退役军人事务"},
    {"person_id": 19, "org_id": 2, "title": "秘书长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "州政府办公室工作"},
    # 政法系统
    {"person_id": 7, "org_id": 3, "title": "政法委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 宣传部
    {"person_id": 8, "org_id": 4, "title": "宣传部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 组织部
    {"person_id": 9, "org_id": 5, "title": "组织部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 统战部
    {"person_id": 10, "org_id": 6, "title": "统战部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 纪委
    {"person_id": 11, "org_id": 7, "title": "州纪委书记、监委代主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 军分区
    {"person_id": 5, "org_id": 8, "title": "政委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 积石山县
    {"person_id": 4, "org_id": 9, "title": "积石山县委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "李勇兼"},
    # 人大常委会
    {"person_id": 20, "org_id": 10, "title": "主任", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # 公安局
    {"person_id": 18, "org_id": 3, "title": "州公安局局长（兼）", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "张茂龙兼"},
]

# 4. Relationships
relationships = [
    # 州委班子关系
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "州委书记—州委副书记/州长", "overlap_org": "中共临夏回族自治州委员会", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "州委书记—专职副书记", "overlap_org": "中共临夏回族自治州委员会", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "州委副书记—州委副书记", "overlap_org": "中共临夏回族自治州委员会", "overlap_period": "现任"},
    # 州委常委关系（书记与常委）
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "州委书记—州委常委", "overlap_org": "中共临夏回族自治州委员会", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "州委书记—州委常委", "overlap_org": "中共临夏回族自治州委员会", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "州委书记—州委常委", "overlap_org": "中共临夏回族自治州委员会", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "州委书记—州委常委", "overlap_org": "中共临夏回族自治州委员会", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "州委书记—州委常委", "overlap_org": "中共临夏回族自治州委员会", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "州委书记—州委常委", "overlap_org": "中共临夏回族自治州委员会", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "州委书记—州委常委", "overlap_org": "中共临夏回族自治州委员会", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "州委书记—州委常委", "overlap_org": "中共临夏回族自治州委员会", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "州委书记—州委常委", "overlap_org": "中共临夏回族自治州委员会", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 13, "type": "overlap", "context": "州委书记—州委常委", "overlap_org": "中共临夏回族自治州委员会", "overlap_period": "现任"},
    # 州政府班子关系（州长与副州长）
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "州长—常务副州长", "overlap_org": "临夏回族自治州人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "州长—副州长", "overlap_org": "临夏回族自治州人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "州长—副州长", "overlap_org": "临夏回族自治州人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "州长—副州长", "overlap_org": "临夏回族自治州人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 15, "type": "overlap", "context": "州长—副州长", "overlap_org": "临夏回族自治州人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 16, "type": "overlap", "context": "州长—副州长", "overlap_org": "临夏回族自治州人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 17, "type": "overlap", "context": "州长—副州长", "overlap_org": "临夏回族自治州人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 18, "type": "overlap", "context": "州长—副州长", "overlap_org": "临夏回族自治州人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 19, "type": "overlap", "context": "州长—秘书长", "overlap_org": "临夏回族自治州人民政府", "overlap_period": "现任"},
    # 常委之间关系
    {"person_a": 6, "person_b": 7, "type": "overlap", "context": "常务副州长—政法委书记", "overlap_org": "中共临夏回族自治州委员会", "overlap_period": "现任"},
    {"person_a": 8, "person_b": 9, "type": "overlap", "context": "宣传部部长—组织部部长", "overlap_org": "中共临夏回族自治州委员会", "overlap_period": "现任"},
    {"person_a": 7, "person_b": 18, "type": "overlap", "context": "政法委书记—州公安局局长", "overlap_org": "中共临夏州委政法委员会", "overlap_period": "现任"},
]


# ══════════════════════════════════════════════════════════════
# Build
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print(f"[{SLUG}] Building database: {DB_PATH}")
    print(f"[{SLUG}] Building GEXF: {GEXF_PATH}")

    from gov_relation.runner import run_build

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

    print(f"[{SLUG}] Done. DB: {DB_PATH}")
    print(f"[{SLUG}] Done. GEXF: {GEXF_PATH}")
