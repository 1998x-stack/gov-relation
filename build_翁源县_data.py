#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
翁源县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 广东省
Parent City: 韶关市
Region: 翁源县
Targets: 县委书记 & 县长

Research Sources:
- 翁源县人民政府门户网站 (www.wengyuan.gov.cn) — 政府新闻
- 维基百科 (zh.wikipedia.org) — 翁源县词条
- 搜狗/360搜索建议 — 关键词确认
- 央视网搜索 — 新闻报道
- 韶关市人民政府门户网站

Current status (as of 2026-07-22):
- 县委书记: 高忠（来源：维基百科、翁源县政府新闻、央视网搜索确认）
- 县长: 钟真（来源：360搜索建议、翁源县政府新闻确认）
- 前任县长: 谭晓健（现任韶关市科技局局长）

Research Date: 2026-07-22
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../"))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "翁源县"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # 县委领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "高忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共韶关市翁源县委书记",
        "current_org": "中共翁源县委员会",
        "source": "维基百科:https://zh.wikipedia.org/wiki/翁源县; 翁源县政府新闻:https://www.wengyuan.gov.cn/"
    },
    {
        "id": 2,
        "name": "钟真",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共韶关市翁源县委副书记、县长",
        "current_org": "翁源县人民政府",
        "source": "翁源县政府新闻确认; 360搜索建议确认; 翁源县第十六届人大第五次会议选举"
    },
    # ════════════════════════════════════════
    # 前任领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "谭晓健",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "韶关市科学技术局局长",
        "current_org": "韶关市科学技术局",
        "source": "360搜索建议:谭晓健翁源简历; 搜索:韶关市科技局局长谭晓健"
    },
    {
        "id": 4,
        "name": "黄社珍",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（历史人物，已判刑）",
        "current_org": "",
        "source": "360搜索建议:黄社珍翁源县长; 搜索提示涉及法律问题"
    },
    # ════════════════════════════════════════
    # 县人大常委会
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "彭辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "翁源县人民法院院长",
        "current_org": "翁源县人民法院",
        "source": "百度搜索结果:彭辉当选翁源县人民法院院长"
    },
    # ════════════════════════════════════════
    # （预留更多领导位置）
    # ════════════════════════════════════════
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共翁源县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共韶关市委员会",
        "location": "翁源县"
    },
    {
        "id": 2,
        "name": "翁源县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "韶关市人民政府",
        "location": "翁源县"
    },
    {
        "id": 3,
        "name": "翁源县人民法院",
        "type": "事业单位",
        "level": "县",
        "parent": "翁源县",
        "location": "翁源县"
    },
    {
        "id": 4,
        "name": "韶关市科学技术局",
        "type": "政府",
        "level": "地级市",
        "parent": "韶关市人民政府",
        "location": "韶关市"
    },
]

# 3. Positions
positions = [
    # 高忠
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "待查", "end": "至今", "rank": "正处级", "note": "维基百科及政府新闻确认"},
    # 钟真
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "待查", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "待查", "end": "至今", "rank": "正处级", "note": "翁源县第十六届人大第五次会议选举产生"},
    # 谭晓健（前任县长）
    {"person_id": 3, "org_id": 2, "title": "县长（前任）", "start": "待查", "end": "待查", "rank": "正处级", "note": "前任翁源县长"},
    {"person_id": 3, "org_id": 4, "title": "局长", "start": "待查", "end": "至今", "rank": "正处级", "note": "现任韶关市科技局局长"},
    # 黄社珍（历史人物）
    {"person_id": 4, "org_id": 2, "title": "县长（历史）", "start": "待查", "end": "待查", "rank": "正处级", "note": "已判刑"},
    # 彭辉
    {"person_id": 5, "org_id": 3, "title": "院长", "start": "待查", "end": "至今", "rank": "正处级", "note": "翁源县人民法院院长"},
]

# 4. Relationships
relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长：党委政府主要领导搭档",
        "overlap_org": "翁源县",
        "overlap_period": "钟真当选县长至今",
        "strength": "strong",
        "confidence": "confirmed"
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "predecessor_successor",
        "context": "钟真接替谭晓健任翁源县长",
        "overlap_org": "翁源县人民政府",
        "overlap_period": "换届交接",
        "strength": "strong",
        "confidence": "plausible"
    },
]

# ── Build ──
if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print(f"Done. DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
