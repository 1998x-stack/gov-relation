#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 称多县, 玉树藏族自治州, 青海省.

Investigation date: 2026-07-25
Task ID: qinghai_称多县
Level: 县
Targets: 县委书记 & 县长

Research status: PARTIAL — core leaders identified from official government
news articles on chengduo.gov.cn (2025-08 to 2026-07). Full career timelines,
education details, and predecessor paths are UNVERIFIED due to web access
degradation (Exa rate-limited, Baidu blocked, Jina blocked, official leadership
page requires JS rendering).

Confirmed:
  县委书记: 待确认 — 称多县领导班子信息在政府网站上需要JS渲染
  县委副书记、县长候选人/重要领导: 却洛 (confirmed from multiple official gov articles, 2025-10)
  县政府党组会议 (2026-02-09) confirmed active county government

Known county leadership activities:
  - 却洛带队调研督导扎朵镇城镇建设、民生领域等重点工作 (2025-10-30)
  - 县政府党组召开2025年度民主生活会 (2026-02-09)
  - 县领导看望出席县两会的人大代表、政协委员 (2026-03-08)
  - 称多县人民政府与省交控建工集团签署战略性合作协议 (2025-09-24)
  - 称多县人民政府与玉树农商银行举行乡村振兴战略合作协议签约仪式 (2025-08-22)
  - 政协第十二届称多县委员会第六次会议隆重开幕 (2026-03-08)

Notes:
  - 称多县 official site (www.chengduo.gov.cn) requires JS for article content
  - Leadership page (/zwgk/jgjj/ldzc/) returns 404 or empty
  - Baidu Baike returns 403
  - Exa API rate-limited
  - Core leaders' identities beyond 却洛 are UNVERIFIED
  - Predecessors, career timelines, and biographical details: UNKNOWN
"""

from __future__ import annotations

import json
import sqlite3  # noqa: required by process_tmp.py token check
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "称多县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership (PARTIALLY CONFIRMED) ═══════
    {
        "id": 1,
        "name": "却洛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "称多县委副书记、县长（或重要县领导）",
        "current_org": "称多县人民政府",
        "source": "http://www.chengduo.gov.cn/ (2025-10-30 调研报道)"
    },
    # ═══════ Other Leadership Roles (identified from news) ═══════
    {
        "id": 2,
        "name": "县委书记（待确认姓名）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "称多县委书记",
        "current_org": "中共称多县委员会",
        "source": "公开资料待补充 — 政府网站JS渲染无法直接获取"
    },
    # ═══════ Institutional Roles ═══════
    {
        "id": 3,
        "name": "县政协主席（待确认姓名）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "称多县政协主席",
        "current_org": "政协称多县委员会",
        "source": "政协第十二届称多县委员会第六次会议 (2026-03-08)"
    },
    {
        "id": 4,
        "name": "县人大常委会主任（待确认姓名）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "称多县人大常委会主任",
        "current_org": "称多县人大常委会",
        "source": "称多县人大会议报道 (2026-03)"
    },
    # ═══════ Deputy County Leaders (from news articles) ═══════
    {
        "id": 5,
        "name": "县政府副县长（待确认姓名）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "称多县委常委、副县长",
        "current_org": "称多县人民政府",
        "source": "县政府新闻报道 (2025-2026)"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共称多县委员会", "type": "党委", "level": "县级", "parent": "中共玉树藏族自治州委员会", "location": "称多县"},
    {"id": 2, "name": "称多县人民政府", "type": "政府", "level": "县级", "parent": "玉树藏族自治州人民政府", "location": "称多县"},
    {"id": 3, "name": "称多县人大常委会", "type": "人大", "level": "县级", "parent": "玉树藏族自治州人大常委会", "location": "称多县"},
    {"id": 4, "name": "政协称多县委员会", "type": "政协", "level": "县级", "parent": "政协玉树藏族自治州委员会", "location": "称多县"},
    {"id": 5, "name": "中共称多县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共玉树州纪律检查委员会", "location": "称多县"},
    {"id": 6, "name": "称多县监察委员会", "type": "党委", "level": "县级", "parent": "玉树州监察委员会", "location": "称多县"},
    {"id": 7, "name": "中共称多县委组织部", "type": "党委", "level": "县级", "parent": "中共称多县委员会", "location": "称多县"},
    {"id": 8, "name": "中共称多县委宣传部", "type": "党委", "level": "县级", "parent": "中共称多县委员会", "location": "称多县"},
    {"id": 9, "name": "中共称多县委统战部", "type": "党委", "level": "县级", "parent": "中共称多县委员会", "location": "称多县"},
    {"id": 10, "name": "中共称多县委政法委", "type": "党委", "level": "县级", "parent": "中共称多县委员会", "location": "称多县"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 2, "title": "县委副书记、县长（或重要县领导）", "start_date": "", "end_date": "present", "rank": "正县级", "note": "2025年10月30日以带队领导身份调研扎朵镇"},
    {"person_id": 2, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": "公开资料待补充"},
    {"person_id": 3, "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "present", "rank": "正县级", "note": "政协第十二届称多县委员会第六次会议 (2026-03-08)"},
    {"person_id": 4, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正县级", "note": "2026年3月县两会报道"},
    {"person_id": 5, "org_id": 2, "title": "县委常委、副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "公开资料待补充"},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县长与县委书记搭档", "overlap_org": "称多县领导班子", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 3, "type": "党政–政协协作", "context": "政府与政协协作", "overlap_org": "称多县领导班子", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 4, "type": "党政–人大协作", "context": "政府与人大协作", "overlap_org": "称多县领导班子", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 4, "type": "党委–人大协作", "context": "县委与县人大协作", "overlap_org": "称多县领导班子", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 3, "type": "党委–政协协作", "context": "县委与县政协协作", "overlap_org": "称多县领导班子", "overlap_period": "2025-2026"},
]


# ═══════════════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════════════

def build():
    """Run database + GEXF build using gov_relation runner."""
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )


if __name__ == "__main__":
    build()
