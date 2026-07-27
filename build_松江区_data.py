#!/usr/bin/env python3
"""松江区领导班子工作关系网络 — 数据构建脚本。

等级: 市辖区(直辖市)
调查日期: 2026-07-25
信息来源:
  - 上海市松江区人民政府网站 (www.songjiang.gov.cn)
  - 松江区融媒体中心官方报道

Confirmed current leaders (2026年7月):
  - 区委书记: 王华杰 (confirmed from government news)
  - 区委副书记、区长: 王靖 (confirmed from government news)
  - 其他区委常委和区领导: 部分依据公开报道，部分标识为待查

Open questions (see open_questions in person JSONs):
  - 王华杰的完整履历
  - 王靖的完整履历
  - 除书记、副书记外的其他区委常委信息
  - 区人大、政协主要领导信息
"""

from __future__ import annotations

import json
import sys
import os
from pathlib import Path
from datetime import datetime

HERE = Path(__file__).resolve().parent

# Find project root
PROJECT_ROOT = HERE
for _ in range(10):
    if (PROJECT_ROOT / "gov_relation").is_dir():
        break
    PROJECT_ROOT = PROJECT_ROOT.parent
else:
    PROJECT_ROOT = HERE.parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import sqlite3  # noqa: used by gov_relation.runner internally
from gov_relation.runner import run_build

# ── Config ────────────────────────────────────────────────────────────────────
SLUG = "松江区"
TODAY = "2026-07-25"

STAGING = HERE
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# Canonical destinations
CANONICAL_DB = PROJECT_ROOT / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = PROJECT_ROOT / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = PROJECT_ROOT / "scripts" / "build" / f"build_{SLUG}_data.py"
CANONICAL_ROOT_BUILD = PROJECT_ROOT / f"build_{SLUG}_data.py"

# ── Research Data Summary ──────────────────────────────────────────────────────
# Confirmed leaders:
# 区委书记: 王华杰 (confirmed from songjiang.gov.cn statistics inspection article, 2026-07-23)
# 区委副书记、区长: 王靖 (confirmed from same article)
#
# The full 区委常委会 roster was not accessible via web fetch (site uses JS/dynamic loading).
# Based on pattern from other Shanghai districts, typical 松江区委常委会 includes:
# 区委书记、区长(副书记)、专职副书记、纪委书记、组织部长、宣传部长、统战部长、
# 政法委书记、常务副区长、人武部政委等。
# These are marked as "unverified" pending access to the leadership page.

# ── Persons ──────────────────────────────────────────────────────────────────
# ID ranges: 1xxx = party, 2xxx = government, 3xxx = congress,
#            4xxx = cppcc, 5xxx = judiciary

persons = [
    # ═══════════════════════════════════════════════════════════════════════
    # 区委领导班子
    # ═══════════════════════════════════════════════════════════════════════
    # 1. 王华杰 — 区委书记
    {
        "id": 1001,
        "name": "王华杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "松江区委书记",
        "current_org": "中共上海市松江区委员会",
        "source": "https://www.songjiang.gov.cn/xwzx/001001/20260724/8f336869-b26e-401a-af3f-381d7107f20f.html",
    },
    # 2. 王靖 — 区委副书记、区长
    {
        "id": 1002,
        "name": "王靖",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "松江区委副书记、区长",
        "current_org": "上海市松江区人民政府",
        "source": "https://www.songjiang.gov.cn/xwzx/001001/20260724/8f336869-b26e-401a-af3f-381d7107f20f.html",
    },
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共上海市松江区委员会",
        "type": "党委",
        "level": "市辖区(直辖市)",
        "parent": "中共上海市委员会",
        "location": "上海市松江区",
    },
    {
        "id": 2,
        "name": "上海市松江区人民政府",
        "type": "政府",
        "level": "市辖区(直辖市)",
        "parent": "上海市人民政府",
        "location": "上海市松江区",
    },
    {
        "id": 3,
        "name": "松江区人民代表大会常务委员会",
        "type": "人大",
        "level": "市辖区(直辖市)",
        "parent": "上海市人民代表大会常务委员会",
        "location": "上海市松江区",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议上海市松江区委员会",
        "type": "政协",
        "level": "市辖区(直辖市)",
        "parent": "中国人民政治协商会议上海市委员会",
        "location": "上海市松江区",
    },
    {
        "id": 5,
        "name": "中共上海市松江区纪律检查委员会",
        "type": "纪委",
        "level": "市辖区(直辖市)",
        "parent": "中共上海市纪律检查委员会",
        "location": "上海市松江区",
    },
    {
        "id": 6,
        "name": "上海市松江区人民法院",
        "type": "司法机关",
        "level": "市辖区(直辖市)",
        "parent": "上海市高级人民法院",
        "location": "上海市松江区",
    },
    {
        "id": 7,
        "name": "上海市松江区人民检察院",
        "type": "司法机关",
        "level": "市辖区(直辖市)",
        "parent": "上海市人民检察院",
        "location": "上海市松江区",
    },
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # Party Committee
    {"person_id": 1001, "org_id": 1, "title": "松江区委书记", "start_date": "", "end_date": "present", "rank": "正局级", "note": "2026年7月在任"},
    {"person_id": 1002, "org_id": 1, "title": "松江区委副书记", "start_date": "", "end_date": "present", "rank": "正局级", "note": "兼任区长"},
    # Government
    {"person_id": 1002, "org_id": 2, "title": "松江区区长", "start_date": "", "end_date": "present", "rank": "正局级", "note": "区政府党组书记"},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # Top leadership partnership
    {"person_a": 1001, "person_b": 1002, "type": "superior_subordinate", "context": "区委书记—区长搭班子", "overlap_org": "松江区", "overlap_period": "present"},
]


def main() -> None:
    print(f"\n{'='*60}")
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 市辖区(直辖市)")
    print(f"  调查日期: {TODAY}")
    print(f"  信息来源: 松江区人民政府网站 (songjiang.gov.cn)")
    print(f"{'='*60}")

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

    # If writing to staging, also refresh canonical copies
    for dst in [CANONICAL_DB, CANONICAL_GEXF]:
        if dst.exists():
            dst.unlink()
    CANONICAL_DB.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_GEXF.parent.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy2(DB_PATH, CANONICAL_DB)
    shutil.copy2(GEXF_PATH, CANONICAL_GEXF)

    print(f"\n{'='*60}")
    print(f"  松江区 数据构建完成")
    print(f"  DB:   {DB_PATH} -> {CANONICAL_DB}")
    print(f"  GEXF: {GEXF_PATH} -> {CANONICAL_GEXF}")
    print(f"  Persons:     {len(persons)}")
    print(f"  Orgs:        {len(organizations)}")
    print(f"  Positions:   {len(positions)}")
    print(f"  Relations:   {len(relationships)}")
    print(f"{'='*60}")
    print(f"  NOTE: This is a partial build with limited roster data.")
    print(f"  Full 区委常委会 roster could not be retrieved from the")
    print(f"  government website (JS-rendered content). Open questions")
    print(f"  are documented in the person JSON files and open_gaps.md.")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
