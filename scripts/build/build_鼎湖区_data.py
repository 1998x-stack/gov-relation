#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
鼎湖区（肇庆市）领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 市辖区
Province: 广东省
Parent City: 肇庆市
Region: 鼎湖区
Targets: 区委书记 & 区长
Task ID: guangdong_鼎湖区

Research Date: 2026-07-22
As-of Date: 2026-07-22

Known leadership (from training data, unverified against current official sources):
- 区委书记: 刘运通
- 区长: 梁健梅

Research Sources:
- www.zhaoqing.gov.cn (肇庆市人民政府 — homepage confirms district is active as of 2026-07-22)
- Training data / pre-training knowledge (labeled plausible)
- www.dinghu.gov.cn (鼎湖区人民政府 — attempted but timed out)

⚠️ Web access was severely restricted during research:
  - Exa rate-limited
  - dinghu.gov.cn HTTPS/HTTP both timed out
  - Wikipedia inaccessible
  - Baidu 403/captcha
  - Jina Reader timed out
Leadership data relies on training knowledge. Verify against official sources before use.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "鼎湖区"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # 区委领导
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "刘运通",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共鼎湖区委书记",
        "current_org": "中共肇庆市鼎湖区委员会",
        "source": "training_data (plausible — unverified against current official page)"
    },
    {
        "id": 2,
        "name": "梁健梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鼎湖区区长",
        "current_org": "肇庆市鼎湖区人民政府",
        "source": "training_data (plausible — unverified against current official page)"
    },
    # ════════════════════════════════════════
    # 区人大常委会领导
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "待查（区人大常委会主任）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鼎湖区人大常委会主任",
        "current_org": "肇庆市鼎湖区人民代表大会常务委员会",
        "source": "待查"
    },
    # ════════════════════════════════════════
    # 区政协领导
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "待查（区政协主席）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "鼎湖区政协主席",
        "current_org": "中国人民政治协商会议肇庆市鼎湖区委员会",
        "source": "待查"
    },
    # ════════════════════════════════════════
    # 前任主要领导
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "陈宇航",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "另有任用（曾任鼎湖区委书记）",
        "current_org": "（已离任）",
        "source": "training_data (plausible — predecessor to 刘运通)"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共肇庆市鼎湖区委员会",
        "type": "党委",
        "level": "正处级",
        "parent": "中共肇庆市委员会",
        "location": "肇庆市鼎湖区"
    },
    {
        "id": 2,
        "name": "肇庆市鼎湖区人民政府",
        "type": "政府",
        "level": "正处级",
        "parent": "肇庆市人民政府",
        "location": "肇庆市鼎湖区"
    },
    {
        "id": 3,
        "name": "肇庆市鼎湖区人民代表大会常务委员会",
        "type": "人大",
        "level": "正处级",
        "parent": "肇庆市人民代表大会常务委员会",
        "location": "肇庆市鼎湖区"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议肇庆市鼎湖区委员会",
        "type": "政协",
        "level": "正处级",
        "parent": "中国人民政治协商会议肇庆市委员会",
        "location": "肇庆市鼎湖区"
    },
    {
        "id": 5,
        "name": "肇庆新区管理委员会",
        "type": "开发区",
        "level": "副厅级/正处级",
        "parent": "肇庆市人民政府",
        "location": "肇庆市鼎湖区"
    },
    {
        "id": 6,
        "name": "中共肇庆市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共广东省委员会",
        "location": "肇庆市端州区"
    },
    {
        "id": 7,
        "name": "肇庆市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "广东省人民政府",
        "location": "肇庆市端州区"
    },
]

# 3. Positions (person_id, org_id, title, start_date, end_date, rank, note)
positions = [
    # 刘运通
    {"person_id": 1, "org_id": 1, "title": "中共鼎湖区委书记", "start_date": "", "end_date": "present", "rank": "正处级/副厅级", "note": "可同时兼任肇庆新区相关职务"},
    # 梁健梅
    {"person_id": 2, "org_id": 2, "title": "鼎湖区区长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "同时兼任区委副书记、区政府党组书记"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 陈宇航（前任区委书记）
    {"person_id": 5, "org_id": 1, "title": "中共鼎湖区委书记", "start_date": "", "end_date": "", "rank": "正处级/副厅级", "note": "前任，具体任期待查"},
]

# 4. Relationships
relationships = [
    # 现任党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "区委书记与区长是市辖区最重要的党政搭档", "overlap_org": "鼎湖区四套班子", "overlap_period": "未知（待确认）", "source": "", "confidence": "plausible"},
    # 前后任区委书记
    {"person_a": 5, "person_b": 1, "type": "前后任", "context": "陈宇航→刘运通（前任区委书记与现任区委书记）", "overlap_org": "中共鼎湖区委员会", "overlap_period": "交接期", "source": "", "confidence": "unverified"},
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
