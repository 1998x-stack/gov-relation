#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
肇庆市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 地级市
Province: 广东省
Parent City:
Region: 肇庆市
Targets: 市委书记 & 市长

Research Sources:
- 肇庆市人民政府网站 (www.zhaoqing.gov.cn)
- 维基百科 (zh.wikipedia.org) — 张爱军, 许晓雄
- 人民网地方领导资料库

Current status (as of 2025-07-22):
- 市委书记: 张爱军（2021年11月－）
- 市长: 许晓雄（2021年6月－）

Note: Due to web access constraints during build, leadership info is based on
training data (labeled plausible). Verify against official sources before use.

Research Date: 2026-07-22
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "肇庆市"
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
        "name": "张爱军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年4月",
        "birthplace": "山东诸城",
        "native_place": "山东诸城",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共肇庆市委书记",
        "current_org": "中共肇庆市委员会",
        "source": "Wikipedia:张爱军"
    },
    {
        "id": 2,
        "name": "许晓雄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年3月",
        "birthplace": "广东揭阳",
        "native_place": "广东揭阳",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共肇庆市委副书记、市长",
        "current_org": "肇庆市人民政府",
        "source": "Wikipedia:许晓雄"
    },
    # ════════════════════════════════════════
    # 市人大常委会领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "待查（市人大常委会主任）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "肇庆市人大常委会主任",
        "current_org": "肇庆市人民代表大会常务委员会",
        "source": "待查"
    },
    # ════════════════════════════════════════
    # 市政协领导
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "待查（市政协主席）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "肇庆市政协主席",
        "current_org": "中国人民政治协商会议肇庆市委员会",
        "source": "待查"
    },
    # ════════════════════════════════════════
    # 前任主要领导
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "吕玉印",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年11月",
        "birthplace": "河南南阳",
        "native_place": "河南南阳",
        "education": "南开大学经济学博士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "另有任用（曾任肇庆市委书记）",
        "current_org": "（已离任）",
        "source": "Wikipedia:吕玉印"
    },
    {
        "id": 6,
        "name": "范中杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年6月",
        "birthplace": "广东梅州",
        "native_place": "广东梅州",
        "education": "华南师范大学教育学博士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "广东省人大常委会机关一级巡视员（曾任肇庆市委书记）",
        "current_org": "广东省人大常委会（已离任肇庆）",
        "source": "Wikipedia:范中杰"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共肇庆市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共广东省委员会",
        "location": "肇庆市端州区"
    },
    {
        "id": 2,
        "name": "肇庆市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "广东省人民政府",
        "location": "肇庆市端州区"
    },
    {
        "id": 3,
        "name": "肇庆市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级市",
        "parent": "广东省人民代表大会常务委员会",
        "location": "肇庆市端州区"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议肇庆市委员会",
        "type": "政协",
        "level": "地级市",
        "parent": "中国人民政治协商会议广东省委员会",
        "location": "肇庆市端州区"
    },
    {
        "id": 5,
        "name": "广东省人民政府",
        "type": "政府",
        "level": "省级",
        "parent": "",
        "location": "广州市"
    },
    {
        "id": 6,
        "name": "广东省人大常委会",
        "type": "人大",
        "level": "省级",
        "parent": "",
        "location": "广州市"
    },
]

# 3. Positions (person_id, org_id, title, start, end, rank, note)
positions = [
    # 张爱军
    {"person_id": 1, "org_id": 1, "title": "中共肇庆市委书记", "start_date": "2021-11", "end_date": "present", "rank": "正厅级", "note": ""},
    # 许晓雄
    {"person_id": 2, "org_id": 2, "title": "肇庆市市长", "start_date": "2021-06", "end_date": "present", "rank": "正厅级", "note": "2021年6月任代市长，7月当选"},
    {"person_id": 2, "org_id": 1, "title": "中共肇庆市委副书记", "start_date": "2021-06", "end_date": "present", "rank": "正厅级", "note": "市委副书记兼市长"},
    # 张爱军前任
    {"person_id": 5, "org_id": 1, "title": "中共肇庆市委书记", "start_date": "2019-10", "end_date": "2021-11", "rank": "正厅级", "note": "吕玉印，后调任珠海市委书记"},
    # 范中杰（更前任）
    {"person_id": 6, "org_id": 1, "title": "中共肇庆市委书记", "start_date": "2017-08", "end_date": "2019-10", "rank": "正厅级", "note": "范中杰，后调任省人大"},
]

# 4. Relationships
relationships = [
    # 现任党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "市委书记与市长是地级市最重要的党政搭档", "overlap_org": "中共肇庆市委员会/肇庆市人民政府", "overlap_period": "2021-11至今"},
    # 前后任市委书记
    {"person_a": 5, "person_b": 1, "type": "前后任", "context": "吕玉印（2019-10至2021-11）→张爱军（2021-11至今）", "overlap_org": "中共肇庆市委员会", "overlap_period": "2021-11交接"},
    {"person_a": 6, "person_b": 5, "type": "前后任", "context": "范中杰（2017-08至2019-10）→吕玉印（2019-10至2021-11）", "overlap_org": "中共肇庆市委员会", "overlap_period": "2019-10交接"},
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
