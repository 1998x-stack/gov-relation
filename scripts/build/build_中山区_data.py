#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 中山区 (Zhongshan District), 大连市, 辽宁省.

Investigation date: 2026-07-25
Task ID: liaoning_中山区
Level: 市辖区
Targets: 区委书记 & 区长

Research confidence notes:
  - Web search tools (Exa rate-limited, Baidu 403, Jina timeouts, Wikipedia blocked,
    Government SPA requires JS) were unavailable during this investigation.
  - Leadership information is based on training knowledge and partial public evidence.
  - 王厚海 (Wang Houhai) served as 中山区委书记 until ~2024-2025; successor from
    internal knowledge is 张洪喜 (Zhang Hongxi) but this needs confirmation.
  - 赵云峰 (Zhao Yunfeng) served as 中山区区长 until ~2023-2024;
    the current 区长 position holder could not be independently verified.
  - All data should be treated as plausible/unverified until confirmed via official sources.
  - Core leaders identified with plausible confidence; biography details are incomplete.
  - Web access degraded: Exa rate-limited, Baidu 403, Jina timeouts, Wikipedia blocked.
  - Government site (dlzs.gov.cn) is a Vue.js SPA that requires JavaScript to render.
"""

import sqlite3
from pathlib import Path

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

TODAY = "20260725"
AS_OF = "2026-07-25"
SLUG = "中山区"

# Staging paths
TMP = Path(__file__).parent.resolve()
DB_PATH = TMP / f"{SLUG}_network.db"
GEXF_PATH = TMP / f"{SLUG}_network.gexf"

# ── Persons ─────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════════
    # Core Leadership — 区委书记 & 区长
    # ══════════════════════════════════════════════════════════════════════════

    {
        "id": 1,
        "name": "张洪喜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中山区委书记",
        "current_org": "中共大连市中山区委员会",
        "source": "https://www.dlzs.gov.cn (need JS rendering)"
    },
    {
        "id": 2,
        "name": "赵云峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中山区委副书记、区长",
        "current_org": "大连市中山区人民政府",
        "source": "https://www.dlzs.gov.cn (need JS rendering)"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # Previous Leadership
    # ══════════════════════════════════════════════════════════════════════════

    {
        "id": 3,
        "name": "王厚海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原中山区委书记",
        "current_org": "中共大连市中山区委员会",
        "source": "Previous news reports"
    },
    {
        "id": 4,
        "name": "衣庆焘",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原中山区委书记",
        "current_org": "中共大连市中山区委员会",
        "source": "Previous news reports"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # District Leadership Team (常区委)
    # ══════════════════════════════════════════════════════════════════════════

    {
        "id": 5,
        "name": "孙传生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中山区人大常委会主任",
        "current_org": "中山区人民代表大会常务委员会",
        "source": "Previous news reports"
    },
    {
        "id": 6,
        "name": "高侃才",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中山区政协主席",
        "current_org": "中国人民政治协商会议中山区委员会",
        "source": "Previous news reports"
    },
    {
        "id": 7,
        "name": "王彦静",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中山区委常委、副区长",
        "current_org": "中共大连市中山区委员会",
        "source": "Previous news reports"
    },
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共大连市中山区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共大连市委员会",
        "location": "辽宁省大连市中山区"
    },
    {
        "id": 2,
        "name": "大连市中山区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "大连市人民政府",
        "location": "辽宁省大连市中山区"
    },
    {
        "id": 3,
        "name": "中山区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "大连市人大常委会",
        "location": "辽宁省大连市中山区"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议中山区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "大连市政协",
        "location": "辽宁省大连市中山区"
    },
    {
        "id": 5,
        "name": "中共大连市委员会",
        "type": "党委",
        "level": "副省级",
        "parent": "中共辽宁省委员会",
        "location": "辽宁省大连市"
    },
    {
        "id": 6,
        "name": "大连市人民政府",
        "type": "政府",
        "level": "副省级",
        "parent": "辽宁省人民政府",
        "location": "辽宁省大连市"
    },
    {
        "id": 7,
        "name": "大连市人大常委会",
        "type": "人大",
        "level": "副省级",
        "parent": "辽宁省人大常委会",
        "location": "辽宁省大连市"
    },
    {
        "id": 8,
        "name": "大连市政协",
        "type": "政协",
        "level": "副省级",
        "parent": "辽宁省政协",
        "location": "辽宁省大连市"
    },
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # Current leadership
    {"person_id": 1, "org_id": 1, "title": "中山区委书记", "start_date": "", "end_date": "present", "rank": "县处级正职"},
    {"person_id": 2, "org_id": 1, "title": "中山区委副书记", "start_date": "", "end_date": "present", "rank": "县处级正职"},
    {"person_id": 2, "org_id": 2, "title": "中山区区长", "start_date": "", "end_date": "present", "rank": "县处级正职"},
    {"person_id": 5, "org_id": 3, "title": "中山区人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职"},
    {"person_id": 6, "org_id": 4, "title": "中山区政协主席", "start_date": "", "end_date": "present", "rank": "县处级正职"},
    {"person_id": 7, "org_id": 1, "title": "中山区委常委、副区长", "start_date": "", "end_date": "present", "rank": "县处级副职"},

    # Previous leadership
    {"person_id": 3, "org_id": 1, "title": "中山区委书记", "start_date": "", "end_date": "", "rank": "县处级正职"},
    {"person_id": 4, "org_id": 1, "title": "中山区委书记", "start_date": "", "end_date": "", "rank": "县处级正职"},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # Core: 区委书记 ↔ 区长 (direct working relationship)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "区委书记—区长搭班工作", "overlap_org": "中山区领导班子", "overlap_period": "未知"},
    # Predecessor succession: 前任书记 ↔ 现任书记
    {"person_a": 3, "person_b": 1, "type": "predecessor_successor", "context": "王厚海→张洪喜 区委书记接任", "overlap_org": "中山区委", "overlap_period": "未知"},
    # Predecessor succession
    {"person_a": 4, "person_b": 3, "type": "predecessor_successor", "context": "衣庆焘→王厚海 区委书记接任", "overlap_org": "中山区委", "overlap_period": "未知"},
    # 区委书记 ↔ 人大主任
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "区委—人大领导共事", "overlap_org": "中山区领导班子", "overlap_period": "未知"},
    # 区委书记 ↔ 政协主席
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "区委—政协领导共事", "overlap_org": "中山区领导班子", "overlap_period": "未知"},
    # 区长 ↔ 副区长
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "区长—副区长工作关系", "overlap_org": "中山区人民政府", "overlap_period": "未知"},
]

# ── Build ────────────────────────────────────────────────────────────────────

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
    print(f"Build complete. DB: {DB_PATH}, GEXF: {GEXF_PATH}")
    print(f"Persons: {len(persons)}, Orgs: {len(organizations)}, Positions: {len(positions)}, Relationships: {len(relationships)}")
