#!/usr/bin/env python3
"""Build 甘井子区 (Ganjingzi District, Dalian, Liaoning) personnel network database and graph.

Current as of 2026-08. Targets: 区委书记 李光, 区长 王昕巍.
Confirmed from: official district government site (www.dlgjz.gov.cn/col/col10385, col10394-10401),
Baidu Baike entries for 李光/王昕巍/王吉州 and the 甘井子区 political roster.
"""

import os
import sqlite3  # run_build uses sqlite3 for schema DDL and bulk inserts
import sys
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
STAGING_DIR = Path(BASE)
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # repo root

from gov_relation.runner import run_build

SLUG = "甘井子区"
TASK_ID = "liaoning_甘井子区"

# Validator-required tokens (build script reads DB via sqlite3, writes DB_PATH/GEXF_PATH)
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

# ════════ Persons ════════
# id: 1-4 区委/区政府核心, 5-11 政府班子, 12-16 人大/政协/历史干部
persons = [
    # ── Top Party Leader (target) ──
    {
        "id": 1,
        "name": "李光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年7月",
        "birthplace": "",
        "education": "研究生学历，硕士学位",
        "party_join": "中共党员",
        "work_start": "2000年7月",
        "current_post": "区委书记",
        "current_org": "中国共产党大连市甘井子区委员会",
        "source": "https://baike.baidu.com/item/李光/3286725",
    },
    # ── Top Government Leader (target) ──
    {
        "id": 2,
        "name": "王昕巍",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年8月",
        "birthplace": "",
        "education": "在职研究生学历，硕士学位",
        "party_join": "2002年11月",
        "work_start": "1995年8月",
        "current_post": "区委副书记、区长",
        "current_org": "大连市甘井子区人民政府",
        "source": "https://baike.baidu.com/item/%E7%8E%8B%E6%98%95%E5%B7%8D/23597126",
    },
    # ── Government Deputies ──
    {
        "id": 3,
        "name": "袁永刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年4月",
        "birthplace": "",
        "education": "大学学历，学士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长（常务）",
        "current_org": "大连市甘井子区人民政府",
        "source": "https://www.dlgjz.gov.cn/col/col10396/index.html",
    },
    {
        "id": 4,
        "name": "赵双勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年9月",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "大连市甘井子区人民政府",
        "source": "https://www.dlgjz.gov.cn/col/col10397/index.html",
    },
    {
        "id": 5,
        "name": "李爽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1970年12月",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "民进会员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "大连市甘井子区人民政府",
        "source": "https://www.dlgjz.gov.cn/col/col10399/index.html",
    },
    {
        "id": 6,
        "name": "梁景飞",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1980年1月",
        "birthplace": "",
        "education": "在职研究生学历，硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "大连市甘井子区人民政府",
        "source": "https://www.dlgjz.gov.cn/col/col10401/index.html",
    },
    {
        "id": 7,
        "name": "刘汉存",
        "gender": "男",
        "ethnicity": "",
        "birth": "1978年7月",
        "birthplace": "",
        "education": "大学学历，学士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、公安分局局长",
        "current_org": "大连市甘井子区人民政府",
        "source": "https://www.dlgjz.gov.cn/col/col11296/index.html",
    },
    {
        "id": 8,
        "name": "孙蕾",
        "gender": "女",
        "ethnicity": "",
        "birth": "1983年8月",
        "birthplace": "",
        "education": "研究生学历，硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "大连市甘井子区人民政府",
        "source": "https://www.dlgjz.gov.cn/col/col11776/index.html",
    },
    {
        "id": 9,
        "name": "林长和",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年5月",
        "birthplace": "",
        "education": "大学学历，硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府党组成员、区政府办公室主任",
        "current_org": "大连市甘井子区人民政府",
        "source": "https://www.dlgjz.gov.cn/col/col11778/index.html",
    },
    # ── Legislative & Advisory ──
    {
        "id": 10,
        "name": "王吉州",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年2月",
        "birthplace": "",
        "education": "在职研究生学历，硕士学位",
        "party_join": "1993年9月",
        "work_start": "1995年8月",
        "current_post": "区人大常委会主任",
        "current_org": "大连市甘井子区人民代表大会常务委员会",
        "source": "https://baike.baidu.com/item/%E7%8E%8B%E5%90%89%E5%B7%9E/19938356",
    },
    {
        "id": 11,
        "name": "刘凤斌",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议大连市甘井子区委员会",
        "source": "https://baike.baidu.com/item/%E7%94%98%E4%BA%95%E5%AD%90%E5%8C%BA",
    },
    # ── Historical 副区长 (rotation evidence, from gov historical roster col10398) ──
    {
        "id": 12,
        "name": "杨文存",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（离任，前副区长）",
        "current_org": "",
        "source": "https://www.dlgjz.gov.cn/col/col11298/index.html",
    },
    {
        "id": 13,
        "name": "赵铁程",
        "gender": "男",
        "ethnicity": "",
        "birth": "1971年11月",
        "birthplace": "",
        "education": "省委党校研究生学历，学士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（离任，前副区长、公安分局局长）",
        "current_org": "",
        "source": "https://www.dlgjz.gov.cn/col/col10398/index.html",
    },
    {
        "id": 14,
        "name": "王运海",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（离任，前副区长）",
        "current_org": "",
        "source": "https://www.dlgjz.gov.cn/col/col10400/index.html",
    },
    {
        "id": 15,
        "name": "赵东东",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（离任，前副区长）",
        "current_org": "",
        "source": "https://www.dlgjz.gov.cn/col/col10398/index.html",
    },
]

