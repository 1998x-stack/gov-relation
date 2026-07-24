#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 三河市 (Sanhe City) leadership network.

三河市 is a county-level city under 廊坊市 (Langfang), 河北省 (Hebei).
Current leadership as of 2026-06 per Baidu Baike.

Research limitations:
- Web search (Exa) was rate-limited during this investigation.
- sanhe.gov.cn site consistently timed out.
- Biographical details for most figures are inferred from news reports.
- Mark all claims with explicit confidence levels.
"""

import sqlite3
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from gov_relation.runner import run_build

SLUG = "三河市"
TASK_DIR = Path(__file__).parent.resolve()

DB_PATH = TASK_DIR / "三河市_network.db"
GEXF_PATH = TASK_DIR / "三河市_network.gexf"

# ── PERSONS ────────────────────────────────────────────────────────────

persons = [
    # ═══════════════════════════════════════════════════════════════════
    # CURRENT TOP LEADERS (confirmed from Baidu Baike, as of 2026-06)
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "陈伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共三河市委书记",
        "current_org": "中共三河市委员会",
        "source": "https://baike.baidu.com/item/%E4%B8%89%E6%B2%B3%E5%B8%82/10175891",
    },
    {
        "id": 2,
        "name": "冉德龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "三河市人民政府市长",
        "current_org": "三河市人民政府",
        "source": "https://baike.baidu.com/item/%E4%B8%89%E6%B2%B3%E5%B8%82/10175891",
    },

    # ═══════════════════════════════════════════════════════════════════
    # PREDECESSORS
    # ═══════════════════════════════════════════════════════════════════
    # 付顺义 — predecessor 市委书记, moved to 三河 after 固安县委书记
    {
        "id": 3,
        "name": "付顺义",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "河北省廊坊市副市长（曾任三河市委书记）",
        "current_org": "廊坊市人民政府",
        "source": "https://baike.baidu.com/item/%E4%B8%89%E6%B2%B3%E5%B8%82/10175891",
    },
    # 伦绍金 — predecessor 市长
    {
        "id": 4,
        "name": "伦绍金",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（曾任三河市人民政府市长）",
        "current_org": "",
        "source": "",
    },

    # ═══════════════════════════════════════════════════════════════════
    # KEY DEPUTIES (standard county-level leadership team structure)
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": 5,
        "name": "崔浩泉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "三河市委常委、常务副市长（推测）",
        "current_org": "三河市人民政府",
        "source": "",
    },
    {
        "id": 6,
        "name": "燕来",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "三河市委常委、组织部部长（推测）",
        "current_org": "中共三河市委员会",
        "source": "",
    },
    {
        "id": 7,
        "name": "闫磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "三河市委常委、纪委书记、监委主任",
        "current_org": "中共三河市纪律检查委员会",
        "source": "",
    },
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共三河市委员会", "type": "党委", "level": "县级", "location": "河北省廊坊市三河市"},
    {"id": 2, "name": "三河市人民政府", "type": "政府", "level": "县级", "location": "河北省廊坊市三河市"},
    {"id": 3, "name": "中共三河市纪律检查委员会", "type": "党委", "level": "县级", "location": "河北省廊坊市三河市"},
    {"id": 4, "name": "廊坊市人民政府", "type": "政府", "level": "地级", "location": "河北省廊坊市"},
    {"id": 5, "name": "中共固安县委员会", "type": "党委", "level": "县级", "location": "河北省廊坊市固安县"},
]

# ── POSITIONS ─────────────────────────────────────────────────────────

positions = [
    # 陈伟
    {"person_id": 1, "org_id": 1, "title": "中共三河市委书记",
     "start": "", "end": "present", "rank": "正处级", "note": "现任，截至2026年6月"},
    # 冉德龙
    {"person_id": 2, "org_id": 2, "title": "三河市人民政府市长",
     "start": "", "end": "present", "rank": "正处级", "note": "现任，截至2026年6月"},
    # 付顺义 - predecessor 市委书记
    {"person_id": 3, "org_id": 1, "title": "中共三河市委书记（前任）",
     "start": "", "end": "", "rank": "正处级", "note": "前任市委书记"},
    {"person_id": 3, "org_id": 4, "title": "廊坊市副市长",
     "start": "", "end": "present", "rank": "副厅级", "note": "现任"},
    # 伦绍金 - predecessor 市长
    {"person_id": 4, "org_id": 2, "title": "三河市人民政府市长（前任）",
     "start": "", "end": "", "rank": "正处级", "note": "前任市长"},
    # 崔浩泉 - deputy
    {"person_id": 5, "org_id": 2, "title": "三河市委常委、常务副市长",
     "start": "", "end": "", "rank": "副处级", "note": "推测任职"},
    # 燕来 - deputy
    {"person_id": 6, "org_id": 1, "title": "三河市委常委、组织部部长",
     "start": "", "end": "", "rank": "副处级", "note": "推测任职"},
    # 闫磊 - discipline
    {"person_id": 7, "org_id": 3, "title": "三河市委常委、纪委书记、监委主任",
     "start": "", "end": "", "rank": "副处级", "note": ""},
]

# ── RELATIONSHIPS ─────────────────────────────────────────────────────

relationships = [
    # 陈伟 ↔ 冉德龙 (current partners in same city committee)
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "三河市委班子搭档，书记和市长",
        "overlap_org": "中共三河市委员会/三河市人民政府",
        "overlap_period": "",
    },
    # 付顺义 → 陈伟 (predecessor-successor, 市委书记)
    {
        "person_a": 3, "person_b": 1,
        "type": "predecessor_successor",
        "context": "付顺义卸任三河市委书记后由陈伟接任",
        "overlap_org": "中共三河市委员会",
        "overlap_period": "",
    },
    # 伦绍金 → 冉德龙 (predecessor-successor, 市长)
    {
        "person_a": 4, "person_b": 2,
        "type": "predecessor_successor",
        "context": "伦绍金卸任三河市长后由冉德龙接任",
        "overlap_org": "三河市人民政府",
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
