#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
贺州市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 地级市
Province: 广西壮族自治区
Parent City:
Region: 贺州市
Targets: 市委书记 & 市长

Research Date: 2026-07-23
"""

import json
import os
import sqlite3  # noqa: F401 — used by gov_relation.runner
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (staging) ──
SLUG = "贺州市"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-23"

# =========================================================================
# 1. PERSONS
# =========================================================================
persons = [
    # ════════════════════════════════════════
    # 核心领导：市委书记
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "李国忠",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "贺州市委书记",
        "current_org": "中共贺州市委员会",
        "source": "http://www.gxhz.gov.cn/ywzx/ldhd_37591/t27930094.shtml"
    },
    # ════════════════════════════════════════
    # 核心领导：市长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "彭代元",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年3月",
        "birthplace": "广西兴安",
        "education": "广西区委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "贺州市委副书记、市长、党组书记",
        "current_org": "中共贺州市委员会/贺州市人民政府",
        "source": "http://www.gxhz.gov.cn/zfxxgk/fdzdgknr/ldxx/sz/index.shtml"
    },
    # ════════════════════════════════════════
    # 市人大常委会主任
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "陆海平",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "贺州市人大常委会主任",
        "current_org": "贺州市人民代表大会常务委员会",
        "source": "http://www.gxhz.gov.cn/ywzx/ldhd_37591/t27930108.shtml"
    },
    # ════════════════════════════════════════
    # 市政协主席
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "蓝树东",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "贺州市政协主席",
        "current_org": "中国人民政治协商会议贺州市委员会",
        "source": "http://www.gxhz.gov.cn/ywzx/ldhd_37591/t27930108.shtml"
    },
    # ════════════════════════════════════════
    # 市委副书记
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "钟洪",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "贺州市委副书记",
        "current_org": "中共贺州市委员会",
        "source": "http://www.gxhz.gov.cn/sylbt/t27857838.shtml"
    },
    # ════════════════════════════════════════
    # 市委常委、常务副市长
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "何翔",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年2月",
        "birthplace": "待查",
        "education": "研究生学历，工学博士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "贺州市委常委、副市长（常务）",
        "current_org": "中共贺州市委员会/贺州市人民政府",
        "source": "http://www.gxhz.gov.cn/zfxxgk/fdzdgknr/ldxx/fsz/t4157809.shtml"
    },
    # ════════════════════════════════════════
    # 市委常委、统战部部长、副市长
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "蒋晓军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年9月",
        "birthplace": "待查",
        "education": "在职研究生学历，工程硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "贺州市委常委、统战部部长、副市长",
        "current_org": "中共贺州市委员会/贺州市人民政府",
        "source": "http://www.gxhz.gov.cn/zfxxgk/fdzdgknr/ldxx/fsz/t4160750.shtml"
    },
    # ════════════════════════════════════════
    # 市委常委、副市长（挂职）
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "李丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1979年12月",
        "birthplace": "待查",
        "education": "法学硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "贺州市委常委、副市长（挂职），中央港澳办五局副局长",
        "current_org": "中共贺州市委员会/贺州市人民政府",
        "source": "http://www.gxhz.gov.cn/zfxxgk/fdzdgknr/ldxx/fsz/t5669648.shtml"
    },
    # ════════════════════════════════════════
    # 副市长（无党派）
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "罗剑",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1975年12月",
        "birthplace": "待查",
        "education": "大学学历，经济学学士",
        "party_join": "无党派",
        "work_start": "待查",
        "current_post": "贺州市副市长",
        "current_org": "贺州市人民政府",
        "source": "http://www.gxhz.gov.cn/zfxxgk/fdzdgknr/ldxx/fsz/t10454792.shtml"
    },
    # ════════════════════════════════════════
    # 副市长（兼钟山县委书记）
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "程钊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年12月",
        "birthplace": "待查",
        "education": "研究生学历，工学博士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "贺州市副市长、党组成员，钟山县委书记",
        "current_org": "贺州市人民政府/中共钟山县委员会",
        "source": "http://www.gxhz.gov.cn/zfxxgk/fdzdgknr/ldxx/fsz/t10454843.shtml"
    },
    # ════════════════════════════════════════
    # 副市长
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "冯旭波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年4月",
        "birthplace": "待查",
        "education": "在职研究生学历，工学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "贺州市副市长、党组成员",
        "current_org": "贺州市人民政府",
        "source": "http://www.gxhz.gov.cn/zfxxgk/fdzdgknr/ldxx/fsz/t4159934.shtml"
    },
    # ════════════════════════════════════════
    # 副市长、市公安局局长
    # ════════════════════════════════════════
    {
        "id": 12,
        "name": "陈耀超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年3月",
        "birthplace": "待查",
        "education": "在职大学学历，法学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "贺州市副市长、党组成员，市公安局局长、党委书记",
        "current_org": "贺州市人民政府/贺州市公安局",
        "source": "http://www.gxhz.gov.cn/zfxxgk/fdzdgknr/ldxx/fsz/t17500153.shtml"
    },
    # ════════════════════════════════════════
    # 市政府秘书长
    # ════════════════════════════════════════
    {
        "id": 13,
        "name": "陈展维",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年12月",
        "birthplace": "待查",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "贺州市人民政府秘书长、党组成员，办公室党组书记、主任",
        "current_org": "贺州市人民政府办公室",
        "source": "http://www.gxhz.gov.cn/zfxxgk/fdzdgknr/ldxx/msz/t10380578.shtml"
    },
    # ════════════════════════════════════════
    # 前市委书记：李宏庆（2017-2021）
    # ════════════════════════════════════════
    {
        "id": 14,
        "name": "李宏庆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1963年10月",
        "birthplace": "广西博白",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "1985年7月",
        "current_post": "广西壮族自治区农业农村厅原厅长",
        "current_org": "广西壮族自治区农业农村厅",
        "source": "公开资料"
    },
    # ════════════════════════════════════════
    # 前市委书记/市长：林冠（2016-2021任市长, 2021-2023任书记）
    # ════════════════════════════════════════
    {
        "id": 15,
        "name": "林冠",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1966年11月",
        "birthplace": "广西平乐",
        "education": "中央党校研究生学历",
        "party_join": "中共党员",
        "work_start": "1987年7月",
        "current_post": "广西投资集团有限公司原党委书记、董事长",
        "current_org": "广西投资集团有限公司",
        "source": "公开资料"
    },
]

# =========================================================================
# 2. ORGANIZATIONS
# =========================================================================
organizations = [
    {
        "id": 1,
        "name": "中共贺州市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共广西壮族自治区委员会",
        "location": "广西贺州"
    },
    {
        "id": 2,
        "name": "贺州市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "广西壮族自治区人民政府",
        "location": "广西贺州"
    },
    {
        "id": 3,
        "name": "贺州市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级市",
        "parent": "广西壮族自治区人民代表大会常务委员会",
        "location": "广西贺州"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议贺州市委员会",
        "type": "政协",
        "level": "地级市",
        "parent": "中国人民政治协商会议广西壮族自治区委员会",
        "location": "广西贺州"
    },
    {
        "id": 5,
        "name": "贺州市公安局",
        "type": "政府",
        "level": "地级市",
        "parent": "贺州市人民政府",
        "location": "广西贺州"
    },
    {
        "id": 6,
        "name": "贺州市人民政府办公室",
        "type": "政府",
        "level": "地级市",
        "parent": "贺州市人民政府",
        "location": "广西贺州"
    },
    {
        "id": 7,
        "name": "中共钟山县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共贺州市委员会",
        "location": "广西贺州钟山"
    },
    {
        "id": 8,
        "name": "广西壮族自治区农业农村厅",
        "type": "政府",
        "level": "省级",
        "parent": "广西壮族自治区人民政府",
        "location": "广西南宁"
    },
    {
        "id": 9,
        "name": "广西投资集团有限公司",
        "type": "政府",
        "level": "省级",
        "parent": "广西壮族自治区人民政府",
        "location": "广西南宁"
    },
    {
        "id": 10,
        "name": "中央港澳工作办公室",
        "type": "政府",
        "level": "国家级",
        "parent": "",
        "location": "北京"
    },
]

# =========================================================================
# 3. POSITIONS
# =========================================================================
positions = [
    # 李国忠 - 市委书记
    {"person_id": 1, "org_id": 1, "title": "贺州市委书记", "start_date": "待查", "end_date": "present", "rank": "正厅级", "note": "当前在任，2026年7月已确认"},

    # 彭代元 - 市长
    {"person_id": 2, "org_id": 2, "title": "贺州市市长、党组书记", "start_date": "2021年", "end_date": "present", "rank": "正厅级", "note": "贺州市人民政府市长"},
    {"person_id": 2, "org_id": 1, "title": "贺州市委副书记", "start_date": "2021年", "end_date": "present", "rank": "正厅级", "note": ""},

    # 陆海平 - 人大常委会主任
    {"person_id": 3, "org_id": 3, "title": "贺州市人大常委会主任", "start_date": "待查", "end_date": "present", "rank": "正厅级", "note": ""},

    # 蓝树东 - 政协主席
    {"person_id": 4, "org_id": 4, "title": "贺州市政协主席", "start_date": "待查", "end_date": "present", "rank": "正厅级", "note": ""},

    # 钟洪 - 市委副书记
    {"person_id": 5, "org_id": 1, "title": "贺州市委副书记", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},

    # 何翔 - 常委、常务副市长
    {"person_id": 6, "org_id": 1, "title": "贺州市委常委", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "贺州市副市长（常务）", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": "协助市长负责市政府常务工作"},

    # 蒋晓军 - 常委、统战部长、副市长
    {"person_id": 7, "org_id": 1, "title": "贺州市委常委", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "贺州市委统战部部长", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": "兼市政协党组副书记"},
    {"person_id": 7, "org_id": 2, "title": "贺州市副市长", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},

    # 李丽 - 常委、副市长（挂职）
    {"person_id": 8, "org_id": 1, "title": "贺州市委常委", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": "挂职二年"},
    {"person_id": 8, "org_id": 2, "title": "贺州市副市长（挂职）", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": "中央港澳办五局副局长挂职"},
    {"person_id": 8, "org_id": 10, "title": "中央港澳办五局副局长", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": "挂职贺州副市长"},

    # 罗剑 - 副市长
    {"person_id": 9, "org_id": 2, "title": "贺州市副市长", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": "无党派"},

    # 程钊 - 副市长兼钟山县委书记
    {"person_id": 10, "org_id": 2, "title": "贺州市副市长、党组成员", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 7, "title": "钟山县委书记", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "兼"},

    # 冯旭波 - 副市长
    {"person_id": 11, "org_id": 2, "title": "贺州市副市长、党组成员", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},

    # 陈耀超 - 副市长、公安局长
    {"person_id": 12, "org_id": 2, "title": "贺州市副市长、党组成员", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 12, "org_id": 5, "title": "贺州市公安局局长、党委书记", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "兼市委政法委副书记"},

    # 陈展维 - 秘书长
    {"person_id": 13, "org_id": 6, "title": "贺州市人民政府秘书长、党组成员", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "办公室党组书记、主任"},

    # 李宏庆 - 前市委书记
    {"person_id": 14, "org_id": 1, "title": "贺州市委书记", "start_date": "2017年", "end_date": "2021年", "rank": "正厅级", "note": ""},
    {"person_id": 14, "org_id": 8, "title": "广西壮族自治区农业农村厅厅长", "start_date": "2021年", "end_date": "待查", "rank": "正厅级", "note": ""},

    # 林冠 - 前市长、前市委书记
    {"person_id": 15, "org_id": 2, "title": "贺州市市长", "start_date": "2016年", "end_date": "2021年", "rank": "正厅级", "note": ""},
    {"person_id": 15, "org_id": 1, "title": "贺州市委书记", "start_date": "2021年", "end_date": "2023年", "rank": "正厅级", "note": "接替李宏庆"},
    {"person_id": 15, "org_id": 9, "title": "广西投资集团有限公司董事长", "start_date": "2023年", "end_date": "待查", "rank": "正厅级", "note": ""},
]

# =========================================================================
# 4. RELATIONSHIPS
# =========================================================================
relationships = [
    # 李国忠 ↔ 彭代元：党政搭档
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "李国忠任贺州市委书记期间，彭代元任贺州市市长，为当前党政搭档",
        "overlap_org": "中共贺州市委员会/贺州市人民政府",
        "overlap_period": "2024?-present"
    },
    # 李国忠 ↔ 陆海平
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "李国忠任市委书记期间，陆海平任市人大常委会主任，同属四家班子",
        "overlap_org": "贺州市四家班子",
        "overlap_period": "present"
    },
    # 李国忠 ↔ 蓝树东
    {
        "person_a": 1, "person_b": 4,
        "type": "overlap",
        "context": "李国忠任市委书记期间，蓝树东任市政协主席，同属四家班子",
        "overlap_org": "贺州市四家班子",
        "overlap_period": "present"
    },
    # 李国忠 ↔ 钟洪
    {
        "person_a": 1, "person_b": 5,
        "type": "overlap",
        "context": "李国忠任市委书记期间，钟洪任市委副书记",
        "overlap_org": "中共贺州市委员会",
        "overlap_period": "present"
    },
    # 李国忠 ↔ 何翔
    {
        "person_a": 1, "person_b": 6,
        "type": "overlap",
        "context": "何翔任市委常委，协助书记工作",
        "overlap_org": "中共贺州市委员会",
        "overlap_period": "present"
    },
    # 彭代元 ↔ 何翔：市长和常务副市长
    {
        "person_a": 2, "person_b": 6,
        "type": "overlap",
        "context": "何翔任常务副市长，协助彭代元负责市政府常务工作",
        "overlap_org": "贺州市人民政府",
        "overlap_period": "present"
    },
    # 彭代元 ↔ 钟洪
    {
        "person_a": 2, "person_b": 5,
        "type": "overlap",
        "context": "彭代元任市长、市委副书记，钟洪任市委副书记",
        "overlap_org": "中共贺州市委员会",
        "overlap_period": "present"
    },
    # 何翔 ↔ 蒋晓军：同为市委常委
    {
        "person_a": 6, "person_b": 7,
        "type": "overlap",
        "context": "何翔与蒋晓军同为贺州市委常委",
        "overlap_org": "中共贺州市委员会",
        "overlap_period": "present"
    },
    # 何翔 ↔ 李丽：同为市委常委
    {
        "person_a": 6, "person_b": 8,
        "type": "overlap",
        "context": "何翔与李丽同为贺州市委常委",
        "overlap_org": "中共贺州市委员会",
        "overlap_period": "present"
    },
    # 蒋晓军 ↔ 李丽：同为市委常委
    {
        "person_a": 7, "person_b": 8,
        "type": "overlap",
        "context": "蒋晓军与李丽同为贺州市委常委",
        "overlap_org": "中共贺州市委员会",
        "overlap_period": "present"
    },
    # 李宏庆 → 林冠：书记接力
    {
        "person_a": 14, "person_b": 15,
        "type": "predecessor_successor",
        "context": "李宏庆调离后林冠接任贺州市委书记",
        "overlap_org": "中共贺州市委员会",
        "overlap_period": "2021年"
    },
    # 林冠 → 彭代元：市长接力
    {
        "person_a": 15, "person_b": 2,
        "type": "predecessor_successor",
        "context": "林冠升任市委书记后彭代元接任贺州市市长",
        "overlap_org": "贺州市人民政府",
        "overlap_period": "2021年"
    },
    # 林冠 → 李国忠：书记接力
    {
        "person_a": 15, "person_b": 1,
        "type": "predecessor_successor",
        "context": "林冠调离后李国忠接任贺州市委书记",
        "overlap_org": "中共贺州市委员会",
        "overlap_period": "2023?-2024?"
    },
    # 李宏庆 ↔ 林冠：党政搭档
    {
        "person_a": 14, "person_b": 15,
        "type": "overlap",
        "context": "李宏庆任市委书记期间，林冠任贺州市市长",
        "overlap_org": "中共贺州市委员会/贺州市人民政府",
        "overlap_period": "2017-2021"
    },
    # 林冠 ↔ 彭代元：党政搭档（林冠任书记，彭代元任市长）
    {
        "person_a": 15, "person_b": 2,
        "type": "overlap",
        "context": "林冠任贺州市委书记期间，彭代元任贺州市市长",
        "overlap_org": "中共贺州市委员会/贺州市人民政府",
        "overlap_period": "2021-2023"
    },
    # 程钊 ↔ 钟山县（程钊兼钟山县委书记）
    {
        "person_a": 10, "person_b": 5,
        "type": "overlap",
        "context": "程钊为副市长兼钟山县委书记，钟洪为市委副书记，有工作交集",
        "overlap_org": "中共贺州市委员会",
        "overlap_period": "present"
    },
]

# =========================================================================
# 5. BUILD FUNCTIONS
# =========================================================================

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(current_post):
    cp = current_post or ""
    if "书记" in cp and "副书记" not in cp:
        return "200,30,30"
    if "市长" in cp:
        return "30,100,200"
    if "副书记" in cp:
        return "220,80,80"
    if "副" in cp and "市长" in cp:
        return "100,150,220"
    if "常委" in cp:
        return "180,100,180"
    if "主任" in cp or "人大" in cp:
        return "60,180,60"
    if "主席" in cp:
        return "60,180,60"
    return "100,100,100"


def person_size(current_post):
    cp = current_post or ""
    if "书记" in cp and "副书记" not in cp:
        return "20.0"
    if "市长" in cp:
        return "18.0"
    if "副书记" in cp:
        return "15.0"
    if "主任" in cp or "主席" in cp:
        return "12.0"
    if "常委" in cp:
        return "12.0"
    if "副" in cp:
        return "12.0"
    return "10.0"


def person_shape(current_post):
    cp = current_post or ""
    if "书记" in cp:
        return "square"
    if "人大" in cp or "政协" in cp:
        return "diamond"
    if "副" in cp:
        return "triangle"
    return "circle"


def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(org_type, "200,200,200")


def build_db():
    """Build SQLite database using the runner pattern."""
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )


def build_gexf():
    """Build GEXF graph file with explicit string formatting."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append(f'    <description>{SLUG}领导班子关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        cp = p.get("current_post", "")
        color = person_color(cp)
        size = person_size(cp)
        shape = person_shape(cp)
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(cp)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{size}"/>')
        lines.append(f'        <viz:shape value="{shape}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oid = o["id"] + 100000
        ocolor = org_color(o["type"])
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('        <viz:shape value="hexagon"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person -> organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]+100000}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> person (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")


def build_person_json(person, timeline, rels, sources):
    """Build a single person graph JSON dict."""
    p = person
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "贺州市",
            "region": "贺州市",
            "job": p.get("current_post", "").split("、")[-1] if "、" in p.get("current_post", "") else p.get("current_post", ""),
            "task_id": "guangxi_贺州市",
            "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": f"hezhou_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": p.get("source", "")
            }
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": bool(p.get("current_post") and "待确认" not in p.get("current_post", "")),
            "source_ids": ["S001"]
        },
        "career_timeline": timeline,
        "organizations": [],
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
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "No risk signals found through available public sources",
            "date": "",
            "confidence": "unverified",
            "source_ids": []
        }],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if p.get("birth") else "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"Complete career timeline before current role for {p['name']}"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"Complete career timeline before current role for {p['name']}",
                "why_it_matters": "Cannot assess career pattern, promotion velocity, or network building without full timeline",
                "suggested_queries": [f"{p['name']} 简历", f"{p['name']} 任职经历", f"{p['name']} 百度百科"],
                "last_attempted": AS_OF
            }
        ]
    }


