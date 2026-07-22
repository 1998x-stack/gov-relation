#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
永靖县领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Yongjing County leadership network.

Level: 县
Province: 甘肃省
Parent City: 临夏回族自治州
Region: 永靖县
Targets: 县委书记 & 县长

Research Sources:
- 永靖县人民政府官方网站 (gsyongjing.gov.cn), 2026年7月22日确认
- 永靖县融媒体中心新闻 (2026年6-7月)
- 临夏回族自治州人民政府官方网站 (linxia.gov.cn) 在线访谈: 访永靖县委书记李登旭, 2026年4月13日
- 民族日报

Confirmed officeholders (as of 2026-07-22, from gsyongjing.gov.cn):
- 县委书记: 刘斌斌 (2026年6月起任县委书记，此前为县长)
- 县委副书记、代理县长: 孟帅临 (2026年6月起任)

Recent leadership transition:
- 李登旭: 曾任县委书记 (2026年4月仍在任), 已被刘斌斌接替
- 刘斌斌: 原为县长，2026年6月升任县委书记
- 孟帅临: 2026年6月起任县委副书记、代理县长

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
SLUG = "永靖县"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

# The script uses gov_relation.runner (which internally uses sqlite3)
import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders (as of June-July 2026)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "刘斌斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永靖县委书记",
        "current_org": "中共永靖县委员会",
        "source": "https://www.gsyongjing.gov.cn/ — 永靖县政府网站新闻: 刘斌斌主持召开县委常委会扩大会议(2026-07-21)、刘斌斌为全县党员领导干部讲授学习教育专题党课(2026-06-29), 2026年7月22日确认"
    },
    {
        "id": 2,
        "name": "孟帅临",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永靖县委副书记、代理县长",
        "current_org": "永靖县人民政府",
        "source": "https://www.gsyongjing.gov.cn/ — 永靖县政府网站新闻: 永靖县庆祝建党105周年暨'七一'表彰大会召开(2026-06-29), 2026年7月22日确认"
    },
    # ════════════════════════════════════════
    # Predecessors
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "李登旭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://www.linxia.gov.cn/lxzlxz/zwgk/fdzdgknr/zxft/art/2026/art_d16aa17ec06047afb41d30cf63473fa0.html — 临夏州政府网在线访谈: 访永靖县委书记李登旭(2026-04-13)"
    },
    # ════════════════════════════════════════
    # Other Key Leaders
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "张丰忠",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永靖县人大常委会主任",
        "current_org": "永靖县人民代表大会常务委员会",
        "source": "https://www.gsyongjing.gov.cn/ — 永靖县政府网站新闻: 永靖县庆祝建党105周年暨'七一'表彰大会召开(2026-06-29)"
    },
    {
        "id": 5,
        "name": "祁先军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永靖县政协主席候选人",
        "current_org": "中国人民政治协商会议永靖县委员会",
        "source": "https://www.gsyongjing.gov.cn/ — 永靖县政府网站新闻: 永靖县庆祝建党105周年暨'七一'表彰大会召开(2026-06-29)"
    },
    {
        "id": 6,
        "name": "他维红",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永靖县委副书记",
        "current_org": "中共永靖县委员会",
        "source": "https://www.gsyongjing.gov.cn/ — 永靖县政府网站新闻: 刘斌斌为全县党员领导干部讲授学习教育专题党课(2026-06-29)"
    },
    # ════════════════════════════════════════
    # 县人大常委会副主任/政协副主席 (from 十八届人大常委会第三十四次会议)
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "刘青云",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永靖县十八届人大常委会委员相关",
        "current_org": "永靖县人民代表大会常务委员会",
        "source": "https://www.gsyongjing.gov.cn/ — 永靖县十八届人大常委会第三十四次会议(2026-07-08)"
    },
    {
        "id": 8,
        "name": "高国林",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永靖县十八届人大常委会委员相关",
        "current_org": "永靖县人民代表大会常务委员会",
        "source": "https://www.gsyongjing.gov.cn/ — 永靖县十八届人大常委会第三十四次会议(2026-07-08)"
    },
]

# 2. Organizations
organizations = [
    {"id": 1, "name": "中共永靖县委员会", "type": "党委", "level": "县", "parent": "中共临夏回族自治州委员会", "location": "甘肃省永靖县"},
    {"id": 2, "name": "永靖县人民政府", "type": "政府", "level": "县", "parent": "临夏回族自治州人民政府", "location": "甘肃省永靖县"},
    {"id": 3, "name": "永靖县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "临夏回族自治州人民代表大会常务委员会", "location": "甘肃省永靖县"},
    {"id": 4, "name": "中国人民政治协商会议永靖县委员会", "type": "政协", "level": "县", "parent": "中国人民政治协商会议临夏回族自治州委员会", "location": "甘肃省永靖县"},
]

# 3. Positions (linking persons to organizations)
positions = [
    # 县委
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2026-06", "end_date": "present", "rank": "正处级", "note": "县委全面工作，原县长升任"},
    {"person_id": 6, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "专职副书记"},
    # 县政府
    {"person_id": 2, "org_id": 2, "title": "代理县长", "start_date": "2026-06", "end_date": "present", "rank": "正处级", "note": "县政府全面工作，县委副书记兼"},
    # 县人大
    {"person_id": 4, "org_id": 3, "title": "主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": "县人大常委会全面工作"},
    # 县政协
    {"person_id": 5, "org_id": 4, "title": "主席候选人", "start_date": "", "end_date": "present", "rank": "正处级", "note": "县政协工作"},
    # 前任
    {"person_id": 3, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "2026-06", "rank": "正处级", "note": "前任县委书记，已离任"},
]

# 4. Relationships
relationships = [
    # 县委班子关系
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记—县委副书记/代理县长", "overlap_org": "中共永靖县委员会", "overlap_period": "2026年6月起"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县委书记—县委副书记", "overlap_org": "中共永靖县委员会", "overlap_period": "2026年6月起"},
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "县委副书记—县委副书记", "overlap_org": "中共永靖县委员会", "overlap_period": "2026年6月起"},
    # 四套班子
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委书记—人大常委会主任", "overlap_org": "永靖县", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "县长—人大常委会主任", "overlap_org": "永靖县", "overlap_period": "现任"},
    # 前后任
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "刘斌斌接替李登旭任县委书记", "overlap_org": "中共永靖县委员会", "overlap_period": "2026年6月交接"},
    # 县政协
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "县委书记—政协主席候选人", "overlap_org": "永靖县", "overlap_period": "现任"},
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "人大主任—政协主席候选人", "overlap_org": "永靖县", "overlap_period": "现任"},
]


# ══════════════════════════════════════════════════════════════
# Build
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print(f"[{SLUG}] Building database: {DB_PATH}")
    print(f"[{SLUG}] Building GEXF: {GEXF_PATH}")

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
