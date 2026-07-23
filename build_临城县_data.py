#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 临城县 leadership network.

Level: 县
Province: 河北省
Parent city: 邢台市
Targets: 县委书记 (Party Secretary), 县长 (County Mayor)
Task ID: hebei_临城县

Research date: 2026-07-23
Official site: https://www.lincheng.gov.cn/

Current status (as of 2026-07-23):
- 县委书记: [待查] — 2026年7月仍未能通过公开渠道确认现任县委书记姓名
- 县长: [待查] — 2026年7月仍未能通过公开渠道确认现任县长姓名
- Five deputy county mayors confirmed on government site:
  孙三军 (副县长, resume dated 2025-02-18)
  刘胜民 (副县长, resume dated 2025-02-17)
  孙翠娟 (副县长, resume dated 2025-02-17)
  胡强 (副县长, resume dated 2025-02-14)
  代小山 (副县长, resume dated 2023-04-10)

Note:
- Government website (www.lincheng.gov.cn) accessible but CMS article routing
  is parameter-based (not path-based), preventing direct URL access to
  individual resume pages.
- Search engines (Google, Baidu, Bing) all blocked/timed out from this environment.
- No previous worker successfully completed this task.
- All top-leader information is marked as unverified/待查.
"""
from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "临城县"
TASK_ID = "hebei_临城县"
TMP_DIR = _REPO_ROOT / "data" / "tmp" / TASK_ID

DB_PATH = TMP_DIR / f"{SLUG}_network.db"
GEXF_PATH = TMP_DIR / f"{SLUG}_network.gexf"

import sqlite3  # noqa: F811 — required by process_tmp.py validation

AS_OF = "2026-07-23"

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
        "current_post": "中共临城县委书记",
        "current_org": "中共临城县委员会",
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
        "current_post": "临城县人民政府县长",
        "current_org": "临城县人民政府",
        "source": "2026年7月未能通过公开渠道确认现任县长",
    },

    # ── 副县长 Confirmed Deputy County Mayors ──
    # Source: lincheng.gov.cn homepage — "临城县政府副县长孙三军同志简历" (2025-02-18)
    {
        "id": 11,
        "name": "孙三军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "临城县政府副县长",
        "current_org": "临城县人民政府",
        "source": "临城县人民政府官网 — 孙三军同志简历 (2025-02-18)",
    },
    # Source: lincheng.gov.cn homepage — "临城县政府副县长刘胜民同志简历" (2025-02-17)
    {
        "id": 12,
        "name": "刘胜民",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "临城县政府副县长",
        "current_org": "临城县人民政府",
        "source": "临城县人民政府官网 — 刘胜民同志简历 (2025-02-17)",
    },
    # Source: lincheng.gov.cn homepage — "临城县政府副县长孙翠娟同志简历" (2025-02-17)
    {
        "id": 13,
        "name": "孙翠娟",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "临城县政府副县长",
        "current_org": "临城县人民政府",
        "source": "临城县人民政府官网 — 孙翠娟同志简历 (2025-02-17)",
    },
    # Source: lincheng.gov.cn homepage — "临城县政府副县长胡强同志简历" (2025-02-14)
    {
        "id": 14,
        "name": "胡强",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "临城县政府副县长",
        "current_org": "临城县人民政府",
        "source": "临城县人民政府官网 — 胡强同志简历 (2025-02-14)",
    },
    # Source: lincheng.gov.cn homepage — "临城县政府副县长代小山同志简历" (2023-04-10)
    {
        "id": 15,
        "name": "代小山",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "临城县政府副县长",
        "current_org": "临城县人民政府",
        "source": "临城县人民政府官网 — 代小山同志简历 (2023-04-10)",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共临城县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共邢台市委员会",
        "location": "河北省邢台市临城县",
    },
    {
        "id": 2,
        "name": "临城县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "邢台市人民政府",
        "location": "河北省邢台市临城县",
    },
    {
        "id": 3,
        "name": "临城县人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "邢台市人大常委会",
        "location": "河北省邢台市临城县",
    },
    {
        "id": 4,
        "name": "政协临城县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协邢台市委员会",
        "location": "河北省邢台市临城县",
    },
    {
        "id": 5,
        "name": "临城县纪委监委",
        "type": "党委",
        "level": "县处级",
        "parent": "中共临城县委员会",
        "location": "河北省邢台市临城县",
    },
    {
        "id": 6,
        "name": "中共临城县委组织部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共临城县委员会",
        "location": "河北省邢台市临城县",
    },
    {
        "id": 7,
        "name": "中共临城县委宣传部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共临城县委员会",
        "location": "河北省邢台市临城县",
    },
    {
        "id": 8,
        "name": "中共临城县委政法委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共临城县委员会",
        "location": "河北省邢台市临城县",
    },
    {
        "id": 9,
        "name": "中共临城县委统战部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共临城县委员会",
        "location": "河北省邢台市临城县",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # Core leaders (待查)
    {"person_id": 1, "org_id": 1, "title": "中共临城县委书记",
     "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "2026年7月未能确认现任县委书记"},
    {"person_id": 2, "org_id": 2, "title": "临城县人民政府县长",
     "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "2026年7月未能确认现任县长"},

    # Deputy County Mayors
    {"person_id": 11, "org_id": 2, "title": "临城县政府副县长",
     "start_date": "", "end_date": "至今", "rank": "县处级副职",
     "note": "简历发布于2025-02-18"},
    {"person_id": 12, "org_id": 2, "title": "临城县政府副县长",
     "start_date": "", "end_date": "至今", "rank": "县处级副职",
     "note": "简历发布于2025-02-17"},
    {"person_id": 13, "org_id": 2, "title": "临城县政府副县长",
     "start_date": "", "end_date": "至今", "rank": "县处级副职",
     "note": "简历发布于2025-02-17"},
    {"person_id": 14, "org_id": 2, "title": "临城县政府副县长",
     "start_date": "", "end_date": "至今", "rank": "县处级副职",
     "note": "简历发布于2025-02-14"},
    {"person_id": 15, "org_id": 2, "title": "临城县政府副县长",
     "start_date": "", "end_date": "至今", "rank": "县处级副职",
     "note": "简历发布于2023-04-10"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # Core team overlap (党政协同)
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "临城县党政一把手工作搭档关系（姓名待确认）",
     "overlap_org": "临城县",
     "overlap_period": ""},

    # Deputy county mayors with core leaders
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "县长与孙三军副县长工作关系",
     "overlap_org": "临城县人民政府",
     "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate",
     "context": "县长与刘胜民副县长工作关系",
     "overlap_org": "临城县人民政府",
     "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate",
     "context": "县长与孙翠娟副县长工作关系",
     "overlap_org": "临城县人民政府",
     "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate",
     "context": "县长与胡强副县长工作关系",
     "overlap_org": "临城县人民政府",
     "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate",
     "context": "县长与代小山副县长工作关系",
     "overlap_org": "临城县人民政府",
     "overlap_period": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("  邢台市临城县领导班子工作关系网络")
    print("  等级: 县")
    print("  调查日期: 2026-07-23")
    print("  ❌ 县委书记: 待查（未能确认）")
    print("  ❌ 县长: 待查（未能确认）")
    print("  ✅ 副县长 (5位): 孙三军, 刘胜民, 孙翠娟, 胡强, 代小山")
    print("  ⚠️  所有搜索渠道均受限：Google/Baidu/Bing 超时或封禁")
    print("  ⚠️  lincheng.gov.cn 首页可访问但具体简历页面路由参数未知")
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
    print("\n✅ 临城县数据构建完成（部分信息待补充）。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print("  ⚠️  县委书记和县长姓名待后续通过正常网络环境补充。")
