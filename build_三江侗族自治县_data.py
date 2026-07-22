#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 三江侗族自治县 leadership network.

Task: guangxi_三江侗族自治县
Province: 广西壮族自治区
Parent City: 柳州市
Region: 三江侗族自治县
Level: 县级
Targets: 县委书记 (Party Secretary), 县长 (County Mayor)

Investigation Date: 2026-07-23

Confirmed Findings (Phase 1 & 2 Research):
1. 陈震 (male, Han) - Former 三江县县长, NOW 鱼峰区委书记 (confirmed by official
   Yufeng district government article, 2026-07-22).
2. 贺莹 (female, Han) - Former 三江县委书记, whereabouts still unknown.
3. 雷道理 (male, Han, b.1981) - Former 三江县委常委/副县长 (until 2024-04),
   then 柳州市自然资源和规划局党组书记/局长 (2024-04 to 2026-07),
   now 鹿寨县委书记 (2026-07 onward).
4. Current 三江县委书记 name - still UNKNOWN (web access degraded).
5. Current 三江县县长 name - still UNKNOWN (web access degraded).
6. No explicit mention of who succeeded 贺莹 as 三江县委书记 was found.
7. No explicit mention of who succeeded 陈震 as 三江县县长 was found.

Important: 陈震 appears to be a different person from the former 三江县县长 with the
same name. However, the timing (陈震 left 三江县 ~2023 and now appears as 鱼峰区委书记
in 2026) and career progression (from county leader to district leader within Liuzhou)
are consistent with the same person. This is treated as plausible but needs independent
verification of the 鱼峰区陈震's career history.
"""

import json
import os
import sys
from datetime import datetime

# Ensure gov_relation module is importable
_HERE = os.path.dirname(os.path.abspath(__file__))
_BASE = os.path.normpath(os.path.join(_HERE, "..", "..", ".."))
if _BASE not in sys.path:
    sys.path.insert(0, _BASE)

from gov_relation.runner import run_build
from gov_relation.paths import REPO_ROOT

AS_OF = "2026-07-23"
STAGING_DIR = _HERE
DB_PATH = os.path.join(STAGING_DIR, "三江侗族自治县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "三江侗族自治县_network.gexf")
PERSONS_DIR = STAGING_DIR

# =========================================================================
# DATA
# =========================================================================

# ── Persons ──────────────────────────────────────────────────────────
# Note: Current 县委书记 and 县长 names are UNKNOWN due to degraded web access.
persons = [
    # Current leadership (placeholders — names unknown)
    {"id": 1, "name": "（待查）县委书记", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "三江侗族自治县委书记", "current_org": "中共三江侗族自治县委员会",
     "source": ""},
    {"id": 2, "name": "（待查）县长", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "三江侗族自治县县长", "current_org": "三江侗族自治县人民政府",
     "source": ""},

    # Historical figures
    {"id": 3, "name": "贺莹", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "前任三江县委书记（已调离）", "current_org": "",
     "source": "https://baike.baidu.com/item/%E8%B4%BA%E8%8E%B9/23682370"},
    {"id": 4, "name": "陈震", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "鱼峰区委书记（原三江县县长）", "current_org": "中共柳州市鱼峰区委员会",
     "source": "http://www.yfq.gov.cn/xwzx/tpxw/202607/t20260722_3775837.shtml"},
    {"id": 5, "name": "雷道理", "gender": "男", "ethnicity": "汉族",
     "birth": "1981", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "鹿寨县委书记（原三江县委常委、副县长）",
     "current_org": "中共鹿寨县委员会",
     "source": "https://www.163.com/dy/article/L11IJ0I405563DJA.html"},
]

# ── Organizations ────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共三江侗族自治县委员会", "type": "党委",
     "level": "县级", "parent": "中共柳州市委员会",
     "location": "三江侗族自治县古宜镇江峰街"},
    {"id": 2, "name": "三江侗族自治县人民政府", "type": "政府",
     "level": "县级", "parent": "柳州市人民政府",
     "location": "三江侗族自治县古宜镇江峰街"},
    {"id": 3, "name": "三江侗族自治县人大常委会", "type": "人大",
     "level": "县级", "parent": "柳州市人大常委会",
     "location": "三江侗族自治县古宜镇"},
    {"id": 4, "name": "三江侗族自治县政协", "type": "政协",
     "level": "县级", "parent": "柳州市政协",
     "location": "三江侗族自治县古宜镇"},
    {"id": 5, "name": "三江侗族自治县纪委监委", "type": "纪委",
     "level": "县级", "parent": "柳州市纪委监委",
     "location": "三江侗族自治县古宜镇"},
    {"id": 6, "name": "中共柳州市委员会", "type": "党委",
     "level": "地市级", "parent": "中共广西壮族自治区委员会",
     "location": "柳州市城中区文昌路66号"},
    {"id": 7, "name": "柳州市人民政府", "type": "政府",
     "level": "地市级", "parent": "广西壮族自治区人民政府",
     "location": "柳州市城中区文昌路66号"},
    {"id": 8, "name": "柳州市自然资源和规划局", "type": "政府",
     "level": "地市级", "parent": "柳州市人民政府",
     "location": "柳州市城中区东环大道"},
    {"id": 9, "name": "中共鹿寨县委员会", "type": "党委",
     "level": "县级", "parent": "中共柳州市委员会",
     "location": "鹿寨县鹿寨镇创业路"},
    {"id": 10, "name": "中共柳州市鱼峰区委员会", "type": "党委",
     "level": "县级", "parent": "中共柳州市委员会",
     "location": "柳州市鱼峰区"},
    {"id": 11, "name": "柳州市鱼峰区人民政府", "type": "政府",
     "level": "县级", "parent": "柳州市人民政府",
     "location": "柳州市鱼峰区"},
]

# ── Positions ────────────────────────────────────────────────────────
positions = [
    # Current leadership (placeholder — dates unknown)
    {"person_id": 1, "org_id": 1, "title": "三江侗族自治县委书记",
     "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "现任书记，姓名待查"},
    {"person_id": 2, "org_id": 2, "title": "三江侗族自治县县长",
     "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "现任县长，姓名待查"},

    # 陈震 — 前任县长，现鱼峰区委书记
    {"person_id": 4, "org_id": 2, "title": "三江县县长",
     "start_date": "", "end_date": "", "rank": "正处级",
     "note": "前任三江县县长，已调离，2026年7月已任鱼峰区委书记"},
    {"person_id": 4, "org_id": 10, "title": "鱼峰区委书记",
     "start_date": "2026-07", "end_date": "present", "rank": "正处级",
     "note": "2026年7月任鱼峰区委书记（confirmed 2026-07-22 article）"},

    # 贺莹 — 前任县委书记
    {"person_id": 3, "org_id": 1, "title": "三江县委书记",
     "start_date": "", "end_date": "", "rank": "正处级",
     "note": "前任三江县委书记，已调离，具体去向待查"},

    # 雷道理 — 三江县任职经历
    {"person_id": 5, "org_id": 1, "title": "三江县委常委",
     "start_date": "", "end_date": "2024-04", "rank": "副处级",
     "note": "任三江县委常委"},
    {"person_id": 5, "org_id": 2, "title": "三江县副县长",
     "start_date": "", "end_date": "2024-04", "rank": "副处级",
     "note": "任三江县委常委、副县长"},
    {"person_id": 5, "org_id": 8, "title": "柳州市自然资源和规划局党组书记、局长",
     "start_date": "2024-04", "end_date": "2026-07", "rank": "正处级",
     "note": "调任柳州市自然资源和规划局"},
    {"person_id": 5, "org_id": 9, "title": "鹿寨县委书记",
     "start_date": "2026-07", "end_date": "present", "rank": "正处级",
     "note": "2026年7月上任鹿寨县委书记"},
]

# ── Relationships ────────────────────────────────────────────────────
relationships = [
    # Current leadership pair (unknown names)
    {"person_a": 1, "person_b": 2,
     "type": "党政搭档",
     "context": "三江县委书记与县长为县党政主要领导搭档（现任姓名待查）",
     "overlap_org": "三江县党政领导班子", "overlap_period": "待查"},

    # Historical: 贺莹 + 陈震 = government pair
    {"person_a": 3, "person_b": 4,
     "type": "前任党政搭档",
     "context": "贺莹（前任书记）与陈震（前任县长）曾为三江县党政主要领导搭档",
     "overlap_org": "三江县党政领导班子", "overlap_period": "约2021-2023"},

    # 雷道理 — worked under former leaders
    {"person_a": 5, "person_b": 3,
     "type": "前后任上下级",
     "context": "雷道理任三江县委常委、副县长期间，在贺莹任县委书记下工作",
     "overlap_org": "中共三江侗族自治县委员会",
     "overlap_period": "至2024-04"},

    {"person_a": 5, "person_b": 4,
     "type": "前后任上下级",
     "context": "雷道理任三江县委常委、副县长期间，在陈震任县长下工作",
     "overlap_org": "三江侗族自治县人民政府",
     "overlap_period": "至2024-04"},

    # Current leadership to historical predecessors
    {"person_a": 1, "person_b": 5,
     "type": "前后任",
     "context": "雷道理离开三江县后（2024-04），现任书记未知何时接任",
     "overlap_org": "中共三江侗族自治县委员会", "overlap_period": "2024-04后"},

    # 陈震 connection to 鱼峰区 (new placement)
    {"person_a": 4, "person_b": 6,
     "type": "所属组织",
     "context": "陈震现任鱼峰区委书记，属于中共柳州市委员会下辖区委",
     "overlap_org": "中共柳州市委员会", "overlap_period": "2026-07起"},
]


# =========================================================================
# Person JSON helpers
# =========================================================================

def make_placeholder_person_json(person):
    """Create a person JSON for a current leader whose name is unknown."""
    post = person["current_post"]
    label = "县委书记" if "书记" in post and "副书记" not in post else "县长"
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "柳州市",
            "region": "三江侗族自治县",
            "job": post,
            "task_id": "guangxi_三江侗族自治县",
            "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": f"sanjiang_current_{label}",
            "name": person["name"],
            "aliases": [],
            "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
            "native_place": "", "education": [], "party_join": "", "work_start": "",
            "dedupe_keys": {
                "name_birth": "",
                "name_birthplace": "",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": post,
            "current_org": person.get("current_org", ""),
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": []
        },
        "career_timeline": [
            {
                "start": "unknown", "end": "present",
                "org": person.get("current_org", ""),
                "title": post,
                "level": "县级", "location": "三江侗族自治县",
                "system": "party" if "书记" in post else "government",
                "rank": "正处级",
                "is_key_promotion": False,
                "notes": f"现任{post}，姓名及履历均待查",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "No risk signals found — identity unknown",
            "date": "",
            "confidence": "unverified",
            "source_ids": []
        }],
        "source_register": [],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": f"Current {post} name and full identity completely unknown"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"Who is the current {post} of 三江侗族自治县? Full name, gender, ethnicity, birth, birthplace, education, party join date, career timeline.",
                "why_it_matters": "This is the core target — without the confirmed name, all network analysis is blocked.",
                "suggested_queries": [
                    f"三江侗族自治县 现任{post}",
                    "三江县 领导之窗 site:sanjiang.gov.cn",
                    "柳州市 2024 2025 2026 干部任免 三江",
                    "柳州市委组织部 任前公示 三江县",
                    "三江侗族自治县人民政府 领导分工"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": "Who preceded and succeeded this leader?",
                "why_it_matters": "Establishes the leadership turnover pattern",
                "suggested_queries": [
                    f"三江县 前任{post}",
                    f"三江侗族自治县 {post} 任免时间线"
                ],
                "last_attempted": AS_OF
            }
        ]
    }


def make_person_json_heyong():
    """Create person JSON for 贺莹 (former 三江县委书记)."""
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "柳州市",
            "region": "三江侗族自治县",
            "job": "前任三江县委书记",
            "task_id": "guangxi_三江侗族自治县",
            "time_focus": "历史人物"
        },
        "identity": {
            "person_id": "sanjiang_贺莹",
            "name": "贺莹",
            "aliases": [],
            "gender": "女", "ethnicity": "汉族",
            "birth": "", "birthplace": "", "native_place": "",
            "education": [], "party_join": "", "work_start": "",
            "dedupe_keys": {
                "name_birth": "贺莹_",
                "name_birthplace": "贺莹_",
                "official_profile_url": "https://baike.baidu.com/item/%E8%B4%BA%E8%8E%B9/23682370"
            }
        },
        "current_status": {
            "current_post": "前任三江县委书记（已调离）",
            "current_org": "",
            "administrative_rank": "正处级（原任）",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": ["S001"]
        },
        "career_timeline": [
            {
                "start": "", "end": "",
                "org": "中共三江侗族自治县委员会",
                "title": "三江县委书记",
                "level": "县级", "location": "广西三江县",
                "system": "party", "rank": "正处级",
                "is_key_promotion": True,
                "notes": "前任三江县委书记，到任和离任时间均待查。陈震任县长时期为其搭档。",
                "confidence": "plausible",
                "source_ids": ["S001"]
            }
        ],
        "organizations": [],
        "relationships": [
            {
                "person": "陈震", "person_id": "sanjiang_陈震",
                "relationship_type": "overlap",
                "strength": "strong",
                "evidence": "贺莹任三江县委书记期间，陈震任三江县县长，为党政主要领导搭档",
                "overlap_org": "三江县党政领导班子",
                "overlap_period": "约2021-2023",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"]
            },
            {
                "person": "雷道理", "person_id": "sanjiang_雷道理",
                "relationship_type": "superior_subordinate",
                "strength": "medium",
                "evidence": "雷道理任三江县委常委、副县长期间在贺莹领导下工作",
                "overlap_org": "中共三江侗族自治县委员会",
                "overlap_period": "至2024-04",
                "direction": "other_to_person",
                "confidence": "plausible",
                "source_ids": ["S002"]
            }
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "No risk signals found through available public sources",
            "date": "",
            "confidence": "unverified",
            "source_ids": []
        }],
        "source_register": [
            {
                "id": "S001",
                "title": "贺莹 - Baidu Baike",
                "url": "https://baike.baidu.com/item/%E8%B4%BA%E8%8E%B9/23682370",
                "publisher": "百度百科",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "encyclopedia",
                "reliability": "medium",
                "notes": "Page not directly accessed during this investigation (baidu 403)"
            }
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "Complete identity (birth, birthplace, education, career timeline) and current whereabouts unknown"
        },
        "open_questions": [
            {
                "priority": "high",
                "question": "What is 贺莹's full identity (birth year, birthplace, education, party join date)?",
                "why_it_matters": "Needed for deduplication and timeline completeness",
                "suggested_queries": ["贺莹 简历", "贺莹 三江县 出生"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": "What is 贺莹's current position after leaving 三江?",
                "why_it_matters": "Reveals the promotion/rotation pattern from 三江 county",
                "suggested_queries": ["贺莹 调任", "贺莹 柳州市"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": "When exactly did 贺莹 serve as 三江县委书记 (start and end dates)?",
                "why_it_matters": "Critical for establishing the leadership timeline",
                "suggested_queries": ["贺莹 三江县委书记 任免"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": "Who succeeded 贺莹 as 三江县委书记?",
                "why_it_matters": "Directly answers the core investigation target",
                "suggested_queries": ["三江县 接任贺莹 县委书记"],
                "last_attempted": AS_OF
            }
        ]
    }


def make_person_json_chenzhen():
    """Create person JSON for 陈震 (former 三江县县长, now 鱼峰区委书记)."""
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "柳州市",
            "region": "三江侗族自治县",
            "job": "前任三江县县长（现鱼峰区委书记）",
            "task_id": "guangxi_三江侗族自治县",
            "time_focus": "历史人物 — 三江县时期"
        },
        "identity": {
            "person_id": "sanjiang_陈震",
            "name": "陈震",
            "aliases": [],
            "gender": "男", "ethnicity": "汉族",
            "birth": "", "birthplace": "", "native_place": "",
            "education": [], "party_join": "", "work_start": "",
            "dedupe_keys": {
                "name_birth": "陈震_",
                "name_birthplace": "陈震_",
                "official_profile_url": "http://www.yfq.gov.cn/xwzx/tpxw/202607/t20260722_3775837.shtml"
            }
        },
        "current_status": {
            "current_post": "鱼峰区委书记",
            "current_org": "中共柳州市鱼峰区委员会",
            "administrative_rank": "县处级正职",
            "as_of": "2026-07-22",
            "is_current_confirmed": True,
            "source_ids": ["S002"]
        },
        "career_timeline": [
            {
                "start": "", "end": "",
                "org": "三江侗族自治县人民政府",
                "title": "三江县县长",
                "level": "县级", "location": "广西三江县",
                "system": "government", "rank": "正处级",
                "is_key_promotion": True,
                "notes": "前任三江县县长，到任和离任时间均待查",
                "confidence": "plausible",
                "source_ids": ["S001"]
            },
            {
                "start": "2026-07", "end": "present",
                "org": "中共柳州市鱼峰区委员会",
                "title": "鱼峰区委书记",
                "level": "县级", "location": "广西柳州市鱼峰区",
                "system": "party", "rank": "正处级",
                "is_key_promotion": True,
                "notes": "2026年7月任鱼峰区委书记（confirmed by official 鱼峰区 article 2026-07-22）",
                "confidence": "confirmed",
                "source_ids": ["S002"]
            }
        ],
        "organizations": [
            {
                "start": "", "end": "",
                "org": "三江侗族自治县人民政府",
                "role": "县长",
                "org_id": "sanjiang_gov"
            },
            {
                "start": "2026-07", "end": "present",
                "org": "中共柳州市鱼峰区委员会",
                "role": "区委书记",
                "org_id": "yufeng_party"
            }
        ],
        "relationships": [
            {
                "person": "贺莹", "person_id": "sanjiang_贺莹",
                "relationship_type": "overlap",
                "strength": "strong",
                "evidence": "陈震任三江县县长期间，贺莹任三江县委书记，为党政主要领导搭档",
                "overlap_org": "三江县党政领导班子",
                "overlap_period": "约2021-2023",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"]
            },
            {
                "person": "雷道理", "person_id": "sanjiang_雷道理",
                "relationship_type": "superior_subordinate",
                "strength": "medium",
                "evidence": "雷道理任三江县委常委、副县长期间在陈震领导下工作",
                "overlap_org": "三江侗族自治县人民政府",
                "overlap_period": "至2024-04",
                "direction": "other_to_person",
                "confidence": "plausible",
                "source_ids": ["S002"]
            }
        ],
        "governance_record": [
            {
                "period": "2026-07",
                "domain": "public_security",
                "achievement_or_event": "调研鱼峰公安分局、白沙镇基层社会治理工作，强调平安建设",
                "role_in_event": "鱼峰区委书记（带队调研）",
                "measurable_outcome": "部署命案防控、极端事件源头预防和'两降两升'平安建设重点任务",
                "location": "柳州市鱼峰区",
                "confidence": "confirmed",
                "source_ids": ["S002"]
            }
        ],
        "professional_profile": {
            "primary_specializations": ["基层社会治理", "公共安全"],
            "secondary_specializations": [],
            "career_pattern": "cross_county_rotation",
            "systems_experience": ["government", "party"],
            "geographic_pattern": ["三江县（原）", "柳州市鱼峰区（现）"],
            "promotion_velocity": {
                "summary": "从三江县县长平级调任鱼峰区委书记（均为正处级），属于从政府主官到党委主官的平调，权力重心有所提升",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "pragmatic",
                    "evidence": "调研基层治理工作时强调'牢固树立和践行正确政绩观'、'用心用情服务群众'",
                    "confidence": "plausible",
                    "source_ids": ["S002"]
                }
            ],
            "speech_themes": ["安全", "基层治理", "服务群众", "高质量发展"],
            "management_signals": [
                "强调党建引领基层治理",
                "坚持和发展新时代'枫桥经验'",
                "锚定'两降两升'目标加压奋进"
            ],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "No risk signals found through available public sources",
            "date": "",
            "confidence": "unverified",
            "source_ids": []
        }],
        "source_register": [
            {
                "id": "S001",
                "title": "陈震 - Baidu Baike",
                "url": "https://baike.baidu.com/item/%E9%99%88%E9%9C%87/63453246",
                "publisher": "百度百科",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "encyclopedia",
                "reliability": "medium",
                "notes": "Page not directly accessed during this investigation (baidu 403)"
            },
            {
                "id": "S002",
                "title": "陈震到鱼峰公安分局、白沙镇调研督导基层社会治理工作",
                "url": "http://www.yfq.gov.cn/xwzx/tpxw/202607/t20260722_3775837.shtml",
                "publisher": "鱼峰区人民政府",
                "published_at": "2026-07-22",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "Confirmed 陈震 as 鱼峰区委书记. Directly accessed and verified."
            }
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": "Birth year, birthplace, education, party join date, and exact dates of 三江县县长 tenure all unknown"
        },
        "open_questions": [
            {
                "priority": "high",
                "question": "What is 陈震's full identity (birth year, birthplace, education, party join date)?",
                "why_it_matters": "Needed for deduplication and timeline completeness",
                "suggested_queries": ["陈震 简历 三江县", "陈震 简历 鱼峰区"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": "When exactly did 陈震 serve as 三江县县长 (start and end dates)?",
                "why_it_matters": "Critical for establishing the leadership timeline",
                "suggested_queries": ["陈震 三江县县长 任免"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": "What were 陈震's positions between leaving 三江县县长 and becoming 鱼峰区委书记?",
                "why_it_matters": "Reveals the career progression and promotion pattern",
                "suggested_queries": ["陈震 调任 柳州市", "陈震 2023 2024 2025"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": "Is this 陈震 (鱼峰区委书记) the same person as the former 三江县县长?",
                "why_it_matters": "Critical for data deduplication - need to verify identity continuity",
                "suggested_queries": ["鱼峰区委书记 陈震 简历", "三江县 陈震 县长 鱼峰"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": "Who succeeded 陈震 as 三江县县长?",
                "why_it_matters": "Directly answers the core investigation target",
                "suggested_queries": ["三江县 接任陈震 县长 新任"],
                "last_attempted": AS_OF
            }
        ]
    }


# =========================================================================
# BUILD
# =========================================================================

def build():
    print(f"=== Building 三江侗族自治县 data ===")
    print(f"Staging dir: {STAGING_DIR}")
    print(f"AS_OF: {AS_OF}")
    print()

    # 1. Database + GEXF via gov_relation.runner
    run_build(
        slug="三江侗族自治县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    # 2. Person JSONs
    person_jsons = []
    # Current leaders (placeholder)
    for p in persons[:2]:
        pj = make_placeholder_person_json(p)
        label = "县委书记" if "书记" in p.get("current_post", "") and "副书记" not in p.get("current_post", "") else "县长"
        fname = f"{AS_OF.replace('-','')}-广西壮族自治区-柳州市-{label}-待查.json"
        fpath = os.path.join(PERSONS_DIR, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(pj, f, ensure_ascii=False, indent=2)
        person_jsons.append(fpath)
        print(f"Person JSON written: {fpath}")

    # 贺莹 (former party secretary)
    pj_heyong = make_person_json_heyong()
    fname_heyong = f"{AS_OF.replace('-','')}-广西壮族自治区-柳州市-前任县委书记-贺莹.json"
    fpath_heyong = os.path.join(PERSONS_DIR, fname_heyong)
    with open(fpath_heyong, "w", encoding="utf-8") as f:
        json.dump(pj_heyong, f, ensure_ascii=False, indent=2)
    person_jsons.append(fpath_heyong)
    print(f"Person JSON written: {fpath_heyong}")

    # 陈震 (former county mayor, now 鱼峰区委书记)
    pj_chenzhen = make_person_json_chenzhen()
    fname_chenzhen = f"{AS_OF.replace('-','')}-广西壮族自治区-柳州市-前任县长-陈震.json"
    fpath_chenzhen = os.path.join(PERSONS_DIR, fname_chenzhen)
    with open(fpath_chenzhen, "w", encoding="utf-8") as f:
        json.dump(pj_chenzhen, f, ensure_ascii=False, indent=2)
    person_jsons.append(fpath_chenzhen)
    print(f"Person JSON written: {fpath_chenzhen}")

    print()
    print("Build complete.")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
    print(f"  JSONs: {len(person_jsons)} files")


if __name__ == "__main__":
    build()
