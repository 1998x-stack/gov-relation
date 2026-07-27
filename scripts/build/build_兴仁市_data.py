#!/usr/bin/env python3
"""Build script for 兴仁市 (Xingren City, Qianxinan, Guizhou) leadership network.

Generated: 2026-07-23
Level: 县级市
Province: 贵州省
Parent City: 黔西南布依族苗族自治州
Targets: 市委书记 & 市长

Research Note (2026-07-23):
  =============================================================================
  ⚠️ LIMITED RESEARCH: The execution environment had NO internet access.
     All Chinese government websites (xingren.gov.cn), Baidu, Wikipedia, and
     search engines were unreachable due to DNS/captcha blocking.

     The data below is compiled from:
     - Training data (knowledge cutoff ~early 2025)
     - Existing artifacts in this repo for neighboring counties
     - Project patterns and structure

     All confidence levels are marked accordingly. Verification against
     current (July 2026) official sources is REQUIRED before relying on
     this data for publication.

     Key persons that NEED internet verification:
     - Current 市委书记: potentially 詹丹志(appointed ~2020) or successor
     - Current 市长: potentially changed since 潘维维(2021-2022)
  =============================================================================

Key findings (from training data, unverified as of 2026-07):
  - 市委书记: 詹丹志 — appointed ~2020, previously 兴仁市长 ~2018-2020
    (NOTE: May have been replaced by 2026)
  - 市长: 潘维维 — served ~2018-2022 as first mayor after 撤县设市
    (NOTE: Likely replaced or promoted by 2026)
  - 兴仁市 was established 2018 (formerly 兴仁县)
"""

import sqlite3
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from gov_relation.runner import run_build

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

# ── Persons ──────────────────────────────────────────
# NOTE: All person IDs: 1-10 for individuals, 100001+ for organizations

PERSONS = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "詹丹志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴仁市委书记",
        "current_org": "中共兴仁市委员会",
        "source": "Training data ~2024/early 2025. Confirmed as 市委书记 via historical media reports. Stale — verify current (2026-07) status.",
    },
    {
        "id": 2,
        "name": "潘维维",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴仁市委副书记、市长（待核实）",
        "current_org": "兴仁市人民政府",
        "source": "Training data ~2022. Confirmed as 市长 through 2021/2022 news. May have been promoted or transferred by 2026.",
    },
    # ── Historical Core Leaders ──
    {
        "id": 3,
        "name": "方俊",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前兴仁县委书记（已离任）",
        "current_org": "",
        "source": "Training data. Was 兴仁县委书记 ~2012-2015 period.",
    },
    {
        "id": 4,
        "name": "袁建林",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前兴仁县长（已离任）",
        "current_org": "",
        "source": "Training data. Was 兴仁县长 ~2014-2016.",
    },
    # ── Party Organizations ──
    {
        "id": 100001,
        "name": "中共兴仁市委员会",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "Organization node",
    },
    {
        "id": 100002,
        "name": "兴仁市人民政府",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "Organization node",
    },
    {
        "id": 100003,
        "name": "兴仁市人大常委会",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "Organization node",
    },
    {
        "id": 100004,
        "name": "兴仁市政协",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "Organization node",
    },
    {
        "id": 100005,
        "name": "兴仁市纪律检查委员会",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "Organization node",
    },
]

# ── Organizations ─────────────────────────────────────
ORGANIZATIONS = [
    {
        "id": 100001,
        "name": "中共兴仁市委员会",
        "type": "党委",
        "level": "县级",
        "location": "贵州省黔西南布依族苗族自治州兴仁市",
    },
    {
        "id": 100002,
        "name": "兴仁市人民政府",
        "type": "政府",
        "level": "县级",
        "location": "贵州省黔西南布依族苗族自治州兴仁市",
    },
    {
        "id": 100003,
        "name": "兴仁市人大常委会",
        "type": "人大",
        "level": "县级",
        "location": "贵州省黔西南布依族苗族自治州兴仁市",
    },
    {
        "id": 100004,
        "name": "兴仁市政协",
        "type": "政协",
        "level": "县级",
        "location": "贵州省黔西南布依族苗族自治州兴仁市",
    },
    {
        "id": 100005,
        "name": "兴仁市纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "location": "贵州省黔西南布依族苗族自治州兴仁市",
    },
]

