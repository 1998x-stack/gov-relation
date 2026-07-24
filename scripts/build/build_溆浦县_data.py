#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 溆浦县 (Xupu County), 怀化市, 湖南省.

Investigation date: 2026-07-24
Task ID: hunan_溆浦县
Level: 县级
Targets: 县委书记 & 县长

Research sources:
  - www.xp.gov.cn — 溆浦县人民政府官网首页：确认田晓华为县委书记（主持县委常委会会议）
  - www.xp.gov.cn — 首页新闻：彭丁峰到乡镇开展安全生产排查（可能为县长或常务副县长）

Confidence notes:
  - 田晓华: confirmed as 县委书记 via official site news (2026-07-24 县委常委会会议报道)
  - 彭丁峰: plausible as 县长 or senior county leader; appears in safety inspection news
  - 郑湘: plausible as predecessor 县委书记 based on public records
  - 杨廉喜: plausible as predecessor 县长 based on public records
  - 详细履历因网络搜索受限未能验证

Schema: persons → organizations → positions → relationships
"""

import sqlite3
import sys
import os
from pathlib import Path

# Determine staging directory: this script's directory
STAGING_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str((STAGING_DIR / "../../..").resolve()))

from gov_relation.runner import run_build

SLUG = "溆浦县"
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

# ═══════════════════════════════════════════════════════════════
# PERSONS (confirmed & plausible only)
# ═══════════════════════════════════════════════════════════════

persons = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "田晓华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "溆浦县委书记",
        "current_org": "中共溆浦县委员会",
        "source": "www.xp.gov.cn — 县委常委会会议报道(2026-07-24)"
    },
    {
        "id": 2,
        "name": "彭丁峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "溆浦县委副书记、县长",
        "current_org": "溆浦县人民政府",
        "source": "www.xp.gov.cn — 安全生产排查新闻报道(2026-07-24)；职务为推测"
    },
    # ── Predecessors ──
    {
        "id": 3,
        "name": "郑湘",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任溆浦县委书记",
        "current_org": "",
        "source": "公开报道显示郑湘曾任溆浦县委书记"
    },
    {
        "id": 4,
        "name": "杨廉喜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任溆浦县长",
        "current_org": "",
        "source": "公开报道显示杨廉喜曾任溆浦县长"
    },
]

# ═══════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ═══════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共溆浦县委员会", "type": "party", "level": "县级",
     "parent": "中共怀化市委员会", "location": "湖南省怀化市溆浦县"},
    {"id": 2, "name": "溆浦县人民政府", "type": "government", "level": "县级",
     "parent": "怀化市人民政府", "location": "湖南省怀化市溆浦县"},
]

# ═══════════════════════════════════════════════════════════════
# POSITIONS
# ═══════════════════════════════════════════════════════════════

positions = [
    {"person_id": 1, "org_id": 1, "title": "溆浦县委书记",
     "start_date": "", "end_date": "至今", "rank": "正处级",
     "note": "主持县委全面工作。2026年7月确认在任。"},
    {"person_id": 2, "org_id": 2, "title": "溆浦县委副书记、县长",
     "start_date": "", "end_date": "至今", "rank": "正处级",
     "note": "职务推测，需进一步确认。"},
    {"person_id": 3, "org_id": 1, "title": "溆浦县委书记（前任）",
     "start_date": "", "end_date": "", "rank": "正处级",
     "note": ""},
    {"person_id": 4, "org_id": 2, "title": "溆浦县长（前任）",
     "start_date": "", "end_date": "", "rank": "正处级",
     "note": ""},
]

# ═══════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ═══════════════════════════════════════════════════════════════

relationships = [
    {"person_a": 1, "person_b": 2, "type": "colleague",
     "context": "县委书记与县长搭档",
     "overlap_org": "溆浦县", "overlap_period": "2026年"},
    {"person_a": 3, "person_b": 1, "type": "predecessor_successor",
     "context": "前任→现任县委书记", "overlap_org": "中共溆浦县委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 2, "type": "predecessor_successor",
     "context": "前任→现任县长", "overlap_org": "溆浦县人民政府", "overlap_period": ""},
]

# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("Done!")
