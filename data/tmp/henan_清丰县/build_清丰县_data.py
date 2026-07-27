#!/usr/bin/env python3
"""清丰县领导班子工作关系网络 — 数据构建脚本。

等级: 县
调查日期: 2026-07-24
信息来源:
  - 清丰县人民政府网站 (www.qingfeng.gov.cn)
  - 央视网搜索 (search.cctv.com)
  - 濮阳市人民政府网站 (www.puyang.gov.cn)
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

# Ensure we can import from project root
HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Config ────────────────────────────────────────────────────────────────────
SLUG = "清丰县"
TODAY = "2026-07-24"

# ── Persons ──────────────────────────────────────────────────────────────────
# Person IDs: 1xxx = party committee, 2xxx = government

persons = [
    # ═══════════════════════════════════════════════════════════════════════
    # 1. 胡志强 — 县委书记
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1001,
        "name": "胡志强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "清丰县委书记",
        "current_org": "中共清丰县委员会",
        "source": "http://www.qingfeng.gov.cn/content/2026/1281187.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 2. 朱广治 — 县委副书记、县长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1002,
        "name": "朱广治",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "清丰县委副书记、县长",
        "current_org": "清丰县人民政府",
        "source": "http://www.qingfeng.gov.cn/content/2026/1310793.html",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 3. 高尚功 — 前任县委书记（2024年在任）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1003,
        "name": "高尚功",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任清丰县委书记（去向待查）",
        "current_org": "中共清丰县委员会（前任）",
        "source": "https://local.cctv.com/2024/05/20/ARTIYFtWq4yBrbwUd6SsVk1k240520.shtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 4. 曹拥军 — 前前任县委书记（2022年在任）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1004,
        "name": "曹拥军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前前任清丰县委书记（去向待查）",
        "current_org": "中共清丰县委员会（前前任）",
        "source": "https://local.cctv.com/2022/08/03/ARTIrhD8sWRi6QxBhINwHaRc220803.shtml",
    },
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共清丰县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共濮阳市委员会",
        "location": "河南省濮阳市清丰县",
    },
    {
        "id": 2,
        "name": "清丰县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "濮阳市人民政府",
        "location": "河南省濮阳市清丰县",
    },
    {
        "id": 3,
        "name": "清丰县人大常委会",
        "type": "人大",
        "level": "县",
        "parent": "濮阳市人大常委会",
        "location": "河南省濮阳市清丰县",
    },
    {
        "id": 4,
        "name": "政协清丰县委员会",
        "type": "政协",
        "level": "县",
        "parent": "政协濮阳市委员会",
        "location": "河南省濮阳市清丰县",
    },
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    {"person_id": 1001, "org_id": 1, "title": "清丰县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "2026年7月在任"},
    {"person_id": 1002, "org_id": 2, "title": "清丰县委副书记、县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "2026年7月在任。2026年2月11日在清丰县第十六届人民代表大会第六次会议上以代县长身份作政府工作报告"},
    {"person_id": 1003, "org_id": 1, "title": "清丰县委书记", "start_date": "~2021", "end_date": "~2025", "rank": "正处级", "note": "2024年5月在任。去向待查"},
    {"person_id": 1004, "org_id": 1, "title": "清丰县委书记", "start_date": "~2020", "end_date": "~2021", "rank": "正处级", "note": "2022年7月在任。去向待查"},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    {
        "person_a": 1001,
        "person_b": 1002,
        "type": "superior_subordinate",
        "context": "县委书记—县长搭班子",
        "overlap_org": "清丰县",
        "overlap_period": "2025~present",
    },
    {
        "person_a": 1001,
        "person_b": 1003,
        "type": "predecessor_successor",
        "context": "高尚功→胡志强，先后任清丰县委书记",
        "overlap_org": "中共清丰县委员会",
        "overlap_period": "~2025",
    },
    {
        "person_a": 1003,
        "person_b": 1004,
        "type": "predecessor_successor",
        "context": "曹拥军→高尚功，先后任清丰县委书记",
        "overlap_org": "中共清丰县委员会",
        "overlap_period": "~2021",
    },
]


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    staging = HERE  # data/tmp/henan_清丰县/
    db_path = staging / f"{SLUG}_network.db"
    gexf_path = staging / f"{SLUG}_network.gexf"

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )

    print(f"\n{'='*60}")
    print(f"  清丰县 数据构建完成")
    print(f"  DB:   {db_path}")
    print(f"  GEXF: {gexf_path}")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs:    {len(organizations)}")
    print(f"  Pos:     {len(positions)}")
    print(f"  Rel:     {len(relationships)}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
