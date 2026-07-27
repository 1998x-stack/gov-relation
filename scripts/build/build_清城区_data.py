#!/usr/bin/env python3
"""Build script for 清城区 (Qingcheng District, Qingyuan, Guangdong) leadership network.

Generated: 2026-07-22
Sources:
  - www.qingcheng.gov.cn (official government website - news articles confirming区委书记)
  - 2026年清城区政府工作报告 (delivered by 区长 庄志辉 on 2026-02-11)
"""

import sqlite3  # noqa: used by gov_relation.runner

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

# fmt: off
PERSONS = [
    # Core targets
    {
        "id": 1,
        "name": "廖家杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "清城区委书记",
        "current_org": "中共清远市清城区委员会",
        "source": "http://www.qingcheng.gov.cn/xxgk/zwdt/qcyw/content/post_2166378.html (confirmed as 区委书记 as of 2026-07-09)",
    },
    {
        "id": 2,
        "name": "庄志辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "清城区区长",
        "current_org": "清远市清城区人民政府",
        "source": "http://www.qingcheng.gov.cn/xxgk/zjgb/zfgzbg/content/post_2120806.html (delivered 2026年政府工作报告 as 区长 on 2026-02-11)",
    },
    # Key deputies - 区委常委/副区长 (partial, from typical district structure)
    # Note: Complete leadership roster requires official leadership page access
    {
        "id": 3,
        "name": "常务副区长（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "清远市清城区人民政府",
        "source": "placeholder - leadership page unavailable",
    },
    {
        "id": 4,
        "name": "区人大常委会主任（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "清远市清城区人大常委会",
        "source": "placeholder - leadership page unavailable",
    },
    {
        "id": 5,
        "name": "区政协主席（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议清远市清城区委员会",
        "source": "placeholder - leadership page unavailable",
    },
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共清远市清城区委员会", "type": "党委", "level": "正处级", "parent": "中共清远市委员会", "location": "清远市清城区"},
    {"id": 2, "name": "清远市清城区人民政府", "type": "政府", "level": "正处级", "parent": "清远市人民政府", "location": "清远市清城区"},
    {"id": 3, "name": "清远市清城区人大常委会", "type": "人大", "level": "正处级", "parent": "清远市人大常委会", "location": "清远市清城区"},
    {"id": 4, "name": "中国人民政治协商会议清远市清城区委员会", "type": "政协", "level": "正处级", "parent": "清远市政协", "location": "清远市清城区"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 1, "title": "清城区委书记", "start_date": "", "end_date": "present", "rank": "正处级/副厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "清城区区长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "同时兼任区委副书记、区政府党组书记"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "区委常委、区政府党组副书记"},
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 5, "org_id": 4, "title": "区政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
]

# Relationships based on organizational overlap and working proximity
RELATIONSHIPS = [
    # 党政正职
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "区委书记-区长党政正职搭档", "overlap_org": "清城区四套班子", "overlap_period": "2025-2026年", "source": "", "confidence": "confirmed"},
    # 区委书记与区委常委
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记—区委常委（常务副区长）", "overlap_org": "清城区委常委会", "overlap_period": "2025-2026年", "source": "", "confidence": "plausible"},
    # 区长与常务副区长
    {"person_a": 2, "person_b": 3, "type": "党政副职搭档", "context": "区长—常务副区长", "overlap_org": "清城区人民政府", "overlap_period": "2025-2026年", "source": "", "confidence": "plausible"},
    # 四套班子正职
    {"person_a": 1, "person_b": 4, "type": "同僚", "context": "区委书记—区人大常委会主任", "overlap_org": "清城区四套班子", "overlap_period": "2025-2026年", "source": "", "confidence": "plausible"},
    {"person_a": 1, "person_b": 5, "type": "同僚", "context": "区委书记—区政协主席", "overlap_org": "清城区四套班子", "overlap_period": "2025-2026年", "source": "", "confidence": "plausible"},
    {"person_a": 2, "person_b": 4, "type": "同僚", "context": "区长—区人大常委会主任", "overlap_org": "清城区四套班子", "overlap_period": "2025-2026年", "source": "", "confidence": "plausible"},
    {"person_a": 2, "person_b": 5, "type": "同僚", "context": "区长—区政协主席", "overlap_org": "清城区四套班子", "overlap_period": "2025-2026年", "source": "", "confidence": "plausible"},
]

# fmt: on

# ═══════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════

DB_PATH = DATABASE_DIR / "清城区_network.db"
GEXF_PATH = GRAPH_DIR / "清城区_network.gexf"

if __name__ == "__main__":
    run_build(
        slug="清城区",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
