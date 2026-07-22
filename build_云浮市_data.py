#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
云浮市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 地级市
Province: 广东省
Parent City:
Region: 云浮市
Targets: 市委书记 & 市长

Research Sources:
- 云浮市人民政府门户网站 (www.yunfu.gov.cn) — 领导之窗
- 百度百科 — 卢荣春、李庆新
- 南方日报/南方+ — 卢荣春任云浮市委书记（2021-07-21）

Current status (as of 2026-07-22):
- 市委书记: 卢荣春（2021年7月－）
- 市长: 李庆新（2021年11月－）

Research Date: 2026-07-22
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "云浮市"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"

import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # 市委领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "卢荣春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967年9月",
        "birthplace": "广东阳江",
        "native_place": "广东阳江",
        "education": "中山大学行政管理专业在职研究生学历，管理学博士",
        "party_join": "中共党员（1988年12月）",
        "work_start": "1990年7月",
        "current_post": "中共云浮市委书记、市人大常委会主任",
        "current_org": "中共云浮市委员会",
        "source": "百度百科:卢荣春"
    },
    {
        "id": 2,
        "name": "李庆新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967年8月",
        "birthplace": "广东东莞",
        "native_place": "广东东莞",
        "education": "广东省委党校在职研究生学历",
        "party_join": "中共党员（1989年1月）",
        "work_start": "1985年7月",
        "current_post": "中共云浮市委副书记、市政府党组书记、市长",
        "current_org": "云浮市人民政府",
        "source": "百度百科:李庆新; yunfu.gov.cn"
    },
    # ════════════════════════════════════════
    # 市政府领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "刘旺先",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年6月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职研究生学历，法学硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "云浮市委常委、市政府党组副书记、常务副市长",
        "current_org": "云浮市人民政府",
        "source": "yunfu.gov.cn 领导之窗"
    },
    {
        "id": 4,
        "name": "邱泽军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年12月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "省社科院在职研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "云浮市委常委、市政府党组成员、副市长",
        "current_org": "云浮市人民政府",
        "source": "yunfu.gov.cn 领导之窗"
    },
    {
        "id": 5,
        "name": "梁东海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年12月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "中山大学岭南学院在职研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "云浮市政府党组成员、副市长",
        "current_org": "云浮市人民政府",
        "source": "yunfu.gov.cn 领导之窗"
    },
    {
        "id": 6,
        "name": "徐贤荣",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1972年5月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职大学",
        "party_join": "民进会员",
        "work_start": "待查",
        "current_post": "云浮市副市长",
        "current_org": "云浮市人民政府",
        "source": "yunfu.gov.cn 领导之窗"
    },
    {
        "id": 7,
        "name": "王诗军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年11月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学学历，工程硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "云浮市政府党组成员、副市长兼市公安局局长",
        "current_org": "云浮市人民政府",
        "source": "yunfu.gov.cn 领导之窗"
    },
    {
        "id": 8,
        "name": "梁世军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年9月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "广东省委党校经济管理专业毕业",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "云浮市政府党组成员、副市长",
        "current_org": "云浮市人民政府",
        "source": "yunfu.gov.cn 领导之窗"
    },
    {
        "id": 9,
        "name": "许翠丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1972年1月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "省社科院在职研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "云浮市政府党组成员、副市长",
        "current_org": "云浮市人民政府",
        "source": "yunfu.gov.cn 领导之窗"
    },
    {
        "id": 10,
        "name": "陈新仪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "云浮市政府党组成员、秘书长、市政府办公室党组书记",
        "current_org": "云浮市人民政府",
        "source": "yunfu.gov.cn 领导之窗"
    },
    # ════════════════════════════════════════
    # 前任主要领导
    # ════════════════════════════════════════
    {
        "id": 11,
        "name": "黄汉标",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广东省人大常委会党组成员（曾任云浮市委书记 2018-2021）",
        "current_org": "广东省人大常委会（已离任云浮）",
        "source": "南方日报; 公开报道"
    },
    {
        "id": 12,
        "name": "王胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "揭阳市委书记（曾任云浮市市长 2016-2021）",
        "current_org": "中共揭阳市委员会（已离任云浮）",
        "source": "公开报道"
    },
    {
        "id": 13,
        "name": "庞国梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "广东湛江",
        "native_place": "广东湛江",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中央人民政府驻澳门特别行政区联络办公室副主任（曾任云浮市委书记 2015-2018）",
        "current_org": "中央政府驻澳门联络办（已离任云浮）",
        "source": "公开报道"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共云浮市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共广东省委员会",
        "location": "云浮市云城区"
    },
    {
        "id": 2,
        "name": "云浮市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "广东省人民政府",
        "location": "云浮市云城区"
    },
    {
        "id": 3,
        "name": "云浮市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级市",
        "parent": "广东省人民代表大会常务委员会",
        "location": "云浮市云城区"
    },
    {
        "id": 4,
        "name": "云浮市公安局",
        "type": "政府",
        "level": "正处级",
        "parent": "云浮市人民政府",
        "location": "云浮市云城区"
    },
    {
        "id": 5,
        "name": "广东省审计厅",
        "type": "政府",
        "level": "省级",
        "parent": "广东省人民政府",
        "location": "广州市"
    },
    {
        "id": 6,
        "name": "中共汕尾市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共广东省委员会",
        "location": "汕尾市"
    },
    {
        "id": 7,
        "name": "中共中山市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共广东省委员会",
        "location": "中山市"
    },
    {
        "id": 8,
        "name": "中共揭阳市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共广东省委员会",
        "location": "揭阳市"
    },
    {
        "id": 9,
        "name": "广东省人大常委会",
        "type": "人大",
        "level": "省级",
        "parent": "",
        "location": "广州市"
    },
    {
        "id": 10,
        "name": "中央政府驻澳门联络办公室",
        "type": "其他",
        "level": "省级",
        "parent": "",
        "location": "澳门"
    },
]

