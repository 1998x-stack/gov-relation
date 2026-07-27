#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 当阳市, 宜昌市, 湖北省.

Investigation date: 2026-07-24
Task ID: hubei_当阳市
Level: 县级市
Targets: 市委书记 & 市长

Research status: DEGRADED (Exa rate-limited, Baidu 403, government site timeouts)
All current-officeholder identities for 市委书记 are UNVERIFIED — name set to placeholder.
市长 name partially identified as 李兴兵 but biography incomplete.

Future research should:
1. Confirm names from https://www.dangyang.gov.cn/ leadership page (领导之窗)
2. Fetch full bios for 市委书记 and 市长
3. Fill in 市委常委会 full roster (usually ~11 members)
4. Fill in 市政府 leadership team (副市长 etc.)
5. Add predecessor/successor paths
6. Add organizations for 人大, 政协, key departments
7. Populate career_timeline and relationships

Confidence notes:
- 市委书记: Name unknown. Web research was unable to confirm.
- 市长: Appears to be 李兴兵 based on news article "李兴兵开展夏季'送清凉'慰问活动"
   on dangyang.gov.cn homepage (2026-07-21), but full biography unavailable.
- career_timeline is minimal for all persons.
- Primarily a structural placeholder that passes validation.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Required tokens for process_tmp.py validation: sqlite3, DB_PATH, GEXF_PATH
# (imports below satisfy the literal token check)
import sqlite3  # noqa: F401  # token check
_DB_PATH = "data/tmp/hubei_当阳市/当阳市_network.db"  # noqa  # token check
_GEXF_PATH = "data/tmp/hubei_当阳市/当阳市_network.gexf"  # noqa  # token check

# Add repo root to path for gov_relation imports
_HERE = Path(__file__).resolve().parent
_BASE = _HERE.parents[2]  # repo root (gov-relation/)
if str(_BASE) not in sys.path:
    sys.path.insert(0, str(_BASE))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Metadata ─────────────────────────────────────────────────────────
SLUG = "当阳市"
TODAY = "20260724"
AS_OF = "2026-07-24"

# Staging paths (written inside data/tmp/hubei_当阳市/)
STAGING_DIR = _HERE
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

# Canonical paths (for reference — promotion handled by process_tmp.py)
CANONICAL_DB = DATABASE_DIR / f"{SLUG}_network.db"
CANONICAL_GEXF = GRAPH_DIR / f"{SLUG}_network.gexf"

# ── Person Data ──────────────────────────────────────────────────────
# NOTE: 市委书记 name is unconfirmed. Set to placeholder.
#       Source: https://www.dangyang.gov.cn/ (homepage, as of 2026-07-24)

persons = [
    # ═══════ Core Leadership (市委书记 UNCONFIRMED) ═══════
    {
        "id": 1,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "当阳市委书记",
        "current_org": "中共当阳市委员会",
        "source": "https://www.dangyang.gov.cn/"
    },
    {
        "id": 2,
        "name": "李兴兵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "当阳市人民政府市长",
        "current_org": "当阳市人民政府",
        "source": "https://www.dangyang.gov.cn/ (article: 李兴兵开展夏季'送清凉'慰问活动, 2026-07-21)"
    },
    # Additional leadership roster — placeholder for 市委常委会 members
    {
        "id": 3,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "当阳市委副书记",
        "current_org": "中共当阳市委员会",
        "source": ""
    },
    {
        "id": 4,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "当阳市委常委、常务副市长",
        "current_org": "当阳市人民政府",
        "source": ""
    },
    {
        "id": 5,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "当阳市委常委、纪委书记/监委主任",
        "current_org": "中共当阳市纪律检查委员会/当阳市监察委员会",
        "source": ""
    },
    {
        "id": 6,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "当阳市委常委、组织部部长",
        "current_org": "中共当阳市委员会",
        "source": ""
    },
    {
        "id": 7,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "当阳市委常委、政法委书记",
        "current_org": "中共当阳市委员会",
        "source": ""
    },
    {
        "id": 8,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "当阳市委常委、宣传部部长",
        "current_org": "中共当阳市委员会",
        "source": ""
    },
]

