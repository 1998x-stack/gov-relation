#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阳春市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县级市
Province: 广东省
Parent City: 阳江市
Region: 阳春市
Targets: 市委书记 & 市长

Research Sources:
- 阳春市人民政府门户网站 (www.yangchun.gov.cn)
- 阳春要闻 (2026年7月新闻)

Current status (as of 2026-07-22):
- 市委书记: 李谦常（阳江市人大常委会副主任兼阳春市委书记）
- 市长: 张艾鹏（阳春市委副书记、市长）
- 人大常委会主任: 曾庆婵
- 政协主席: 黄忠宏

Research Date: 2026-07-22
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "阳春市"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # 市委领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "李谦常",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "阳江市人大常委会副主任、中共阳春市委书记",
        "current_org": "中共阳春市委员会",
        "source": "阳春市人民政府门户网站:李谦常"
    },
    {
        "id": 2,
        "name": "张艾鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共阳春市委副书记、市长",
        "current_org": "阳春市人民政府",
        "source": "阳春市人民政府门户网站:张艾鹏"
    },
    # ════════════════════════════════════════
    # 市人大常委会领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "曾庆婵",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "阳春市人大常委会主任",
        "current_org": "阳春市人民代表大会常务委员会",
        "source": "阳春市人民政府门户网站:曾庆婵"
    },
    # ════════════════════════════════════════
    # 市政协领导
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "黄忠宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "阳春市政协主席",
        "current_org": "中国人民政治协商会议阳春市委员会",
        "source": "阳春市人民政府门户网站:黄忠宏"
    },
    # ════════════════════════════════════════
    # 其他市委常委/副市长（新闻中提及）
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "梁健敏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "阳春市领导（市委常委/副市长）",
        "current_org": "中共阳春市委员会",
        "source": "阳春市人民政府门户网站"
    },
    {
        "id": 6,
        "name": "刘昌博",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "阳春市领导（市委常委/副市长）",
        "current_org": "中共阳春市委员会",
        "source": "阳春市人民政府门户网站"
    },
    {
        "id": 7,
        "name": "郭飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "阳春市领导（市委常委/副市长）",
        "current_org": "中共阳春市委员会",
        "source": "阳春市人民政府门户网站"
    },
    {
        "id": 8,
        "name": "蓝瑜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "阳春市领导（市委常委/副市长）",
        "current_org": "中共阳春市委员会",
        "source": "阳春市人民政府门户网站"
    },
    {
        "id": 9,
        "name": "陈超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "阳春市领导（市委常委/副市长）",
        "current_org": "中共阳春市委员会",
        "source": "阳春市人民政府门户网站"
    },
    {
        "id": 10,
        "name": "徐英媚",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "阳春市领导（市委常委/副市长）",
        "current_org": "中共阳春市委员会",
        "source": "阳春市人民政府门户网站"
    },
    {
        "id": 11,
        "name": "李文辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "阳春市领导（市委常委/副市长）",
        "current_org": "中共阳春市委员会",
        "source": "阳春市人民政府门户网站"
    },
    {
        "id": 12,
        "name": "梁柳珠",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "阳春市领导（市委常委/副市长）",
        "current_org": "中共阳春市委员会",
        "source": "阳春市人民政府门户网站"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共阳春市委员会",
        "type": "党委",
        "level": "县级市",
        "parent": "中共阳江市委",
        "location": "阳春市"
    },
    {
        "id": 2,
        "name": "阳春市人民政府",
        "type": "政府",
        "level": "县级市",
        "parent": "阳江市人民政府",
        "location": "阳春市"
    },
    {
        "id": 3,
        "name": "阳春市人民代表大会常务委员会",
        "type": "人大",
        "level": "县级市",
        "parent": "阳江市人民代表大会常务委员会",
        "location": "阳春市"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议阳春市委员会",
        "type": "政协",
        "level": "县级市",
        "parent": "中国人民政治协商会议阳江市委员会",
        "location": "阳春市"
    },
    {
        "id": 5,
        "name": "阳江市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级市",
        "parent": "广东省人民代表大会常务委员会",
        "location": "阳江市"
    },
]

# 3. Positions (person_id, org_id, title, start, end, rank, note)
positions = [
    # 李谦常 — 市委书记
    {"person_id": 1, "org_id": 1, "title": "中共阳春市委书记", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "同时担任阳江市人大常委会副主任（副厅级）"},
    {"person_id": 1, "org_id": 5, "title": "阳江市人大常委会副主任", "start_date": "待查", "end_date": "present", "rank": "副厅级", "note": "兼任"},
    # 张艾鹏 — 市长
    {"person_id": 2, "org_id": 2, "title": "阳春市市长", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": "市委副书记、市长"},
    {"person_id": 2, "org_id": 1, "title": "中共阳春市委副书记", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": ""},
    # 曾庆婵 — 人大常委会主任
    {"person_id": 3, "org_id": 3, "title": "阳春市人大常委会主任", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": ""},
    # 黄忠宏 — 政协主席
    {"person_id": 4, "org_id": 4, "title": "阳春市政协主席", "start_date": "待查", "end_date": "present", "rank": "正处级", "note": ""},
    # 梁健敏 — 市领导
    {"person_id": 5, "org_id": 1, "title": "阳春市领导", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "具体职务待查"},
    # 刘昌博 — 市领导
    {"person_id": 6, "org_id": 1, "title": "阳春市领导", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "具体职务待查"},
    # 郭飞 — 市领导
    {"person_id": 7, "org_id": 1, "title": "阳春市领导", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "具体职务待查"},
    # 蓝瑜 — 市领导
    {"person_id": 8, "org_id": 1, "title": "阳春市领导", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "具体职务待查"},
    # 陈超 — 市领导
    {"person_id": 9, "org_id": 1, "title": "阳春市领导", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "具体职务待查"},
    # 徐英媚 — 市领导
    {"person_id": 10, "org_id": 1, "title": "阳春市领导", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "具体职务待查"},
    # 李文辉 — 市领导
    {"person_id": 11, "org_id": 1, "title": "阳春市领导", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "具体职务待查"},
    # 梁柳珠 — 市领导
    {"person_id": 12, "org_id": 1, "title": "阳春市领导", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "具体职务待查"},
]

# 4. Relationships
relationships = [
    # 现任党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "市委书记李谦常与市长张艾鹏是阳春市最重要的党政搭档", "overlap_org": "中共阳春市委员会/阳春市人民政府", "overlap_period": "至今"},
    # 人大与党委
    {"person_a": 1, "person_b": 3, "type": "同城协作", "context": "市委书记与市人大常委会主任同城工作", "overlap_org": "阳春市四套班子", "overlap_period": "至今"},
    # 政协与党委
    {"person_a": 1, "person_b": 4, "type": "同城协作", "context": "市委书记与市政协主席同城工作", "overlap_org": "阳春市四套班子", "overlap_period": "至今"},
    # 市长与人大
    {"person_a": 2, "person_b": 3, "type": "协作", "context": "市长与市人大常委会主任同城工作", "overlap_org": "阳春市四套班子", "overlap_period": "至今"},
    # 市长与政协
    {"person_a": 2, "person_b": 4, "type": "协作", "context": "市长与市政协主席同城工作", "overlap_org": "阳春市四套班子", "overlap_period": "至今"},
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
