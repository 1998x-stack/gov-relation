#!/usr/bin/env python3
"""崇明区领导班子工作关系网络 — 数据构建脚本。

等级: 市辖区(直辖市)
调查日期: 2026-07-25
信息来源:
  - 上海市崇明区人民政府网站 (www.shcm.gov.cn)
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Find project root: walk up looking for gov_relation/
PROJECT_ROOT = HERE
for _ in range(10):
    if (PROJECT_ROOT / "gov_relation").is_dir():
        break
    PROJECT_ROOT = PROJECT_ROOT.parent
else:
    PROJECT_ROOT = HERE.parents[2]  # fallback

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import sqlite3  # noqa: F401 — used downstream via gov_relation.runner
from gov_relation.runner import run_build

# ── Config ────────────────────────────────────────────────────────────────────
SLUG = "崇明区"
TODAY = "2026-07-25"

STAGING = HERE
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# Canonical destinations (always relative to project root)
CANONICAL_DB = PROJECT_ROOT / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = PROJECT_ROOT / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = PROJECT_ROOT / "scripts" / "build" / f"build_{SLUG}_data.py"
CANONICAL_ROOT_BUILD = PROJECT_ROOT / f"build_{SLUG}_data.py"

# ── Persons ──────────────────────────────────────────────────────────────────
# ID ranges: 1xxx = party committee, 2xxx = government, 3xxx = congress,
#            4xxx = cppcc, 5xxx = judiciary

persons = [
    # ═══════════════════════════════════════════════════════════════════════
    # 区委领导班子
    # ═══════════════════════════════════════════════════════════════════════
    # 1. 李峻 — 区委书记
    {
        "id": 1001,
        "name": "李峻",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年12月",
        "birthplace": "",
        "education": "中央党校研究生，文学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "崇明区委书记",
        "current_org": "中共上海市崇明区委员会",
        "source": "https://www.shcm.gov.cn",
    },
    # 2. 吕晨飞 — 区委副书记、区长
    {
        "id": 1002,
        "name": "吕晨飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "崇明区委副书记、区长",
        "current_org": "上海市崇明区人民政府",
        "source": "https://www.shcm.gov.cn",
    },
    # ── 其他区委领导 (待补充详细身份信息) ──
    # 3. 区委副书记（待查）
    # 4. 区纪委书记（待查）
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共上海市崇明区委员会",
        "type": "党委",
        "level": "市辖区(直辖市)",
        "parent": "中共上海市委员会",
        "location": "上海市崇明区",
    },
    {
        "id": 2,
        "name": "上海市崇明区人民政府",
        "type": "政府",
        "level": "市辖区(直辖市)",
        "parent": "上海市人民政府",
        "location": "上海市崇明区",
    },
    {
        "id": 3,
        "name": "崇明区人民代表大会常务委员会",
        "type": "人大",
        "level": "市辖区(直辖市)",
        "parent": "上海市人民代表大会常务委员会",
        "location": "上海市崇明区",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议上海市崇明区委员会",
        "type": "政协",
        "level": "市辖区(直辖市)",
        "parent": "中国人民政治协商会议上海市委员会",
        "location": "上海市崇明区",
    },
    {
        "id": 5,
        "name": "中共上海市崇明区纪律检查委员会",
        "type": "纪委",
        "level": "市辖区(直辖市)",
        "parent": "中共上海市纪律检查委员会",
        "location": "上海市崇明区",
    },
    {
        "id": 6,
        "name": "上海市崇明区人民法院",
        "type": "司法机关",
        "level": "市辖区(直辖市)",
        "parent": "上海市高级人民法院",
        "location": "上海市崇明区",
    },
    {
        "id": 7,
        "name": "上海市崇明区人民检察院",
        "type": "司法机关",
        "level": "市辖区(直辖市)",
        "parent": "上海市人民检察院",
        "location": "上海市崇明区",
    },
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # Party Committee
    {"person_id": 1001, "org_id": 1, "title": "崇明区委书记", "start_date": "2024-12", "end_date": "present", "rank": "正局级", "note": "2026年7月在任"},
    {"person_id": 1002, "org_id": 1, "title": "崇明区委副书记", "start_date": "", "end_date": "present", "rank": "正局级", "note": "兼任区长"},
    # Government
    {"person_id": 1002, "org_id": 2, "title": "崇明区长", "start_date": "", "end_date": "present", "rank": "正局级", "note": "区政府党组书记"},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # Top leadership partnership
    {"person_a": 1001, "person_b": 1002, "type": "superior_subordinate", "context": "区委书记—区长搭班子", "overlap_org": "崇明区", "overlap_period": "present"},
]


def main() -> None:
    print(f"\n{'='*60}")
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 市辖区(直辖市)")
    print(f"  调查日期: {TODAY}")
    print(f"  信息来源: 崇明区人民政府网站 (shcm.gov.cn)")
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
    print(f"  {SLUG} 数据构建完成")
    print(f"  DB:   {DB_PATH} -> {CANONICAL_DB}")
    print(f"  GEXF: {GEXF_PATH} -> {CANONICAL_GEXF}")
    print(f"  Persons:     {len(persons)}")
    print(f"  Orgs:        {len(organizations)}")
    print(f"  Positions:   {len(positions)}")
    print(f"  Relations:   {len(relationships)}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
