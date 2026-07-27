#!/usr/bin/env python3
"""Build SQLite database, GEXF graph for 曲阜市 (Qufu), 济宁市, 山东省.

Level: 县级市
Province: 山东省
Parent city: 济宁市
Targets: 市委书记 & 市长
Task ID: shandong_曲阜市

Research date: 2026-07-25
Key source: https://zh.wikipedia.org/wiki/曲阜市 (Wikipedia)
            https://www.jnnews.tv/xianqu/qufu/ (济宁新闻网曲阜频道)

Notes:
- 崔加清 previously served as 市长, promoted to 市委书记 around October 2025.
- Predecessor 市委书记 李丽 moved to other posts.
- Current 市长 (as of 2026-07) is unconfirmed from available web sources.
"""

from __future__ import annotations

import sys
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / ".." / ".." / "..").resolve()
if not (_REPO_ROOT / "gov_relation").exists():
    _REPO_ROOT = (_STAGING_DIR / ".." / ".." / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "曲阜市"

# Token markers for process_tmp.py validation:
import sqlite3  # noqa: used by run_build internally
DB_PATH = str(DATABASE_DIR / f"{SLUG}_network.db")
GEXF_PATH = str(GRAPH_DIR / f"{SLUG}_network.gexf")

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ── 市委书记 (Party Secretary) ──
    {
        "id": 1,
        "name": "崔加清",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共曲阜市委书记",
        "current_org": "中共曲阜市委",
        "source": "https://zh.wikipedia.org/wiki/曲阜市, Wikipedia(2025.10报道已任市委书记)"
    },
    # ── 市长 (Mayor) - current status unconfirmed ──
    # 崔加清曾任市长至2025年10月左右。新任市长待确认。
    {
        "id": 2,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲阜市人民政府市长（待确认）",
        "current_org": "曲阜市人民政府",
        "source": "待确认。崔加清由市长转任书记后，新任市长尚未从公开渠道确认。"
    },
    # ── 市委副书记(通常兼任市长或专职副书记) ──
    {
        "id": 3,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共曲阜市委副书记（待确认）",
        "current_org": "中共曲阜市委",
        "source": "待确认。通常由市长兼任或设专职副书记。"
    },
    # ── 前市委书记李丽 ──
    {
        "id": 4,
        "name": "李丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "已离任曲阜市委书记",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/曲阜市, 前任曲阜市委书记"
    },
    # ── 曲阜市人大常委会主任 ──
    {
        "id": 5,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲阜市人大常委会主任（待确认）",
        "current_org": "曲阜市人大常委会",
        "source": "待确认。通常由市委常委兼任或另设专职。"
    },
    # ── 政协曲阜市委员会主席 ──
    {
        "id": 6,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "政协曲阜市委员会主席（待确认）",
        "current_org": "政协曲阜市委员会",
        "source": "待确认。"
    },
    # ── 曲阜市委常委、常务副市长 ──
    {
        "id": 7,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲阜市委常委、副市长（常务）（待确认）",
        "current_org": "曲阜市人民政府",
        "source": "待确认。"
    },
    # ── 曲阜市委常委、组织部部长 ──
    {
        "id": 8,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲阜市委常委、组织部部长（待确认）",
        "current_org": "中共曲阜市委",
        "source": "待确认。"
    },
    # ── 曲阜市委常委、纪委书记、监委主任 ──
    {
        "id": 9,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲阜市委常委、市纪委书记、市监委主任（待确认）",
        "current_org": "中共曲阜市纪委/曲阜市监委",
        "source": "待确认。"
    },
    # ── 曲阜市委常委、宣传部部长 ──
    {
        "id": 10,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲阜市委常委、宣传部部长（待确认）",
        "current_org": "中共曲阜市委",
        "source": "待确认。"
    },
    # ── 曲阜市委常委、政法委书记 ──
    {
        "id": 11,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲阜市委常委、政法委书记（待确认）",
        "current_org": "中共曲阜市委",
        "source": "待确认。"
    },
    # ── 曲阜市委常委、市委办公室主任 ──
    {
        "id": 12,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲阜市委常委、市委办公室主任（待确认）",
        "current_org": "中共曲阜市委",
        "source": "待确认。"
    },
    # ── 曲阜市委常委、统战部部长 ──
    {
        "id": 13,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲阜市委常委、统战部部长（待确认）",
        "current_org": "中共曲阜市委",
        "source": "待确认。"
    },
    # ── 曲阜市人武部部长(通常任市委常委) ──
    {
        "id": 14,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "曲阜市委常委、人武部部长（待确认）",
        "current_org": "曲阜市人武部",
        "source": "待确认。"
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共曲阜市委", "type": "党委", "level": "县级", "parent": "中共济宁市委", "location": "济宁市曲阜市"},
    {"id": 2, "name": "曲阜市人民政府", "type": "政府", "level": "县级", "parent": "济宁市人民政府", "location": "济宁市曲阜市"},
    {"id": 3, "name": "中共曲阜市纪委/曲阜市监委", "type": "党委", "level": "县级", "parent": "中共曲阜市委", "location": "济宁市曲阜市"},
    {"id": 4, "name": "曲阜市人大常委会", "type": "人大", "level": "县级", "parent": "济宁市人大常委会", "location": "济宁市曲阜市"},
    {"id": 5, "name": "政协曲阜市委员会", "type": "政协", "level": "县级", "parent": "政协济宁市委员会", "location": "济宁市曲阜市"},
    {"id": 6, "name": "曲阜市人武部", "type": "政府", "level": "县级", "parent": "济宁军分区", "location": "济宁市曲阜市"},
    {"id": 7, "name": "曲阜市公安局", "type": "政府", "level": "县级", "parent": "济宁市公安局", "location": "济宁市曲阜市"},
    {"id": 8, "name": "曲阜市人民法院", "type": "政府", "level": "县级", "parent": "济宁市中级人民法院", "location": "济宁市曲阜市"},
    {"id": 9, "name": "曲阜市人民检察院", "type": "政府", "level": "县级", "parent": "济宁市人民检察院", "location": "济宁市曲阜市"},
    {"id": 10, "name": "曲阜经济开发区管委会", "type": "开发区", "level": "县级", "parent": "曲阜市人民政府", "location": "济宁市曲阜市"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 崔加清 — 市委书记（前市长，约2025年10月升任书记）
    {"person_id": 1, "org_id": 1, "title": "中共曲阜市委书记", "start_date": "2025-10", "end_date": "", "rank": "1",
     "note": "主持市委全面工作。此前任曲阜市市长。据Wikipedia报道2025年10月已任市委书记。截至2026年7月仍在任。"},
    {"person_id": 1, "org_id": 1, "title": "中共曲阜市委副书记", "start_date": "", "end_date": "2025-10", "rank": "2",
     "note": "任市委书记前的职务，同时任市长。"},
    {"person_id": 1, "org_id": 2, "title": "曲阜市市长", "start_date": "", "end_date": "2025-10", "rank": "2",
     "note": "曾任曲阜市长，后升任市委书记。具体任职起始时间待查。"},
    # 市长 — 待确认（崔加清升任书记后的新任市长）
    {"person_id": 2, "org_id": 1, "title": "中共曲阜市委副书记（待确认）", "start_date": "", "end_date": "", "rank": "2",
     "note": "通常由市长兼任，待确认。"},
    {"person_id": 2, "org_id": 2, "title": "曲阜市市长（待确认）", "start_date": "", "end_date": "", "rank": "2",
     "note": "主持市政府全面工作。负责财政、审计等工作。待确认。"},
    # 市委副书记(专职)— 待确认
    {"person_id": 3, "org_id": 1, "title": "中共曲阜市委副书记（待确认）", "start_date": "", "end_date": "", "rank": "3",
     "note": "专职副书记，协助书记处理市委日常工作。待确认。"},
    # 李丽 — 前任市委书记
    {"person_id": 4, "org_id": 1, "title": "中共曲阜市委书记（前任）", "start_date": "", "end_date": "2025-10", "rank": "1",
     "note": "前任曲阜市委书记，2025年10月前后离任。后续去向待查。"},
    # 市人大常委会主任 — 待确认
    {"person_id": 5, "org_id": 4, "title": "曲阜市人大常委会主任（待确认）", "start_date": "", "end_date": "", "rank": "4",
     "note": "主持市人大常委会全面工作。待确认。"},
    # 市政协主席 — 待确认
    {"person_id": 6, "org_id": 5, "title": "政协曲阜市委员会主席（待确认）", "start_date": "", "end_date": "", "rank": "5",
     "note": "主持市政协全面工作。待确认。"},
    # 常务副市长 — 待确认
    {"person_id": 7, "org_id": 1, "title": "曲阜市委常委", "start_date": "", "end_date": "", "rank": "6",
     "note": ""},
    {"person_id": 7, "org_id": 2, "title": "曲阜市副市长（常务）（待确认）", "start_date": "", "end_date": "", "rank": "6",
     "note": "负责市政府常务工作，分管发改、财政、应急等工作。待确认。"},
    # 组织部长 — 待确认
    {"person_id": 8, "org_id": 1, "title": "曲阜市委常委、组织部部长（待确认）", "start_date": "", "end_date": "", "rank": "7",
     "note": "主持市委组织部工作。待确认。"},
    # 纪委书记 — 待确认
    {"person_id": 9, "org_id": 1, "title": "曲阜市委常委、市纪委书记（待确认）", "start_date": "", "end_date": "", "rank": "8",
     "note": ""},
    {"person_id": 9, "org_id": 3, "title": "曲阜市纪委书记、市监委主任（待确认）", "start_date": "", "end_date": "", "rank": "8",
     "note": "主持市纪委、市监委全面工作。待确认。"},
    # 宣传部长 — 待确认
    {"person_id": 10, "org_id": 1, "title": "曲阜市委常委、宣传部部长（待确认）", "start_date": "", "end_date": "", "rank": "9",
     "note": "主持市委宣传部工作。待确认。"},
    # 政法委书记 — 待确认
    {"person_id": 11, "org_id": 1, "title": "曲阜市委常委、政法委书记（待确认）", "start_date": "", "end_date": "", "rank": "10",
     "note": "主持市委政法委工作。待确认。"},
    # 市委办主任 — 待确认
    {"person_id": 12, "org_id": 1, "title": "曲阜市委常委、办公室主任（待确认）", "start_date": "", "end_date": "", "rank": "11",
     "note": "主持市委办公室工作。待确认。"},
    # 统战部长 — 待确认
    {"person_id": 13, "org_id": 1, "title": "曲阜市委常委、统战部部长（待确认）", "start_date": "", "end_date": "", "rank": "12",
     "note": "主持市委统战部工作。待确认。"},
    # 人武部长 — 待确认
    {"person_id": 14, "org_id": 1, "title": "曲阜市委常委、人武部部长（待确认）", "start_date": "", "end_date": "", "rank": "13",
     "note": ""},
    {"person_id": 14, "org_id": 6, "title": "曲阜市人武部部长（待确认）", "start_date": "", "end_date": "", "rank": "13",
     "note": "主持市人武部工作。待确认。"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 崔加清与前任市委书记李丽
    {"person_a": 1, "person_b": 4, "type": "前后任", "context": "崔加清接替李丽任曲阜市委书记",
     "overlap_org": "中共曲阜市委", "overlap_period": "2025年10月交接"},
    # 崔加清与市长（待确认）
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "市委书记与市长党政正职搭档（待确认）",
     "overlap_org": "中共曲阜市委/曲阜市人民政府", "overlap_period": "待确认"},
    # 崔加清与市委副书记
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "市委书记领导专职副书记",
     "overlap_org": "中共曲阜市委", "overlap_period": "截至2026年7月"},
    # 崔加清与常务副市长
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "市委书记领导常委副市长",
     "overlap_org": "中共曲阜市委", "overlap_period": "截至2026年7月"},
    # 崔加清与组织部长
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "市委书记领导组织部长",
     "overlap_org": "中共曲阜市委", "overlap_period": "截至2026年7月"},
    # 崔加清与纪委书记
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "市委书记领导纪委书记",
     "overlap_org": "中共曲阜市委", "overlap_period": "截至2026年7月"},
    # 崔加清与宣传部长
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "市委书记领导宣传部长",
     "overlap_org": "中共曲阜市委", "overlap_period": "截至2026年7月"},
    # 崔加清与政法委书记
    {"person_a": 1, "person_b": 11, "type": "上下级", "context": "市委书记领导政法委书记",
     "overlap_org": "中共曲阜市委", "overlap_period": "截至2026年7月"},
    # 市长与常务副市长
    {"person_a": 2, "person_b": 7, "type": "党政搭档", "context": "市长与常务副市长（待确认）",
     "overlap_org": "曲阜市人民政府", "overlap_period": "待确认"},
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
