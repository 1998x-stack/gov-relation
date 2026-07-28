#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 文成县 leadership network.

Data source: www.wencheng.gov.cn (official government website)
Information currency: 2026-07-28 (current as of July 2026)

Confirmed leaders:
   县委书记: 罗招政
   县长: 杨德听
   县领导 (partially identified from news): 刘金红, 郑文东, 张呈念, 吴可塑, 郑宁
"""
import sqlite3  # noqa: F401 — used by gov_relation.runner; token for process_tmp.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "文成县"
SCRIPT_DIR = Path(__file__).resolve().parent
DB_PATH = SCRIPT_DIR / f"{SLUG}_network.db"
GEXF_PATH = SCRIPT_DIR / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────
persons = [
    # === 县委主要领导 ===
    {
        "id": 1, "name": "罗招政", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "文成县委书记",
        "current_org": "中共文成县委员会",
        "source": "http://www.wencheng.gov.cn/",
    },
    {
        "id": 2, "name": "杨德听", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "文成县委副书记、县长",
        "current_org": "文成县人民政府",
        "source": "http://www.wencheng.gov.cn/",
    },
    # === 其他县领导(从新闻报道中确认) ===
    {
        "id": 3, "name": "刘金红", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "文成县领导",
        "current_org": "文成县",
        "source": "http://www.wencheng.gov.cn/",
    },
    {
        "id": 4, "name": "郑文东", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "文成县领导",
        "current_org": "文成县",
        "source": "http://www.wencheng.gov.cn/",
    },
    {
        "id": 5, "name": "张呈念", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "文成县领导",
        "current_org": "文成县",
        "source": "http://www.wencheng.gov.cn/",
    },
    {
        "id": 6, "name": "吴可塑", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "文成县副县长",
        "current_org": "文成县人民政府",
        "source": "http://www.wencheng.gov.cn/",
    },
    {
        "id": 7, "name": "郑宁", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "文成县副县长",
        "current_org": "文成县人民政府",
        "source": "http://www.wencheng.gov.cn/",
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1, "name": "中共文成县委员会", "type": "党委",
        "level": "县级", "parent": "温州市", "location": "文成县",
    },
    {
        "id": 2, "name": "文成县人民政府", "type": "政府",
        "level": "县级", "parent": "温州市", "location": "文成县",
    },
    {
        "id": 3, "name": "文成县", "type": "政府",
        "level": "县级", "parent": "温州市", "location": "文成县",
    },
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 罗招政
    {"person_id": 1, "org_id": 1, "title": "文成县委书记", "start": "", "end": "至今", "rank": "正处级", "note": "现任"},
    # 杨德听
    {"person_id": 2, "org_id": 2, "title": "文成县县长", "start": "", "end": "至今", "rank": "正处级", "note": "现任；县委副书记"},
    {"person_id": 2, "org_id": 1, "title": "文成县委副书记", "start": "", "end": "至今", "rank": "副处级", "note": "现任"},
    # 刘金红
    {"person_id": 3, "org_id": 3, "title": "文成县领导", "start": "", "end": "至今", "rank": "", "note": "现任"},
    # 郑文东
    {"person_id": 4, "org_id": 3, "title": "文成县领导", "start": "", "end": "至今", "rank": "", "note": "现任"},
    # 张呈念
    {"person_id": 5, "org_id": 3, "title": "文成县领导", "start": "", "end": "至今", "rank": "", "note": "现任"},
    # 吴可塑
    {"person_id": 6, "org_id": 2, "title": "文成县副县长", "start": "", "end": "至今", "rank": "副处级", "note": "现任"},
    # 郑宁
    {"person_id": 7, "org_id": 2, "title": "文成县副县长", "start": "", "end": "至今", "rank": "副处级", "note": "现任"},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长工作搭档",
        "overlap_org": "文成县委/县政府",
        "overlap_period": "至今",
        #  confirmed from multiple news articles showing them together
    },
]

# ── Run Build ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    db_path = DB_PATH
    gexf_path = GEXF_PATH

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
    )

    print(f"\n✅ Build complete.")
    print(f"   DB:   {db_path}")
    print(f"   GEXF: {gexf_path}")