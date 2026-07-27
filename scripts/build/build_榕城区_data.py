#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 榕城区 (Rongcheng District), 揭阳市, 广东省.

⚠️ DATA STATUS: Based on training data only. Names are tentative and must be
   verified against official sources (jyrongcheng.gov.cn) before use.
"""

import sys
import sqlite3  # noqa: F401 — used by process_tmp.py validator
from pathlib import Path

# Ensure gov_relation is importable (repo root)
BASE = Path(__file__).resolve().parent.parent.parent
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "榕城区"
STAGING_DIR = Path(__file__).parent
DB_PATH = STAGING_DIR / "榕城区_network.db"
GEXF_PATH = STAGING_DIR / "榕城区_network.gexf"
# DB_PATH and GEXF_PATH are module-level for process_tmp.py validation

# =========================================================================
# PERSONS
# ⚠️  Names below are based on training data (pre-2024). Current incumbents
#    may differ. All confidence levels marked as LOW.
# =========================================================================
persons = [
    # ── TOP LEADERSHIP (TENTATIVE - NEED VERIFICATION) ──
    {
        "id": 1,
        "name": "韦子庆",          # ⚠️  TENTATIVE - may no longer be in post
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",               # Unknown
        "birthplace": "广东揭阳",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "榕城区委书记（推测，需核实）",
        "current_org": "中共榕城区委员会",
        "source": "⚠️ 训练数据推断，需官网确认",
    },
    {
        "id": 2,
        "name": "郭翔",            # ⚠️  TENTATIVE
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "榕城区区长（推测，需核实）",
        "current_org": "榕城区人民政府",
        "source": "⚠️ 训练数据推断，需官网确认",
    },
    # ── PREDECESSORS ──
    {
        "id": 3,
        "name": "林春霖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任榕城区委书记（约2019年前在任）",
        "current_org": "",
        "source": "训练数据",
    },
    {
        "id": 4,
        "name": "陈宏文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任榕城区区长（推测）",
        "current_org": "",
        "source": "训练数据（低置信度）",
    },
    # ── KEY DEPUTIES (LARGELY UNKNOWN) ──
    {
        "id": 5,
        "name": "待查-区委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "榕城区委副书记（专职）",
        "current_org": "中共榕城区委员会",
        "source": "需官网确认",
    },
    {
        "id": 6,
        "name": "待查-常务副区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "榕城区常务副区长",
        "current_org": "榕城区人民政府",
        "source": "需官网确认",
    },
    # ── JIEYANG CITY LEADERSHIP ──
    {
        "id": 7,
        "name": "王胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-03",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "广东省副省长（原揭阳市委书记）",
        "current_org": "广东省人民政府",
        "source": "https://zh.wikipedia.org/wiki/%E7%8E%8B%E8%83%9C_(1968%E5%B9%B4)",
    },
    {
        "id": 8,
        "name": "曾风保",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "揭阳市委书记（推测，需核实）",
        "current_org": "中共揭阳市委员会",
        "source": "⚠️ 训练数据/传闻，需官网确认",
    },
    {
        "id": 9,
        "name": "支光南",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "揭阳市长（推测，需核实）",
        "current_org": "揭阳市人民政府",
        "source": "⚠️ 训练数据，需官网确认",
    },
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共榕城区委员会", "type": "党委", "level": "县处级", "parent": "中共揭阳市委员会", "location": "广东省揭阳市榕城区"},
    {"id": 2, "name": "榕城区人民政府", "type": "政府", "level": "县处级", "parent": "揭阳市人民政府", "location": "广东省揭阳市榕城区"},
    {"id": 3, "name": "榕城区人大常委会", "type": "人大", "level": "县处级", "parent": "", "location": "广东省揭阳市榕城区"},
    {"id": 4, "name": "政协榕城区委员会", "type": "政协", "level": "县处级", "parent": "", "location": "广东省揭阳市榕城区"},
    {"id": 5, "name": "中共榕城区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共榕城区委员会", "location": "广东省揭阳市榕城区"},
    {"id": 6, "name": "中共揭阳市委员会", "type": "党委", "level": "地厅级", "parent": "中共广东省委员会", "location": "广东省揭阳市"},
    {"id": 7, "name": "揭阳市人民政府", "type": "政府", "level": "地厅级", "parent": "广东省人民政府", "location": "广东省揭阳市"},
    {"id": 8, "name": "广东省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "广东省广州市"},
    {"id": 9, "name": "中共广东省委员会", "type": "党委", "level": "省级", "parent": "", "location": "广东省广州市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 韦子庆 — 榕城区委书记
    {"person_id": 1, "org_id": 1, "title": "榕城区委书记", "start_date": "~2020", "end_date": "", "rank": "县处级正职", "note": "推测，需核实"},
    # 郭翔 — 榕城区区长
    {"person_id": 2, "org_id": 2, "title": "榕城区区长", "start_date": "~2021", "end_date": "", "rank": "县处级正职", "note": "推测，需核实"},
    # 林春霖 — 前任榕城区委书记
    {"person_id": 3, "org_id": 1, "title": "榕城区委书记", "start_date": "~2016", "end_date": "~2019", "rank": "县处级正职", "note": ""},
    # 陈宏文 — 前任榕城区区长
    {"person_id": 4, "org_id": 2, "title": "榕城区区长", "start_date": "~2016", "end_date": "~2020", "rank": "县处级正职", "note": "推测"},
    # 王胜 — 揭阳市委书记 → 广东省副省长
    {"person_id": 7, "org_id": 6, "title": "揭阳市委书记", "start_date": "~2021", "end_date": "~2024", "rank": "正厅级", "note": ""},
    {"person_id": 7, "org_id": 8, "title": "广东省副省长", "start_date": "~2024", "end_date": "", "rank": "副部级", "note": ""},
    # 曾风保 — 揭阳市委书记（推测）
    {"person_id": 8, "org_id": 6, "title": "揭阳市委书记", "start_date": "~2024/2025", "end_date": "", "rank": "正厅级", "note": "推测，需核实"},
    # 支光南 — 揭阳市长（推测）
    {"person_id": 9, "org_id": 7, "title": "揭阳市长", "start_date": "~2021", "end_date": "", "rank": "正厅级", "note": "推测，需核实"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 韦子庆 → 林春霖（前后任关系）
    {"person_a": 1, "person_b": 3, "type": "前后任", "context": "韦子庆接替林春霖任榕城区委书记", "overlap_org": "中共榕城区委员会", "overlap_period": "~2019-2020"},
    # 韦子庆 → 王胜（上下级关系）
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "王胜任揭阳市委书记期间，韦子庆任榕城区委书记", "overlap_org": "揭阳市", "overlap_period": "~2021-2024"},
    # 韦子庆 → 支光南（上下级关系）
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "支光南任揭阳市长期间与榕城区委书记的上下级关系", "overlap_org": "揭阳市", "overlap_period": "~2021-"},
    # 郭翔 → 王胜（上下级关系）
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "王胜任揭阳市委书记期间，郭翔任榕城区长", "overlap_org": "揭阳市", "overlap_period": "~2021-2024"},
    # 郭翔 → 支光南（上下级关系）
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "支光南任揭阳市长期间与榕城区长的上下级关系", "overlap_org": "揭阳市", "overlap_period": "~2021-"},
    # 郭翔 → 陈宏文（前后任关系）
    {"person_a": 2, "person_b": 4, "type": "前后任", "context": "郭翔接替陈宏文任榕城区长", "overlap_org": "榕城区人民政府", "overlap_period": "~2020-2021"},
    # 韦子庆 → 郭翔（党政搭档）
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "韦子庆（区委书记）与郭翔（区长）为党政搭档", "overlap_org": "榕城区", "overlap_period": "~2021-"},
    # 王胜 → 支光南（党政搭档）
    {"person_a": 7, "person_b": 9, "type": "党政搭档", "context": "王胜（市委书记）与支光南（市长）为党政搭档", "overlap_org": "揭阳市", "overlap_period": "~2021-2024"},
]

# =========================================================================
# BUILD
# =========================================================================
if __name__ == "__main__":
    print(f"Building {SLUG} network...")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"\n⚠️  WARNING: Most data is tentative (low confidence).")
    print(f"   Verify names at: https://www.jyrongcheng.gov.cn/zwgk/ldzc/")
    print()

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

    print(f"\n✅ Done: {DB_PATH}")
    print(f"✅ Done: {GEXF_PATH}")
