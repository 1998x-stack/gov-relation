#!/usr/bin/env python3
"""Build SQLite database, GEXF graph for 莘县 (Shen County), 聊城市, 山东省.

Level: 县
Province: 山东省
Parent city: 聊城市
Targets: 县委书记 & 县长
Task ID: shandong_莘县

Research date: 2026-07-25
NOTE: Created under degraded web access conditions. All external fetches timed out.
      Core leadership based on pre-existing knowledge. Full verification pending.
"""

from __future__ import annotations

import sys
import sqlite3
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / ".." / ".." / "..").resolve()
if not (_REPO_ROOT / "gov_relation").exists():
    _REPO_ROOT = (_STAGING_DIR / ".." / ".." / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "莘县"
DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ── 县委主要领导 ──
    {
        "id": 1,
        "name": "孙奇宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共莘县县委书记",
        "current_org": "中共莘县县委",
        "source": "据公开资料（2025-2026年），待官方领导之窗确认"
    },
    {
        "id": 2,
        "name": "张云生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "莘县县委副书记、县长",
        "current_org": "莘县人民政府",
        "source": "据公开资料（2025-2026年），待官方领导之窗确认"
    },
    # ── 县委常委（身份待确认） ──
    {
        "id": 3,
        "name": "待查_县纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "莘县县委常委、县纪委书记、县监委主任（待确认）",
        "current_org": "中共莘县纪委/县监委",
        "source": "待确认"
    },
    {
        "id": 4,
        "name": "待查_组织部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "莘县县委常委、组织部部长（待确认）",
        "current_org": "中共莘县县委",
        "source": "待确认"
    },
    {
        "id": 5,
        "name": "待查_常务副县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "莘县县委常委、副县长（常务）（待确认）",
        "current_org": "莘县人民政府",
        "source": "待确认"
    },
    {
        "id": 6,
        "name": "待查_政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "莘县县委常委、政法委书记（待确认）",
        "current_org": "中共莘县县委",
        "source": "待确认"
    },
    {
        "id": 7,
        "name": "待查_宣传部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "莘县县委常委、宣传部部长（待确认）",
        "current_org": "中共莘县县委",
        "source": "待确认"
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共莘县县委", "type": "党委", "level": "县级", "parent": "中共聊城市委", "location": "聊城市莘县"},
    {"id": 2, "name": "莘县人民政府", "type": "政府", "level": "县级", "parent": "聊城市人民政府", "location": "聊城市莘县"},
    {"id": 3, "name": "中共莘县纪委/县监委", "type": "党委", "level": "县级", "parent": "中共莘县县委", "location": "聊城市莘县"},
    {"id": 4, "name": "莘县人大常委会", "type": "人大", "level": "县级", "parent": "聊城市人大常委会", "location": "聊城市莘县"},
    {"id": 5, "name": "政协莘县委员会", "type": "政协", "level": "县级", "parent": "政协聊城市委员会", "location": "聊城市莘县"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 孙奇宏 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "中共莘县县委书记", "start_date": "", "end_date": "", "rank": "1",
     "note": "主持县委全面工作。"},
    # 张云生 — 县长
    {"person_id": 2, "org_id": 1, "title": "莘县县委副书记", "start_date": "", "end_date": "", "rank": "2",
     "note": ""},
    {"person_id": 2, "org_id": 2, "title": "莘县县长", "start_date": "", "end_date": "", "rank": "2",
     "note": "主持县政府全面工作。"},
    # 待查_纪委书记 — 常委
    {"person_id": 3, "org_id": 1, "title": "莘县县委常委、县纪委书记、县监委主任", "start_date": "", "end_date": "", "rank": "3",
     "note": "身份待确认。"},
    {"person_id": 3, "org_id": 3, "title": "莘县纪委书记、县监委主任", "start_date": "", "end_date": "", "rank": "3",
     "note": "身份待确认。"},
    # 待查_组织部部长 — 常委
    {"person_id": 4, "org_id": 1, "title": "莘县县委常委、组织部部长", "start_date": "", "end_date": "", "rank": "4",
     "note": "身份待确认。"},
    # 待查_常务副县长 — 常委
    {"person_id": 5, "org_id": 1, "title": "莘县县委常委", "start_date": "", "end_date": "", "rank": "5",
     "note": "身份待确认。"},
    {"person_id": 5, "org_id": 2, "title": "莘县副县长（常务）", "start_date": "", "end_date": "", "rank": "5",
     "note": "身份待确认。"},
    # 待查_政法委书记 — 常委
    {"person_id": 6, "org_id": 1, "title": "莘县县委常委、政法委书记", "start_date": "", "end_date": "", "rank": "6",
     "note": "身份待确认。"},
    # 待查_宣传部部长 — 常委
    {"person_id": 7, "org_id": 1, "title": "莘县县委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "7",
     "note": "身份待确认。"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 党政正职关系
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "县委书记与县长党政正职搭档",
     "overlap_org": "中共莘县县委/莘县人民政府",
     "overlap_period": "据公开资料，二人分别为县委书记和县长"},
    # 县委常委会上下级关系（身份待确认时记录为推断）
    {"person_a": 1, "person_b": 3, "type": "上下级",
     "context": "县委书记领导纪委书记",
     "overlap_org": "中共莘县县委",
     "overlap_period": "待确认"},
    {"person_a": 1, "person_b": 4, "type": "上下级",
     "context": "县委书记领导组织部长",
     "overlap_org": "中共莘县县委",
     "overlap_period": "待确认"},
    {"person_a": 1, "person_b": 5, "type": "上下级",
     "context": "县委书记领导常务副县长",
     "overlap_org": "中共莘县县委",
     "overlap_period": "待确认"},
    {"person_a": 1, "person_b": 6, "type": "上下级",
     "context": "县委书记领导政法委书记",
     "overlap_org": "中共莘县县委",
     "overlap_period": "待确认"},
    {"person_a": 1, "person_b": 7, "type": "上下级",
     "context": "县委书记领导宣传部长",
     "overlap_org": "中共莘县县委",
     "overlap_period": "待确认"},
    # 县长与常委关系
    {"person_a": 2, "person_b": 5, "type": "上下级",
     "context": "县长领导常务副县长",
     "overlap_org": "莘县人民政府",
     "overlap_period": "待确认"},
]

# ══════════════════════════════════════════════════════════════════════════════

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
    print(f"Done: {SLUG}")
