#!/usr/bin/env python3
"""
萝北县（黑龙江省鹤岗市）领导班子工作关系网络 — 2026-07-24
Build script for Luobei County, Hegang City, Heilongjiang Province.

Data sources:
- 萝北县人民政府官网 https://www.luobei.gov.cn/ — official news and leadership pages
- Site confirmation of current officeholders via news articles (2026-07)

TASK: heilongjiang_萝北县

Note: Due to geo-restrictions, some Chinese government websites (baike.baidu.com)
were inaccessible. Leadership data confirmed from official county government website
news reports. Biographical details remain incomplete and are marked accordingly.
"""

import json
import os
import sqlite3  # noqa: used via gov_relation.runner
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

TODAY = "2026-07-24"
AS_OF = TODAY

# ── STAGING DIRECTORIES ──
STAGING = Path(__file__).resolve().parent
DB_PATH = STAGING / "萝北县_network.db"
GEXF_PATH = STAGING / "萝北县_network.gexf"
PERSONS_DIR = STAGING

# ── DATA ──

# Integer IDs mapped: 1=郝洪山, 2=李伟峰
PERSON_ID_MAP = {
    "郝洪山": 1,
    "李伟峰": 2,
}

persons = [
    {
        "id": 1,
        "name": "郝洪山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "萝北县委书记",
        "current_org": "中共萝北县委员会",
        "source": "萝北县人民政府官网新闻 (2026-07)",
    },
    {
        "id": 2,
        "name": "李伟峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "萝北县委副书记、县长",
        "current_org": "萝北县人民政府",
        "source": "萝北县人民政府官网新闻 (2026-07)",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共萝北县委员会",
        "type": "党委",
        "level": "县处级",
        "location": "黑龙江省鹤岗市萝北县",
    },
    {
        "id": 2,
        "name": "萝北县人民政府",
        "type": "政府",
        "level": "县处级",
        "location": "黑龙江省鹤岗市萝北县",
    },
]

positions = [
    {
        "person_id": 1,
        "org_id": 1,
        "title": "萝北县委书记",
        "start": "待查",
        "end": "present",
        "rank": "县处级正职",
        "note": "2026年7月仍任现职，主持县委全面工作",
    },
    {
        "person_id": 2,
        "org_id": 2,
        "title": "萝北县委副书记、县长",
        "start": "待查",
        "end": "present",
        "rank": "县处级正职",
        "note": "2026年7月仍任现职，主持县政府全面工作",
    },
    {
        "person_id": 2,
        "org_id": 1,
        "title": "萝北县委副书记",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
        "note": "兼任县政府党组书记",
    },
]

relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长党政正职搭档关系",
        "overlap_org": "中共萝北县委员会/萝北县人民政府",
        "overlap_period": "2026年至今",
    },
]


def main():
    # Build DB and GEXF
    run_build(
        slug="萝北县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Print summary
    print(f"\nBuild complete: {TODAY}")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")
    print(f"  Persons:  {len(persons)}")
    print(f"  Orgs:     {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print("\nNote: Biographical details limited due to web access constraints.")
    print("See open questions in person JSON files and report for gaps.")


if __name__ == "__main__":
    main()