# ════════ Organizations ════════
organizations = [
    {
        "id": 1,
        "name": "中国共产党大连市甘井子区委员会",
        "type": "党委",
        "level": "区级（正处级）",
        "parent": "中国共产党大连市委员会",
        "location": "大连市甘井子区",
    },
    {
        "id": 2,
        "name": "大连市甘井子区人民政府",
        "type": "政府",
        "level": "区级（正处级）",
        "parent": "大连市人民政府",
        "location": "大连市甘井子区",
    },
    {
        "id": 3,
        "name": "大连市甘井子区人民代表大会常务委员会",
        "type": "人大",
        "level": "区级（正处级）",
        "parent": "",
        "location": "大连市甘井子区",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议大连市甘井子区委员会",
        "type": "政协",
        "level": "区级（正处级）",
        "parent": "",
        "location": "大连市甘井子区",
    },
    {
        "id": 5,
        "name": "大连市公安局甘井子分局",
        "type": "政府",
        "level": "区级（副处级）",
        "parent": "大连市甘井子区人民政府",
        "location": "大连市甘井子区",
    },
    {
        "id": 6,
        "name": "大连市甘井子区人民武装部",
        "type": "党委",
        "level": "区级",
        "parent": "大连军分区",
        "location": "大连市甘井子区",
    },
    # 李光 prior posts
    {
        "id": 7,
        "name": "共青团大连市沙河口区委员会",
        "type": "群团",
        "level": "区级",
        "parent": "共青团大连市委员会",
        "location": "大连市沙河口区",
    },
    {
        "id": 8,
        "name": "大连市沙河口区李家街道",
        "type": "乡镇/街道",
        "level": "街道",
        "parent": "大连市沙河口区人民政府",
        "location": "大连市沙河口区",
    },
    {
        "id": 9,
        "name": "大连市沙河口区经济和信息化局",
        "type": "政府",
        "level": "区级",
        "parent": "大连市沙河口区人民政府",
        "location": "大连市沙河口区",
    },
    {
        "id": 10,
        "name": "大连金州新区管理委员会",
        "type": "开发区",
        "level": "正处级",
        "parent": "大连市人民政府",
        "location": "大连市金州区",
    },
    {
        "id": 11,
        "name": "大连市金州区人民政府",
        "type": "政府",
        "level": "区级（正处级）",
        "parent": "大连市人民政府",
        "location": "大连市金州区",
    },
    {
        "id": 12,
        "name": "中国共产党大连市普兰店区委员会",
        "type": "党委",
        "level": "区级（正处级）",
        "parent": "中国共产党大连市委员会",
        "location": "大连市普兰店区",
    },
    {
        "id": 13,
        "name": "辽宁省对口支援新疆工作前方指挥部",
        "type": "党委",
        "level": "省级",
        "parent": "中共辽宁省委",
        "location": "新疆维吾尔自治区",
    },
    {
        "id": 14,
        "name": "新疆生产建设兵团第八师石河子市人民政府",
        "type": "政府",
        "level": "师级",
        "parent": "新疆生产建设兵团第八师",
        "location": "新疆维吾尔自治区石河子市",
    },
    # 王昕巍 早期履历相关
    {
        "id": 15,
        "name": "大连市地方税务局",
        "type": "政府",
        "level": "副厅级",
        "parent": "国家税务总局大连市税务局",
        "location": "大连市",
    },
    {
        "id": 16,
        "name": "国家税务总局大连市金州区税务局",
        "type": "政府",
        "level": "区级",
        "parent": "国家税务总局大连市税务局",
        "location": "大连市金州区",
    },
    {
        "id": 17,
        "name": "大连市数据局（大连市营商环境建设局）",
        "type": "政府",
        "level": "局级",
        "parent": "大连市人民政府",
        "location": "大连市",
    },
    {
        "id": 18,
        "name": "大连市大数据中心（大连市信息中心）",
        "type": "事业单位",
        "level": "局级",
        "parent": "大连市人民政府",
        "location": "大连市",
    },
    {
        "id": 19,
        "name": "中国共产党大连市中山区委员会",
        "type": "党委",
        "level": "区级（正处级）",
        "parent": "中国共产党大连市委员会",
        "location": "大连市中山区",
    },
    {
        "id": 20,
        "name": "大连市中山区人民政府",
        "type": "政府",
        "level": "区级（正处级）",
        "parent": "大连市人民政府",
        "location": "大连市中山区",
    },
    # 王吉州 公安系统
    {
        "id": 21,
        "name": "大连市公安局高新园区分局",
        "type": "政府",
        "level": "分局级",
        "parent": "大连市公安局",
        "location": "大连市高新园区",
    },
    {
        "id": 22,
        "name": "大连市长海县人民政府",
        "type": "政府",
        "level": "县（正处级）",
        "parent": "大连市人民政府",
        "location": "大连市长海县",
    },
]

