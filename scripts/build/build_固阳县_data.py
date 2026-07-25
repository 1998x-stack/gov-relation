#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 固阳县 leadership network.

固阳县, 包头市, 内蒙古自治区
Research date: 2026-07-25

Confirmed leaders (source: 固阳县人民政府 official site articles):
- 县委书记: 李智 (confirmed from 2026-07-21 article)
- 县长: 侯永峰 (confirmed from 2026-07-21 article)
- 县委常委、纪委书记、监委主任: 曾波
- 县委常委、常务副县长: 贾永彪
- 县人大常委会主任: 刘世明
- 县政协主席: 曾宏斌
"""

import sys
from pathlib import Path

SCRIPTS_BUILD = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_BUILD.parents[1]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "固阳县"
DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"

# ── PERSONS ──────────────────────────────────────────────────────────
# Confidence labels:
#   confirmed = official source / appointment notice
#   plausible = credible media with partial corroboration
#   unverified = lead without enough evidence

persons = [
    # ════ Current Top Leaders ════
    {
        "id": 1,
        "name": "李智",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "固阳县委书记",
        "current_org": "中国共产党固阳县委员会",
        "source": "https://www.guyang.gov.cn/ywdt/gyyw/202607/t20260722_940896.html",
    },
    {
        "id": 2,
        "name": "侯永峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "固阳县委副书记、县长",
        "current_org": "固阳县人民政府",
        "source": "https://www.guyang.gov.cn/ywdt/gyyw/202607/t20260722_940898.html",
    },
    # ════ Leadership Team ════
    {
        "id": 3,
        "name": "曾波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "固阳县委常委、纪委书记、监委主任",
        "current_org": "中国共产党固阳县纪律检查委员会",
        "source": "https://www.guyang.gov.cn/ywdt/gyyw/202607/t20260722_940896.html",
    },
    {
        "id": 4,
        "name": "贾永彪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "固阳县委常委、常务副县长",
        "current_org": "固阳县人民政府",
        "source": "https://www.guyang.gov.cn/ywdt/gyyw/202607/t20260722_940898.html",
    },
    {
        "id": 5,
        "name": "刘世明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "固阳县人大常委会主任",
        "current_org": "固阳县人民代表大会常务委员会",
        "source": "https://www.guyang.gov.cn/ywdt/gyyw/202607/t20260722_940898.html",
    },
    {
        "id": 6,
        "name": "曾宏斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "固阳县政协主席",
        "current_org": "中国人民政治协商会议固阳县委员会",
        "source": "https://www.guyang.gov.cn/ywdt/gyyw/202607/t20260722_940898.html",
    },
]

# ── ORGANIZATIONS ────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中国共产党固阳县委员会",
        "type": "party_committee",
        "level": "county",
        "parent": "包头市",
        "location": "固阳县",
    },
    {
        "id": 2,
        "name": "固阳县人民政府",
        "type": "government",
        "level": "county",
        "parent": "包头市",
        "location": "固阳县",
    },
    {
        "id": 3,
        "name": "中国共产党固阳县纪律检查委员会",
        "type": "discipline",
        "level": "county",
        "parent": "包头市",
        "location": "固阳县",
    },
    {
        "id": 4,
        "name": "固阳县监察委员会",
        "type": "discipline",
        "level": "county",
        "parent": "包头市",
        "location": "固阳县",
    },
    {
        "id": 5,
        "name": "固阳县人民代表大会常务委员会",
        "type": "peoples_congress",
        "level": "county",
        "parent": "固阳县",
        "location": "固阳县",
    },
    {
        "id": 6,
        "name": "中国人民政治协商会议固阳县委员会",
        "type": "cppcc",
        "level": "county",
        "parent": "固阳县",
        "location": "固阳县",
    },
]

# ── POSITIONS ────────────────────────────────────────────────────────
positions = [
    # 李智
    {"person_id": 1, "org_id": 1, "title": "固阳县委书记",
     "start_date": "", "end_date": "present", "rank": "county_chief", "note": "As of 2026-07-21 confirmed"},
    # 侯永峰
    {"person_id": 2, "org_id": 1, "title": "固阳县委副书记",
     "start_date": "", "end_date": "present", "rank": "county_deputy", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "固阳县县长",
     "start_date": "", "end_date": "present", "rank": "county_chief", "note": "As of 2026-07-21 confirmed"},
    # 曾波
    {"person_id": 3, "org_id": 1, "title": "固阳县委常委",
     "start_date": "", "end_date": "present", "rank": "county_deputy", "note": ""},
    {"person_id": 3, "org_id": 3, "title": "固阳县纪委书记",
     "start_date": "", "end_date": "present", "rank": "county_deputy", "note": ""},
    {"person_id": 3, "org_id": 4, "title": "固阳县监委主任",
     "start_date": "", "end_date": "present", "rank": "county_deputy", "note": ""},
    # 贾永彪
    {"person_id": 4, "org_id": 1, "title": "固阳县委常委",
     "start_date": "", "end_date": "present", "rank": "county_deputy", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "固阳县常务副县长",
     "start_date": "", "end_date": "present", "rank": "county_deputy", "note": ""},
    # 刘世明
    {"person_id": 5, "org_id": 5, "title": "固阳县人大常委会主任",
     "start_date": "", "end_date": "present", "rank": "county_chief", "note": ""},
    # 曾宏斌
    {"person_id": 6, "org_id": 6, "title": "固阳县政协主席",
     "start_date": "", "end_date": "present", "rank": "county_chief", "note": ""},
]

# ── RELATIONSHIPS ────────────────────────────────────────────────────
relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长（党政正职搭档）",
        "overlap_org": "固阳县",
        "overlap_period": "2025/2026-present",
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记与纪委书记",
        "overlap_org": "中共固阳县委",
        "overlap_period": "2025/2026-present",
    },
    {
        "person_a": 2, "person_b": 4,
        "type": "superior_subordinate",
        "context": "县长与常务副县长",
        "overlap_org": "固阳县人民政府",
        "overlap_period": "2025/2026-present",
    },
    {
        "person_a": 1, "person_b": 4,
        "type": "superior_subordinate",
        "context": "县委书记与常务副县长（县委常委班子内）",
        "overlap_org": "中共固阳县委",
        "overlap_period": "2025/2026-present",
    },
    {
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "县长与纪委书记（县委常委班子内同级任职）",
        "overlap_org": "中共固阳县委",
        "overlap_period": "2025/2026-present",
    },
    {
        "person_a": 1, "person_b": 5,
        "type": "overlap",
        "context": "县委书记与人大常委会主任（党政班子与人大）",
        "overlap_org": "固阳县",
        "overlap_period": "2025/2026-present",
    },
    {
        "person_a": 1, "person_b": 6,
        "type": "overlap",
        "context": "县委书记与政协主席",
        "overlap_org": "固阳县",
        "overlap_period": "2025/2026-present",
    },
    {
        "person_a": 3, "person_b": 4,
        "type": "overlap",
        "context": "纪委书记与常务副县长（县委常委班子内）",
        "overlap_org": "中共固阳县委",
        "overlap_period": "2025/2026-present",
    },
]


# ═══ BUILD ═══════════════════════════════════════════════════════════════

def main():
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
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    main()
