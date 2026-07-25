#!/usr/bin/env python3
"""Build SQLite database, GEXF graph for 东营区 (Dongying District), 东营市, 山东省.

Level: 市辖区
Province: 山东省
Parent city: 东营市
Targets: 区委书记 & 区长
Task ID: shandong_东营区

Research date: 2026-07-25
Official source: http://www.dyq.gov.cn/ (东营区人民政府)
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

SLUG = "东营区"

# process_tmp tokens: sqlite3 is used via gov_relation.schema; DB_PATH and GEXF_PATH are below
DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ── 区委常委会 (District Party Standing Committee) ──
    {
        "id": 1,
        "name": "赵明印",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共东营区委书记、区委党校校长",
        "current_org": "中共东营区委",
        "source": "东营区人民政府官网(dyq.gov.cn)新闻(2026.07), 东营日报(2026.07)"
    },
    {
        "id": 2,
        "name": "燕雪英",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共东营区委副书记、区长、区政府党组书记",
        "current_org": "东营区人民政府",
        "source": "东营区人民政府官网(dyq.gov.cn)新闻(2026.06-07)"
    },
    {
        "id": 3,
        "name": "陈林廷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共东营区委常委、区纪委书记、区监委主任",
        "current_org": "中共东营区纪委/东营区监委",
        "source": "东营区人民政府官网(dyq.gov.cn)新闻(2026.06)"
    },
    {
        "id": 4,
        "name": "朱科峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共东营区委常委、副区长",
        "current_org": "中共东营区委/东营区人民政府",
        "source": "东营区人民政府官网(dyq.gov.cn)新闻(2026.06)"
    },
    {
        "id": 5,
        "name": "盖滨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共东营区委常委、副区长",
        "current_org": "中共东营区委/东营区人民政府",
        "source": "东营区人民政府官网(dyq.gov.cn)新闻(2026.06)"
    },
    # ── 其他区级领导 ──
    {
        "id": 6,
        "name": "杜书亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "东营区政协主席",
        "current_org": "政协东营区委员会",
        "source": "东营区人民政府官网(dyq.gov.cn)新闻(2026.07)"
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共东营区委", "type": "党委", "level": "县级", "parent": "中共东营市委", "location": "东营市东营区"},
    {"id": 2, "name": "东营区人民政府", "type": "政府", "level": "县级", "parent": "东营市人民政府", "location": "东营市东营区"},
    {"id": 3, "name": "中共东营区纪委/东营区监委", "type": "党委", "level": "县级", "parent": "中共东营区委/东营市纪委监委", "location": "东营市东营区"},
    {"id": 4, "name": "政协东营区委员会", "type": "政协", "level": "县级", "parent": "政协东营市委员会", "location": "东营市东营区"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 赵明印
    {"person_id": 1, "org_id": 1, "title": "中共东营区委书记、区委党校校长", "start_date": "", "end_date": "", "rank": "1", "note": "2026年7月在任"},
    # 燕雪英
    {"person_id": 2, "org_id": 1, "title": "中共东营区委副书记", "start_date": "", "end_date": "", "rank": "2", "note": "2026年6月在任"},
    {"person_id": 2, "org_id": 2, "title": "东营区区长、区政府党组书记", "start_date": "", "end_date": "", "rank": "2", "note": "2026年6月在任"},
    # 陈林廷
    {"person_id": 3, "org_id": 1, "title": "中共东营区委常委", "start_date": "", "end_date": "", "rank": "3", "note": ""},
    {"person_id": 3, "org_id": 3, "title": "区纪委书记、区监委主任", "start_date": "", "end_date": "", "rank": "3", "note": ""},
    # 朱科峰
    {"person_id": 4, "org_id": 1, "title": "中共东营区委常委", "start_date": "", "end_date": "", "rank": "4", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "东营区副区长", "start_date": "", "end_date": "", "rank": "4", "note": ""},
    # 盖滨
    {"person_id": 5, "org_id": 1, "title": "中共东营区委常委", "start_date": "", "end_date": "", "rank": "5", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "东营区副区长", "start_date": "", "end_date": "", "rank": "5", "note": ""},
    # 杜书亮
    {"person_id": 6, "org_id": 4, "title": "东营区政协主席", "start_date": "", "end_date": "", "rank": "1p", "note": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记与区长党政正职搭档", "overlap_org": "东营区委/区政府", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记领导纪委书记", "overlap_org": "中共东营区委", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区委书记领导区委常委、副区长", "overlap_org": "中共东营区委", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区委书记领导区委常委、副区长", "overlap_org": "中共东营区委", "overlap_period": "2026年至今"},
    {"person_a": 2, "person_b": 4, "type": "党政搭档", "context": "区长与副区长", "overlap_org": "东营区人民政府", "overlap_period": "2026年至今"},
    {"person_a": 2, "person_b": 5, "type": "党政搭档", "context": "区长与副区长", "overlap_org": "东营区人民政府", "overlap_period": "2026年至今"},
    {"person_a": 4, "person_b": 5, "type": "同级协作", "context": "同为区委常委、副区长", "overlap_org": "中共东营区委/东营区人民政府", "overlap_period": "2026年至今"},
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
