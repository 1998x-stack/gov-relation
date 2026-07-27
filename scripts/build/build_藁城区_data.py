#!/usr/bin/env python3
"""Build 石家庄市藁城区 (Gaocheng District, Shijiazhuang) leadership network data.

Level: 市辖区
Province: 河北省
Parent city: 石家庄市
Targets: 区委书记 (Party Secretary), 区长 (Mayor)
Task ID: hebei_藁城区

Research date: 2026-07-23
Official source: http://www.gc.gov.cn/ (石家庄市藁城区人民政府 — accessible but 领导之窗 section not easily navigable)

Current status (as of 2026-07-23):
- 区委书记: 万树军 (Wan Shujun) — confirmed from "藁城区委常委会（扩大）会议召开 万树军主持并讲话" (2026-05-16) on gc.gov.cn
- 区长: 【待确认】 — government site accessible but appointment notice not found via available search channels
- 人大常委会主任: 李更顺 — confirmed from "藁城区三届人大常委会举行第四十六次会议" (2026-05-10) on gc.gov.cn

Known evidence:
  - 万树军主持区委常委会(扩大)会议: http://www.gc.gov.cn/columns/c3738baa-7db0-4496-aef3-215e0bccb4ba/202605/16/... (via news list page)
  - 李更顺出席区人大常委会会议: http://www.gc.gov.cn/columns/c3738baa-7db0-4496-aef3-215e0bccb4ba/202605/11/48a02ff2-278f-4e11-b0e6-d39fba9188a8.html

Search limitations:
  - Exa search API: rate-limited
  - Google search: blocked
  - Baidu: 403
  - Jina Reader: timeout
  - Direct site search: JavaScript-rendered results

Note: 区长信息需要进一步通过石家庄市委组织部任前公示或藁城区人大任命公告确认。
"""
from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "藁城区"
TASK_ID = "hebei_藁城区"
TMP_DIR = _REPO_ROOT / "data" / "tmp" / TASK_ID

DB_PATH = TMP_DIR / f"{SLUG}_network.db"
GEXF_PATH = TMP_DIR / f"{SLUG}_network.gexf"

import sqlite3  # noqa: F811 — required by process_tmp.py validation

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 区委领导 (Party Committee)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "万树军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "藁城区委书记",
        "current_org": "中共石家庄市藁城区委员会",
        "source": "gc.gov.cn 藁城要闻 — 2026年5月16日'藁城区委常委会（扩大）会议召开 万树军主持并讲话'",
    },
    # 区长 — 公开渠道尚未确认
    {
        "id": 2,
        "name": "【待确认】藁城区区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "藁城区委副书记、区长",
        "current_org": "藁城区人民政府",
        "source": "搜索受限 — 尚未在公开来源确认当前区长姓名，需通过石家庄市委组织部任前公示或藁城区人大任命公告确认",
    },
    # 区人大常委会主任
    {
        "id": 3,
        "name": "李更顺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "藁城区人大常委会主任",
        "current_org": "藁城区人大常委会",
        "source": "gc.gov.cn 藁城要闻 — 2026年5月10日'藁城区三届人大常委会举行第四十六次会议 李更顺出席'",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共石家庄市藁城区委员会",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共石家庄市委员会",
        "location": "河北省石家庄市藁城区",
    },
    {
        "id": 2,
        "name": "藁城区人民政府",
        "type": "政府",
        "level": "市辖区",
        "parent": "石家庄市人民政府",
        "location": "河北省石家庄市藁城区",
    },
    {
        "id": 3,
        "name": "藁城区人大常委会",
        "type": "人大",
        "level": "市辖区",
        "parent": "石家庄市人大常委会",
        "location": "河北省石家庄市藁城区",
    },
    {
        "id": 4,
        "name": "政协藁城区委员会",
        "type": "政协",
        "level": "市辖区",
        "parent": "政协石家庄市委员会",
        "location": "河北省石家庄市藁城区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 区委书记
    {"person_id": 1, "org_id": 1, "title": "藁城区委书记", "start": "", "end": "至今", "rank": "", "note": "2026年5月16日主持区委常委会（扩大）会议"},
    # 区长（待确认）
    {"person_id": 2, "org_id": 2, "title": "藁城区委副书记、区长", "start": "", "end": "至今", "rank": "", "note": "待确认"},
    {"person_id": 2, "org_id": 1, "title": "藁城区委副书记", "start": "", "end": "至今", "rank": "", "note": "待确认"},
    # 人大常委会主任
    {"person_id": 3, "org_id": 3, "title": "藁城区人大常委会主任", "start": "", "end": "至今", "rank": "", "note": "2026年5月10日出席会议"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 党政一把手工作关系
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "区委书记与区长党政工作搭档关系", "overlap_org": "藁城区", "overlap_period": ""},
    # 区委书记与人大主任
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "区委书记与人大常委会主任党政关系", "overlap_org": "藁城区", "overlap_period": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("  石家庄市藁城区领导班子工作关系网络")
    print("  等级: 市辖区")
    print("  调查日期: 2026-07-23")
    print("=" * 60)
    print()
    print("  已确认:")
    print("    ✓ 区委书记: 万树军（2026-05-16 主持区委常委会）")
    print("    ✓ 人大常委会主任: 李更顺（2026-05-10 出席区委常委会会议）")
    print("    ? 区长: 待确认")
    print()
    print("  ⚠️  搜索限制: Exa限速、Google屏蔽、百度403")
    print("  区长信息需通过石家庄市委组织部公告或藁城区人大任命公告补充。")
    print()
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print("\n✅ 藁城区数据构建完成。")
    print("  ⚠️  区长信息为待确认占位，需补充调查。")
