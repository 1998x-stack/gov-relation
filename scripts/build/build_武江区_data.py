#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 武江区 (Wujiang District, 韶关市, 广东省) leadership network."""

import sqlite3
import sys
import os
from datetime import datetime
from pathlib import Path

# Get staging directory (this file's directory)
STAGING_DIR = Path(__file__).parent.resolve()

# Add repo root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))

from gov_relation.runner import run_build

SLUG = "武江区"
NOW = "2026-07-22"

# Output paths: write to staging directory
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

# ── PERSONS ────────────────────────────────────────────────────────────

persons = [
    # ── Current leadership ──
    {
        "id": 1,
        "name": "张广晖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "武江区委书记",
        "current_org": "中共韶关市武江区委员会",
        "source": "http://www.sgwjq.gov.cn/",
    },
    {
        "id": 2,
        "name": "谢佳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "武江区委副书记、区长",
        "current_org": "武江区人民政府",
        "source": "http://www.sgwjq.gov.cn/",
    },
    # ── District People's Congress (人大) ──
    {
        "id": 3,
        "name": "孙理鸣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "武江区人大常委会主任",
        "current_org": "武江区人民代表大会常务委员会",
        "source": "http://www.sgwjq.gov.cn/zwgk/ghjh/content/post_2807428.html",
    },
    # ── District Political Consultative Conference (政协) ──
    {
        "id": 4,
        "name": "彭波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "武江区政协主席",
        "current_org": "中国人民政治协商会议韶关市武江区委员会",
        "source": "http://www.sgwjq.gov.cn/zwgk/ghjh/content/post_2807428.html",
    },
    # ── Vice District Mayors (副区长) ──
    {
        "id": 5,
        "name": "刘喆焱",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "武江区副区长",
        "current_org": "武江区人民政府",
        "source": "http://www.sgwjq.gov.cn/xwzx/ywdt/content/post_2864729.html",
    },
    {
        "id": 6,
        "name": "何丽芳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "武江区副区长",
        "current_org": "武江区人民政府",
        "source": "http://www.sgwjq.gov.cn/xwzx/ywdt/content/post_2864465.html",
    },
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共韶关市武江区委员会", "type": "党委", "level": "县处级", "parent": "中共韶关市委", "location": "韶关市武江区"},
    {"id": 2, "name": "武江区人民政府", "type": "政府", "level": "县处级", "parent": "韶关市人民政府", "location": "韶关市武江区"},
    {"id": 3, "name": "武江区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "韶关市人大常委会", "location": "韶关市武江区"},
    {"id": 4, "name": "中国人民政治协商会议韶关市武江区委员会", "type": "政协", "level": "县处级", "parent": "韶关市政协", "location": "韶关市武江区"},
    {"id": 5, "name": "中共韶关市武江区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共韶关市纪委", "location": "韶关市武江区"},
    {"id": 6, "name": "中共韶关市武江区委组织部", "type": "党委", "level": "县处级", "parent": "中共韶关市武江区委员会", "location": "韶关市武江区"},
    {"id": 7, "name": "武江区工业和信息化局", "type": "政府", "level": "乡科级", "parent": "武江区人民政府", "location": "韶关市武江区"},
]

# ── POSITIONS ──────────────────────────────────────────────────────────

positions = [
    # 张广晖
    {"person_id": 1, "org_id": 1, "title": "武江区委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "confirmed as of 2026-07-22"},
    # 谢佳
    {"person_id": 2, "org_id": 2, "title": "武江区区长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "confirmed as of 2026-07-22"},
    {"person_id": 2, "org_id": 1, "title": "武江区委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "confirmed as of 2026-07-22"},
    # 孙理鸣
    {"person_id": 3, "org_id": 3, "title": "武江区人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "confirmed as of 2025-12-15"},
    # 彭波
    {"person_id": 4, "org_id": 4, "title": "武江区政协主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "confirmed as of 2025-12-15"},
    # 刘喆焱
    {"person_id": 5, "org_id": 2, "title": "武江区副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "confirmed as of 2026-07-22"},
    # 何丽芳
    {"person_id": 6, "org_id": 2, "title": "武江区副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "confirmed as of 2026-07-22"},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────────

relationships = [
    # 张广晖 — 谢佳 (区委书记—区长: top 2 leaders)
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记与区长，武江区党政主要领导",
        "overlap_org": "中共韶关市武江区委员会/武江区人民政府",
        "overlap_period": "至今",
    },
    # 张广晖 — 孙理鸣 (区委书记—人大主任)
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "区委书记与区人大常委会主任，共同出席书记专题会议",
        "overlap_org": "中共韶关市武江区委员会/武江区人大常委会",
        "overlap_period": "至今",
    },
    # 张广晖 — 彭波 (区委书记—政协主席)
    {
        "person_a": 1, "person_b": 4,
        "type": "overlap",
        "context": "区委书记与区政协主席，共同出席书记专题会议",
        "overlap_org": "中共韶关市武江区委员会/武江区政协",
        "overlap_period": "至今",
    },
    # 谢佳 — 刘喆焱 (区长—副区长)
    {
        "person_a": 2, "person_b": 5,
        "type": "superior_subordinate",
        "context": "区长与副区长，共同参加区工信局调研",
        "overlap_org": "武江区人民政府",
        "overlap_period": "至今",
    },
    # 张广晖 — 刘喆焱 (区委书记—副区长)
    {
        "person_a": 1, "person_b": 5,
        "type": "superior_subordinate",
        "context": "区委书记与副区长，共同参加辖区企业调研",
        "overlap_org": "武江区人民政府",
        "overlap_period": "至今",
    },
    # 张广晖 — 何丽芳 (区委书记—副区长)
    {
        "person_a": 1, "person_b": 6,
        "type": "superior_subordinate",
        "context": "区委书记与副区长，共同参加一线调研",
        "overlap_org": "武江区人民政府",
        "overlap_period": "至今",
    },
]

# ── RUN ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
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

    print(f"\nDone at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
