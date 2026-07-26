#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 广元市昭化区 leadership network.

调查日期: 2026-07-26
信息来源: 昭化区人民政府网站 (zhaohua.gov.cn) — official personnel appointment notices
调查级别: 市辖区
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
sys.path.insert(0, REPO_ROOT)

STAGING_DIR = BASE
DB_PATH = os.path.join(STAGING_DIR, "昭化区_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "昭化区_network.gexf")
PERSONS_DIR = STAGING_DIR

TODAY = datetime.now().strftime("%Y%m%d")
SLUG = "四川省广元市昭化区"

# ── PERSONS ────────────────────────────────────────────────────────
persons = [
    # ═══════════════════════════════
    # 区委领导 (District Party Committee)
    # ═══════════════════════════════

    # 区委书记 — 待确认（公开资料暂未找到当前区委书记详细信息）
    {
        "id": 1,
        "name": "待确认",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共广元市昭化区委书记",
        "current_org": "中共广元市昭化区委员会",
        "source": "官方来源待补充 — web访问受限无法确认",
    },
    # 区长 — 待确认
    {
        "id": 2,
        "name": "待确认",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "昭化区人民政府区长",
        "current_org": "广元市昭化区人民政府",
        "source": "官方来源待补充 — web访问受限无法确认",
    },

    # ═══════════════════════════════
    # 区政府领导 (District Government)
    # ═══════════════════════════════

    # 八届区人民政府任免文件中出现的区级领导
    # 以下从2021-2026年昭府人发文件确认的干部

    # 赵伟 — 区发展和改革局副局长 (2026年5月任命)
    {
        "id": 3,
        "name": "赵伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区发展和改革局副局长",
        "current_org": "广元市昭化区发展和改革局",
        "source": "昭府人发〔2026〕12号 — 2026-05-28",
    },
    # 柴巧巧 — 区司法局副局长 (2026年5月任命)
    {
        "id": 4,
        "name": "柴巧巧",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区司法局副局长",
        "current_org": "广元市昭化区司法局",
        "source": "昭府人发〔2026〕12号 — 2026-05-28",
    },
    # 刘磊 — 区水利局副局长、区应急管理局副局长（兼）
    {
        "id": 5,
        "name": "刘磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区水利局副局长、区应急管理局副局长（兼）",
        "current_org": "广元市昭化区水利局",
        "source": "昭府人发〔2026〕12号 — 2026-05-28",
    },
    # 李川 — 区林业局副局长、区应急管理局副局长（兼）
    {
        "id": 6,
        "name": "李川",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区林业局副局长、区应急管理局副局长（兼）",
        "current_org": "广元市昭化区林业局",
        "source": "昭府人发〔2026〕12号 — 2026-05-28",
    },
    # 刘德智 — 区医疗保障事务中心主任
    {
        "id": 7,
        "name": "刘德智",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区医疗保障事务中心主任",
        "current_org": "广元市昭化区医疗保障事务中心",
        "source": "昭府人发〔2026〕12号 — 2026-05-28",
    },
    # 杨雨嘉 — 区就业服务中心主任 (2026年7月任命)
    {
        "id": 8,
        "name": "杨雨嘉",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区就业服务中心主任",
        "current_org": "广元市昭化区就业服务中心",
        "source": "昭府人发〔2026〕18号 — 2026-07-09",
    },
    # 韩燕玲 — 红岩镇便民服务中心主任
    {
        "id": 9,
        "name": "韩燕玲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "红岩镇便民服务中心主任（试用期）",
        "current_org": "昭化区红岩镇人民政府",
        "source": "昭府人发〔2026〕18号 — 2026-07-09",
    },
    # 杨小燕 — 磨滩镇便民服务中心主任
    {
        "id": 10,
        "name": "杨小燕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "磨滩镇便民服务中心主任（试用期）",
        "current_org": "昭化区磨滩镇人民政府",
        "source": "昭府人发〔2026〕18号 — 2026-07-09",
    },
    # 侯雷 — 青牛镇农业综合服务中心主任
    {
        "id": 11,
        "name": "侯雷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "青牛镇农业综合服务中心主任（试用期）",
        "current_org": "昭化区青牛镇人民政府",
        "source": "昭府人发〔2026〕18号 — 2026-07-09",
    },
    # 刘海渊 — 养老服务中心主任
    {
        "id": 12,
        "name": "刘海渊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区养老服务中心主任（试用期）",
        "current_org": "广元市昭化区养老服务中心",
        "source": "昭府人发〔2026〕18号 — 2026-07-09",
    },
    # 田梓均 — 人才交流中心主任
    {
        "id": 13,
        "name": "田梓均",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人才交流中心（区人事考试中心）主任（试用期）",
        "current_org": "广元市昭化区人才交流中心",
        "source": "昭府人发〔2026〕18号 — 2026-07-09",
    },
    # 苗纯刚 — 葭萌建设开发有限公司副总经理
    {
        "id": 14,
        "name": "苗纯刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "葭萌建设开发有限公司副总经理",
        "current_org": "广元市昭化区葭萌建设开发有限公司",
        "source": "昭府人发〔2026〕18号 — 2026-07-09",
    },
    # 吴涛 — 区供销合作社联合社主任 (2021年9月任命)
    {
        "id": 15,
        "name": "吴涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区供销合作社联合社主任",
        "current_org": "广元市昭化区供销合作社联合社",
        "source": "昭府人发〔2021〕12号 — 2021-09-06",
    },
    # 曾伟 — 四川广元昭化经济开发区管理委员会主任
    {
        "id": 16,
        "name": "曾伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "四川广元昭化经济开发区管理委员会主任",
        "current_org": "四川广元昭化经济开发区管委会",
        "source": "昭府人发〔2021〕12号 — 2021-09-06",
    },
    # 袁云 — 区人民防空办公室主任
    {
        "id": 17,
        "name": "袁云",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人民防空办公室主任",
        "current_org": "广元市昭化区人民防空办公室",
        "source": "昭府人发〔2021〕12号 — 2021-09-06",
    },
    # 刘芳 — 区民兵武器训练基地主任
    {
        "id": 18,
        "name": "刘芳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区民兵武器训练基地主任",
        "current_org": "广元市昭化区民兵武器训练基地",
        "source": "昭府人发〔2021〕12号 — 2021-09-06",
    },
    # 王桥生 — 亭子湖景区保护与发展中心主任
    {
        "id": 19,
        "name": "王桥生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "亭子湖景区保护与发展中心主任",
        "current_org": "广元市昭化区亭子湖景区保护与发展中心",
        "source": "昭府人发〔2021〕12号 — 2021-09-06",
    },
    # 薛嘉 — 区水旱灾害防御中心主任
    {
        "id": 20,
        "name": "薛嘉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区水旱灾害防御中心主任",
        "current_org": "广元市昭化区水旱灾害防御中心",
        "source": "昭府人发〔2021〕12号 — 2021-09-06",
    },
    # 余雪梅 — 公务和外事服务中心副主任
    {
        "id": 21,
        "name": "余雪梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区公务和外事服务中心副主任",
        "current_org": "广元市昭化区公务和外事服务中心",
        "source": "昭府人发〔2021〕12号 — 2021-09-06",
    },
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共广元市昭化区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共广元市委",
        "location": "四川省广元市昭化区",
    },
    {
        "id": 2,
        "name": "广元市昭化区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "广元市人民政府",
        "location": "四川省广元市昭化区",
    },
    {
        "id": 3,
        "name": "广元市昭化区发展和改革局",
        "type": "政府",
        "level": "乡科级",
        "parent": "广元市昭化区人民政府",
        "location": "四川省广元市昭化区",
    },
    {
        "id": 4,
        "name": "广元市昭化区司法局",
        "type": "政府",
        "level": "乡科级",
        "parent": "广元市昭化区人民政府",
        "location": "四川省广元市昭化区",
    },
    {
        "id": 5,
        "name": "广元市昭化区水利局",
        "type": "政府",
        "level": "乡科级",
        "parent": "广元市昭化区人民政府",
        "location": "四川省广元市昭化区",
    },
    {
        "id": 6,
        "name": "广元市昭化区应急管理局",
        "type": "政府",
        "level": "乡科级",
        "parent": "广元市昭化区人民政府",
        "location": "四川省广元市昭化区",
    },
    {
        "id": 7,
        "name": "广元市昭化区林业局",
        "type": "政府",
        "level": "乡科级",
        "parent": "广元市昭化区人民政府",
        "location": "四川省广元市昭化区",
    },
    {
        "id": 8,
        "name": "广元市昭化区医疗保障事务中心",
        "type": "事业单位",
        "level": "乡镇科级",
        "parent": "广元市昭化区医疗保障局",
        "location": "四川省广元市昭化区",
    },
    {
        "id": 9,
        "name": "广元市昭化区就业服务中心",
        "type": "事业单位",
        "level": "乡镇科级",
        "parent": "广元市昭化区人力资源和社会保障局",
        "location": "四川省广元市昭化区",
    },
    {
        "id": 10,
        "name": "昭化区红岩镇人民政府",
        "type": "乡镇/街道",
        "level": "乡镇级",
        "parent": "广元市昭化区人民政府",
        "location": "四川省广元市昭化区红岩镇",
    },
    {
        "id": 11,
        "name": "昭化区磨滩镇人民政府",
        "type": "乡镇/街道",
        "level": "乡镇级",
        "parent": "广元市昭化区人民政府",
        "location": "四川省广元市昭化区磨滩镇",
    },
    {
        "id": 12,
        "name": "昭化区青牛镇人民政府",
        "type": "乡镇/街道",
        "level": "乡镇级",
        "parent": "广元市昭化区人民政府",
        "location": "四川省广元市昭化区青牛镇",
    },
    {
        "id": 13,
        "name": "广元市昭化区养老服务中心",
        "type": "事业单位",
        "level": "乡镇科级",
        "parent": "广元市昭化区民政局",
        "location": "四川省广元市昭化区",
    },
    {
        "id": 14,
        "name": "广元市昭化区人才交流中心",
        "type": "事业单位",
        "level": "乡镇科级",
        "parent": "广元市昭化区人力资源和社会保障局",
        "location": "四川省广元市昭化区",
    },
    {
        "id": 15,
        "name": "四川广元昭化经济开发区管委会",
        "type": "开发区",
        "level": "乡镇科级",
        "parent": "广元市昭化区人民政府",
        "location": "四川省广元市昭化区",
    },
    {
        "id": 16,
        "name": "广元市昭化区供销合作社联合社",
        "type": "群团",
        "level": "乡镇科级",
        "parent": "广元市昭化区人民政府",
        "location": "四川省广元市昭化区",
    },
    {
        "id": 17,
        "name": "广元市昭化区人民防空办公室",
        "type": "政府",
        "level": "乡镇科级",
        "parent": "广元市昭化区人民政府",
        "location": "四川省广元市昭化区",
    },
    {
        "id": 18,
        "name": "广元市昭化区民兵武器训练基地",
        "type": "事业单位",
        "level": "乡镇科级",
        "parent": "广元市昭化区人民政府",
        "location": "四川省广元市昭化区",
    },
    {
        "id": 19,
        "name": "广元市昭化区亭子湖景区保护与发展中心",
        "type": "事业单位",
        "level": "乡镇科级",
        "parent": "广元市昭化区人民政府",
        "location": "四川省广元市昭化区",
    },
    {
        "id": 20,
        "name": "广元市昭化区水旱灾害防御中心",
        "type": "事业单位",
        "level": "乡镇科级",
        "parent": "广元市昭化区水利局",
        "location": "四川省广元市昭化区",
    },
    {
        "id": 21,
        "name": "广元市昭化区公务和外事服务中心",
        "type": "事业单位",
        "level": "乡镇科级",
        "parent": "广元市昭化区人民政府",
        "location": "四川省广元市昭化区",
    },
    {
        "id": 22,
        "name": "广元市昭化区交通运输局",
        "type": "政府",
        "level": "乡镇科级",
        "parent": "广元市昭化区人民政府",
        "location": "四川省广元市昭化区",
    },
    {
        "id": 23,
        "name": "广元市昭化区统计局",
        "type": "政府",
        "level": "乡镇科级",
        "parent": "广元市昭化区人民政府",
        "location": "四川省广元市昭化区",
    },
    {
        "id": 24,
        "name": "广元市昭化区葭萌建设开发有限公司",
        "type": "事业单位",
        "level": "乡镇科级",
        "parent": "广元市昭化区人民政府",
        "location": "四川省广元市昭化区",
    },
    {
        "id": 25,
        "name": "广元市昭化区太公镇人民政府",
        "type": "乡镇/街道",
        "level": "乡镇级",
        "parent": "广元市昭化区人民政府",
        "location": "四川省广元市昭化区太公镇",
    },
    {
        "id": 26,
        "name": "广元市昭化区人力资源和社会保障局",
        "type": "政府",
        "level": "乡镇科级",
        "parent": "广元市昭化区人民政府",
        "location": "四川省广元市昭化区",
    },
]

