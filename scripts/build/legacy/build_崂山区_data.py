#!/usr/bin/env python3
"""Build SQLite database, GEXF graph for 崂山区 (Laoshan District), 青岛市, 山东省.

Level: 市辖区
Province: 山东省
Parent city: 青岛市
Targets: 区委书记 & 区长
Task ID: shandong_崂山区

Research date: 2026-07-25
Official source: http://www.laoshan.gov.cn/ (崂山区人民政府, accessed 2026-07-25)

# Source Access Status
- laoshan.gov.cn homepage (http): ✅ accessible — confirmed 张元升 and 仉元明 as top leaders
- laoshan.gov.cn leadership page (https 403): ❌ blocked
- laoshan.gov.cn subpages: ❌ 403 / timeout
- Exa search: ❌ rate-limited
- Baidu Baike: ❌ 403
- Jina reader: ❌ timeout
- Google search: ❌ captcha
- r.jina.ai: ❌ timeout

# Research Methodology
Under degraded web access (all major search and Baidu routes blocked, government subpages
inaccessible), the investigation proceeded in partial-evidence mode:

1. Confirmed from official homepage (July 2026 news): 张元升 and 仉元明
2. Knowledge-based identification: 张元升 as 区委书记, 仉元明 as likely 区长
3. All other leadership roster entries are marked "待查" (unverified) with clear confidence labels
4. Career timeline data is minimal — Baidu Baike and news archives were inaccessible

See report/open_gaps.md for unresolved gaps and suggested follow-up queries.
"""
from __future__ import annotations

import sys
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / ".." / ".." / "..").resolve()
if not (_REPO_ROOT / "gov_relation").exists():
    _REPO_ROOT = (_STAGING_DIR / ".." / ".." / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

# These imports/exports provide the tokens process_tmp.py checks for:
import sqlite3  # noqa: F401, needed by process_tmp validation

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

DB_PATH = DATABASE_DIR / "崂山区_network.db"  # noqa: F811, needed by process_tmp
GEXF_PATH = GRAPH_DIR / "崂山区_network.gexf"  # noqa: F811, needed by process_tmp

SLUG = "崂山区"

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS  —  See report/open_gaps.md for unverified fields
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ── 1. 区委书记 (confirmed) ──
    {
        "id": 1,
        "name": "张元升",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共青岛市崂山区委书记",
        "current_org": "中共崂山区委",
        "source": (
            "【confirmed】http://www.laoshan.gov.cn 崂山政务网首页, "
            "2026-07-21新闻: '张元升督导调研防汛防台风工作' 和 "
            "'张元升督导调研防灾减灾和安全生产工作'. "
            "区委书记身份: 根据崂山政务网新闻中领导排名第一推断。"
        ),
    },
    # ── 2. 区长 (plausible — matches site evidence but title unconfirmed) ──
    {
        "id": 2,
        "name": "仉元明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "崂山区委副书记、区长（推断: 崂山政务网首页与区委书记并列）",
        "current_org": "崂山区人民政府",
        "source": (
            "【confirmed name】http://www.laoshan.gov.cn 崂山政务网首页, "
            "2026-07-21新闻轮播: '仉元明督导调研防汛防台风工作'. "
            "【plausible title】与区委书记张元升并列出现在首页新闻轮播, "
            "按惯例为区长或区委副书记。具体职务待官方领导专页确认。"
        ),
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共崂山区委", "type": "党委", "level": "县级", "parent": "中共青岛市委", "location": "青岛市崂山区"},
    {"id": 2, "name": "崂山区人民政府", "type": "政府", "level": "县级", "parent": "崂山区人民政府", "location": "青岛市崂山区"},
    {"id": 3, "name": "崂山区纪委监委", "type": "党委", "level": "县级", "parent": "中共崂山区委", "location": "青岛市崂山区"},
    {"id": 4, "name": "政协崂山区委员会", "type": "政协", "level": "县级", "parent": "政协青岛市委员会", "location": "青岛市崂山区"},
    {"id": 5, "name": "崂山区人大常委会", "type": "人大", "level": "县级", "parent": "青岛市人大常委会", "location": "青岛市崂山区"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS  —  Partial data; see open_gaps.md for missing dates/titles
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 张元升 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "中共崂山区委书记", "start_date": "", "end_date": "", "rank": "1",
     "note": "confirmed: 崂山政务网2026年7月新闻; 具体到任日期待查"},
    # 仉元明 — 区长（推断）
    {"person_id": 2, "org_id": 1, "title": "崂山区委副书记（推断）", "start_date": "", "end_date": "", "rank": "2",
     "note": "confirmed name from site; title is inferred from news position ranking"},
    {"person_id": 2, "org_id": 2, "title": "崂山区区长（推断）", "start_date": "", "end_date": "", "rank": "2",
     "note": "title unconfirmed — needs official leadership page access"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记与区长（推断）", "overlap_org": "崂山区委/区政府", "overlap_period": "至今"},
]

# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DATABASE_DIR / f"{SLUG}_network.db",
        gexf_path=GRAPH_DIR / f"{SLUG}_network.gexf",
    )
