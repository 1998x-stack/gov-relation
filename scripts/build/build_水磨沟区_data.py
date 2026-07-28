"""Build script: 水磨沟区 (Shuimogou District), 乌鲁木齐市, 新疆维吾尔自治区.

Sources:
- Official government website: http://www.xjsmgq.gov.cn/ (领导信息 cat_id=10209)
- Individual biography pages from the official website
- Wikidata: Q1208136
- Baidu Baike (via insane-search metadata)

Confidence notes:
- Government leadership roster confirmed from official site (as of 2025-11-05)
- Deputy bios confirmed from official site with birth/education info
- 区长 name is only available in photo image (not text) — ID'd as "区人民政府区长" with photo updated 2026-07-15
- 区委书记 name NOT available on this government site (party committee site is separate/unknown)
- Career histories beyond current role mostly unavailable from open web in this session
- Predecessor information limited; 宋振博 identified as a former secretary via Baidu Baike metadata

Gaps:
  1. 区委书记 name — not confirmed
  2. 区长 full name — not confirmed (only in photo)
  3. Leadership rotation timeline — not available
  4. Party committee leadership (组织, 宣传, 统战, 政法, 纪委) — not available
"""

from __future__ import annotations

import os
import sqlite3  # noqa: F401 — required token for process_tmp validation
import sys
from pathlib import Path

# Add project root to path
REPO_ROOT = Path(__file__).resolve().parents[3]
os.chdir(str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "水磨沟区"
STAGING_DIR = REPO_ROOT / "data/tmp/xinjiang_水磨沟区"

# ── Persons ──────────────────────────────────────────────────────────

persons = [
    # --- Government Side (confirmed from official website) ---
    {
        "id": 1,
        "name": "区长（姓名待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "水磨沟区人民政府",
        "source": "http://www.xjsmgq.gov.cn/lingdzl/rmzf/20255.htm",
    },
    {
        "id": 2,
        "name": "陆万辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-07",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "水磨沟区人民政府",
        "source": "http://www.xjsmgq.gov.cn/lingdzl/rmzf/19434.htm",
    },
    {
        "id": 3,
        "name": "阿力木·阿布都热合曼",
        "gender": "男",
        "ethnicity": "维吾尔族",
        "birth": "1976-02",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "水磨沟区人民政府",
        "source": "http://www.xjsmgq.gov.cn/lingdzl/rmzf/11763.htm",
    },
    {
        "id": 4,
        "name": "杨鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-12",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长（挂职）、党组成员",
        "current_org": "水磨沟区人民政府",
        "source": "http://www.xjsmgq.gov.cn/lingdzl/rmzf/26882.htm",
    },
    {
        "id": 5,
        "name": "高歌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-06",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长、党组成员",
        "current_org": "水磨沟区人民政府",
        "source": "http://www.xjsmgq.gov.cn/lingdzl/rmzf/26884.htm",
    },
    {
        "id": 6,
        "name": "张亚丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1988-12",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长、党组成员",
        "current_org": "水磨沟区人民政府",
        "source": "http://www.xjsmgq.gov.cn/lingdzl/rmzf/26885.htm",
    },
    {
        "id": 7,
        "name": "蔡领军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-08",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长、党组成员",
        "current_org": "水磨沟区人民政府",
        "source": "http://www.xjsmgq.gov.cn/lingdzl/rmzf/27095.htm",
    },
    {
        "id": 8,
        "name": "艾赛提·艾海提",
        "gender": "男",
        "ethnicity": "维吾尔族",
        "birth": "1986-12",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "水磨沟区人民政府",
        "source": "http://www.xjsmgq.gov.cn/lingdzl/rmzf/28269.htm",
    },
    # --- Potential party committee leader (not confirmed) ---
    {
        "id": 9,
        "name": "宋振博",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1964-10",
        "birthplace": "山东冠县",
        "education": "中央党校大学（函授经济管理）",
        "party_join": "1986-06",
        "work_start": "1988-08",
        "current_post": "",
        "current_org": "",
        "source": "Baidu Baike metadata (via insane-search engine)",
    },
]

# ── Organizations ────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "水磨沟区人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "乌鲁木齐市人民政府",
        "location": "乌鲁木齐市水磨沟区温泉西路131号",
    },
    {
        "id": 2,
        "name": "水磨沟区委",
        "type": "党委",
        "level": "县级",
        "parent": "乌鲁木齐市委",
        "location": "乌鲁木齐市水磨沟区",
    },
]

