#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 冀州区 (Jizhou District) leadership network.

冀州区 is a district under 衡水市 (Hengshui), 河北省 (Hebei).
Current leadership as of 2024-2026.

Research limitations:
- All web search channels (Exa rate-limited, Baidu 403/captcha, jizhou.gov.cn timeout, Jina timeout)
  were unavailable during this investigation.
- Biographical details are sourced from training data (last updated 2025-04) and may lag.
- Mark all claims with explicit confidence levels.
- Open gaps documented in person JSON files and report/open_gaps.md.
"""

import sys
import os
import sqlite3
from pathlib import Path

# Add project root to path
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from gov_relation.runner import run_build

SLUG = "冀州区"
TASK_DIR = Path(__file__).parent.resolve()

DB_PATH = TASK_DIR / "冀州区_network.db"
GEXF_PATH = TASK_DIR / "冀州区_network.gexf"

# ── PERSONS ────────────────────────────────────────────────────────────

persons = [
    # ═══════════════════════════════════════════════════════════════════
    # CURRENT TOP LEADERS (plausible from training data, as of 2024-2025)
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "张洪涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共衡水市冀州区委书记",
        "current_org": "中共衡水市冀州区委员会",
        "source": "Training data (2025-04); web search unavailable for verification",
    },
    {
        "id": 2,
        "name": "门保彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "衡水市冀州区人民政府区长",
        "current_org": "衡水市冀州区人民政府",
        "source": "Training data (2025-04); web search unavailable for verification",
    },

    # ═══════════════════════════════════════════════════════════════════
    # PREDECESSORS
    # ═══════════════════════════════════════════════════════════════════
    # 贾宏迅 — predecessor 区委书记, moved to 衡水市副市长/衡水高新区
    {
        "id": 3,
        "name": "贾宏迅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "衡水市人民政府副市长（曾任冀州区委书记）",
        "current_org": "衡水市人民政府",
        "source": "Training data (2025-04)",
    },
    # 张赤峰 — predecessor 区长 (2021)
    {
        "id": 4,
        "name": "张赤峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（曾任冀州区人民政府区长）",
        "current_org": "",
        "source": "Training data (2025-04)",
    },
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共衡水市冀州区委员会", "type": "党委", "level": "县级", "location": "河北省衡水市冀州区"},
    {"id": 2, "name": "衡水市冀州区人民政府", "type": "政府", "level": "县级", "location": "河北省衡水市冀州区"},
    {"id": 3, "name": "衡水市人民政府", "type": "政府", "level": "地级", "location": "河北省衡水市"},
]

# ── POSITIONS ─────────────────────────────────────────────────────────

positions = [
    # 张洪涛 - 区委书记
    {"person_id": 1, "org_id": 1, "title": "中共衡水市冀州区委书记",
     "start": "", "end": "present", "rank": "正处级", "note": "现任，约2021年起任；web search unavailable"},
    # 门保彬 - 区长
    {"person_id": 2, "org_id": 2, "title": "衡水市冀州区人民政府区长",
     "start": "", "end": "present", "rank": "正处级", "note": "现任，约2021年起任；web search unavailable"},
    # 贾宏迅 - predecessor 区委书记
    {"person_id": 3, "org_id": 1, "title": "中共衡水市冀州区委书记（前任）",
     "start": "", "end": "", "rank": "正处级", "note": "前任区委书记，后任衡水市副市长"},
    {"person_id": 3, "org_id": 3, "title": "衡水市人民政府副市长",
     "start": "", "end": "present", "rank": "副厅级", "note": "现任"},
    # 张赤峰 - predecessor 区长
    {"person_id": 4, "org_id": 2, "title": "衡水市冀州区人民政府区长（前任）",
     "start": "", "end": "", "rank": "正处级", "note": "前任区长"},
]

# ── RELATIONSHIPS ─────────────────────────────────────────────────────

relationships = [
    # 张洪涛 ↔ 门保彬 (current partners in same district committee)
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "冀州区委班子搭档，区委书记和区长",
        "overlap_org": "中共衡水市冀州区委员会/冀州区人民政府",
        "overlap_period": "约2021-至今",
    },
    # 贾宏迅 → 张洪涛 (predecessor-successor, 区委书记)
    {
        "person_a": 3, "person_b": 1,
        "type": "predecessor_successor",
        "context": "贾宏迅卸任冀州区委书记后由张洪涛接任",
        "overlap_org": "中共衡水市冀州区委员会",
        "overlap_period": "",
    },
    # 张赤峰 → 门保彬 (predecessor-successor, 区长)
    {
        "person_a": 4, "person_b": 2,
        "type": "predecessor_successor",
        "context": "张赤峰卸任冀州区区长后由门保彬接任",
        "overlap_org": "衡水市冀州区人民政府",
        "overlap_period": "",
    },
]

# ── RUN ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=str(DB_PATH),
        gexf_path=str(GEXF_PATH),
        overwrite=True,
    )
    print(f"\nDone. DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
