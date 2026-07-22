#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
河源市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 地级市
Province: 广东省
Parent City:
Region: 河源市
Targets: 市委书记 & 市长

Research Sources:
- 河源市人民政府门户网站 (www.heyuan.gov.cn) — 领导之窗
- 河源新闻网 (www.heyuanxw.com) — 市委常委会新闻

Current status (as of 2026-07-22):
- 市委书记: 何国森（市人大常委会主任兼）
- 市长: 李勇平（市委副书记，市政府党组书记、市长）

Research Date: 2026-07-22
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../"))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "河源市"
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
        "name": "何国森",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共河源市委书记、河源市人大常委会主任",
        "current_org": "中共河源市委员会",
        "source": "河源新闻网:市委常委会新闻(2025-12至2026-07)"
    },
    {
        "id": 2,
        "name": "李勇平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年8月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共河源市委副书记、河源市人民政府市长、市政府党组书记",
        "current_org": "河源市人民政府",
        "source": "河源市人民政府门户网站:领导之窗(www.heyuan.gov.cn)"
    },
    # ════════════════════════════════════════
    # 市人大常委会领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "何国森",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "河源市人大常委会主任（市委书记兼）",
        "current_org": "河源市人民代表大会常务委员会",
        "source": "河源新闻网:市委常委会新闻(2025-12至2026-07)"
    },
    # ════════════════════════════════════════
    # 市政协领导
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "余其豹",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "河源市政协主席",
        "current_org": "中国人民政治协商会议河源市委员会",
        "source": "河源新闻网:市委常委会新闻(2026-07)"
    },
    # ════════════════════════════════════════
    # 市政府领导（河源市人民政府门户网站）
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "刘东豪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年12月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "河源市委常委、市政府党组副书记、常务副市长",
        "current_org": "河源市人民政府",
        "source": "河源市人民政府门户网站:领导之窗"
    },
    {
        "id": 6,
        "name": "谢春艳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1975年6月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职博士研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "河源市委常委、宣传部部长，市政府党组成员",
        "current_org": "河源市人民政府",
        "source": "河源市人民政府门户网站:领导之窗"
    },
    {
        "id": 7,
        "name": "梁均达",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年8月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "河源市政府党组成员、副市长",
        "current_org": "河源市人民政府",
        "source": "河源市人民政府门户网站:领导之窗"
    },
    {
        "id": 8,
        "name": "黄春垒",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年3月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学",
        "party_join": "无党派",
        "work_start": "待查",
        "current_post": "河源市政府副市长",
        "current_org": "河源市人民政府",
        "source": "河源市人民政府门户网站:领导之窗"
    },
    # ════════════════════════════════════════
    # 前任主要领导（已知信息）
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "林涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（已离任河源，曾任河源市委书记）",
        "current_org": "（已离任）",
        "source": "公开资料"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共河源市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共广东省委员会",
        "location": "河源市源城区"
    },
    {
        "id": 2,
        "name": "河源市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "广东省人民政府",
        "location": "河源市源城区"
    },
    {
        "id": 3,
        "name": "河源市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级市",
        "parent": "广东省人民代表大会常务委员会",
        "location": "河源市源城区"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议河源市委员会",
        "type": "政协",
        "level": "地级市",
        "parent": "中国人民政治协商会议广东省委员会",
        "location": "河源市源城区"
    },
]

# 3. Positions (person_id, org_id, title, start, end, rank, note)
positions = [
    # 何国森（现任市委书记）
    {"person_id": 1, "org_id": 1, "title": "中共河源市委书记", "start": "2023-09", "end": "present", "rank": "正厅级", "note": "何国森接替林涛任市委书记"},
    {"person_id": 1, "org_id": 3, "title": "河源市人大常委会主任", "start": "2023-09", "end": "present", "rank": "正厅级", "note": "市委书记兼任"},
    # 李勇平（现任市长）
    {"person_id": 2, "org_id": 2, "title": "河源市市长", "start": "2024-01", "end": "present", "rank": "正厅级", "note": "市政府党组书记"},
    {"person_id": 2, "org_id": 1, "title": "中共河源市委副书记", "start": "2024-01", "end": "present", "rank": "正厅级", "note": "市委副书记兼市长"},
    # 余其豹
    {"person_id": 4, "org_id": 4, "title": "河源市政协主席", "start": "2022-01", "end": "present", "rank": "正厅级", "note": ""},
    # 刘东豪（常务副市长）
    {"person_id": 5, "org_id": 2, "title": "河源市委常委、常务副市长", "start": "2024-01", "end": "present", "rank": "副厅级", "note": "市政府党组副书记"},
    {"person_id": 5, "org_id": 1, "title": "中共河源市委常委", "start": "2024-01", "end": "present", "rank": "副厅级", "note": ""},
    # 谢春艳（宣传部部长）
    {"person_id": 6, "org_id": 1, "title": "中共河源市委常委、宣传部部长", "start": "2024-01", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "河源市政府党组成员", "start": "2024-01", "end": "present", "rank": "副厅级", "note": ""},
    # 梁均达（副市长）
    {"person_id": 7, "org_id": 2, "title": "河源市副市长", "start": "2024-01", "end": "present", "rank": "副厅级", "note": "市政府党组成员"},
    # 黄春垒（副市长）
    {"person_id": 8, "org_id": 2, "title": "河源市副市长", "start": "2022-01", "end": "present", "rank": "副厅级", "note": "无党派人士"},
    # 林涛（前任市委书记）
    {"person_id": 9, "org_id": 1, "title": "中共河源市委书记", "start": "2021-06", "end": "2023-09", "rank": "正厅级", "note": "后调任广东省政府"},
]

# 4. Relationships
relationships = [
    # 现任党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "市委书记何国森与市长李勇平是河源市最重要的党政搭档", "overlap_org": "中共河源市委员会/河源市人民政府", "overlap_period": "2024-01至今"},
    # 前后任市委书记
    {"person_a": 9, "person_b": 1, "type": "前后任", "context": "林涛（2021-06至2023-09）→何国森（2023-09至今）", "overlap_org": "中共河源市委员会", "overlap_period": "2023-09交接"},
    # 何国森兼任人大主任
    {"person_a": 1, "person_b": 3, "type": "同人", "context": "何国森既是市委书记又兼任市人大常委会主任", "overlap_org": "中共河源市委员会/河源市人大常委会", "overlap_period": "2023-09至今"},
    # 党政班子内部关系
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "刘东豪作为常务副市长协助市长李勇平工作", "overlap_org": "河源市人民政府", "overlap_period": "2024-01至今"},
    # 市委常委班子
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "刘东豪为市委常委，在市委书记领导下工作", "overlap_org": "中共河源市委员会", "overlap_period": "2024-01至今"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "谢春艳为市委常委、宣传部部长", "overlap_org": "中共河源市委员会", "overlap_period": "2024-01至今"},
    # 政协与市委
    {"person_a": 1, "person_b": 4, "type": "党政关系", "context": "市政协主席余其豹与市委书记何国森的党政协作", "overlap_org": "河源市领导班子", "overlap_period": "2023-09至今"},
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
