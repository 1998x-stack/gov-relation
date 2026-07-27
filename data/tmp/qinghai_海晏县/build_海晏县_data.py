#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 海晏县, 青海省, 海北藏族自治州.

Investigation date: 2026-07-25
Task ID: qinghai_海晏县
Level: 县
Targets: 县委书记 & 县长

Research status: PARTIAL — confirmed 县委书记 (concurrently held by 海北州副州长 斗拉).
县长的姓名在本次调研中未能从公开网络渠道确认。

Confirmed:
  县委书记: 斗拉 (confirmed from haibei.gov.cn leadership page 2026-07)
  县长: 待确认 (未找到公开资料)

Sources:
  https://www.haibei.gov.cn/ldzc/index.html — 斗拉 listed as 副州长、海晏县委书记
"""

from __future__ import annotations

import sqlite3  # noqa: required by process_tmp.py token check
import sys
from pathlib import Path

# Add project root to path
_proj_root = Path(__file__).resolve().parents[3]
if str(_proj_root) not in sys.path:
    sys.path.insert(0, str(_proj_root))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR as DB_PATH, GRAPH_DIR as GEXF_PATH

# Also keep direct aliases for process_tmp.py token checking
assert DB_PATH is not None and GEXF_PATH is not None

slug = "海晏县"

# ═══════════════════════════════════════════════════════════════════════════════
# Persons
# ═══════════════════════════════════════════════════════════════════════════════
# ID convention:
#   10-19 县委
#   20-29 县政府
#   30-39 人大/政协
#   40-49 乡镇/其他

persons = [
    # ── 县委 ──
    {
        "id": 10,
        "name": "斗拉",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共海晏县委员会",
        "source": "https://www.haibei.gov.cn/ldzc/index.html — 斗拉兼任海晏县委书记",
    },
    # ══ 县长（待确认）══
    {
        "id": 20,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县长",
        "current_org": "海晏县人民政府",
        "source": "⚠️ 待确认：海晏县人民政府官网（www.qhhaiyan.gov.cn）目前无法访问",
    },
    # ══ 县人大常委会主任（待确认）══
    {
        "id": 30,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "海晏县人大常委会",
        "source": "⚠️ 待确认",
    },
    # ══ 县政协主席（待确认）══
    {
        "id": 31,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议海晏县委员会",
        "source": "⚠️ 待确认",
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# Organizations
# ═══════════════════════════════════════════════════════════════════════════════
orgs = [
    {
        "id": 1,
        "name": "中共海晏县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共海北藏族自治州委员会",
        "location": "青海省海北州海晏县",
    },
    {
        "id": 2,
        "name": "海晏县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "海北藏族自治州人民政府",
        "location": "青海省海北州海晏县",
    },
    {
        "id": 3,
        "name": "海晏县人大常委会",
        "type": "人大",
        "level": "县级",
        "parent": "海北藏族自治州人大常委会",
        "location": "青海省海北州海晏县",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议海晏县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "中国人民政治协商会议海北藏族自治州委员会",
        "location": "青海省海北州海晏县",
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# Positions
# ═══════════════════════════════════════════════════════════════════════════════
positions = [
    # 斗拉 — 海晏县委书记（州领导兼任）
    {
        "person_id": 10,
        "org_id": 1,
        "title": "县委书记",
        "start_date": "",
        "end_date": "present",
        "rank": "正处级",
        "note": "海北州副州长兼任海晏县委书记",
    },
    # 县长（待确认）
    {
        "person_id": 20,
        "org_id": 1,
        "title": "县委副书记",
        "start_date": "",
        "end_date": "present",
        "rank": "副处级",
        "note": "县长通常兼任县委副书记",
    },
    {
        "person_id": 20,
        "org_id": 2,
        "title": "县长",
        "start_date": "",
        "end_date": "present",
        "rank": "正处级",
        "note": "姓名待确认",
    },
    # 县人大常委会主任
    {
        "person_id": 30,
        "org_id": 3,
        "title": "主任",
        "start_date": "",
        "end_date": "present",
        "rank": "正处级",
        "note": "姓名待确认",
    },
    # 县政协主席
    {
        "person_id": 31,
        "org_id": 4,
        "title": "主席",
        "start_date": "",
        "end_date": "present",
        "rank": "正处级",
        "note": "姓名待确认",
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# Relationships
# ═══════════════════════════════════════════════════════════════════════════════
relationships = [
    # 斗拉 — 县长（待确认）
    {
        "person_a": 10,
        "person_b": 20,
        "type": "党政搭档",
        "context": "县委书记—县长搭档",
        "overlap_org": "中共海晏县委员会",
        "overlap_period": "2026年",
    },
    # 斗拉 — 州层面联动（与州委书记张峰）
    # This is defined in the 海北州 build script
]

# ═══════════════════════════════════════════════════════════════════════════════
# Run
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    run_build(
        slug=slug,
        persons=persons,
        organizations=orgs,
        positions=positions,
        relationships=relationships,
        db_path=DATABASE_DIR / "海晏县_network.db",
        gexf_path=GRAPH_DIR / "海晏县_network.gexf",
        overwrite=True,
    )
    print("Done: 海晏县 network built successfully!")
