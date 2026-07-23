#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 平乡县 leadership network.

Level: 县
Province: 河北省
Parent city: 邢台市
Targets: 县委书记 (Party Secretary), 县长 (County Mayor)
Task ID: hebei_平乡县

Research date: 2026-07-23
Official site: https://www.pingxiang.gov.cn/

Current status (as of 2026-07-23):
- 县委书记: [待查] — 2026年7月仍未能通过公开渠道确认现任县委书记姓名
- 县长: [待查] — 2026年7月仍未能通过公开渠道确认现任县长姓名

Note:
- Government website (www.pingxiang.gov.cn) is a JS-rendered SPA (React/webpack)
  behind WAF CDN with token-based routing (/1ywuKELSO2ahQuWZ/), preventing
  direct URL access to leadership pages.
- Search engines (Google, Baidu, Bing, DuckDuckGo) all blocked/timed out from
  this environment.
- Exa search reached free rate limit; Jina Reader unavailable.
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

SLUG = "平乡县"
TASK_ID = "hebei_平乡县"
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
        "name": "待查（平乡县委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共平乡县委书记",
        "current_org": "中共平乡县委员会",
        "source": "未确认 — 平乡县人民政府官网 (www.pingxiang.gov.cn) 为JS渲染SPA，无法通过文本爬虫获取领导信息；所有搜索引擎均封锁",
    },
    {
        "id": 2,
        "name": "待查（平乡县县长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平乡县人民政府县长",
        "current_org": "平乡县人民政府",
        "source": "未确认 — 同上",
    },

    # ── 县级机构负责人 Default Org Leaders (positions only, placeholder) ──
    # Note: All deputy-level leaders are also unknown/待查 due to same access limitations.
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共平乡县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共邢台市委员会",
        "location": "河北省邢台市平乡县",
    },
    {
        "id": 2,
        "name": "平乡县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "邢台市人民政府",
        "location": "河北省邢台市平乡县",
    },
    {
        "id": 3,
        "name": "平乡县人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "邢台市人大常委会",
        "location": "河北省邢台市平乡县",
    },
    {
        "id": 4,
        "name": "政协平乡县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协邢台市委员会",
        "location": "河北省邢台市平乡县",
    },
    {
        "id": 5,
        "name": "中共平乡县纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共平乡县委员会",
        "location": "河北省邢台市平乡县",
    },
    {
        "id": 6,
        "name": "中共平乡县委组织部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共平乡县委员会",
        "location": "河北省邢台市平乡县",
    },
    {
        "id": 7,
        "name": "中共平乡县委宣传部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共平乡县委员会",
        "location": "河北省邢台市平乡县",
    },
    {
        "id": 8,
        "name": "中共平乡县委政法委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共平乡县委员会",
        "location": "河北省邢台市平乡县",
    },
    {
        "id": 9,
        "name": "中共平乡县委统战部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共平乡县委员会",
        "location": "河北省邢台市平乡县",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # Core leaders (names unknown)
    {"person_id": 1, "org_id": 1, "title": "中共平乡县委书记",
     "start_date": "", "end_date": "至今", "rank": "县处级正职",
     "note": "姓名待查 — 所有公开网络渠道均无法获取当前县委书记信息"},
    {"person_id": 2, "org_id": 2, "title": "平乡县人民政府县长",
     "start_date": "", "end_date": "至今", "rank": "县处级正职",
     "note": "姓名待查 — 所有公开网络渠道均无法获取当前县长信息"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # Core team overlap (the two top leaders work together in the same county)
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "平乡县党政一把手工作搭档关系（姓名均待查）",
     "overlap_org": "平乡县",
     "overlap_period": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("  邢台市平乡县领导班子工作关系网络")
    print("  等级: 县")
    print("  调查日期: 2026-07-23")
    print("  ❌ 县委书记: 待查")
    print("  ❌ 县长: 待查")
    print("  ❌ 其他领导: 均待查")
    print("  ⚠️  主要来源: 平乡县人民政府官网 (www.pingxiang.gov.cn) — SPA/WAF封锁")
    print("  ⚠️  所有搜索工具（Google/Baidu/Bing/DuckDuckGo/Exa/Jina）均不可用")
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
    print(f"\n✅ 平乡县数据构建完成（基础骨架，领导信息待补充）。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print("  ⚠️  所有核心领导信息为待查。建议从以下渠道补充：")
    print("    - 邢台市人民政府官网任前公示栏目")
    print("    - 河北省委组织部干部任免公告")
    print("    - 百度百科平乡县词条")
    print("    - 使用浏览器（非curl）访问平乡县人民政府官网领导之窗")