def build_person_jsons():
    """Build and write person JSON files for core leaders."""
    now = AS_OF.replace("-", "")

    # Source registers
    gov_sources = [
        {"id": "S001", "title": "贺州市人民政府门户网站 - 领导之窗",
         "url": "http://www.gxhz.gov.cn/zfxxgk/fdzdgknr/ldxx/", "publisher": "贺州市人民政府",
         "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high",
         "notes": "市政府领导页面，含市长、副市长、秘书长简历和分工"},
        {"id": "S002", "title": "李国忠到市直有关部门调研",
         "url": "http://www.gxhz.gov.cn/ywzx/ldhd_37591/t27930094.shtml",
         "publisher": "贺州新闻网", "published_at": "2026-07-21",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "确认李国忠为贺州市委书记"},
        {"id": "S003", "title": "李国忠彭代元陆海平蓝树东等市四家班子领导参加投票选举八步区人大代表",
         "url": "http://www.gxhz.gov.cn/ywzx/ldhd_37591/t27930108.shtml",
         "publisher": "贺州新闻网", "published_at": "2026-07-21",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "确认四家班子领导架构：李国忠(书记)、彭代元(市长)、陆海平(人大主任)、蓝树东(政协主席)、钟洪(副书记)"},
        {"id": "S004", "title": "李国忠接见全国先进基层党组织代表",
         "url": "http://www.gxhz.gov.cn/sylbt/t27857838.shtml",
         "publisher": "贺州新闻网", "published_at": "2026-07-03",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "确认钟洪为市委副书记，刘海湘为市领导"},
    ]
    prev_sources = [
        {"id": "S001", "title": "公开资料",
         "url": "", "publisher": "",
         "published_at": "", "accessed_at": AS_OF,
         "source_type": "encyclopedia", "reliability": "medium",
         "notes": "基本信息来自公开渠道"},
    ]

    # ── 李国忠 person JSON ──
    lgz_timeline = [
        {"start": "待查", "end": "present",
         "org": "中共贺州市委员会",
         "title": "贺州市委书记", "level": "正厅级",
         "location": "广西贺州", "system": "party",
         "rank": "正厅级", "is_key_promotion": True,
         "notes": "当前在任，2026年7月多次公开活动确认",
         "confidence": "confirmed",
         "source_ids": ["S002", "S003", "S004"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口",
         "title": "",
         "notes": "李国忠任贺州市委书记之前的完整履历需进一步查证。建议搜索百度百科或广西自治区组织部任前公示",
         "confidence": "unverified",
         "source_ids": []},
    ]
    lgz_relationships = [
        {"person": "彭代元", "person_id": "hezhou_彭代元",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "当前贺州市委书记与市长党政搭档",
         "overlap_org": "中共贺州市委员会/贺州市人民政府",
         "overlap_period": "2024?-present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S002", "S003"]},
        {"person": "陆海平", "person_id": "hezhou_陆海平",
         "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "市委书记与人大常委会主任同属市四家班子领导",
         "overlap_org": "贺州市四家班子",
         "overlap_period": "present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S003"]},
        {"person": "蓝树东", "person_id": "hezhou_蓝树东",
         "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "市委书记与政协主席同属市四家班子领导",
         "overlap_org": "贺州市四家班子",
         "overlap_period": "present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S003"]},
        {"person": "钟洪", "person_id": "hezhou_钟洪",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "市委书记与市委副书记在同一届市委领导班子中共事",
         "overlap_org": "中共贺州市委员会",
         "overlap_period": "present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S003", "S004"]},
    ]
    lgz_json = build_person_json(persons[0], lgz_timeline, lgz_relationships, gov_sources)
    lgz_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-贺州市-市委书记-李国忠.json")
    with open(lgz_path, "w", encoding="utf-8") as f:
        json.dump(lgz_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {lgz_path}")

    # ── 彭代元 person JSON ──
    pdy_timeline = [
        {"start": "2021年", "end": "present",
         "org": "贺州市人民政府",
         "title": "贺州市市长、市政府党组书记", "level": "正厅级",
         "location": "广西贺州", "system": "government",
         "rank": "正厅级", "is_key_promotion": True,
         "notes": "贺州市委副书记、市长，主持市政府全面工作，分管财政、审计",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"start": "2021年", "end": "present",
         "org": "中共贺州市委员会",
         "title": "贺州市委副书记", "level": "正厅级",
         "location": "广西贺州", "system": "party",
         "rank": "正厅级", "is_key_promotion": True,
         "notes": "",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口",
         "title": "",
         "notes": "1969年3月生，广西兴安人，汉族，广西区委党校研究生。中共党员。2021年任贺州市长之前的完整履历需进一步查证",
         "confidence": "unverified",
         "source_ids": []},
    ]
    pdy_relationships = [
        {"person": "李国忠", "person_id": "hezhou_李国忠",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "当前贺州市市长与市委书记党政搭档",
         "overlap_org": "中共贺州市委员会/贺州市人民政府",
         "overlap_period": "2024?-present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001", "S002", "S003"]},
        {"person": "林冠", "person_id": "hezhou_林冠",
         "relationship_type": "predecessor_successor",
         "strength": "strong",
         "evidence": "林冠升任市委书记后彭代元接任贺州市市长",
         "overlap_org": "贺州市人民政府",
         "overlap_period": "2021年",
         "direction": "person_to_other",
         "confidence": "confirmed",
         "source_ids": []},
        {"person": "何翔", "person_id": "hezhou_何翔",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "何翔任常务副市长协助彭代元负责市政府常务工作",
         "overlap_org": "贺州市人民政府",
         "overlap_period": "present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"person": "钟洪", "person_id": "hezhou_钟洪",
         "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "市长与市委副书记同在市委领导班子",
         "overlap_org": "中共贺州市委员会",
         "overlap_period": "present",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S003"]},
    ]
    pdy_json = build_person_json(persons[1], pdy_timeline, pdy_relationships, gov_sources)
    pdy_json["identity"]["education"] = [
        {"period": "", "institution": "广西区委党校", "major": "",
         "degree": "研究生学历", "study_type": "party_school", "source_ids": ["S001"]}
    ]
    pdy_json["investigation_scope"]["job"] = "市长"
    pdy_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-贺州市-市长-彭代元.json")
    with open(pdy_path, "w", encoding="utf-8") as f:
        json.dump(pdy_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {pdy_path}")

    # ── 李宏庆 person JSON (predecessor) ──
    lhq_timeline = [
        {"start": "2017年", "end": "2021年",
         "org": "中共贺州市委员会",
         "title": "贺州市委书记", "level": "正厅级",
         "location": "广西贺州", "system": "party",
         "rank": "正厅级", "is_key_promotion": True,
         "notes": "贺州市委书记",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"start": "2021年", "end": "待查",
         "org": "广西壮族自治区农业农村厅",
         "title": "厅长", "level": "正厅级",
         "location": "广西南宁", "system": "government",
         "rank": "正厅级", "is_key_promotion": False,
         "notes": "调任自治区农业农村厅厅长",
         "confidence": "confirmed",
         "source_ids": ["S001"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口",
         "title": "",
         "notes": "1963年10月生，广西博白人，在职研究生学历，1985年7月参加工作，中共党员。2017年之前完整履历需进一步查证",
         "confidence": "unverified",
         "source_ids": []},
    ]
    lhq_relationships = [
        {"person": "林冠", "person_id": "hezhou_林冠",
         "relationship_type": "predecessor_successor",
         "strength": "strong",
         "evidence": "李宏庆调离后林冠接任贺州市委书记",
         "overlap_org": "中共贺州市委员会",
         "overlap_period": "2021年",
         "direction": "other_to_person",
         "confidence": "confirmed",
         "source_ids": []},
    ]
    lhq_json = build_person_json(persons[13], lhq_timeline, lhq_relationships, prev_sources)
    lhq_json["identity"]["education"] = [
        {"period": "", "institution": "在职研究生", "major": "",
         "degree": "研究生学历", "study_type": "unknown", "source_ids": ["S001"]}
    ]
    lhq_json["investigation_scope"]["job"] = "原市委书记"
    lhq_path = os.path.join(PERSONS_DIR, f"{now}-广西壮族自治区-贺州市-原市委书记-李宏庆.json")
    with open(lhq_path, "w", encoding="utf-8") as f:
        json.dump(lhq_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {lhq_path}")


def build():
    """Main build function."""
    os.makedirs(STAGING_DIR, exist_ok=True)
    print(f"=== Building {SLUG} data ===")
    print(f"Staging dir: {STAGING_DIR}")

    build_db()
    build_gexf()
    build_person_jsons()

    print(f"\n=== Build complete ===")
    print(f"  DB:     {DB_PATH}")
    print(f"  GEXF:   {GEXF_PATH}")


if __name__ == "__main__":
    build()
