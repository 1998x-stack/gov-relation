#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 承德县 leadership network.

Level: 县
Province: 河北省
Parent city: 承德市
Targets: 县委书记 (Party Secretary), 县长 (County Mayor)
Task ID: hebei_承德县

Research date: 2026-07-24
Official site: https://www.chengde.gov.cn/ (承德市人民政府)
County sub-site: http://www.cdx.gov.cn/ (承德县人民政府 — timed out in this environment)

Current status (as of 2026-07-24):
- 县委书记: [待查] — 2026年7月仍未能通过公开渠道确认现任县委书记姓名
- 县长: [待查] — 2026年7月仍未能通过公开渠道确认现任县长姓名
- 承德县属于承德市下辖县，县政府驻地下板城镇

Note:
- Government website (www.cdx.gov.cn) timed out or returned 404 on leadership paths
- Parent city site (www.chengde.gov.cn) accessible but does not expose county-level
  leadership rosters via predictable URL paths
- Search engines (Exa rate-limited, Baidu 403, Bing timeout) all blocked from this environment
- Wikipedia page for 承德县 does not list current political leadership
- No existing artifacts in repo for 承德县
- All top-leader information is marked as unverified/待查
"""
from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "承德县"
TASK_ID = "hebei_承德县"
TMP_DIR = _REPO_ROOT / "data" / "tmp" / TASK_ID

DB_PATH = TMP_DIR / f"{SLUG}_network.db"
GEXF_PATH = TMP_DIR / f"{SLUG}_network.gexf"

import sqlite3  # noqa: F811 — required by process_tmp.py validation

AS_OF = "2026-07-24"

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ── 县领导 Core Leaders (names unknown/待查) ──
    {
        "id": 1,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共承德县委书记",
        "current_org": "中共承德县委员会",
        "source": "2026年7月未能通过公开渠道确认现任县委书记",
    },
    {
        "id": 2,
        "name": "（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "承德县人民政府县长",
        "current_org": "承德县人民政府",
        "source": "2026年7月未能通过公开渠道确认现任县长",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共承德县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共承德市委员会",
        "location": "河北省承德市承德县",
    },
    {
        "id": 2,
        "name": "承德县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "承德市人民政府",
        "location": "河北省承德市承德县",
    },
    {
        "id": 3,
        "name": "承德县人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "承德市人大常委会",
        "location": "河北省承德市承德县",
    },
    {
        "id": 4,
        "name": "政协承德县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协承德市委员会",
        "location": "河北省承德市承德县",
    },
    {
        "id": 5,
        "name": "承德县纪委监委",
        "type": "党委",
        "level": "县处级",
        "parent": "中共承德县委员会",
        "location": "河北省承德市承德县",
    },
    {
        "id": 6,
        "name": "中共承德县委组织部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共承德县委员会",
        "location": "河北省承德市承德县",
    },
    {
        "id": 7,
        "name": "中共承德县委宣传部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共承德县委员会",
        "location": "河北省承德市承德县",
    },
    {
        "id": 8,
        "name": "中共承德县委政法委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共承德县委员会",
        "location": "河北省承德市承德县",
    },
    {
        "id": 9,
        "name": "中共承德县委统战部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共承德县委员会",
        "location": "河北省承德市承德县",
    },
    {
        "id": 10,
        "name": "下板城镇人民政府",
        "type": "政府",
        "level": "乡科级",
        "parent": "承德县人民政府",
        "location": "河北省承德市承德县下板城镇",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # Core leaders (待查)
    {"person_id": 1, "org_id": 1, "title": "中共承德县委书记",
     "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "2026年7月未能确认现任县委书记"},
    {"person_id": 2, "org_id": 2, "title": "承德县人民政府县长",
     "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "2026年7月未能确认现任县长"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # Core team overlap (党政协同)
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "承德县党政一把手工作搭档关系（姓名待确认）",
     "overlap_org": "承德县",
     "overlap_period": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("  承德县领导班子工作关系网络")
    print("  等级: 县（河北省承德市下辖）")
    print("  调查日期: 2026-07-24")
    print("  ❌ 县委书记: 待查（未能确认）")
    print("  ❌ 县长: 待查（未能确认）")
    print("  ⚠️  所有搜索渠道均受限：Exa 限流、Baidu 403、Bing 超时")
    print("  ⚠️  cdx.gov.cn 无法访问（超时/404）")
    print("  ⚠️  核心领导信息待后续补充")
    print("=" * 60)
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print("\n✅ 承德县数据构建完成（部分信息待补充）。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print("  ⚠️  县委书记和县长姓名待后续通过正常网络环境补充。")