# 3. Positions (person_id, org_id, title, start, end, rank, note)
positions = [
    # 卢荣春 — 现任市委书记
    {"person_id": 1, "org_id": 1, "title": "中共云浮市委书记", "start_date": "2021-07", "end_date": "present", "rank": "正厅级", "note": "2021年7月任云浮市委书记"},
    {"person_id": 1, "org_id": 3, "title": "云浮市人大常委会主任", "start_date": "2021-08", "end_date": "present", "rank": "正厅级", "note": "兼任市人大常委会主任"},
    # 卢荣春 — 省审计厅厅长（前任）
    {"person_id": 1, "org_id": 5, "title": "广东省审计厅党组书记、厅长", "start_date": "2018-03", "end_date": "2021-07", "rank": "正厅级", "note": "曾任广东省审计厅厅长"},
    {"person_id": 1, "org_id": 5, "title": "广东省审计厅党组书记", "start_date": "2017-03", "end_date": "2018-03", "rank": "正厅级", "note": ""},
    {"person_id": 1, "org_id": 5, "title": "广东省审计厅副厅长、党组成员", "start_date": "2010-06", "end_date": "2017-03", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 5, "title": "广东省审计厅办公室主任", "start_date": "2005-10", "end_date": "2009-09", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 5, "title": "广东省审计厅副厅级干部（绩效审计分局局长）", "start_date": "2009-09", "end_date": "2010-06", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 5, "title": "广东省审计厅办公室（原省财政厅办公室）调研员/副主任", "start_date": "2000-06", "end_date": "2005-10", "rank": "正处级", "note": "2000年机构改革从财政厅转入审计厅"},
    # 卢荣春 — 省财政厅
    {"person_id": 1, "org_id": 5, "title": "广东省财政厅干部/科员/副主任科员/主任科员", "start_date": "1990-07", "end_date": "2000-06", "rank": "科员至正科级", "note": "1990年中山大学毕业进入省财政厅"},
    # 李庆新 — 现任市长
    {"person_id": 2, "org_id": 2, "title": "云浮市市长", "start_date": "2021-11", "end_date": "present", "rank": "正厅级", "note": "2021年11月16日任代市长，11月26日当选市长"},
    {"person_id": 2, "org_id": 1, "title": "中共云浮市委副书记", "start_date": "2021-11", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "云浮市政府党组书记", "start_date": "2021-11", "end_date": "present", "rank": "正厅级", "note": ""},
    # 李庆新 — 前任
    {"person_id": 2, "org_id": 7, "title": "中山市委常委、政法委书记", "start_date": "2020-09", "end_date": "2021-11", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 6, "title": "汕尾市委常委", "start_date": "2019-10", "end_date": "2020-09", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 6, "title": "汕尾市委常委、城区委书记", "start_date": "2017-01", "end_date": "2019-10", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 6, "title": "汕尾市委常委、秘书长、办公室主任", "start_date": "2012-10", "end_date": "2017-01", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 6, "title": "汕尾市委常委、陆河县委书记", "start_date": "2012-09", "end_date": "2012-10", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 6, "title": "汕尾市陆河县委书记、县人大常委会主任", "start_date": "2008-07", "end_date": "2012-08", "rank": "正处级", "note": ""},
    # 李庆新 — 东莞
    # (东莞时期无法精确关联到具体组织ID，简化为东莞市委)
    {"person_id": 2, "org_id": 2, "title": "东莞市桥头镇党委副书记、镇长", "start_date": "2006-09", "end_date": "2008-07", "rank": "正处级", "note": "东莞桥头镇"},
    {"person_id": 2, "org_id": 2, "title": "东莞市团委书记、党组书记", "start_date": "2003-12", "end_date": "2006-09", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "东莞市团委副书记", "start_date": "1999-12", "end_date": "2003-12", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "东莞市团委学校部部长等职", "start_date": "1992-02", "end_date": "1999-12", "rank": "科级", "note": "从学校教师转入共青团系统"},
    # 刘旺先 — 常务副市长
    {"person_id": 3, "org_id": 2, "title": "云浮市委常委、市政府党组副书记、常务副市长", "start_date": "未知", "end_date": "present", "rank": "副厅级", "note": "负责市政府常务工作"},
    # 邱泽军 — 副市长
    {"person_id": 4, "org_id": 2, "title": "云浮市委常委、市政府党组成员、副市长", "start_date": "未知", "end_date": "present", "rank": "副厅级", "note": "负责生态环境、住建、交通等方面工作"},
    # 梁东海 — 副市长
    {"person_id": 5, "org_id": 2, "title": "云浮市政府党组成员、副市长", "start_date": "未知", "end_date": "present", "rank": "副厅级", "note": "负责科技、工信、市场监管、商务等方面工作"},
    # 徐贤荣 — 副市长
    {"person_id": 6, "org_id": 2, "title": "云浮市副市长", "start_date": "未知", "end_date": "present", "rank": "副厅级", "note": "负责教育、文化、卫健、体育等方面工作"},
    # 王诗军 — 副市长兼公安局长
    {"person_id": 7, "org_id": 2, "title": "云浮市政府党组成员、副市长兼市公安局局长", "start_date": "未知", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 4, "title": "云浮市公安局局长", "start_date": "未知", "end_date": "present", "rank": "正处级", "note": "副市长兼任"},
    # 梁世军 — 副市长
    {"person_id": 8, "org_id": 2, "title": "云浮市政府党组成员、副市长", "start_date": "未知", "end_date": "present", "rank": "副厅级", "note": "负责农业农村、乡村振兴、水务等方面工作"},
    # 许翠丽 — 副市长
    {"person_id": 9, "org_id": 2, "title": "云浮市政府党组成员、副市长", "start_date": "未知", "end_date": "present", "rank": "副厅级", "note": "负责民政、人社、自然资源等方面工作"},
    # 陈新仪 — 秘书长
    {"person_id": 10, "org_id": 2, "title": "云浮市政府党组成员、秘书长、市政府办公室党组书记", "start_date": "未知", "end_date": "present", "rank": "正处级", "note": "负责市政府办公室工作"},
    # 黄汉标 — 前任市委书记
    {"person_id": 11, "org_id": 1, "title": "中共云浮市委书记", "start_date": "2018", "end_date": "2021-07", "rank": "正厅级", "note": "前任云浮市委书记"},
    {"person_id": 11, "org_id": 9, "title": "广东省人大常委会党组成员", "start_date": "2021-07", "end_date": "present", "rank": "正厅级", "note": "卸任后调省人大"},
    # 王胜 — 前任市长
    {"person_id": 12, "org_id": 2, "title": "云浮市市长", "start_date": "2016", "end_date": "2021-08", "rank": "正厅级", "note": "前任云浮市长"},
    {"person_id": 12, "org_id": 8, "title": "揭阳市委书记", "start_date": "2021-08", "end_date": "present", "rank": "正厅级", "note": "调任揭阳市委书记"},
    # 庞国梅 — 更早前任市委书记
    {"person_id": 13, "org_id": 1, "title": "中共云浮市委书记", "start_date": "2015", "end_date": "2018", "rank": "正厅级", "note": "前任云浮市委书记"},
    {"person_id": 13, "org_id": 10, "title": "中央政府驻澳门联络办公室副主任", "start_date": "2018", "end_date": "present", "rank": "副部级", "note": "调任中联办副主任"},
]

