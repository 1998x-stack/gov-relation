#!/usr/bin/env python3
"""Build SQLite database, GEXF graph for 微山县 (Weishan County), 济宁市, 山东省.

Level: 县
Province: 山东省
Parent city: 济宁市
Targets: 县委书记 & 县长
Task ID: shandong_微山县

Research date: 2026-07-25
Official source: http://www.weishan.gov.cn/ (微山县人民政府)
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

SLUG = "微山县"

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ── 县委主要领导 ──
    {
        "id": 1,
        "name": "李勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共微山县委书记",
        "current_org": "中共微山县委",
        "source": "http://www.weishan.gov.cn/, 微山县政府门户网站新闻(2026.07)"
    },
    {
        "id": 2,
        "name": "郭鑫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "微山县委副书记、县长",
        "current_org": "微山县人民政府",
        "source": "http://www.weishan.gov.cn/, 微山县政府门户网站新闻(2026.07)"
    },
    # ── 县委常委 ──
    {
        "id": 3,
        "name": "田玉平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "微山县委常委、县纪委书记、县监委主任",
        "current_org": "中共微山县纪委/县监委",
        "source": "http://www.weishan.gov.cn/, 微山县政府门户网站新闻(2026.07)"
    },
    {
        "id": 4,
        "name": "徐征",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "微山县委常委、组织部部长",
        "current_org": "中共微山县委",
        "source": "http://www.weishan.gov.cn/, 微山县政府门户网站新闻(2026.07)"
    },
    {
        "id": 5,
        "name": "李晓娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "微山县领导（推测县委常委/副县长）",
        "current_org": "微山县人民政府/县委",
        "source": "http://www.weishan.gov.cn/, 微山县政府门户网站新闻(2026.06-07)"
    },
    {
        "id": 6,
        "name": "孔鲁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "微山县领导（推测县委常委/副县长）",
        "current_org": "微山县人民政府/县委",
        "source": "http://www.weishan.gov.cn/, 微山县政府门户网站新闻(2026.06)"
    },
    # ── 县政府领导 ──
    {
        "id": 7,
        "name": "李福厚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "微山县副县长",
        "current_org": "微山县人民政府",
        "source": "http://www.weishan.gov.cn/, 微山县政府门户网站新闻(2026.07)"
    },
    {
        "id": 8,
        "name": "曹勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "微山县人大常委会副主任（推测）",
        "current_org": "微山县人大常委会",
        "source": "http://www.weishan.gov.cn/, 微山县政府门户网站新闻(2026.07)"
    },
    {
        "id": 9,
        "name": "程敏",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "微山县领导",
        "current_org": "",
        "source": "http://www.weishan.gov.cn/, 微山县政府门户网站新闻(2026.07)"
    },
    {
        "id": 10,
        "name": "邵长岭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "微山县领导",
        "current_org": "",
        "source": "http://www.weishan.gov.cn/, 微山县政府门户网站新闻(2026.06-07)"
    },
    {
        "id": 11,
        "name": "张峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "微山县领导",
        "current_org": "",
        "source": "http://www.weishan.gov.cn/, 微山县政府门户网站新闻(2026.06)"
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共微山县委", "type": "党委", "level": "县级", "parent": "中共济宁市委", "location": "济宁市微山县"},
    {"id": 2, "name": "微山县人民政府", "type": "政府", "level": "县级", "parent": "济宁市人民政府", "location": "济宁市微山县"},
    {"id": 3, "name": "中共微山县纪委/县监委", "type": "党委", "level": "县级", "parent": "中共微山县委", "location": "济宁市微山县"},
    {"id": 4, "name": "微山县人大常委会", "type": "人大", "level": "县级", "parent": "济宁市人大常委会", "location": "济宁市微山县"},
    {"id": 5, "name": "政协微山县委员会", "type": "政协", "level": "县级", "parent": "政协济宁市委员会", "location": "济宁市微山县"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 李勇 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "中共微山县委书记", "start_date": "", "end_date": "", "rank": "1",
     "note": "主持县委全面工作。截至2026年7月在任。"},
    # 郭鑫 — 县长
    {"person_id": 2, "org_id": 1, "title": "微山县委副书记", "start_date": "", "end_date": "", "rank": "2",
     "note": ""},
    {"person_id": 2, "org_id": 2, "title": "微山县县长", "start_date": "", "end_date": "", "rank": "2",
     "note": "主持县政府全面工作。"},
    # 田玉平 — 纪委书记
    {"person_id": 3, "org_id": 1, "title": "微山县委常委、县纪委书记、县监委主任", "start_date": "", "end_date": "", "rank": "3",
     "note": ""},
    {"person_id": 3, "org_id": 3, "title": "微山县纪委书记、县监委主任", "start_date": "", "end_date": "", "rank": "3",
     "note": ""},
    # 徐征 — 组织部长
    {"person_id": 4, "org_id": 1, "title": "微山县委常委、组织部部长", "start_date": "", "end_date": "", "rank": "4",
     "note": ""},
    # 李晓娟 — 县领导
    {"person_id": 5, "org_id": 1, "title": "微山县领导", "start_date": "", "end_date": "", "rank": "5",
     "note": "具体职务待确认。2026年6月-7月出席多项县级会议。"},
    {"person_id": 5, "org_id": 2, "title": "微山县领导", "start_date": "", "end_date": "", "rank": "5",
     "note": "具体职务待确认。"},
    # 孔鲁 — 县领导
    {"person_id": 6, "org_id": 1, "title": "微山县领导", "start_date": "", "end_date": "", "rank": "6",
     "note": "具体职务待确认。2026年6月出席生态环保会议。"},
    # 李福厚 — 副县长
    {"person_id": 7, "org_id": 2, "title": "微山县副县长", "start_date": "", "end_date": "", "rank": "7",
     "note": "2026年7月17日出席高标准农田建设突出问题整治推进会议并主持。"},
    # 曹勇 — 推测为人大副主任
    {"person_id": 8, "org_id": 4, "title": "微山县人大常委会副主任（推测）", "start_date": "", "end_date": "", "rank": "8",
     "note": "2026年7月17日参加高标准农田建设会议，县人大常委会副主任列席。具体职务待确认。"},
    # 程敏 — 县领导
    {"person_id": 9, "org_id": 2, "title": "微山县领导", "start_date": "", "end_date": "", "rank": "9",
     "note": "2026年7月参加台风防范会议，具体职务待确认。"},
    # 邵长岭 — 县领导
    {"person_id": 10, "org_id": 2, "title": "微山县领导", "start_date": "", "end_date": "", "rank": "10",
     "note": "2026年6月-7月出席多项县级会议，具体职务待确认。"},
    # 张峰 — 县领导
    {"person_id": 11, "org_id": 2, "title": "微山县领导", "start_date": "", "end_date": "", "rank": "11",
     "note": "2026年6月参加生态环保会议，具体职务待确认。"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 党政正职关系
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "县委书记与县长党政正职搭档",
     "overlap_org": "微山县委/县政府",
     "overlap_period": "截至2026年7月"},
    # 县委常委会上下级关系
    {"person_a": 1, "person_b": 3, "type": "上下级",
     "context": "县委书记领导纪委书记",
     "overlap_org": "中共微山县委",
     "overlap_period": "截至2026年7月"},
    {"person_a": 1, "person_b": 4, "type": "上下级",
     "context": "县委书记领导组织部长",
     "overlap_org": "中共微山县委",
     "overlap_period": "截至2026年7月"},
    {"person_a": 1, "person_b": 5, "type": "上下级",
     "context": "县委书记领导县领导李晓娟",
     "overlap_org": "中共微山县委",
     "overlap_period": "截至2026年7月"},
    {"person_a": 1, "person_b": 6, "type": "上下级",
     "context": "县委书记领导县领导孔鲁",
     "overlap_org": "中共微山县委",
     "overlap_period": "截至2026年6月"},
    # 县长与副县长关系
    {"person_a": 2, "person_b": 7, "type": "上下级",
     "context": "县长领导副县长李福厚",
     "overlap_org": "微山县人民政府",
     "overlap_period": "截至2026年7月"},
    {"person_a": 2, "person_b": 5, "type": "上下级",
     "context": "县长领导县领导李晓娟",
     "overlap_org": "微山县人民政府",
     "overlap_period": "截至2026年7月"},
    {"person_a": 2, "person_b": 9, "type": "上下级",
     "context": "县长领导程敏",
     "overlap_org": "微山县人民政府",
     "overlap_period": "截至2026年7月"},
    # 书记与人大关系
    {"person_a": 1, "person_b": 8, "type": "同级协作",
     "context": "县委书记与人大常委会副主任",
     "overlap_org": "微山县四套班子",
     "overlap_period": "截至2026年7月"},
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
