#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 揭东区 (Jiedong District), 揭阳市, 广东省.

⚠️ DATA STATUS: Based on pre-2024 training data and publicly known facts.
   Current incumbents (post-2025) may differ. All uncertain fields marked explicitly.
"""

import sqlite3
import sys
from pathlib import Path

# Ensure gov_relation is importable
# Script is at data/tmp/guangdong_揭东区/build_揭东区_data.py, repo root is parent.parent.parent.parent (4 levels up)
BASE = Path(__file__).resolve().parent.parent.parent.parent
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "揭东区"

# Staging: output to the staging directory; process_tmp.py promotes to canonical paths
STAGING_DIR = Path(__file__).resolve().parent
DB_PATH = STAGING_DIR / "揭东区_network.db"
GEXF_PATH = STAGING_DIR / "揭东区_network.gexf"

# =========================================================================
# PERSONS
# ⚠️  Names based on pre-2024 knowledge. Current incumbents may differ.
# =========================================================================
persons = [
    # ── TOP LEADERSHIP (NEED VERIFICATION) ──
    {
        "id": 1,
        "name": "梁柱华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "揭东区委书记（推测，需核实）",
        "current_org": "中共揭东区委员会",
        "source": "训练数据（低置信度，需官网确认）",
    },
    {
        "id": 2,
        "name": "修文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "揭东区区长（推测，需核实）",
        "current_org": "揭东区人民政府",
        "source": "训练数据（低置信度，需官网确认）",
    },
    # ── PREDECESSORS ──
    {
        "id": 3,
        "name": "方烽",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任揭东区委书记（约2019-2021年在任）",
        "current_org": "",
        "source": "训练数据",
    },
    {
        "id": 4,
        "name": "蔡淡群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任揭东区委书记（约2017-2019年在任）",
        "current_org": "",
        "source": "训练数据",
    },
    {
        "id": 5,
        "name": "许剑芒",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任揭东区区长（推测）",
        "current_org": "",
        "source": "训练数据（低置信度）",
    },
    # ── KEY DEPUTIES (LARGELY UNKNOWN) ──
    {
        "id": 6,
        "name": "待查-区委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "揭东区委副书记（专职）",
        "current_org": "中共揭东区委员会",
        "source": "需官网确认",
    },
    {
        "id": 7,
        "name": "待查-常务副区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "揭东区常务副区长",
        "current_org": "揭东区人民政府",
        "source": "需官网确认",
    },
    # ── JIEYANG CITY LEADERSHIP ──
    {
        "id": 8,
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
        "id": 9,
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
        "source": "训练数据，需官网确认",
    },
    {
        "id": 10,
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
        "source": "训练数据，需官网确认",
    },
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共揭东区委员会", "type": "党委", "level": "县处级", "parent": "中共揭阳市委员会", "location": "广东省揭阳市揭东区"},
    {"id": 2, "name": "揭东区人民政府", "type": "政府", "level": "县处级", "parent": "揭阳市人民政府", "location": "广东省揭阳市揭东区"},
    {"id": 3, "name": "揭东区人大常委会", "type": "人大", "level": "县处级", "parent": "", "location": "广东省揭阳市揭东区"},
    {"id": 4, "name": "政协揭东区委员会", "type": "政协", "level": "县处级", "parent": "", "location": "广东省揭阳市揭东区"},
    {"id": 5, "name": "中共揭东区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共揭东区委员会", "location": "广东省揭阳市揭东区"},
    {"id": 6, "name": "中共揭阳市委员会", "type": "党委", "level": "地厅级", "parent": "中共广东省委员会", "location": "广东省揭阳市"},
    {"id": 7, "name": "揭阳市人民政府", "type": "政府", "level": "地厅级", "parent": "广东省人民政府", "location": "广东省揭阳市"},
    {"id": 8, "name": "广东省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "广东省广州市"},
    {"id": 9, "name": "中共广东省委员会", "type": "党委", "level": "省级", "parent": "", "location": "广东省广州市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 梁柱华 — 揭东区委书记
    {"person_id": 1, "org_id": 1, "title": "揭东区委书记", "start": "~2021", "end": "", "rank": "县处级正职", "note": "推测，需核实"},
    # 修文 — 揭东区区长
    {"person_id": 2, "org_id": 2, "title": "揭东区区长", "start": "~2021", "end": "", "rank": "县处级正职", "note": "推测，需核实"},
    # 方烽 — 前任揭东区委书记
    {"person_id": 3, "org_id": 1, "title": "揭东区委书记", "start": "~2019", "end": "~2021", "rank": "县处级正职", "note": ""},
    # 蔡淡群 — 前任揭东区委书记
    {"person_id": 4, "org_id": 1, "title": "揭东区委书记", "start": "~2017", "end": "~2019", "rank": "县处级正职", "note": ""},
    # 许剑芒 — 前任揭东区区长
    {"person_id": 5, "org_id": 2, "title": "揭东区区长", "start": "~2019", "end": "~2021", "rank": "县处级正职", "note": "推测"},
    # 王胜 — 揭阳市委书记 → 广东省副省长
    {"person_id": 8, "org_id": 6, "title": "揭阳市委书记", "start": "~2021", "end": "~2024", "rank": "正厅级", "note": ""},
    {"person_id": 8, "org_id": 8, "title": "广东省副省长", "start": "~2024", "end": "", "rank": "副部级", "note": ""},
    # 曾风保 — 揭阳市委书记（推测）
    {"person_id": 9, "org_id": 6, "title": "揭阳市委书记", "start": "~2024", "end": "", "rank": "正厅级", "note": "推测，需核实"},
    # 支光南 — 揭阳市长（推测）
    {"person_id": 10, "org_id": 7, "title": "揭阳市长", "start": "~2021", "end": "", "rank": "正厅级", "note": "推测，需核实"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 梁柱华 → 方烽（前后任关系）
    {"person_a": 1, "person_b": 3, "type": "前后任", "context": "梁柱华接替方烽任揭东区委书记", "overlap_org": "中共揭东区委员会", "overlap_period": "~2021"},
    # 方烽 → 蔡淡群（前后任关系）
    {"person_a": 3, "person_b": 4, "type": "前后任", "context": "方烽接替蔡淡群任揭东区委书记", "overlap_org": "中共揭东区委员会", "overlap_period": "~2019"},
    # 梁柱华 → 修文（党政搭档）
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "梁柱华（区委书记）与修文（区长）为党政搭档", "overlap_org": "揭东区", "overlap_period": "~2021-"},
    # 修文 → 许剑芒（前后任关系）
    {"person_a": 2, "person_b": 5, "type": "前后任", "context": "修文接替许剑芒任揭东区区长", "overlap_org": "揭东区人民政府", "overlap_period": "~2021"},
    # 梁柱华 → 王胜（上下级关系）
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "王胜任揭阳市委书记期间，梁柱华任揭东区委书记", "overlap_org": "揭阳市", "overlap_period": "~2021-2024"},
    # 修文 → 王胜（上下级关系）
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "王胜任揭阳市委书记期间，修文任揭东区区长", "overlap_org": "揭阳市", "overlap_period": "~2021-2024"},
    # 梁柱华 → 支光南（上下级关系）
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "支光南任揭阳市长期间与揭东区委书记的上下级关系", "overlap_org": "揭阳市", "overlap_period": "~2021-"},
    # 修文 → 支光南（上下级关系）
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "支光南任揭阳市长期间与揭东区区长的上下级关系", "overlap_org": "揭阳市", "overlap_period": "~2021-"},
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
    print(f"   Verify names at: https://www.jiedong.gov.cn/zwgk/ldzc/")
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
