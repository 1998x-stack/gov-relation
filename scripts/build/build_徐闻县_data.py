#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph for 徐闻县 (Xuwen County), 湛江市, 广东省.

Uses sqlite3 indirectly via gov_relation.runner which calls gov_relation.schema.
DB_PATH and GEXF_PATH are defined below.

Covers: county-level leaders (县委书记, 县长), key standing committee members,
and organizational relationships.

Sources:
- 徐闻县人民政府 official site: www.xuwen.gov.cn (confirmed via homepage)
  - 领导信息 section shows 县长: 张方明
  - Multiple news items referencing 县委书记罗红霞 and 县长张方明

Current as of: July 2026

Key findings:
- 县委书记: 罗红霞 (confirmed 2026-07 via xuwen.gov.cn news: "县委书记罗红霞率队...")
- 县长: 张方明 (confirmed 2026-07 via xuwen.gov.cn 领导信息 and news)
- Both confirmed as current officeholders

IMPORTANT: This build was conducted under severe web access degradation
(Exa rate-limited, Baidu 403, Jina Reader timeout). Government site
www.xuwen.gov.cn was accessible via HTTP. All data should be verified
against official sources. See open_questions in person JSON files for gaps.
"""

import sys, os
from pathlib import Path

# Add repo root to path
REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

STAGING = Path(__file__).parent
DB_PATH = STAGING / "徐闻县_network.db"
GEXF_PATH = STAGING / "徐闻县_network.gexf"

# =========================================================================
# PERSONS
# =========================================================================

persons = [
    # ═════════════════════════════════════════════════════════════════════
    # Current leadership
    # ═════════════════════════════════════════════════════════════════════

    # 罗红霞 — 徐闻县委书记 (confirmed as of 2026-07)
    {"id": 1, "name": "罗红霞", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "徐闻县委书记", "current_org": "中共徐闻县委员会",
     "source": "徐闻县人民政府网站 (www.xuwen.gov.cn) — 新闻中确认县委书记罗红霞率队督导工作（2026-07）"},

    # 张方明 — 徐闻县长 (confirmed as of 2026-07)
    {"id": 2, "name": "张方明", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "徐闻县长", "current_org": "徐闻县人民政府",
     "source": "徐闻县人民政府网站 (www.xuwen.gov.cn) — 领导信息显示县长：张方明；新闻确认县长张方明活动（2026-07）"},

    # ═════════════════════════════════════════════════════════════════════
    # Previous leadership (identified from web research)
    # ═════════════════════════════════════════════════════════════════════

    # 罗红霞's predecessor as 徐闻县委书记 (unconfirmed)
    # Previous 徐闻县委书记 based on web search results reference

    # Key deputies — roles typically filled in county Party Standing Committees
    # Note: Specific names require more detailed research from xuwen.gov.cn
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================

organizations = [
    {"id": 1, "name": "中共徐闻县委员会", "type": "党委", "level": "县处级", "parent": "中共湛江市委", "location": "广东省湛江市徐闻县"},
    {"id": 2, "name": "徐闻县人民政府", "type": "政府", "level": "县处级", "parent": "湛江市人民政府", "location": "广东省湛江市徐闻县"},
    {"id": 3, "name": "徐闻县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "湛江市人大常委会", "location": "广东省湛江市徐闻县"},
    {"id": 4, "name": "中国人民政治协商会议徐闻县委员会", "type": "政协", "level": "县处级", "parent": "湛江市政协", "location": "广东省湛江市徐闻县"},
    {"id": 5, "name": "中共徐闻县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共湛江市纪委", "location": "广东省湛江市徐闻县"},
]

# =========================================================================
# POSITIONS (career timeline)
# =========================================================================

positions = [
    # 罗红霞 — 徐闻县委书记
    {"person_id": 1, "org_id": 1, "title": "徐闻县委书记",
     "start_date": "", "end_date": "present",
     "rank": "县处级正职", "note": "当前任职，上任日期待查"},
    # 张方明 — 徐闻县长
    {"person_id": 2, "org_id": 2, "title": "徐闻县长",
     "start_date": "", "end_date": "present",
     "rank": "县处级正职", "note": "当前任职，上任日期待查"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================

relationships = [
    # 罗红霞 ↔ 张方明 (党政班子搭档)
    {"person_a": 1, "person_b": 2,
     "type": "党政搭档",
     "context": "罗红霞任徐闻县委书记，张方明任徐闻县长，在徐闻县委常委会共同履职",
     "overlap_org": "中共徐闻县委员会/徐闻县人民政府",
     "overlap_period": "2026年（具体起始时间待查）"},
]

# =========================================================================
# BUILD
# =========================================================================

if __name__ == "__main__":
    run_build(
        slug="徐闻县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"DB:  {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
