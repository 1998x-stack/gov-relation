#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 临河区 leadership network.

临河区, 巴彦淖尔市, 内蒙古自治区
Research date: 2026-07-25
"""

import sqlite3  # noqa: F401 — used by process_tmp.py for validation

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from pathlib import Path

BASE = Path(__file__).resolve().parent
SLUG = "临河区"
DB_PATH = BASE / f"{SLUG}_network.db"
GEXF_PATH = BASE / f"{SLUG}_network.gexf"

AS_OF = "2026-07-25"

# ── PERSONS ──────────────────────────────────────────────────────────
# Confidence: confirmed = official source / appointment notice
#             plausible = credible media with partial corroboration
#             unverified = lead without enough evidence

persons = [
    # ════ Current Leaders ════
    {
        "id": 1,
        "name": "赵峻岭",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "临河区委书记",
        "current_org": "中国共产党巴彦淖尔市临河区委员会",
        "source": "http://www.linhe.gov.cn (2026-07 区委常委会会议报道)",
        "notes": "confirmed: 2026年7月以临河区委书记身份公开出席活动（区委常委会主持、防汛督导）",
    },
    {
        "id": 2,
        "name": "安文哲",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "临河区区长",
        "current_org": "临河区人民政府",
        "source": "http://www.linhe.gov.cn (2026-07 招商引资报道)",
        "notes": "confirmed: 2026年7月以临河区长身份赴北京市招商引资",
    },
    {
        "id": 3,
        "name": "袁忠利",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "临河区委常委、副区长",
        "current_org": "临河区人民政府",
        "source": "http://www.linhe.gov.cn (2026-07-23 政银企对接会报道)",
        "notes": "confirmed: 2026年7月以区委常委、副区长身份出席政银企对接会",
    },
]

# ── ORGANIZATIONS ────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中国共产党巴彦淖尔市临河区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中国共产党巴彦淖尔市委员会",
        "location": "内蒙古自治区巴彦淖尔市临河区",
    },
    {
        "id": 2,
        "name": "临河区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "巴彦淖尔市人民政府",
        "location": "内蒙古自治区巴彦淖尔市临河区",
    },
    {
        "id": 3,
        "name": "临河区纪委监委",
        "type": "纪律检查",
        "level": "县处级",
        "parent": "巴彦淖尔市纪委监委",
        "location": "内蒙古自治区巴彦淖尔市临河区",
    },
    {
        "id": 4,
        "name": "临河区委组织部",
        "type": "党委部门",
        "level": "乡科级",
        "parent": "临河区委",
        "location": "内蒙古自治区巴彦淖尔市临河区",
    },
    {
        "id": 5,
        "name": "临河区委宣传部",
        "type": "党委部门",
        "level": "乡科级",
        "parent": "临河区委",
        "location": "内蒙古自治区巴彦淖尔市临河区",
    },
    {
        "id": 6,
        "name": "临河区委政法委",
        "type": "党委部门",
        "level": "乡科级",
        "parent": "临河区委",
        "location": "内蒙古自治区巴彦淖尔市临河区",
    },
]

# ── POSITIONS ────────────────────────────────────────────────────────

positions = [
    # Current leadership positions
    {"person_id": 1, "org_id": 1, "title": "临河区委书记", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "临河区区长", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "临河区委常委、副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": ""},
]

# ── RELATIONSHIPS ────────────────────────────────────────────────────
# All relationships inferred from confirmed co-presence in same leadership team

relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "区委书记—区长搭档",
        "overlap_org": "临河区党政领导班子",
        "overlap_period": "至2026年7月现任",
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "overlap",
        "context": "区委书记—区委常委",
        "overlap_org": "临河区委常委会",
        "overlap_period": "至2026年7月现任",
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "overlap",
        "context": "区长—副区长",
        "overlap_org": "临河区人民政府",
        "overlap_period": "至2026年7月现任",
    },
]

# ── BUILD ────────────────────────────────────────────────────────────

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
    print(f"Done. DB: {DB_PATH}, GEXF: {GEXF_PATH}")
