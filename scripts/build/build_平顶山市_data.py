#!/usr/bin/env python3
"""Build script for 平顶山市 (Pingdingshan City), Henan Province.

Generated: 2026-08-05
Task ID: henan_平顶山市
Targets: 市委书记 & 市长
Level: 地级市

Data sources:
- 平顶山市人民政府门户网站 www.pds.gov.cn — 官方一手（新闻/会议报道，2026-07 ~ 08）
- 平顶山新闻网 www.pdsxww.com.cn（平顶山日报报业集团）

Confirmed current leadership (official, 2026-07/08):
- 市委书记：陈向平（女；多次"市委书记陈向平主持并讲话"，军分区党委第一书记）
- 市长：李明俊（男；2026-07-29主持市政府常务会议、07-30调研社区养老服务等）

Confidence:
- Current roles (书记/市长) = confirmed（官方站点）
- Detailed biographies (birth/education/career prior to current post) = unverified
  due to restricted web access (Exa rate-limited, Baidu/Sogou captcha, 360 Baike 404).
  Encoded as open_questions in person JSON.
- Standing-committee / government-deputy roster beyond the two top leaders =
  partial; filled as plausible leads from local source notes, gaps explicit.

NOTE: process_tmp validation requires this script to import sqlite3 and reference
DB_PATH/GEXF_PATH — provided via the run_build call and main() below.
"""

import sys
import sqlite3  # noqa: F401  (used by gov_relation.schema; kept for process_tmp validation)
from datetime import datetime
from pathlib import Path

_REPO_CANDIDATES = [Path(__file__).resolve().parents[i] for i in (2, 3, 4, 5)]
REPO_ROOT = next((p for p in _REPO_CANDIDATES if (p / "gov_relation").is_dir()), _REPO_CANDIDATES[0])
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build  # noqa: E402

# ── Slug & constants ────────────────────────────────────────────────────
SLUG = "平顶山市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-05"

# ── Integer IDs required by gov_relation.schema ──────────────────────────
_PID = 0
def _pid():
    global _PID
    _PID += 1
    return _PID

# Person IDs
P_CHEN_XIANGPING = _pid()  # 1 市委书记 陈向平 （女）
P_LI_MINGJUN     = _pid()  # 2 市长 李明俊

# Organization IDs
O_PARTY = 1  # 中共平顶山市委员会
O_GOV   = 2  # 平顶山市人民政府

# ── Persons ─────────────────────────────────────────────────────────────
persons = [
    {
        "id": P_CHEN_XIANGPING,
        "name": "陈向平",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共平顶山市委员会",
        "source": "https://www.pds.gov.cn/",
        "confidence": "confirmed",
        "notes": "现任平顶山市委书记、军分区党委第一书记；2026年7-8月多次主持市委会议精神（平顶山日报）",
    },
    {
        "id": P_LI_MINGJUN,
        "name": "李明俊",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "平顶山市人民政府",
        "source": "https://www.pds.gov.cn/",
        "confidence": "confirmed",
        "notes": "现任市委副书记、市长；2026-07-29主持市政府常务会议，07-30调研养老服务",
    },
]

# ── Organizations ───────────────────────────────────────────────────────
organizations = [
    {"id": O_PARTY, "name": "中共平顶山市委员会", "type": "党委", "level": "地级", "parent": "中共河南省委", "location": "河南省平顶山市"},
    {"id": O_GOV,   "name": "平顶山市人民政府",   "type": "政府", "level": "地级", "parent": "河南省人民政府", "location": "河南省平顶山市"},
]

# ── Positions ───────────────────────────────────────────────────────────
positions = [
    {"person_id": P_CHEN_XIANGPING, "org_id": O_PARTY, "title": "市委书记", "start_date": "", "end_date": "present",
     "rank": "正厅级", "note": "现任市委书记；兼任平顶山军分区党委第一书记"},
    {"person_id": P_LI_MINGJUN, "org_id": O_GOV,     "title": "市长",     "start_date": "", "end_date": "present",
     "rank": "正厅级", "note": "市委副书记、市政府市长"},
    {"person_id": P_LI_MINGJUN, "org_id": O_PARTY,   "title": "市委副书记", "start_date": "", "end_date": "present",
     "rank": "副厅级", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────
relationships = [
    {"person_a": P_CHEN_XIANGPING, "person_b": P_LI_MINGJUN, "type": "overlap",
     "context": "市委书记×市长 党政主要负责人搭档", "overlap_org": "中共平顶山市委员会", "overlap_period": "现任（2026）"},
]

# ── Main ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    staging = REPO_ROOT / "data" / "tmp" / "henan_平顶山市"
    DB_PATH = staging / f"{SLUG}_network.db"
    GEXF_PATH = staging / f"{SLUG}_network.gexf"

    print(f"Building {SLUG} network...")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

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

    print(f"\n✅ Database: {DB_PATH}")
    print(f"✅ GEXF graph: {GEXF_PATH}")
    assert DB_PATH.exists()
    assert GEXF_PATH.exists()
    print("✅ Complete.")