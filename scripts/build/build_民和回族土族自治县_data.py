#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 民和回族土族自治县 (Minhe Hui and Tu Autonomous County), 海东市, 青海省."""

import sys
import os
import sqlite3
from datetime import datetime

# Add repo root to path
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, BASE)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

TASK_ID = "qinghai_民和回族土族自治县"
TMP = os.path.join(BASE, "data/tmp", TASK_ID)
DB_PATH = os.path.join(TMP, "民和回族土族自治县_network.db")
GEXF_PATH = os.path.join(TMP, "民和回族土族自治县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    {
        "id": 1,
        "name": "朱智泰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "民和回族土族自治县委书记",
        "current_org": "中共民和回族土族自治县委员会",
        "source": "https://www.minhe.gov.cn/html/431/417886.html"
    },
    {
        "id": 2,
        "name": "肖克忠",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "民和回族土族自治县县长",
        "current_org": "民和回族土族自治县人民政府",
        "source": "https://www.minhe.gov.cn/html/431/417874.html"
    },

    # ── Deputy Party Secretary & Key Standing Committee Members ──
    {
        "id": 3,
        "name": "马忠录",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "民和回族土族自治县委副书记",
        "current_org": "中共民和回族土族自治县委员会",
        "source": "https://www.minhe.gov.cn/html/431/417886.html"
    },
    {
        "id": 4,
        "name": "祁东良",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "民和回族土族自治县委常委",
        "current_org": "中共民和回族土族自治县委员会",
        "source": "https://www.minhe.gov.cn/html/431/417886.html"
    },
    {
        "id": 5,
        "name": "杨亚军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "民和回族土族自治县委常委",
        "current_org": "中共民和回族土族自治县委员会",
        "source": "https://www.minhe.gov.cn/html/431/417886.html"
    },
    {
        "id": 6,
        "name": "焦兴龙",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "民和回族土族自治县委常委",
        "current_org": "中共民和回族土族自治县委员会",
        "source": "https://www.minhe.gov.cn/html/431/417886.html"
    },
    {
        "id": 7,
        "name": "杨学明",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "民和回族土族自治县委常委",
        "current_org": "中共民和回族土族自治县委员会",
        "source": "https://www.minhe.gov.cn/html/431/417886.html"
    },
    {
        "id": 8,
        "name": "李菁",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "民和回族土族自治县委常委",
        "current_org": "中共民和回族土族自治县委员会",
        "source": "https://www.minhe.gov.cn/html/431/417886.html"
    },
    {
        "id": 9,
        "name": "汪伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "民和回族土族自治县委常委",
        "current_org": "中共民和回族土族自治县委员会",
        "source": "https://www.minhe.gov.cn/html/431/417886.html"
    },
    {
        "id": 10,
        "name": "宁建盛",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "民和回族土族自治县委常委",
        "current_org": "中共民和回族土族自治县委员会",
        "source": "https://www.minhe.gov.cn/html/431/417886.html"
    },

    # ── Other Key Figures (Presidium members mentioned in news) ──
    {
        "id": 11,
        "name": "李进仓",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（县领导）",
        "current_org": "",
        "source": "https://www.minhe.gov.cn/html/431/417884.html"
    },
    {
        "id": 12,
        "name": "段广恩",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（县领导）",
        "current_org": "",
        "source": "https://www.minhe.gov.cn/html/431/417884.html"
    },
]

organizations = [
    {"id": 1, "name": "中共民和回族土族自治县委员会", "type": "党委",
     "level": "县处级", "parent": "中共海东市委", "location": "青海省海东市民和回族土族自治县"},
    {"id": 2, "name": "民和回族土族自治县人民政府", "type": "政府",
     "level": "县处级", "parent": "海东市人民政府", "location": "青海省海东市民和回族土族自治县"},
    {"id": 3, "name": "民和回族土族自治县人大常委会", "type": "人大",
     "level": "县处级", "parent": "", "location": "青海省海东市民和回族土族自治县"},
    {"id": 4, "name": "政协民和回族土族自治县委员会", "type": "政协",
     "level": "县处级", "parent": "", "location": "青海省海东市民和回族土族自治县"},
    {"id": 5, "name": "中共民和回族土族自治县纪律检查委员会", "type": "党委",
     "level": "县处级", "parent": "中共民和回族土族自治县委员会", "location": "青海省海东市民和回族土族自治县"},
]

positions = [
    # 朱智泰 - 县委书记
    {"person_id": 1, "org_id": 1, "title": "民和回族土族自治县委书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "2026年7月17日中共民和县委十八届一次全体会议当选县委书记，仍在任（截至2026年7月）"},

    # 肖克忠 - 县长
    {"person_id": 2, "org_id": 2, "title": "民和回族土族自治县县长",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "兼任县政府党组书记。2026年7月10日以县长身份主持县政府党组会议"},
    {"person_id": 2, "org_id": 1, "title": "民和回族土族自治县委副书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "2026年7月17日中共民和县委十八届一次全体会议当选县委副书记"},

    # 马忠录 - 县委副书记
    {"person_id": 3, "org_id": 1, "title": "民和回族土族自治县委副书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "2026年7月17日中共民和县委十八届一次全体会议当选县委副书记"},

    # 县委常委
    {"person_id": 4, "org_id": 1, "title": "民和回族土族自治县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "民和回族土族自治县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "民和回族土族自治县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "民和回族土族自治县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "民和回族土族自治县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "民和回族土族自治县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "民和回族土族自治县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},

    # 其他领导
    {"person_id": 11, "org_id": 1, "title": "（县领导）",
     "start_date": "", "end_date": "present", "rank": "县处级",
     "note": "在第十八次党代会主席台就座，具体职务待确认"},
    {"person_id": 12, "org_id": 1, "title": "（县领导）",
     "start_date": "", "end_date": "present", "rank": "县处级",
     "note": "在第十八次党代会主席台就座，具体职务待确认"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "现任县委书记与县长，同一届领导班子党政主要领导搭档",
     "overlap_org": "中共民和回族土族自治县委员会/民和回族土族自治县人民政府",
     "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "朱智泰与马忠录，县委书记与县委副书记",
     "overlap_org": "中共民和回族土族自治县委员会",
     "overlap_period": "2026年至今"},
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "肖克忠与马忠录，同为县委副书记，党政班子搭档",
     "overlap_org": "中共民和回族土族自治县委员会",
     "overlap_period": "2026年至今"},
]

# ── BUILD ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    os.makedirs(TMP, exist_ok=True)
    run_build(
        slug="民和回族土族自治县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"Done. DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