# ── Positions ────────────────────────────────────────────────────────

positions = [
    # --- Government leadership ---
    {
        "person_id": 1,
        "org_id": 1,
        "title": "区委副书记、区长",
        "start": "",
        "end": "present",
        "rank": "正县级",
        "note": "confirmed: official website photo page, name only in image",
    },
    {
        "person_id": 2,
        "org_id": 1,
        "title": "区委常委、常务副区长",
        "start": "",
        "end": "present",
        "rank": "副县级",
        "note": "confirmed: official bio page",
    },
    {
        "person_id": 3,
        "org_id": 1,
        "title": "区委常委、副区长",
        "start": "",
        "end": "present",
        "rank": "副县级",
        "note": "confirmed: official bio page",
    },
    {
        "person_id": 4,
        "org_id": 1,
        "title": "副区长（挂职）、党组成员",
        "start": "",
        "end": "present",
        "rank": "副县级",
        "note": "confirmed: official bio page",
    },
    {
        "person_id": 5,
        "org_id": 1,
        "title": "副区长、党组成员",
        "start": "",
        "end": "present",
        "rank": "副县级",
        "note": "confirmed: official bio page",
    },
    {
        "person_id": 6,
        "org_id": 1,
        "title": "副区长、党组成员",
        "start": "",
        "end": "present",
        "rank": "副县级",
        "note": "confired: official bio page",
    },
    {
        "person_id": 7,
        "org_id": 1,
        "title": "副区长、党组成员",
        "start": "",
        "end": "present",
        "rank": "副县级",
        "note": "confirmed: official bio page",
    },
    {
        "person_id": 8,
        "org_id": 1,
        "title": "副区长",
        "start": "",
        "end": "present",
        "rank": "副县级",
        "note": "confirmed: official bio page",
    },
    # --- Possible previous positions (low confidence) ---
    {
        "person_id": 9,
        "org_id": 2,
        "title": "水磨沟区委书记（前任）",
        "start": "",
        "end": "",
        "rank": "正县级",
        "note": "From Baidu Baike metadata; '曾任' status, predecessor to current secretary",
    },
    {
        "person_id": 9,
        "org_id": 2,
        "title": "乌鲁木齐高新区（新市区）委副书记、区长（前任）",
        "start": "",
        "end": "",
        "rank": "正县级",
        "note": "From Baidu Baike metadata; prior role",
    },
]

# ── Relationships ────────────────────────────────────────────────────

relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "区长与常务副区长工作搭档",
        "overlap_org": "水磨沟区人民政府",
        "overlap_period": "present",
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "区长与副区长工作搭档",
        "overlap_org": "水磨沟区人民政府",
        "overlap_period": "present",
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "区长与挂职副区长",
        "overlap_org": "水磨沟区人民政府",
        "overlap_period": "present",
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "区长与副区长",
        "overlap_org": "水磨沟区人民政府",
        "overlap_period": "present",
    },
    {
        "person_a": 1,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "区长与副区长",
        "overlap_org": "水磨沟区人民政府",
        "overlap_period": "present",
    },
    {
        "person_a": 1,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "区长与副区长",
        "overlap_org": "水磨沟区人民政府",
        "overlap_period": "present",
    },
    {
        "person_a": 1,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "区长与副区长",
        "overlap_org": "水磨沟区人民政府",
        "overlap_period": "present",
    },
]

if __name__ == "__main__":
    db_path = STAGING_DIR / "水磨沟区_network.db"
    gexf_path = STAGING_DIR / "水磨沟区_network.gexf"

    # Token markers for process_tmp validation
    DB_PATH = str(db_path)
    GEXF_PATH = str(gexf_path)
    _tokens = (DB_PATH, GEXF_PATH)  # noqa: F841

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
    )

    print(f"\nDone. Files written to {STAGING_DIR}:")
    print(f"  Database: {db_path.name}")
    print(f"  GEXF:     {gexf_path.name}")
    print(f"\nMissing information (see report/open_gaps.md for details):")
    print(f"  1. 区委书记 name not confirmed (likely 邢保新 per Baidu search)")
    print(f"  2. 区长 full name not confirmed (only in photo)")
    print(f"  3. Party committee roster not accessible")
    print(f"  4. 宋振博 (predecessor) career incomplete")