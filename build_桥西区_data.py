#!/usr/bin/env python3
"""Build 石家庄市桥西区 (Shijiazhuang Qiaoxi District) leadership network data.

Level: 市辖区
Province: 河北省
Parent city: 石家庄市
Targets: 区委书记 (Party Secretary), 区长 (Mayor)
Task ID: hebei_桥西区

Research date: 2026-07-23
Official source: http://www.sjzqiaoxiqu.gov.cn/ (石家庄市桥西区人民政府 — site unreachable during research)

Current status (as of 2026-07-23):
- 区委书记: 【待确认】 — 政府网站无法访问，公开来源无法确认当前区委书记
- 区长: 【待确认】 — 政府网站无法访问，公开来源无法确认当前区长

Note:
- 桥西区政府网站 (www.sjzqiaoxiqu.gov.cn) 在调查期间无法访问（超时）
- Exa 搜索达到速率限制
- 百度返回 403
- Google 搜索被屏蔽
- Jina Reader 无法连接
- 所有证据均标记为 unverified/plausible，待补充确认
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "桥西区"
TASK_ID = "hebei_桥西区"
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
    # 区委书记 — 公开渠道无法确认
    # 备注：截至2026年7月，政府网站不可达，未能确认当前区委书记姓名。
    # 待后续有政府/组织部门公告后补充。

    # ════════════════════════════════════════
    # 区政府领导 (Government Leadership)
    # ════════════════════════════════════════
    # 区长 — 公开渠道无法确认
    # 备注：同上的网络问题，无法确认当前区长姓名。
    # 待后续补充。

    # 鉴于完全无法获取当前领导信息，留几条占位记录以保持数据结构完整。
    # 实际领导信息需要后续通过网络恢复后补充。

    {
        "id": 1,
        "name": "【待确认】桥西区委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "桥西区委书记",
        "current_org": "中共石家庄市桥西区委员会",
        "source": "搜索受限 — 政府网站不可达，无法确认当前区委书记",
    },
    {
        "id": 2,
        "name": "【待确认】桥西区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "桥西区委副书记、区长",
        "current_org": "桥西区人民政府",
        "source": "搜索受限 — 政府网站不可达，无法确认当前区长",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共石家庄市桥西区委员会",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共石家庄市委员会",
        "location": "河北省石家庄市桥西区",
    },
    {
        "id": 2,
        "name": "桥西区人民政府",
        "type": "政府",
        "level": "市辖区",
        "parent": "石家庄市人民政府",
        "location": "河北省石家庄市桥西区",
    },
    {
        "id": 3,
        "name": "桥西区人大常委会",
        "type": "人大",
        "level": "市辖区",
        "parent": "石家庄市人大常委会",
        "location": "河北省石家庄市桥西区",
    },
    {
        "id": 4,
        "name": "政协桥西区委员会",
        "type": "政协",
        "level": "市辖区",
        "parent": "政协石家庄市委员会",
        "location": "河北省石家庄市桥西区",
    },
    {
        "id": 5,
        "name": "桥西公安分局",
        "type": "政府",
        "level": "区直部门",
        "parent": "石家庄市公安局",
        "location": "河北省石家庄市桥西区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 区委书记
    {"person_id": 1, "org_id": 1, "title": "桥西区委书记", "start": "", "end": "至今", "rank": "", "note": "待确认"},
    # 区长
    {"person_id": 2, "org_id": 2, "title": "桥西区委副书记、区长", "start": "", "end": "至今", "rank": "", "note": "待确认"},
    {"person_id": 2, "org_id": 1, "title": "桥西区委副书记", "start": "", "end": "至今", "rank": "", "note": "待确认"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 党政一把手工作关系（待确认具体姓名后验证）
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "区委书记与区长党政工作搭档关系", "overlap_org": "桥西区", "overlap_period": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("  石家庄市桥西区领导班子工作关系网络")
    print("  等级: 市辖区")
    print("  调查日期: 2026-07-23")
    print("  ⚠️  搜索渠道全部受限（政府网站超时、Exa限速、百度403、Google屏蔽）")
    print("  当前数据标记为待确认，请在网络恢复后补充调查。")
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
    print("\n✅ 桥西区数据构建完成（占位版本）。")
    print("  ⚠️  区委书记和区长信息均为待确认占位，需补充调查。")