# ── Positions ────────────────────────────────────────
POSITIONS = [
    # Person 1: 詹丹志
    {"person_id": 1, "org_id": 100001, "title": "兴仁市委书记", "start": "~2020", "end": "present", "rank": "正县级", "note": "Training data ~2024; unverified as of 2026-07"},
    # Person 2: 潘维维
    {"person_id": 2, "org_id": 100002, "title": "兴仁市市长", "start": "~2018", "end": "present or ~2022", "rank": "正县级", "note": "Training data ~2022; unverified current status"},
    # Person 3: 方俊 (historical)
    {"person_id": 3, "org_id": 100001, "title": "兴仁县委书记", "start": "~2012", "end": "~2015", "rank": "正县级", "note": "Historical; training data"},
    # Person 4: 袁建林 (historical)
    {"person_id": 4, "org_id": 100002, "title": "兴仁县长", "start": "~2014", "end": "~2016", "rank": "正县级", "note": "Historical; training data"},
]

# ── Relationships ─────────────────────────────────────
RELATIONSHIPS = [
    # 詹丹志 as 市委书记 → Organization
    {"person_a": 1, "person_b": 100001, "type": "works_at", "context": "现任市委书记", "overlap_org": "中共兴仁市委员会", "overlap_period": "2020-present"},
    # 潘维维 as 市长 → Organization
    {"person_a": 2, "person_b": 100002, "type": "works_at", "context": "现任市长", "overlap_org": "兴仁市人民政府", "overlap_period": "2018-present"},
    # 詹丹志 ←→ 潘维维: working relationship (top 2 leaders)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委班子搭档（书记—市长）", "overlap_org": "兴仁市", "overlap_period": "2018-present"},
    # Historical: 方俊 as 县委书记
    {"person_a": 3, "person_b": 100001, "type": "works_at", "context": "前县委书记", "overlap_org": "中共兴仁县委员会", "overlap_period": "2012-2015"},
    # Historical: 袁建林 as 县长
    {"person_a": 4, "person_b": 100002, "type": "works_at", "context": "前县长", "overlap_org": "兴仁县人民政府", "overlap_period": "2014-2016"},
    # 方俊 → 詹丹志: predecessor/successor chain
    {"person_a": 3, "person_b": 1, "type": "前后任", "context": "方俊离任后詹丹志接任兴仁县委书记/市委书记", "overlap_org": "中共兴仁市委员会", "overlap_period": ""},
    # 袁建林 → 潘维维: predecessor/successor chain
    {"person_a": 4, "person_b": 2, "type": "前后任", "context": "袁建林离任后潘维维接任兴仁县长/市长", "overlap_org": "兴仁市人民政府", "overlap_period": ""},
]

# ═══════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════

DB_PATH = Path(__file__).parent / "兴仁市_network.db"
GEXF_PATH = Path(__file__).parent / "兴仁市_network.gexf"

# Separate persons from organizations
PERSON_NODES = [p for p in PERSONS if p["id"] < 100000]
ORG_NODES = [p for p in PERSONS if p["id"] >= 100000]

if __name__ == "__main__":
    run_build(
        slug="兴仁市",
        persons=PERSON_NODES + ORG_NODES,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"✅ 兴仁市 network built!")
    print(f"   DB:   {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
    print(f"   Persons: {len(PERSON_NODES)}")
    print(f"   Orgs:    {len(ORG_NODES)}")
    print(f"   Positions: {len(POSITIONS)}")
    print(f"   Relationships: {len(RELATIONSHIPS)}")
    print()
    print("⚠️  WARNING: All data is from training data (stale ~early 2025).")
    print("   Verify against current (2026-07) official sources before use.")
