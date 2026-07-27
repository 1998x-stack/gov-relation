#!/usr/bin/env python3
"""
宽城区（长春市）领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Kuancheng District leadership.

Level: 市辖区 — 副厅级
Province: 吉林省
Parent city: 长春市
Targets: 区委书记 & 区长

Sources:
- baike.baidu.com/item/%E5%AE%BD%E5%9F%8E%E5%8C%BA (accessed 2026-07-25)
  Confirmed current leadership: 区委书记 高文禄, 区长 刘百军 (as of June 2026)
"""

import os
import sys
import sqlite3
from datetime import datetime

# Ensure gov_relation package is importable
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

# ── Persons ──
# id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start,
# current_post, current_org, source

PERSONS = [
    # ═══ 区委书记 ═══
    {
        "id": 1,
        "name": "高文禄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共长春市宽城区委员会",
        "source": "baike.baidu.com/item/宽城区 (2026-07-25, 截至2026年6月)",
    },
    # ═══ 区长 ═══
    {
        "id": 2,
        "name": "刘百军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区长",
        "current_org": "长春市宽城区人民政府",
        "source": "baike.baidu.com/item/宽城区 (2026-07-25, 截至2026年6月)",
    },
]

# ── Organizations ──
# id, name, type, level, parent, location

ORGANIZATIONS = [
    {
        "id": 1,
        "name": "中共长春市宽城区委员会",
        "type": "党委",
        "level": "副厅级",
        "parent": "中共长春市委",
        "location": "长春市宽城区",
    },
    {
        "id": 2,
        "name": "长春市宽城区人民政府",
        "type": "政府",
        "level": "副厅级",
        "parent": "长春市人民政府",
        "location": "长春市宽城区",
    },
]

# ── Positions ──
# person_id, org_id, title, start, end, rank, note

POSITIONS = [
    # 高文禄 — 区委书记
    {
        "person_id": 1,
        "org_id": 1,
        "title": "区委书记",
        "start": "",
        "end": "至今",
        "rank": "副厅级",
        "note": "主持区委全面工作。具体上任时间待查。公开资料显示截至2026年6月在任。",
    },
    # 刘百军 — 区长
    {
        "person_id": 2,
        "org_id": 2,
        "title": "区长",
        "start": "",
        "end": "至今",
        "rank": "副厅级",
        "note": "主持区政府全面工作。具体上任时间待查。公开资料显示截至2026年6月在任。",
    },
]

# ── Relationships ──
# person_a, person_b, type, context, overlap_org, overlap_period

RELATIONSHIPS = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记与区长党政正职搭档",
        "overlap_org": "中共长春市宽城区委员会/长春市宽城区人民政府",
        "overlap_period": "任期内重叠",
    },
]

# ════════════════════════════════════════════
# BUILD
# ════════════════════════════════════════════

DB_PATH = os.path.join(SCRIPT_DIR, "宽城区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "宽城区_network.gexf")

if __name__ == "__main__":
    run_build(
        slug="宽城区",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("[DONE] Build complete.")
