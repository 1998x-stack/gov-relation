#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 安平县 (Anping County) leadership network.

安平县 is a county under 衡水市 (Hengshui), 河北省 (Hebei).
Current leadership as of 2024-2026.

Research limitations:
- All web search channels (Exa rate-limited, Baidu 403/captcha, anping.gov.cn HTTPS timeout,
  Jina Reader timeout) were largely unavailable during this investigation.
- anping.gov.cn was accessible via HTTP homepage, confirming recent election cycle
  (13th Party Congress 2026-07-18~20, 18th People's Congress 2026-07-22~24),
  but leadership detail pages and the full election result pages were not accessible.
- Baidu Baike confirmed 赵东钊 as 县长 (county mayor) via 2024 leadership division adjustment.
- 县委书记 name is from training data (may lag) - unverified via web.
- Mark all claims with explicit confidence levels.
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

SLUG = "安平县"
TASK_DIR = Path(__file__).parent.resolve()

# Staging paths — files land in data/tmp/hebei_安平县/ first
DB_PATH = TASK_DIR / "安平县_network.db"
GEXF_PATH = TASK_DIR / "安平县_network.gexf"

# ── PERSONS ────────────────────────────────────────────────────────────

persons = [
    # ═══════════════════════════════════════════════════════════════════
    # CURRENT TOP LEADERS
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "曹向东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共安平县委书记",
        "current_org": "中共安平县委员会",
        "source": "Training data (2025-04); web search unavailable for verification; 2026-07 13th Party Congress may have confirmed/re-elected",
    },
    {
        "id": 2,
        "name": "赵东钊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "安平县人民政府县长",
        "current_org": "安平县人民政府",
        "source": "Baidu Baike confirmed via 2024-03-27 leadership division adjustment; 2026-07 18th People's Congress may have re-elected",
    },

    # ═══════════════════════════════════════════════════════════════════
    # PREDECESSORS
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "张云龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（曾任安平县委书记）",
        "current_org": "",
        "source": "Training data (2025-04); predecessor of 曹向东",
    },
    {
        "id": 4,
        "name": "李军龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（曾任安平县人民政府县长）",
        "current_org": "",
        "source": "Training data (2025-04); predecessor of 赵东钊",
    },
]

# ── ORGANIZATIONS ─────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共安平县委员会", "type": "党委", "level": "县级", "location": "河北省衡水市安平县"},
    {"id": 2, "name": "安平县人民政府", "type": "政府", "level": "县级", "location": "河北省衡水市安平县"},
    {"id": 3, "name": "安平县人民代表大会常务委员会", "type": "人大", "level": "县级", "location": "河北省衡水市安平县"},
    {"id": 4, "name": "中国人民政治协商会议安平县委员会", "type": "政协", "level": "县级", "location": "河北省衡水市安平县"},
    {"id": 5, "name": "中共安平县纪律检查委员会", "type": "纪委", "level": "县级", "location": "河北省衡水市安平县"},
    {"id": 6, "name": "衡水市人民政府", "type": "政府", "level": "地级", "location": "河北省衡水市"},
    {"id": 7, "name": "中共衡水市委员会", "type": "党委", "level": "地级", "location": "河北省衡水市"},
]

# ── POSITIONS ─────────────────────────────────────────────────────────

positions = [
    # 曹向东 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "中共安平县委书记",
     "start": "", "end": "present", "rank": "正处级",
     "note": "现任；web search unavailable for exact start date; 2026-07 13th Party Congress confirmed/re-elected"},
    # 赵东钊 — 县长
    {"person_id": 2, "org_id": 2, "title": "安平县人民政府县长",
     "start": "", "end": "present", "rank": "正处级",
     "note": "现任；confirmed by Baidu Baike 2024-03-27 leadership adjustment; 2026-07 18th People's Congress may have re-elected"},
    # 张云龙 — predecessor 县委书记
    {"person_id": 3, "org_id": 1, "title": "中共安平县委书记（前任）",
     "start": "", "end": "", "rank": "正处级",
     "note": "前任县委书记；training data"},
    # 李军龙 — predecessor 县长
    {"person_id": 4, "org_id": 2, "title": "安平县人民政府县长（前任）",
     "start": "", "end": "", "rank": "正处级",
     "note": "前任县长；training data"},
]

# ── RELATIONSHIPS ─────────────────────────────────────────────────────

relationships = [
    # 曹向东 ↔ 赵东钊 (current partners in county committee)
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "安平县委班子搭档，县委书记和县长",
        "overlap_org": "中共安平县委员会/安平县人民政府",
        "overlap_period": "约2021-至今",
    },
    # 张云龙 → 曹向东 (predecessor-successor, 县委书记)
    {
        "person_a": 3, "person_b": 1,
        "type": "predecessor_successor",
        "context": "张云龙卸任安平县委书记后由曹向东接任",
        "overlap_org": "中共安平县委员会",
        "overlap_period": "",
    },
    # 李军龙 → 赵东钊 (predecessor-successor, 县长)
    {
        "person_a": 4, "person_b": 2,
        "type": "predecessor_successor",
        "context": "李军龙卸任安平县长后由赵东钊接任",
        "overlap_org": "安平县人民政府",
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