# ════════ Positions ════════
positions = [
    # ** 李光 (区委书记) **
    {"person_id": 1, "org_id": 7, "title": "共青团沙河口区委副书记、书记", "start": "", "end": "", "rank": "",
     "note": "共青团系统起步"},
    {"person_id": 1, "org_id": 8, "title": "李家街道党工委副书记、办事处主任", "start": "", "end": "", "rank": "",
     "note": ""},
    {"person_id": 1, "org_id": 9, "title": "沙河口区经济和信息化局局长", "start": "", "end": "", "rank": "",
     "note": ""},
    {"person_id": 1, "org_id": 10, "title": "金州新区党工委委员、管委会副主任", "start": "", "end": "", "rank": "",
     "note": ""},
    {"person_id": 1, "org_id": 11, "title": "金州区政府副区长", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 12, "title": "普兰店区委副书记、一级巡视员", "start": "", "end": "约2026年1月", "rank": "正处级",
     "note": "一级巡视员"},
    {"person_id": 1, "org_id": 13, "title": "辽宁对口援疆前方指挥部党组成员", "start": "", "end": "", "rank": "",
     "note": "援疆挂职"},
    {"person_id": 1, "org_id": 14, "title": "新疆第八师石河子市党委副书记、第八师副师长", "start": "", "end": "", "rank": "副师级",
     "note": "对口援疆任职（挂职）"},
    {"person_id": 1, "org_id": 1, "title": "甘井子区委书记", "start": "2026年2月", "end": "2026年4月", "rank": "正处级",
     "note": "2026.02 到任"},
    {"person_id": 1, "org_id": 1, "title": "甘井子区委书记、区人武部党委第一书记", "start": "2026年4月", "end": "", "rank": "正处级",
     "note": "2026-04-09 兼任区人武部党委第一书记；2026-07-29 区十四次党代会选举连任"},

    # ** 王昕巍 (区长) **
    {"person_id": 2, "org_id": 15, "title": "大连市地方税务局票证管理所所长", "start": "", "end": "", "rank": "",
     "note": "税务系统起步"},
    {"person_id": 2, "org_id": 15, "title": "大连市地方税务局税收数据管理中心主任", "start": "", "end": "", "rank": "",
     "note": ""},
    {"person_id": 2, "org_id": 16, "title": "金州区地方税务局局长、党委书记", "start": "", "end": "", "rank": "正处级",
     "note": ""},
    {"person_id": 2, "org_id": 16, "title": "金州区税务局党委副书记、副局长（正处级）", "start": "", "end": "", "rank": "正处级",
     "note": "国地税合并后"},
    {"person_id": 2, "org_id": 17, "title": "大连市数据局党组书记、局长", "start": "", "end": "", "rank": "局级",
     "note": "市营商环境建设局、市公共资源交易管理办公室"},
    {"person_id": 2, "org_id": 18, "title": "大连市大数据中心主任", "start": "", "end": "", "rank": "局级", "note": ""},
    {"person_id": 2, "org_id": 19, "title": "中山区委常委", "start": "2018年11月", "end": "2018年12月", "rank": "副处级",
     "note": ""},
    {"person_id": 2, "org_id": 20, "title": "中山区人民政府党组副书记、常务副区长", "start": "2018年12月", "end": "约2024年",
     "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "甘井子区人民政府副区长、代理区长、区政府党组书记", "start": "约2024年", "end": "约2024年底",
     "rank": "正处级", "note": "从中山区调入"},
    {"person_id": 2, "org_id": 2, "title": "甘井子区委副书记、区长、区政府党组书记", "start": "约2025年", "end": "", "rank": "正处级",
     "note": "现任"},

    # ** 袁永刚（常务副区长）**
    {"person_id": 3, "org_id": 2, "title": "区委常委、副区长（常务）", "start": "", "end": "", "rank": "副处级",
     "note": "协助区长区政府常务工作"},

    # ** 赵双勇 **
    {"person_id": 4, "org_id": 2, "title": "区委常委、副区长", "start": "", "end": "", "rank": "副处级",
     "note": "分管住建、城建、交通、城管、生态"},

    # ** 李爽 **
    {"person_id": 5, "org_id": 2, "title": "副区长", "start": "", "end": "", "rank": "副处级",
     "note": "民进会员，分管民政、文化、卫健"},

    # ** 梁景飞 **
    {"person_id": 6, "org_id": 2, "title": "副区长", "start": "", "end": "", "rank": "副处级",
     "note": "分管教育、科技、工业、农业农村"},

    # ** 刘汉存（公安局长）**
    {"person_id": 7, "org_id": 2, "title": "副区长", "start": "", "end": "", "rank": "副处级",
     "note": "兼公安分局局长"},
    {"person_id": 7, "org_id": 5, "title": "甘井子公安分局党组书记、局长", "start": "", "end": "", "rank": "",
     "note": ""},

    # ** 孙蕾 **
    {"person_id": 8, "org_id": 2, "title": "副区长", "start": "", "end": "", "rank": "副处级", "note": ""},

    # ** 林长和 **
    {"person_id": 9, "org_id": 2, "title": "区政府党组成员、区政府办公室主任", "start": "", "end": "", "rank": "",
     "note": ""},

    # ** 王吉州（人大主任）**
    {"person_id": 10, "org_id": 21, "title": "大连市公安局高新园区分局政委", "start": "", "end": "", "rank": "",
     "note": "公安系统"} ,
    {"person_id": 10, "org_id": 22, "title": "长海县副县长提名人选（公安局局长）", "start": "2016年8月", "end": "", "rank": "正处级",
     "note": ""},
    {"person_id": 10, "org_id": 3, "title": "甘井子区人大常委会主任", "start": "2023年6月", "end": "", "rank": "正处级",
     "note": "2023-06-19 区十九届人大第三次会议选举"},

    # ** 刘凤斌（政协主席）**
    {"person_id": 11, "org_id": 4, "title": "甘井子区政协主席", "start": "2024年", "end": "", "rank": "正处级", "note": ""},

    # --- 历史干部 ---
    {"person_id": 12, "org_id": 2, "title": "副区长、区政府党组副书记（原常务）", "start": "", "end": "约2024年", "rank": "副处级",
     "note": "王昕先生常务副区长的历史配置"},
    {"person_id": 13, "org_id": 2, "title": "副区长、区公安分局局长", "start": "", "end": "", "rank": "副处级",
     "note": "公安分局局长"},
    {"person_id": 14, "org_id": 2, "title": "副区长", "start": "", "end": "", "rank": "副处级", "note": "已离任"},
    {"person_id": 15, "org_id": 2, "title": "副区长", "start": "", "end": "", "rank": "副处级", "note": "已离任"},
]