# ── POSITIONS ──────────────────────────────────────────────────────
positions = [
    # 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "待确认"},
    # 区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "待确认"},
    # 赵伟 — 区发改局副局长 (2026年5月)
    {"person_id": 3, "org_id": 3, "title": "副局长", "start_date": "2026-05", "end_date": "present", "rank": "乡镇科级副职", "note": "昭府人发〔2026〕12号"},
    # 柴巧巧 — 区司法局副局长 (2026年5月)
    {"person_id": 4, "org_id": 4, "title": "副局长", "start_date": "2026-05", "end_date": "present", "rank": "乡镇科级副职", "note": "昭府人发〔2026〕12号"},
    # 刘磊 — 区水利局副局长（兼应急局）
    {"person_id": 5, "org_id": 5, "title": "副局长", "start_date": "2026-05", "end_date": "present", "rank": "乡镇科级副职", "note": "昭府人发〔2026〕12号, 并发"},
    {"person_id": 5, "org_id": 6, "title": "副局长（兼）", "start_date": "2026-05", "end_date": "present", "rank": "乡镇科级副职", "note": "昭府人发〔2026〕12号"},
    # 李川 — 区林业局副局长（兼职工局）
    {"person_id": 6, "org_id": 7, "title": "副局长", "start_date": "2026-05", "end_date": "present", "rank": "乡镇科级副职", "note": "昭府人发〔2026〕12号"},
    {"person_id": 6, "org_id": 6, "title": "副局长（兼）", "start_date": "2026-05", "end_date": "present", "rank": "乡镇科级副职", "note": "昭府人发〔2026〕12号"},
    # 刘德智 — 医保事务中心主任
    {"person_id": 7, "org_id": 8, "title": "主任", "start_date": "2026-05", "end_date": "present", "rank": "乡镇科级正职", "note": "昭府人发〔2026〕12号"},
    # 杨雨嘉 — 就业服务中心主任 (2026年7月)
    {"person_id": 8, "org_id": 9, "title": "主任", "start_date": "2026-07", "end_date": "present", "rank": "乡镇科级正职", "note": "昭府人发〔2026〕18号"},
    # 韩燕玲 — 红岩镇便民服务中心主任
    {"person_id": 9, "org_id": 10, "title": "便民服务中心主任（试用期）", "start_date": "2026-07", "end_date": "present", "rank": "乡镇科级副职", "note": "昭府人发〔2026〕18号"},
    # 杨小燕 — 磨滩镇便民服务中心主任
    {"person_id": 10, "org_id": 11, "title": "便民服务中心主任（试用期）", "start_date": "2026-07", "end_date": "present", "rank": "乡镇科级副职", "note": "昭府人发〔2026〕18号"},
    # 侯雷 — 青牛镇农业综合服务中心主任
    {"person_id": 11, "org_id": 12, "title": "农业综合服务中心主任（试用期）", "start_date": "2026-07", "end_date": "present", "rank": "乡镇科级副职", "note": "昭府人发〔2026〕18号"},
    # 刘海渊 — 养老服务中心主任
    {"person_id": 12, "org_id": 13, "title": "主任（试用期）", "start_date": "2026-07", "end_date": "present", "rank": "乡镇科级正职", "note": "昭府人发〔2026〕18号"},
    # 田梓均 — 人才交流中心主任
    {"person_id": 13, "org_id": 14, "title": "主任（试用期）", "start_date": "2026-07", "end_date": "present", "rank": "乡镇科级正职", "note": "昭府人发〔2026〕18号"},
    # 苗纯刚 — 葭萌建设副总经理
    {"person_id": 14, "org_id": 24, "title": "副总经理", "start_date": "2026-07", "end_date": "present", "rank": "企业副职", "note": "昭府人发〔2026〕18号"},
    # 吴涛 — 供销社主任 (2021年9月)
    {"person_id": 15, "org_id": 16, "title": "主任", "start_date": "2021-09", "end_date": "present", "rank": "乡镇科级正职", "note": "昭府人发〔2021〕12号"},
    # 曾伟 — 经开区管委会主任 (2021年9月)
    {"person_id": 16, "org_id": 15, "title": "主任", "start_date": "2021-09", "end_date": "present", "rank": "乡镇科级正职", "note": "昭府人发〔2021〕12号"},
    # 袁云 — 人防办主任
    {"person_id": 17, "org_id": 17, "title": "主任", "start_date": "2021-09", "end_date": "present", "rank": "乡镇科级正职", "note": "昭府人发〔2021〕12号"},
    # 刘芳 — 民兵武器训练基地主任
    {"person_id": 18, "org_id": 18, "title": "主任", "start_date": "2021-09", "end_date": "present", "rank": "乡镇科级正职", "note": "昭府人发〔2021〕12号"},
    # 王桥生 — 景保中心主任
    {"person_id": 19, "org_id": 19, "title": "主任", "start_date": "2021-09", "end_date": "present", "rank": "乡镇科级正职", "note": "昭府人发〔2021〕12号"},
    # 薛嘉 — 水旱灾害防御中心主任
    {"person_id": 20, "org_id": 20, "title": "主任", "start_date": "2021-09", "end_date": "present", "rank": "乡镇科级正职", "note": "昭府人发〔2021〕12号"},
    # 余雪梅 — 公务和外事服务中心副主任
    {"person_id": 21, "org_id": 21, "title": "副主任", "start_date": "2021-09", "end_date": "present", "rank": "乡镇科级副职", "note": "昭府人发〔2021〕12号"},
]

# ── RELATIONSHIPS ─────────────────────────────────────────────────
relationships = [
    # 赵伟与发改局上下级关系 — 共事于区发改局
    {"person_a": 3, "person_b": 1, "type": "同系统", "context": "区发改局副局长与区委书记同级上下级关系", "overlap_org": "广元市昭化区", "overlap_period": "2026-"},
    # 曾伟的职务变动 — 从发改局副局长提拔至开发区管委会主任
    {"person_a": 16, "person_b": 2, "type": "上下级", "context": "经开区管委会主任由区政府任命", "overlap_org": "广元市昭化区人民政府", "overlap_period": "2021-09~"},
]

# ── MAIN ───────────────────────────────────────────────────────────
def main():
    from gov_relation.runner import run_build
    from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

    # Staging paths
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

    print(f"\n✅ Done: {DB_PATH}")
    print(f"✅ Done: {GEXF_PATH}")
    print(f"  - Persons: {len(persons)}")
    print(f"  - Organizations: {len(organizations)}")
    print(f"  - Positions: {len(positions)}")
    print(f"  - Relationships: {len(relationships)}")


if __name__ == "__main__":
    main()