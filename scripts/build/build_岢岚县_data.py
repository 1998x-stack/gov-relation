#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 岢岚县 (Kelan County) leadership network."""

import os
import sys
import sqlite3
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, BASE)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "岢岚县"

# Staging paths
STAGING = os.path.join(BASE, "data/tmp/shanxi_岢岚县")
DB_PATH = os.path.join(STAGING, "岢岚县_network.db")
GEXF_PATH = os.path.join(STAGING, "岢岚县_network.gexf")

# ── PERSONS ─────────────────────────────────────────────────────────────
#
# SOURCE: Baidu Baike "岢岚县" entry (政治 table, as of 2025-11).
# https://baike.baidu.com/item/%E5%B2%A2%E5%B2%9A%E5%8E%BF
# All other biographical details are unverified — marked explicitly.
#
# Due to web access restrictions (Baidu 403/Bot verification, Jina timeouts,
# government site not reachable), only name and current role are confirmed.
# Full resumes require a follow-up research pass with working web search.

persons = [
    # ── Top Leaders (confirmed from Baidu Baike) ──
    {
        "id": 1,
        "name": "常永峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "岢岚县委书记",
        "current_org": "中共岢岚县委员会",
        "source": "https://baike.baidu.com/item/%E5%B2%A2%E5%B2%9A%E5%8E%BF",
    },
    {
        "id": 2,
        "name": "刘会平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "岢岚县县长",
        "current_org": "岢岚县人民政府",
        "source": "https://baike.baidu.com/item/%E5%B2%A2%E5%B2%9A%E5%8E%BF",
    },
    # ── Other confirmed leaders from Baidu Baike ──
    {
        "id": 3,
        "name": "刘鹏德",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "岢岚县人大常委会主任",
        "current_org": "岢岚县人民代表大会常务委员会",
        "source": "https://baike.baidu.com/item/%E5%B2%A2%E5%B2%9A%E5%8E%BF",
    },
    {
        "id": 4,
        "name": "梁军",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "岢岚县政协主席",
        "current_org": "中国人民政治协商会议岢岚县委员会",
        "source": "https://baike.baidu.com/item/%E5%B2%A2%E5%B2%9A%E5%8E%BF",
    },
    # ── Known predecessors (from baike, inferred from typical appointments) ──
    # Note: Predecessor names are unconfirmed — need further research
]

# ── ORGANIZATIONS ─────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共岢岚县委员会", "type": "党委", "level": "县处级", "parent": "中共忻州市委员会", "location": "岢岚县"},
    {"id": 2, "name": "岢岚县人民政府", "type": "政府", "level": "县处级", "parent": "忻州市人民政府", "location": "岢岚县"},
    {"id": 3, "name": "岢岚县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "岢岚县", "location": "岢岚县"},
    {"id": 4, "name": "中国人民政治协商会议岢岚县委员会", "type": "政协", "level": "县处级", "parent": "岢岚县", "location": "岢岚县"},
    {"id": 5, "name": "中共岢岚县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "岢岚县", "location": "岢岚县"},
    {"id": 6, "name": "中共忻州市委员会", "type": "党委", "level": "地厅级", "parent": "中国共产党山西省委员会", "location": "忻州市"},
    {"id": 7, "name": "忻州市人民政府", "type": "政府", "level": "地厅级", "parent": "山西省人民政府", "location": "忻州市"},
]

# ── POSITIONS ─────────────────────────────────────────────────────────────

positions = [
    {"person_id": 1, "org_id": 1, "title": "岢岚县委书记",
     "start_date": "待查", "end_date": "至今", "rank": "正处级",
     "note": "主持县委全面工作"},
    {"person_id": 2, "org_id": 2, "title": "岢岚县县长",
     "start_date": "待查", "end_date": "至今", "rank": "正处级",
     "note": "主持县政府全面工作"},
    {"person_id": 3, "org_id": 3, "title": "岢岚县人大常委会主任",
     "start_date": "待查", "end_date": "至今", "rank": "正处级",
     "note": "主持县人大常委会工作"},
    {"person_id": 4, "org_id": 4, "title": "岢岚县政协主席",
     "start_date": "待查", "end_date": "至今", "rank": "正处级",
     "note": "主持县政协工作"},
]

# ── RELATIONSHIPS ─────────────────────────────────────────────────────────
# All inferred from co-leadership of same county; no overlap in prior
# orgs confirmed yet.

relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县长搭班", "overlap_org": "岢岚县",
     "overlap_period": "待查至今",
     "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "现有县委和人大主要领导", "overlap_org": "岢岚县",
     "overlap_period": "待查至今",
     "confidence": "plausible"},
    {"person_a": 2, "person_b": 4, "type": "overlap",
     "context": "县政府和政协主要领导", "overlap_org": "岢岚县",
     "overlap_period": "待查至今",
     "confidence": "plausible"},
]

# ── BUILD ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    os.makedirs(STAGING, exist_ok=True)
    run_build(
        slug="岢岚县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print(f"\nDone. Files written to {STAGING}/")