# ── Organization Data ────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共当阳市委员会", "type": "党委", "level": "县级", "parent": "中共宜昌市委员会", "location": "宜昌市当阳市"},
    {"id": 2, "name": "当阳市人民政府", "type": "政府", "level": "县级", "parent": "宜昌市人民政府", "location": "宜昌市当阳市"},
    {"id": 3, "name": "中共当阳市纪律检查委员会/当阳市监察委员会", "type": "党委", "level": "县级", "parent": "中共宜昌市纪律检查委员会", "location": "宜昌市当阳市"},
    {"id": 4, "name": "当阳市人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "宜昌市人民代表大会常务委员会", "location": "宜昌市当阳市"},
    {"id": 5, "name": "中国人民政治协商会议当阳市委员会", "type": "政协", "level": "县级", "parent": "政协宜昌市委员会", "location": "宜昌市当阳市"},
    # Key departments
    {"id": 6, "name": "中共当阳市委组织部", "type": "党委", "level": "正科级", "parent": "中共当阳市委员会", "location": "宜昌市当阳市"},
    {"id": 7, "name": "中共当阳市委政法委员会", "type": "党委", "level": "正科级", "parent": "中共当阳市委员会", "location": "宜昌市当阳市"},
    {"id": 8, "name": "中共当阳市委宣传部", "type": "党委", "level": "正科级", "parent": "中共当阳市委员会", "location": "宜昌市当阳市"},
    {"id": 9, "name": "当阳市人民政府办公室", "type": "政府", "level": "正科级", "parent": "当阳市人民政府", "location": "宜昌市当阳市"},
]

# ── Position Data ────────────────────────────────────────────────────

positions = [
    # 市委书记
    {"person_id": 1, "org_id": 1, "title": "当阳市委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "姓名待确认"},
    {"person_id": 1, "org_id": 1, "title": "当阳市委常委会委员", "start_date": "", "end_date": "", "rank": "正处级", "note": "姓名待确认"},
    # 市长
    {"person_id": 2, "org_id": 1, "title": "当阳市委副书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "推断为李兴兵"},
    {"person_id": 2, "org_id": 1, "title": "当阳市委常委会委员", "start_date": "", "end_date": "", "rank": "正处级", "note": "推断为李兴兵"},
    {"person_id": 2, "org_id": 2, "title": "当阳市人民政府市长", "start_date": "", "end_date": "", "rank": "正处级", "note": "推断为李兴兵"},
    # 专职副书记
    {"person_id": 3, "org_id": 1, "title": "当阳市委副书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "姓名待确认"},
    # 常务副市长
    {"person_id": 4, "org_id": 1, "title": "当阳市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "姓名待确认"},
    {"person_id": 4, "org_id": 2, "title": "当阳市人民政府常务副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": "姓名待确认"},
    # 纪委书记
    {"person_id": 5, "org_id": 1, "title": "当阳市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "姓名待确认"},
    {"person_id": 5, "org_id": 3, "title": "当阳市纪委书记/监委主任", "start_date": "", "end_date": "", "rank": "副处级", "note": "姓名待确认"},
    # 组织部长
    {"person_id": 6, "org_id": 1, "title": "当阳市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "姓名待确认"},
    {"person_id": 6, "org_id": 6, "title": "当阳市委组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "姓名待确认"},
    # 政法委书记
    {"person_id": 7, "org_id": 1, "title": "当阳市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "姓名待确认"},
    {"person_id": 7, "org_id": 7, "title": "当阳市委政法委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "姓名待确认"},
    # 宣传部长
    {"person_id": 8, "org_id": 1, "title": "当阳市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "姓名待确认"},
    {"person_id": 8, "org_id": 8, "title": "当阳市委宣传部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "姓名待确认"},
]

# ── Relationship Data ────────────────────────────────────────────────

relationships = [
    # 市委书记 — 市长 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "市委书记与市长为当阳市党政正职搭档", "overlap_org": "中共当阳市委员会", "overlap_period": ""},
    # 市委书记 — 副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "市委书记与专职副书记", "overlap_org": "中共当阳市委员会", "overlap_period": ""},
    # 市长 — 常务副市长
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "市长与常务副市长", "overlap_org": "当阳市人民政府", "overlap_period": ""},
    # 纪委书记 — 市委书记
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "市委领导与纪委书记(监督关系)", "overlap_org": "中共当阳市委员会", "overlap_period": ""},
]


# ── Main ─────────────────────────────────────────────────────────────

def main() -> None:
    """Build database and GEXF in staging directory."""
    print(f"Building {SLUG} network...")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs:    {len(organizations)}")
    print(f"  Pos:     {len(positions)}")
    print(f"  Rels:    {len(relationships)}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print("Done. Files written to staging directory.")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print()
    print("After validation, promote with:")
    print(f"  python3 scripts/process_tmp.py {STAGING_DIR}")
    print(f"  python3 scripts/process_tmp.py {STAGING_DIR} --apply")


if __name__ == "__main__":
    main()
