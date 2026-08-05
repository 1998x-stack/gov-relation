#!/usr/bin/env python3
"""
Build SQLite database and GEXF graph for 望都县 leadership network.

Province: 河北省保定市望都县
Level: 县 (county)
Research date: 2026-08-05
Task: hebei_望都县 (targets 县委书记 & 县长)

Environment / data-integrity note:
  External web access was fully degraded during this task. Exa free MCP API returned
  rate-limit errors on every call, and we therefore stopped using Exa (per source
  fallback playbook). Baidu/Bing/thepaper direct fetches returned transport errors.
  The official county site (no reachable host confirmed), bigger mirrors
  (r.jina.ai) and Jina Reader all timed out on repeated attempts. No valid
  source-backed biography for the current 县委书记 / 县长 could be confirmed in
  this environment.

  Per source_fallbacks.md "Artifact Mode Under Partial Evidence", we still create
  structurally valid artifacts. The core-leader identities are recorded as
  `待查_*` (to-be-checked) with `unverified` confidence, exactly matching the
  established repo convention for this scenario (see the 吉林省-辉南县 case
  written the same week). We do NOT fabricate names, dates, birthplace, education,
  or party dates.

  Structural / near-certain facts encoded:
  - 望都县 is a county-level division of 保定市, 河北省.
  - 望都县 lies south of 保定市区 adjacent to 顺平县/唐县/清苑区 etc.;
    it is known as "辣椒之乡" (chili pepper hub).
  - The county party committee and county government bodies exist and hold
    to the standard county-level administrative hierarchy.
  These are recorded with confidence `confirmed` (organizational structure) and
  the individual holder names as `unverified`.

All `待查` holder records are marked `unverified` and carry critical
`open_questions` to drive follow-up.
"""

import json
import os
import sys
from pathlib import Path

def _find_repo_root(start: Path) -> Path:
    """Walk up from the script location to the repo root (contains gov_relation/)."""
    cur = start.resolve()
    for _ in range(6):
        if (cur / "gov_relation").is_dir():
            return cur
        nxt = cur.parent
        if nxt == cur:
            break
        cur = nxt
    raise RuntimeError(f"could not locate repo root from {start}")

_REPO_ROOT = _find_repo_root(Path(__file__).parent)
for _p in (_REPO_ROOT, os.path.join(_REPO_ROOT, "scripts")):
    if _p not in sys.path:
        sys.path.insert(0, str(_p))

import sqlite3  # noqa: E402

from gov_relation.runner import run_build  # noqa: E402

SLUG = "望都县"
DB_PATH = Path(__file__).parent / f"{SLUG}_network.db"
GEXF_PATH = Path(__file__).parent / f"{SLUG}_network.gexf"
AS_OF = "2026-08-05"
TODAY = "2026-08-05"

# ────────────────────────────────────────────────────────────────────────────
# Persons
# ────────────────────────────────────────────────────────────────────────────
persons = [
    # ── 县委书记 (Party Secretary) — Identity not confirmed in this env ──
    {
        "id": 1,
        "name": "待查_县委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "望都县委书记",
        "current_org": "中共望都县委员会",
        "source": "web search unavailable; identity unverified (see report/open_gaps.md)",
    },
    # ── 县委副书记、县长 (County Mayor) — Identity not confirmed ──
    {
        "id": 2,
        "name": "待查_县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "望都县委副书记、县长",
        "current_org": "望都县人民政府",
        "source": "web search unavailable; identity unverified (see report/open_gaps.md)",
    },
    # ── 县委常委、常务副县长 ── (identity unverified)
    {
        "id": 3,
        "name": "待查_常务副县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "望都县人民政府",
        "source": "unverified",
    },
    # ── 县委常委、纪委书记 ── (identity unverified)
    {
        "id": 4,
        "name": "待查_纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县纪委书记",
        "current_org": "中共望都县纪律检查委员会",
        "source": "unverified",
    },
    # ── 保定市（地级市）主要党政领导 — context nodes with plausible identity ──
    {
        "id": 5,
        "name": "待查（原保定市委书记易人）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "保定市委书记",
        "current_org": "中共保定市委员会",
        "source": "unverified (leadership turnover at city level not confirmable under degraded web)",
    },
]

# ────────────────────────────────────────────────────────────────────────────
# Organizations
# ────────────────────────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共望都县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共保定市委员会",
        "location": "望都县",
    },
    {
        "id": 2,
        "name": "望都县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "保定市人民政府",
        "location": "望都县",
    },
    {
        "id": 3,
        "name": "中共望都县纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共保定市纪律检查委员会",
        "location": "望都县",
    },
    {
        "id": 4,
        "name": "中共保定市委员会",
        "type": "党委",
        "level": "地厅级",
        "parent": "中共河北省委员会",
        "location": "保定市",
    },
    {
        "id": 5,
        "name": "保定市人民政府",
        "type": "政府",
        "level": "地厅级",
        "parent": "河北省人民政府",
        "location": "保定市",
    },
    {
        "id": 6,
        "name": "中共河北省委员会",
        "type": "党委",
        "level": "省部级",
        "parent": "",
        "location": "石家庄市",
    },
    {
        "id": 7,
        "name": "河北省人民政府",
        "type": "政府",
        "level": "省部级",
        "parent": "",
        "location": "石家庄市",
    },
]

# ────────────────────────────────────────────────────────────────────────────
# Positions
# ────────────────────────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "县委书记",
     "start": "", "end": "present", "rank": "县处级正职",
     "note": "name unverified (待查). Needs 保定市委组织部公示/任前公示 to confirm. (confidence: unverified)"},
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长",
     "start": "", "end": "present", "rank": "县处级正职",
     "note": "name unverified (待查). Needs 民大 confirmation. (confidence: unverified)"},
    {"person_id": 3, "org_id": 2, "title": "县委常委、常务副县长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "name unverified. (confidence: unverified)"},
    {"person_id": 4, "org_id": 3, "title": "县委常委、县纪委书记",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "name unverified. (confidence: unverified)"},
    {"person_id": 5, "org_id": 4, "title": "保定市委书记",
     "start": "", "end": "present", "rank": "地厅级正职",
     "note": "city-level leadership not confirmable in this env (confidence: unverified)"},
]

# ────────────────────────────────────────────────────────────────────────────
# Relationships
# ────────────────────────────────────────────────────────────────────────────
relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长（党政正职搭档，密接互动，职务结构上为党政双核）",
        "overlap_org": "望都县", "overlap_period": "",
    },
    {
        "person_a": 3, "person_b": 2,
        "type": "superior_subordinate",
        "context": "常务副县长协助县长（县人民政府内部层级）",
        "overlap_org": "望都县人民政府", "overlap_period": "",
    },
    {
        "person_a": 1, "person_b": 4,
        "type": "same_system",
        "context": "纪委书记受县委领导（党委领导体系内），组成县委常委会",
        "overlap_org": "中共望都县委员会", "overlap_period": "",
    },
]

if __name__ == "__main__":
    print(f"Building {SLUG} network...")
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
    print(f"Done. Wrote {DB_PATH.relative_to(Path.cwd())} and {GEXF_PATH.relative_to(Path.cwd())}")