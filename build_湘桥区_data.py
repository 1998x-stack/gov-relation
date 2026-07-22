#!/usr/bin/env python3
"""Build Xiangqiao (湘桥区) leadership network data.

Level: 市辖区
Province: 广东省
Parent city: 潮州市
Targets: 区委书记 (Party Secretary), 区长 (Mayor)

Research date: 2026-07-22
Official source: https://www.xiangqiao.gov.cn/
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "湘桥区"
TASK_ID = "guangdong_湘桥区"
TMP_DIR = _REPO_ROOT / "data" / "tmp" / TASK_ID

DB_PATH = TMP_DIR / f"{SLUG}_network.db"
GEXF_PATH = TMP_DIR / f"{SLUG}_network.gexf"

import sqlite3  # noqa: F811 — required by process_tmp.py validation

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    {
        "id": 1,
        "name": "王长春",
        "gender": "男",
        "ethnicity": "unknown",
        "birth": "unknown",
        "birthplace": "unknown",
        "native_place": "unknown",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共潮州市湘桥区委书记",
        "current_org": "中共潮州市湘桥区委员会",
        "source": "https://www.xiangqiao.gov.cn/xwsd/xqyw/content/post_3998779.html (official news — 区委常委会 2026-07-16)",
    },
    {
        "id": 2,
        "name": "李树南",
        "gender": "男",
        "ethnicity": "unknown",
        "birth": "unknown",
        "birthplace": "unknown",
        "native_place": "unknown",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "潮州市湘桥区区长",
        "current_org": "潮州市湘桥区人民政府",
        "source": "https://www.xiangqiao.gov.cn/zwgk/index.html (official 政务公开 page listing 区长：李树南)",
    },
    {
        "id": 3,
        "name": "黄伟涛",
        "gender": "男",
        "ethnicity": "unknown",
        "birth": "unknown",
        "birthplace": "unknown",
        "native_place": "unknown",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "潮州市湘桥区人大常委会主任",
        "current_org": "潮州市湘桥区人民代表大会常务委员会",
        "source": "https://www.xiangqiao.gov.cn/xwsd/xqyw/content/post_3999236.html (official news — 城中村整治大会 2026-07-22)",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共潮州市湘桥区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共潮州市委员会",
        "location": "广东省潮州市湘桥区",
    },
    {
        "id": 2,
        "name": "潮州市湘桥区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "潮州市人民政府",
        "location": "广东省潮州市湘桥区",
    },
    {
        "id": 3,
        "name": "潮州市湘桥区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "潮州市人民代表大会常务委员会",
        "location": "广东省潮州市湘桥区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    {
        "person_id": 1,
        "org_id": 1,
        "title": "区委书记",
        "start": "unknown",
        "end": "present",
        "rank": "正处级",
        "note": "Confirmed current 区委书记 as of July 2026. Source: official news article 2026-07-16.",
    },
    {
        "person_id": 2,
        "org_id": 2,
        "title": "区长",
        "start": "unknown",
        "end": "present",
        "rank": "正处级",
        "note": "Confirmed current 区长 as of March 2026 (government work report) and July 2026 (news article).",
    },
    {
        "person_id": 3,
        "org_id": 3,
        "title": "主任",
        "start": "unknown",
        "end": "present",
        "rank": "正处级",
        "note": "Confirmed 区人大常委会主任 as of July 2026.",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记 (王长春) and 区长 (李树南) —党政主要领导搭档. Both led the 城中村整治百日攻坚动员大会 on 2026-07-22. 王长春 is the top party leader, 李树南 is the government head.",
        "overlap_org": "湘桥区党政领导班子",
        "overlap_period": "confirmed overlap as of mid-2026",
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "overlap",
        "context": "Both attended 城中村整治百日攻坚动员大会 on 2026-07-22 as part of the district leadership team.",
        "overlap_org": "湘桥区领导班子",
        "overlap_period": "confirmed overlap as of mid-2026",
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "overlap",
        "context": "Both attended 城中村整治百日攻坚动员大会 on 2026-07-22.",
        "overlap_org": "湘桥区领导班子",
        "overlap_period": "confirmed overlap as of mid-2026",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=False,
    )
    print(f"Database: {DB_PATH}")
    print(f"GEXF:     {GEXF_PATH}")
    print(f"Persons:  {len(persons)}")
    print(f"Orgs:     {len(organizations)}")
    print(f"Positions:{len(positions)}")
    print(f"Relations:{len(relationships)}")