# 4. Relationships
relationships = [
    # 现任党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "市委书记与市长是云浮市最重要的党政搭档", "overlap_org": "中共云浮市委员会/云浮市人民政府", "overlap_period": "2021-11至今"},
    # 市委书记前后任
    {"person_a": 11, "person_b": 1, "type": "前后任", "context": "黄汉标（2018-2021）→卢荣春（2021-至今）", "overlap_org": "中共云浮市委员会", "overlap_period": "2021-07交接"},
    {"person_a": 13, "person_b": 11, "type": "前后任", "context": "庞国梅（2015-2018）→黄汉标（2018-2021）", "overlap_org": "中共云浮市委员会", "overlap_period": "2018交接"},
    # 市长前后任
    {"person_a": 12, "person_b": 2, "type": "前后任", "context": "王胜（2016-2021）→李庆新（2021-至今）", "overlap_org": "云浮市人民政府", "overlap_period": "2021-11交接"},
    # 市政府领导班子（工作关系）
    {"person_a": 2, "person_b": 3, "type": "政府领导班子", "context": "市长与常务副市长是市政府核心工作关系", "overlap_org": "云浮市人民政府", "overlap_period": "2021-11至今"},
    {"person_a": 2, "person_b": 4, "type": "政府领导班子", "context": "市长与副市长在市政府共同工作", "overlap_org": "云浮市人民政府", "overlap_period": "2021-11至今"},
    {"person_a": 2, "person_b": 5, "type": "政府领导班子", "context": "市长与副市长在市政府共同工作", "overlap_org": "云浮市人民政府", "overlap_period": "2021-11至今"},
    {"person_a": 2, "person_b": 6, "type": "政府领导班子", "context": "市长与副市长在市政府共同工作", "overlap_org": "云浮市人民政府", "overlap_period": "2021-11至今"},
    {"person_a": 2, "person_b": 7, "type": "政府领导班子", "context": "市长与副市长在市政府共同工作", "overlap_org": "云浮市人民政府", "overlap_period": "2021-11至今"},
    {"person_a": 2, "person_b": 8, "type": "政府领导班子", "context": "市长与副市长在市政府共同工作", "overlap_org": "云浮市人民政府", "overlap_period": "2021-11至今"},
    {"person_a": 2, "person_b": 9, "type": "政府领导班子", "context": "市长与副市长在市政府共同工作", "overlap_org": "云浮市人民政府", "overlap_period": "2021-11至今"},
    # 卢荣春与前任省审计厅系统的关系
    {"person_a": 1, "person_b": 12, "type": "上下级关系", "context": "卢荣春（省审计厅厅长）与王胜（云浮市长）在2021年曾任广东省内正厅级职务", "overlap_org": "广东省", "overlap_period": "2021"},
]

# ── Build ──
if __name__ == "__main__":
    print(f"Building {SLUG} network...")
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
    print("Done.")