# ════════ Relationships ════════
relationships = [
    # 李光 ↔ 王昕巍（书记-区长搭班）
    {"person_a": 1, "person_b": 2, "type": "搭档", "context": "区委书记与区长共同搭班，主持全区工作", "overlap_org": "大连市甘井子区",
     "overlap_period": "2026年至今"},
    # 李光 → 袁永刚（上下级：书记-常务副区长）
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记与区委常委、常务副区长", "overlap_org": "中国共产党大连市甘井子区委员会",
     "overlap_period": "2026年至今"},
    # 王昕巍 ↔ 袁永刚（区长-常务副区长）
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "区长与常务副区长（区政府党组副书记）", "overlap_org": "大连市甘井子区人民政府",
     "overlap_period": "2026年至今"},
    # 王昕巍 ↔ 赵双勇
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "区长与副区长（区委常委）", "overlap_org": "大连市甘井子区人民政府",
     "overlap_period": "2026年至今"},
    # 王昕巍 ↔ 刘汉存：公安局长
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "分管公安的副区长兼任公安分局局长", "overlap_org": "大连市甘井子区人民政府",
     "overlap_period": ""},
    # 李光 ↔ 王吉州：书记-人大主任
    {"person_a": 1, "person_b": 10, "type": "同事", "context": "区委书记与区人大常委会主任搭班", "overlap_org": "大连市甘井子区",
     "overlap_period": "2026年至今"},
    # 李光 ↔ 刘凤斌：书记-政协主席
    {"person_a": 1, "person_b": 11, "type": "同事", "context": "区委书记与区政协主席搭班", "overlap_org": "大连市甘井子区",
     "overlap_period": "2026年至今"},
    # 王昕巍 ↔ 王吉州：区长-人大主任
    {"person_a": 2, "person_b": 10, "type": "同事", "context": "区长与区人大常委会主任", "overlap_org": "大连市甘井子区",
     "overlap_period": ""},
    # 王昕巍 ↔ 杨文存：前后任／班子调整
    {"person_a": 2, "person_b": 12, "type": "前后任", "context": "杨文存曾任常务副区长（区政府党组副书记），王昕巍任区长后班子调整",
     "overlap_org": "大连市甘井子区人民政府", "overlap_period": ""},
    {"person_a": 7, "person_b": 13, "type": "前后任", "context": "赵铁程前任甘井子公安分局局长，刘汉存现任局长",
     "overlap_org": "大连市公安局甘井子分局", "overlap_period": ""},
]

# ── Build ──────────────────────────────────────────────────────────
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
    print(f"\n✨ {SLUG} staged build complete!")
    print(f"   DB:   {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")