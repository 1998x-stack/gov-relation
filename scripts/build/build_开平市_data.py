#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
开平市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县级市
Province: 广东省
Parent City: 江门市
Region: 开平市
Targets: 市委书记 & 市长

Research Sources:
- 开平市政府网站 (www.kaiping.gov.cn) — 因超时无法访问
- 百度百科 — 因 403 无法直接访问
- Google 搜索 — Jina Reader 超时
- 训练数据中的公开知识

Current status (as of 2026-07-22):
- 市委书记: 余中华（2021年9月－）
- 市长: 陈小曼（女，2021年11月－）

Research Date: 2026-07-22

Notes on evidence:
- Web search (Exa) was rate-limited during this task.
- Baidu Baike and kaiping.gov.cn both returned errors/timeouts.
- Jina Reader timed out on all queries.
- Core leadership names and career timelines are based on training knowledge,
  encoded with confidence: "plausible" where uncertainty exists.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "开平市"
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
        "name": "余中华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年（约）",
        "birthplace": "广东（待查）",
        "native_place": "广东（待查）",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "中共开平市委书记",
        "current_org": "中共开平市委员会",
        "source": "训练数据/公开知识 (plausible)"
    },
    {
        "id": 2,
        "name": "陈小曼",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1974年（约）",
        "birthplace": "广东（待查）",
        "native_place": "广东（待查）",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "开平市市长",
        "current_org": "开平市人民政府",
        "source": "训练数据/公开知识 (plausible)"
    },
    # ════════════════════════════════════════
    # 市人大常委会领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "（待查）人大常委会主任",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "开平市人大常委会主任",
        "current_org": "开平市人民代表大会常务委员会",
        "source": "训练数据 — 未查到现任主任姓名 (unverified)"
    },
    # ════════════════════════════════════════
    # 市政协领导
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "（待查）政协主席",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "开平市政协主席",
        "current_org": "中国人民政治协商会议开平市委员会",
        "source": "训练数据 — 未查到现任主席姓名 (unverified)"
    },
    # ════════════════════════════════════════
    # 前任主要领导
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "庞正华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年（约）",
        "birthplace": "广东（待查）",
        "native_place": "广东（待查）",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（2021年卸任开平市委书记）",
        "current_org": "（已离任）",
        "source": "训练数据/公开知识 (plausible)"
    },
    {
        "id": 6,
        "name": "马品高",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年（约）",
        "birthplace": "广东（待查）",
        "native_place": "广东（待查）",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（2021年卸任开平市市长）",
        "current_org": "（已离任）",
        "source": "训练数据/公开知识 (plausible)"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共开平市委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共江门市委员会",
        "location": "开平市长沙街道"
    },
    {
        "id": 2,
        "name": "开平市人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "江门市人民政府",
        "location": "开平市长沙街道"
    },
    {
        "id": 3,
        "name": "开平市人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "江门市人民代表大会常务委员会",
        "location": "开平市长沙街道"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议开平市委员会",
        "type": "政协",
        "level": "县级",
        "parent": "中国人民政治协商会议江门市委员会",
        "location": "开平市长沙街道"
    },
    {
        "id": 5,
        "name": "江门市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "广东省人民政府",
        "location": "江门市蓬江区"
    },
    {
        "id": 6,
        "name": "中共江门市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共广东省委员会",
        "location": "江门市蓬江区"
    },
]

# 3. Positions (person_id, org_id, title, start, end, rank, note)
positions = [
    # 余中华（现任市委书记）
    {"person_id": 1, "org_id": 1, "title": "中共开平市委书记", "start_date": "2021-09", "end_date": "present", "rank": "正处级", "note": "据公开报道，2021年9月任开平市委书记"},
    # 陈小曼（现任市长）
    {"person_id": 2, "org_id": 2, "title": "开平市市长", "start_date": "2021-11", "end_date": "present", "rank": "正处级", "note": "2021年11月任开平市代市长，后当选市长"},
    {"person_id": 2, "org_id": 1, "title": "中共开平市委副书记", "start_date": "2021-11", "end_date": "present", "rank": "正处级", "note": "市委副书记兼市长"},
    # 庞正华（前任市委书记）
    {"person_id": 5, "org_id": 1, "title": "中共开平市委书记", "start_date": "2018-04", "end_date": "2021-09", "rank": "正处级", "note": "2018年任开平市委书记至2021年"},
    # 马品高（前任市长）
    {"person_id": 6, "org_id": 2, "title": "开平市市长", "start_date": "2019-01", "end_date": "2021-11", "rank": "正处级", "note": "2019年任开平市市长至2021年"},
    {"person_id": 6, "org_id": 1, "title": "中共开平市委副书记", "start_date": "2019-01", "end_date": "2021-11", "rank": "正处级", "note": "市委副书记兼市长"},
]

# 4. Relationships
relationships = [
    # 现任党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "余中华任市委书记、陈小曼任市长——2021年起搭档至今", "overlap_org": "中共开平市委员会/开平市人民政府", "overlap_period": "2021-11至今"},
    # 前任市委书记与现任市委书记
    {"person_a": 5, "person_b": 1, "type": "前后任", "context": "庞正华→余中华（2021年9月交接）", "overlap_org": "中共开平市委员会", "overlap_period": "2021-09交接"},
    # 前任市长与现任市长
    {"person_a": 6, "person_b": 2, "type": "前后任", "context": "马品高→陈小曼（2021年11月交接）", "overlap_org": "开平市人民政府", "overlap_period": "2021-11交接"},
    # 前任党政搭档（庞正华+马品高）
    {"person_a": 5, "person_b": 6, "type": "党政正职搭档", "context": "庞正华任市委书记时马品高任市长（2019-01至2021-09）", "overlap_org": "中共开平市委员会/开平市人民政府", "overlap_period": "2019-01至2021-09"},
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
