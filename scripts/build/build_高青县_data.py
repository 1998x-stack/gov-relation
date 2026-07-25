#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 高青县, 淄博市, 山东省.

Investigation date: 2026-07-25
Task ID: shandong_高青县
Level: 县
Targets: 县委书记 & 县长

IMPORTANT: Web research was severely degraded — Exa rate-limited, Baidu 403,
government site (www.gaoqing.gov.cn) unreachable, Jina Reader blocked.
This build uses partial evidence from Wikipedia and general knowledge.
All uncertain claims are explicitly labeled.

Key findings (from partial evidence):
- 县委书记: 待查 (web research blocked — need re-investigation)
- 县长: 待查 (web research blocked — need re-investigation)
- 高青县建制: confirmed from Wikipedia (zh.wikipedia.org)
- 行政区划: 2街道7镇 confirmed

Confidence notes:
- NO current leader names confirmed via accessible web sources
- All leadership data marked as unverified
- This build creates the scaffolding; needs follow-up research
"""

import json
import os
import sqlite3  # noqa: F401
import sys
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from gov_relation.runner import run_build  # noqa: E402

SLUG = "高青县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

STAGING_DIR = Path(BASE)
DB_PATH = str(STAGING_DIR / f"{SLUG}_network.db")
GEXF_PATH = str(STAGING_DIR / f"{SLUG}_network.gexf")

# ═══════════════════════════════════════════════════════════════════════════════
# Data
# ═══════════════════════════════════════════════════════════════════════════════

# Note: All leaders are marked as unverified because web search was blocked.
# Names marked "待查" need follow-up research.

persons_data = [
    # ══════════════════════════════════════════════════════════════════════════
    # Party Committee (县委) Leadership - CURRENT
    # ══════════════════════════════════════════════════════════════════════════

    # 县委书记 — Current Party Secretary of Gaoqing County
    # WEB SEARCH WAS BLOCKED — NAME UNAVAILABLE
    {
        "id": 1,
        "name": "待查（县委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "高青县委书记",
        "current_org": "中共高青县委员会",
        "source": "unverified — web search blocked (Exa rate-limited, Baidu 403, gov site unreachable)"
    },
    # 县长 — Current County Mayor of Gaoqing County
    {
        "id": 2,
        "name": "待查（县长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "高青县人民政府县长",
        "current_org": "高青县人民政府",
        "source": "unverified — web search blocked (Exa rate-limited, Baidu 403, gov site unreachable)"
    },
    # 县委副书记（分管日常工作的副书记）
    {
        "id": 3,
        "name": "待查（县委副书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "高青县委副书记",
        "current_org": "中共高青县委员会",
        "source": "unverified — web search blocked"
    },
    # 县委常委、常务副县长
    {
        "id": 4,
        "name": "待查（常务副县长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "高青县委常委、常务副县长",
        "current_org": "高青县人民政府",
        "source": "unverified — web search blocked"
    },
    # 县委常委、组织部部长
    {
        "id": 5,
        "name": "待查（组织部部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "高青县委常委、组织部部长",
        "current_org": "中共高青县委组织部",
        "source": "unverified — web search blocked"
    },
    # 县委常委、纪委书记、监委主任
    {
        "id": 6,
        "name": "待查（纪委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "高青县委常委、纪委书记、县监委主任",
        "current_org": "中共高青县纪律检查委员会",
        "source": "unverified — web search blocked"
    },
    # 县委常委、政法委书记
    {
        "id": 7,
        "name": "待查（政法委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "高青县委常委、政法委书记",
        "current_org": "中共高青县委政法委员会",
        "source": "unverified — web search blocked"
    },
    # 县委常委、宣传部部长
    {
        "id": 8,
        "name": "待查（宣传部部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "高青县委常委、宣传部部长",
        "current_org": "中共高青县委宣传部",
        "source": "unverified — web search blocked"
    },
    # 县委常委、县委办公室主任
    {
        "id": 9,
        "name": "待查（县委办公室主任）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "高青县委常委、县委办公室主任",
        "current_org": "中共高青县委办公室",
        "source": "unverified — web search blocked"
    },
    # 县委常委、统战部部长
    {
        "id": 10,
        "name": "待查（统战部部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "高青县委常委、统战部部长",
        "current_org": "中共高青县委统战部",
        "source": "unverified — web search blocked"
    },
    # 县委常委、人武部政委
    {
        "id": 11,
        "name": "待查（人武部政委）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "高青县委常委、县人武部政委",
        "current_org": "高青县人民武装部",
        "source": "unverified — web search blocked"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # Government (县政府) - Additional members
    # ══════════════════════════════════════════════════════════════════════════

    # 副县长、县公安局局长
    {
        "id": 12,
        "name": "待查（副县长兼公安局长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "高青县人民政府副县长、县公安局局长",
        "current_org": "高青县公安局",
        "source": "unverified — web search blocked"
    },
    # 副县长（分管日常工作外其他领域）
    {
        "id": 13,
        "name": "待查（副县长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "高青县人民政府副县长",
        "current_org": "高青县人民政府",
        "source": "unverified — web search blocked"
    },
    {
        "id": 14,
        "name": "待查（副县长2）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "高青县人民政府副县长",
        "current_org": "高青县人民政府",
        "source": "unverified — web search blocked"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 人大 (County People's Congress)
    # ══════════════════════════════════════════════════════════════════════════

    # 县人大常委会主任
    {
        "id": 15,
        "name": "待查（人大常委会主任）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "高青县人大常委会主任",
        "current_org": "高青县人民代表大会常务委员会",
        "source": "unverified — web search blocked"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 政协 (CPPCC)
    # ══════════════════════════════════════════════════════════════════════════

    # 县政协主席
    {
        "id": 16,
        "name": "待查（政协主席）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "高青县政协主席",
        "current_org": "政协高青县委员会",
        "source": "unverified — web search blocked"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 司法机构
    # ══════════════════════════════════════════════════════════════════════════

    # 县人民法院院长
    {
        "id": 17,
        "name": "待查（法院院长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "高青县人民法院院长",
        "current_org": "高青县人民法院",
        "source": "unverified — web search blocked"
    },
    # 县人民检察院检察长
    {
        "id": 18,
        "name": "待查（检察院检察长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "高青县人民检察院检察长",
        "current_org": "高青县人民检察院",
        "source": "unverified — web search blocked"
    },
]

organizations_data = [
    {
        "id": 1,
        "name": "中共高青县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共淄博市委员会",
        "location": "山东省淄博市高青县",
    },
    {
        "id": 2,
        "name": "高青县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "淄博市人民政府",
        "location": "山东省淄博市高青县",
    },
    {
        "id": 3,
        "name": "高青县人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "淄博市人民代表大会常务委员会",
        "location": "山东省淄博市高青县",
    },
    {
        "id": 4,
        "name": "政协高青县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协淄博市委员会",
        "location": "山东省淄博市高青县",
    },
    {
        "id": 5,
        "name": "高青县人民法院",
        "type": "司法",
        "level": "县处级",
        "parent": "淄博市中级人民法院",
        "location": "山东省淄博市高青县",
    },
    {
        "id": 6,
        "name": "高青县人民检察院",
        "type": "司法",
        "level": "县处级",
        "parent": "淄博市人民检察院",
        "location": "山东省淄博市高青县",
    },
    {
        "id": 7,
        "name": "中共高青县委组织部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共高青县委员会",
        "location": "山东省淄博市高青县",
    },
    {
        "id": 8,
        "name": "中共高青县委宣传部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共高青县委员会",
        "location": "山东省淄博市高青县",
    },
    {
        "id": 9,
        "name": "中共高青县委统战部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共高青县委员会",
        "location": "山东省淄博市高青县",
    },
    {
        "id": 10,
        "name": "中共高青县委政法委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共高青县委员会",
        "location": "山东省淄博市高青县",
    },
    {
        "id": 11,
        "name": "中共高青县委办公室",
        "type": "党委",
        "level": "县处级",
        "parent": "中共高青县委员会",
        "location": "山东省淄博市高青县",
    },
    {
        "id": 12,
        "name": "中共高青县纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共高青县委员会",
        "location": "山东省淄博市高青县",
    },
    {
        "id": 13,
        "name": "高青县人民武装部",
        "type": "政府",
        "level": "县处级",
        "parent": "淄博军分区",
        "location": "山东省淄博市高青县",
    },
    {
        "id": 14,
        "name": "高青县公安局",
        "type": "政府",
        "level": "乡科级",
        "parent": "高青县人民政府",
        "location": "山东省淄博市高青县",
    },
    {
        "id": 15,
        "name": "高青经济开发区",
        "type": "开发区",
        "level": "县处级",
        "parent": "高青县人民政府",
        "location": "山东省淄博市高青县",
    },
]

positions_data = [
    # ═══ 县委书记 (待查) ═══
    {
        "person_id": 1,
        "org_id": 1,
        "title": "高青县委书记",
        "start_date": "unknown",
        "end_date": "现任",
        "rank": "县处级正职",
        "note": "需要进一步调研确认姓名和到任时间",
    },

    # ═══ 县长 (待查) ═══
    {
        "person_id": 2,
        "org_id": 1,
        "title": "高青县委副书记",
        "start_date": "unknown",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "需要进一步调研确认姓名和到任时间",
    },
    {
        "person_id": 2,
        "org_id": 2,
        "title": "高青县人民政府县长",
        "start_date": "unknown",
        "end_date": "现任",
        "rank": "县处级正职",
        "note": "需要进一步调研确认姓名和到任时间",
    },

    # ═══ 县委副书记 (待查) ═══
    {
        "person_id": 3,
        "org_id": 1,
        "title": "高青县委副书记",
        "start_date": "unknown",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "需要进一步调研确认姓名和到任时间",
    },

    # ═══ 常务副县长 (待查) ═══
    {
        "person_id": 4,
        "org_id": 1,
        "title": "高青县委常委",
        "start_date": "unknown",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "",
    },
    {
        "person_id": 4,
        "org_id": 2,
        "title": "高青县人民政府常务副县长",
        "start_date": "unknown",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "需要进一步调研确认姓名",
    },

    # ═══ 组织部部长 (待查) ═══
    {
        "person_id": 5,
        "org_id": 1,
        "title": "高青县委常委",
        "start_date": "unknown",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "",
    },
    {
        "person_id": 5,
        "org_id": 7,
        "title": "高青县委组织部部长",
        "start_date": "unknown",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "需要进一步调研确认姓名",
    },

    # ═══ 纪委书记 (待查) ═══
    {
        "person_id": 6,
        "org_id": 1,
        "title": "高青县委常委",
        "start_date": "unknown",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "",
    },
    {
        "person_id": 6,
        "org_id": 12,
        "title": "高青县纪委书记、县监委主任",
        "start_date": "unknown",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "需要进一步调研确认姓名",
    },

    # ═══ 政法委书记 (待查) ═══
    {
        "person_id": 7,
        "org_id": 1,
        "title": "高青县委常委",
        "start_date": "unknown",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "",
    },
    {
        "person_id": 7,
        "org_id": 10,
        "title": "高青县委政法委书记",
        "start_date": "unknown",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "需要进一步调研确认姓名",
    },

    # ═══ 宣传部部长 (待查) ═══
    {
        "person_id": 8,
        "org_id": 1,
        "title": "高青县委常委",
        "start_date": "unknown",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "",
    },
    {
        "person_id": 8,
        "org_id": 8,
        "title": "高青县委宣传部部长",
        "start_date": "unknown",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "需要进一步调研确认姓名",
    },

    # ═══ 县委办公室主任 (待查) ═══
    {
        "person_id": 9,
        "org_id": 1,
        "title": "高青县委常委",
        "start_date": "unknown",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "",
    },
    {
        "person_id": 9,
        "org_id": 11,
        "title": "高青县委办公室主任",
        "start_date": "unknown",
        "end_date": "现任",
        "rank": "乡科级正职",
        "note": "需要进一步调研确认姓名",
    },

    # ═══ 统战部部长 (待查) ═══
    {
        "person_id": 10,
        "org_id": 1,
        "title": "高青县委常委",
        "start_date": "unknown",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "",
    },
    {
        "person_id": 10,
        "org_id": 9,
        "title": "高青县委统战部部长",
        "start_date": "unknown",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "需要进一步调研确认姓名",
    },

    # ═══ 人武部政委 (待查) ═══
    {
        "person_id": 11,
        "org_id": 1,
        "title": "高青县委常委",
        "start_date": "unknown",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "",
    },
    {
        "person_id": 11,
        "org_id": 13,
        "title": "高青县人武部政委",
        "start_date": "unknown",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "需要进一步调研确认姓名",
    },

    # ═══ 副县长兼公安局长 (待查) ═══
    {
        "person_id": 12,
        "org_id": 2,
        "title": "高青县人民政府副县长",
        "start_date": "unknown",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "",
    },
    {
        "person_id": 12,
        "org_id": 14,
        "title": "高青县公安局局长",
        "start_date": "unknown",
        "end_date": "现任",
        "rank": "乡科级正职",
        "note": "需要进一步调研确认姓名",
    },

    # ═══ 副县长 (待查) ═══
    {
        "person_id": 13,
        "org_id": 2,
        "title": "高青县人民政府副县长",
        "start_date": "unknown",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "需要进一步调研确认姓名",
    },
    {
        "person_id": 14,
        "org_id": 2,
        "title": "高青县人民政府副县长",
        "start_date": "unknown",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "需要进一步调研确认姓名",
    },

    # ═══ 人大常委会主任 (待查) ═══
    {
        "person_id": 15,
        "org_id": 3,
        "title": "高青县人大常委会主任",
        "start_date": "unknown",
        "end_date": "现任",
        "rank": "县处级正职",
        "note": "需要进一步调研确认姓名",
    },

    # ═══ 政协主席 (待查) ═══
    {
        "person_id": 16,
        "org_id": 4,
        "title": "高青县政协主席",
        "start_date": "unknown",
        "end_date": "现任",
        "rank": "县处级正职",
        "note": "需要进一步调研确认姓名",
    },

    # ═══ 法院院长 (待查) ═══
    {
        "person_id": 17,
        "org_id": 5,
        "title": "高青县人民法院院长",
        "start_date": "unknown",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "需要进一步调研确认姓名",
    },

    # ═══ 检察院检察长 (待查) ═══
    {
        "person_id": 18,
        "org_id": 6,
        "title": "高青县人民检察院检察长",
        "start_date": "unknown",
        "end_date": "现任",
        "rank": "县处级副职",
        "note": "需要进一步调研确认姓名",
    },
]

relationships_data = [
    # ═══ 县委书记 ↔ 县长 —— 党政搭档 ═══
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长党政搭档",
        "overlap_org": "中共高青县委员会",
        "overlap_period": "现任",
    },

    # ═══ 县委书记 ↔ 县委副书记 ═══
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记与县委副书记",
        "overlap_org": "中共高青县委员会",
        "overlap_period": "现任",
    },

    # ═══ 县委书记 ↔ 常委成员 ═══
    {
        "person_a": 1,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "县委书记与常务副县长",
        "overlap_org": "中共高青县委员会",
        "overlap_period": "现任",
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "县委书记与组织部部长",
        "overlap_org": "中共高青县委员会",
        "overlap_period": "现任",
    },
    {
        "person_a": 1,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "县委书记与纪委书记",
        "overlap_org": "中共高青县委员会",
        "overlap_period": "现任",
    },
    {
        "person_a": 1,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "县委书记与政法委书记",
        "overlap_org": "中共高青县委员会",
        "overlap_period": "现任",
    },
    {
        "person_a": 1,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "县委书记与宣传部部长",
        "overlap_org": "中共高青县委员会",
        "overlap_period": "现任",
    },
    {
        "person_a": 1,
        "person_b": 9,
        "type": "superior_subordinate",
        "context": "县委书记与县委办公室主任",
        "overlap_org": "中共高青县委员会",
        "overlap_period": "现任",
    },
    {
        "person_a": 1,
        "person_b": 10,
        "type": "superior_subordinate",
        "context": "县委书记与统战部部长",
        "overlap_org": "中共高青县委员会",
        "overlap_period": "现任",
    },
    {
        "person_a": 1,
        "person_b": 11,
        "type": "superior_subordinate",
        "context": "县委书记与人武部政委",
        "overlap_org": "中共高青县委员会",
        "overlap_period": "现任",
    },

    # ═══ 县长 ↔ 副县长们 ═══
    {
        "person_a": 2,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "县长与常务副县长",
        "overlap_org": "高青县人民政府",
        "overlap_period": "现任",
    },
    {
        "person_a": 2,
        "person_b": 12,
        "type": "superior_subordinate",
        "context": "县长与副县长、公安局长",
        "overlap_org": "高青县人民政府",
        "overlap_period": "现任",
    },
    {
        "person_a": 2,
        "person_b": 13,
        "type": "superior_subordinate",
        "context": "县长与副县长",
        "overlap_org": "高青县人民政府",
        "overlap_period": "现任",
    },
    {
        "person_a": 2,
        "person_b": 14,
        "type": "superior_subordinate",
        "context": "县长与副县长",
        "overlap_org": "高青县人民政府",
        "overlap_period": "现任",
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON helpers
# ═══════════════════════════════════════════════════════════════════════════════

def make_person_json(person: dict) -> dict:
    """Generate the deep person JSON for a single person."""
    pid = f"gaoqing_{person['name']}"
    
    career_entries = []
    for pos in positions_data:
        if pos["person_id"] == person["id"]:
            org_name = ""
            for org in organizations_data:
                if org["id"] == pos["org_id"]:
                    org_name = org["name"]
                    break
            career_entries.append({
                "start": pos.get("start_date", ""),
                "end": pos.get("end_date", ""),
                "org": org_name,
                "title": pos.get("title", ""),
                "level": pos.get("rank", ""),
                "notes": pos.get("note", ""),
                "confidence": "unverified",
            })

    relationships_list = []
    for rel in relationships_data:
        other_id = None
        if rel["person_a"] == person["id"]:
            other_id = rel["person_b"]
        elif rel["person_b"] == person["id"]:
            other_id = rel["person_a"]
        if other_id:
            other_person = None
            for p in persons_data:
                if p["id"] == other_id:
                    other_person = p
                    break
            if other_person:
                relationships_list.append({
                    "person": other_person["name"],
                    "person_id": f"gaoqing_{other_person['name']}",
                    "relationship_type": rel.get("type", ""),
                    "strength": "strong" if rel.get("type") in ("superior_subordinate", "predecessor_successor") else "medium",
                    "evidence": rel.get("context", ""),
                    "overlap_org": rel.get("overlap_org", ""),
                    "overlap_period": rel.get("overlap_period", ""),
                    "direction": "undirected",
                    "confidence": "unverified",
                })

    source_urls = []
    if person.get("source"):
        for s in person["source"].split(";"):
            s = s.strip()
            if s:
                source_urls.append({"label": s[:80], "url": "", "note": ""})

    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "山东省",
            "city": "淄博市",
            "region": "高青县",
            "job": person.get("current_post", ""),
            "task_id": "shandong_高青县",
            "time_focus": "2024-2026",
        },
        "identity": {
            "person_id": pid,
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("birthplace", ""),
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth', 'unknown')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace', 'unknown')}",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": False,
        },
        "career_timeline": career_entries,
        "organizations": [{"org_id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations_data],
        "relationships": relationships_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "公开资料不足，无法推断工作风格",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至调研日未发现公开违规违纪记录（调研时Web搜索受限）",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": [{"id": "S001", "title": "Web research blocked — no external sources accessible", "url": "", "publisher": "", "published_at": "", "accessed_at": AS_OF, "source_type": "inferred", "reliability": "low"}],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": f"{person['name']}的姓名、完整履历均需重新调研",
        },
        "open_questions": [
            {"priority": "critical", "question": f"{person['name']}的真实姓名", "why_it_matters": "核心人物身份未确认", "suggested_queries": [f"高青县 {person['current_post']}"], "last_attempted": AS_OF},
            {"priority": "critical", "question": f"{person['name']}的完整职业履历", "why_it_matters": "核心人物履历完整性", "suggested_queries": [f"高青县 {person['current_post']} 简历"], "last_attempted": AS_OF},
        ],
    }


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    # ── Build DB + GEXF ──
    run_build(
        slug=SLUG,
        persons=persons_data,
        organizations=organizations_data,
        positions=positions_data,
        relationships=relationships_data,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # ── Write person JSONs for core leaders ──
    # Core person IDs: 1(县委书记), 2(县长)
    # Since names are all "待查", we write minimal placeholder JSONs
    core_ids = [1, 2]
    for pid in core_ids:
        person = None
        for p in persons_data:
            if p["id"] == pid:
                person = p
                break
        if person:
            job_slug = person["current_post"].split("、")[0] if person["current_post"] else "unknown"
            filename = f"{TODAY}-山东省-淄博市-{job_slug}-待查.json"
            filepath = STAGING_DIR / filename
            data = make_person_json(person)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Person JSON: {filepath}")

    print(f"\nDB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"Persons: {len(persons_data)}")
    print(f"Organizations: {len(organizations_data)}")
    print(f"Positions: {len(positions_data)}")
    print(f"Relationships: {len(relationships_data)}")
    print("Done.")


if __name__ == "__main__":
    main()
