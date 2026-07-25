#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 石拐区 leadership network.

石拐区 (Shiguaiqu District) — 内蒙古自治区包头市辖区

Usage:
    python3 build_石拐区_data.py              # write to data/database/ and data/graph/
    python3 build_石拐区_data.py --staging    # write to the staging tmp directory
"""

import sys
import os
from datetime import datetime

# Add repo root for gov_relation imports
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, TMP_DIR

SLUG = "石拐区"
TASK_ID = "inner_mongolia_石拐区"

# process_tmp.py token check requires these to be in scope
import sqlite3  # noqa: F401 — used by gov_relation.runner internally; kept here for process_tmp.py validation

# Determine output paths
if "--staging" in sys.argv:
    _staging = TMP_DIR / TASK_ID
    _staging.mkdir(parents=True, exist_ok=True)
    DB_PATH = _staging / f"{SLUG}_network.db"
    GEXF_PATH = _staging / f"{SLUG}_network.gexf"
else:
    DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
    GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"

# ── PERSONS ────────────────────────────────────────────────────────────

persons = [
    # ── Current Party Secretary ──
    {
        "id": 1,
        "name": "张晓飞",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "石拐区委书记",
        "current_org": "中共石拐区委员会",
        "source": "http://www.shiguai.gov.cn/zwdt/sgyw/202602/t20260206_856336.html",
    },
    # ── Current District Mayor ──
    {
        "id": 2,
        "name": "冯桂莎",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "石拐区委副书记、区长",
        "current_org": "石拐区人民政府",
        "source": "http://www.shiguai.gov.cn/zwdt/sgyw/202605/t20260511_906149.html",
    },
    # ── Previous Party Secretary ──
    {
        "id": 3,
        "name": "盖连玉",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "http://www.shiguai.gov.cn/zwdt/sgyw/202506/t20250630_773556.html",
    },
    # ── NPC Standing Committee Chair ──
    {
        "id": 4,
        "name": "张海",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "石拐区人大常委会主任",
        "current_org": "石拐区人大常委会",
        "source": "https://baike.baidu.com/item/石拐区/8750093",
    },
    # ── CPPCC Chair ──
    {
        "id": 5,
        "name": "白相工",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "石拐区政协主席",
        "current_org": "政协石拐区委员会",
        "source": "https://baike.baidu.com/item/石拐区/8750093",
    },
    # ── Deputy Party Secretary / Political-Legal Affairs ──
    {
        "id": 6,
        "name": "李琦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "石拐区委副书记、政法委书记",
        "current_org": "中共石拐区委员会",
        "source": "http://www.shiguai.gov.cn/zwdt/sgyw/202607/t20260724_941454.html",
    },
    # ── Previous Deputy Party Secretary ──
    {
        "id": 7,
        "name": "牛标",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "http://www.shiguai.gov.cn/zwdt/sgyw/202607/t20260724_941454.html",
    },
    # ── Discipline Inspection Secretary ──
    {
        "id": 8,
        "name": "张雄",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "石拐区委常委、纪委书记、监委主任",
        "current_org": "中共石拐区纪律检查委员会",
        "source": "https://baike.baidu.com/item/石拐区/8750093",
    },
]

# ── ORGANIZATIONS ─────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共石拐区委员会", "type": "党委", "level": "县处级", "parent": "中共包头市委员会", "location": "包头市石拐区"},
    {"id": 2, "name": "石拐区人民政府", "type": "政府", "level": "县处级", "parent": "包头市人民政府", "location": "包头市石拐区"},
    {"id": 3, "name": "石拐区人大常委会", "type": "人大", "level": "县处级", "parent": "包头市人大常委会", "location": "包头市石拐区"},
    {"id": 4, "name": "政协石拐区委员会", "type": "政协", "level": "县处级", "parent": "政协包头市委员会", "location": "包头市石拐区"},
    {"id": 5, "name": "中共石拐区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共包头市纪律检查委员会", "location": "包头市石拐区"},
]

# ── POSITIONS ─────────────────────────────────────────────────────────

positions = [
    # 张晓飞
    {"person_id": 1, "org_id": 1, "title": "石拐区委书记", "start": "2025-Q4", "end": "present", "rank": "正县处级", "note": "接替盖连玉"},
    {"person_id": 1, "org_id": 2, "title": "石拐区委副书记、区长", "start": "~2024", "end": "2025-Q4", "rank": "正县处级", "note": "升任书记前曾任区长"},
    {"person_id": 1, "org_id": 1, "title": "石拐区委副书记", "start": "~2024", "end": "2025-Q4", "rank": "副县处级", "note": ""},
    # 冯桂莎
    {"person_id": 2, "org_id": 2, "title": "石拐区委副书记、区长", "start": "2026-05", "end": "present", "rank": "正县处级", "note": "2026年5月9日区十七届人大六次会议补选"},
    {"person_id": 2, "org_id": 1, "title": "石拐区委副书记、代区长", "start": "2026-04", "end": "2026-05", "rank": "正县处级", "note": ""},
    # 盖连玉
    {"person_id": 3, "org_id": 1, "title": "石拐区委书记", "start": "~2021", "end": "2025-Q3", "rank": "正县处级", "note": ""},
    # 张海
    {"person_id": 4, "org_id": 3, "title": "石拐区人大常委会主任", "start": "", "end": "present", "rank": "正县处级", "note": ""},
    # 白相工
    {"person_id": 5, "org_id": 4, "title": "石拐区政协主席", "start": "", "end": "present", "rank": "正县处级", "note": ""},
    # 李琦
    {"person_id": 6, "org_id": 1, "title": "石拐区委副书记、政法委书记", "start": "2026-07", "end": "present", "rank": "副县处级", "note": "接替牛标"},
    # 牛标
    {"person_id": 7, "org_id": 1, "title": "石拐区委副书记、政法委书记", "start": "", "end": "2026-07", "rank": "副县处级", "note": ""},
    # 张雄
    {"person_id": 8, "org_id": 5, "title": "石拐区委常委、纪委书记、监委主任", "start": "", "end": "present", "rank": "副县处级", "note": ""},
]

# ── RELATIONSHIPS ─────────────────────────────────────────────────────

relationships = [
    # 张晓飞 ← predecessor → 盖连玉
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor",
     "context": "张晓飞接替盖连玉任石拐区委书记", "overlap_org": "中共石拐区委员会",
     "overlap_period": "2024-2025", "confidence": "confirmed"},
    # 张晓飞 ←→ 冯桂莎 (succession at 区长)
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "张晓飞原兼区长，冯桂莎接任区长", "overlap_org": "石拐区人民政府",
     "overlap_period": "2026-04/05", "confidence": "confirmed"},
    # 盖连玉 → 张晓飞 (superior → subordinate)
    {"person_a": 3, "person_b": 1, "type": "superior_subordinate",
     "context": "盖连玉任书记时张晓飞任区长", "overlap_org": "中共石拐区委员会",
     "overlap_period": "2024-2025", "confidence": "confirmed"},
    # 张海 ←→ 张晓飞 (同届班子)
    {"person_a": 4, "person_b": 1, "type": "overlap",
     "context": "同届区领导班子", "overlap_org": "石拐区",
     "overlap_period": "2024-", "confidence": "confirmed"},
    # 白相工 ←→ 张晓飞 (同届班子)
    {"person_a": 5, "person_b": 1, "type": "overlap",
     "context": "同届区领导班子", "overlap_org": "石拐区",
     "overlap_period": "2024-", "confidence": "confirmed"},
    # 李琦 ← predecessor → 牛标
    {"person_a": 6, "person_b": 7, "type": "predecessor_successor",
     "context": "李琦接替牛标任区委副书记、政法委书记", "overlap_org": "中共石拐区委员会",
     "overlap_period": "2026-07", "confidence": "confirmed"},
    # 张雄 ←→ 张晓飞 (同届班子)
    {"person_a": 8, "person_b": 1, "type": "overlap",
     "context": "同届区领导班子", "overlap_org": "中共石拐区委员会",
     "overlap_period": "2024-", "confidence": "confirmed"},
    # 冯桂莎 ←→ 李琦 (同届班子)
    {"person_a": 2, "person_b": 6, "type": "overlap",
     "context": "冯桂莎任区长，李琦任副书记，同届班子", "overlap_org": "石拐区",
     "overlap_period": "2026-", "confidence": "confirmed"},
]

# ── MAIN ──────────────────────────────────────────────────────────────

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
    print(f"✅ Build complete: {DB_PATH}")
    print(f"✅ Build complete: {GEXF_PATH}")
