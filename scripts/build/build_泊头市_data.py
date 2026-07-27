#!/usr/bin/env python3
"""
河北省沧州市泊头市领导班子工作关系网络 — 2026-07-24
research_date: 2026-07-24
sources:
  - botou.gov.cn — 市政府领导介绍 (2025-12-12)
  - botou.gov.cn — 泊头市情概况 (2025-12-23)
confidence: 部分信息经官方来源确认；市委书记任职情况待进一步核实
"""

import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
# DB_PATH = DATABASE_DIR / "泊头市_network.db"
# GEXF_PATH = GRAPH_DIR / "泊头市_network.gexf"

SLUG = "泊头市"

# ── PERSONS ──
persons = [
    # ===== Current leaders (as of 2025-12-12, botou.gov.cn) =====
    {
        "id": 1,
        "name": "张荣霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "泊头市委书记",
        "current_org": "中共泊头市委",
        "source": "botou.gov.cn — 市政府领导介绍 王志亮字段'市委副书记'(2025-12-12); 公开新闻报道（张荣霞2021年任泊头市委书记）",
    },
    {
        "id": 2,
        "name": "王志亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "泊头市委副书记、市长",
        "current_org": "泊头市人民政府",
        "source": "botou.gov.cn — 市政府领导介绍 (2025-12-12)",
    },
    {
        "id": 3,
        "name": "沈军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "泊头市委常委、常务副市长",
        "current_org": "泊头市人民政府",
        "source": "botou.gov.cn — 市政府领导介绍 (2025-12-12)",
    },
    {
        "id": 4,
        "name": "姚晓雨",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "泊头市政府党组成员、副市长",
        "current_org": "泊头市人民政府",
        "source": "botou.gov.cn — 市政府领导介绍 (2025-12-12)",
    },
    {
        "id": 5,
        "name": "田雅男",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "泊头市政府党组成员、副市长",
        "current_org": "泊头市人民政府",
        "source": "botou.gov.cn — 市政府领导介绍 (2025-12-12)",
    },
    {
        "id": 6,
        "name": "冯文涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "泊头市政府党组成员、副市长",
        "current_org": "泊头市人民政府",
        "source": "botou.gov.cn — 市政府领导介绍 (2025-12-12)",
    },
    {
        "id": 7,
        "name": "杨涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "泊头市政府党组成员、副市长、公安局局长",
        "current_org": "泊头市人民政府",
        "source": "botou.gov.cn — 市政府领导介绍 (2025-12-12)",
    },
]

# ── ORGANIZATIONS ──
organizations = [
    {"id": 1, "name": "中共泊头市委", "type": "党委", "level": "县级", "parent": "中共沧州市委", "location": "河北省沧州市泊头市"},
    {"id": 2, "name": "泊头市人民政府", "type": "政府", "level": "县级", "parent": "沧州市人民政府", "location": "河北省沧州市泊头市"},
    {"id": 3, "name": "泊头市公安局", "type": "政府", "level": "科级", "parent": "泊头市人民政府", "location": "河北省沧州市泊头市"},
]

# ── POSITIONS (当前任职) ──
positions = [
    {"person_id": 1, "org_id": 1, "title": "泊头市委书记", "start": "2021(约)", "end": "present", "rank": "正处级", "note": "接任时间待进一步核查"},
    {"person_id": 2, "org_id": 2, "title": "泊头市委副书记、市长", "start": "2025(约)", "end": "present", "rank": "正处级", "note": "主持市政府全面工作，分管审计局"},
    {"person_id": 3, "org_id": 2, "title": "泊头市委常委、常务副市长", "start": "2025(约)", "end": "present", "rank": "副处级", "note": "负责常务工作"},
    {"person_id": 4, "org_id": 2, "title": "泊头市政府党组成员、副市长", "start": "2025(约)", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "泊头市政府党组成员、副市长", "start": "2025(约)", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "泊头市政府党组成员、副市长", "start": "2025(约)", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 3, "title": "泊头市政府党组成员、副市长、公安局局长", "start": "2025(约)", "end": "present", "rank": "副处级", "note": "兼任公安局局长"},
]

# ── RELATIONSHIPS ──
relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "党政主要领导搭档。张荣霞（市委书记）与王志亮（市长）共同负责泊头市全面工作。",
        "overlap_org": "中共泊头市委、泊头市人民政府",
        "overlap_period": "2025-至今",
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "superior_subordinate",
        "context": "沈军作为常务副市长协助王志亮工作，分管市政府常务工作。",
        "overlap_org": "泊头市人民政府",
        "overlap_period": "2025-至今",
    },
    {
        "person_a": 2, "person_b": 4,
        "type": "overlap",
        "context": "姚晓雨作为副市长在王志亮领导下开展工作。",
        "overlap_org": "泊头市人民政府",
        "overlap_period": "2025-至今",
    },
    {
        "person_a": 2, "person_b": 5,
        "type": "overlap",
        "context": "田雅男作为副市长在王志亮领导下开展工作。",
        "overlap_org": "泊头市人民政府",
        "overlap_period": "2025-至今",
    },
    {
        "person_a": 2, "person_b": 6,
        "type": "overlap",
        "context": "冯文涛作为副市长在王志亮领导下开展工作。",
        "overlap_org": "泊头市人民政府",
        "overlap_period": "2025-至今",
    },
    {
        "person_a": 2, "person_b": 7,
        "type": "overlap",
        "context": "杨涛作为副市长兼公安局局长在王志亮领导下开展工作。",
        "overlap_org": "泊头市人民政府",
        "overlap_period": "2025-至今",
    },
]

# ── RUN ──
if __name__ == "__main__":
    db_path = DATABASE_DIR / "泊头市_network.db"
    gexf_path = GRAPH_DIR / "泊头市_network.gexf"

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
    )
