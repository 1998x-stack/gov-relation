#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 长海县, 大连市, 辽宁省.

Investigation date: 2026-07-25
Task ID: liaoning_长海县
Level: 县
Targets: 县委书记 & 县长

Research status: PARTIAL — Only 陆凯 (former 长海县委副书记, now 苏家屯区代区长)
identified from cross-reference. Current 县委书记 and 县长 could not be confirmed
due to severe web access degradation (Exa rate-limited, Baidu 403, Sogou captcha,
Jina Reader timeouts, government site unreachable, search engines all blocked).

Known facts:
  - 陆凯 served as 长海县委副书记 until ~April 2026 then moved to 苏家屯区
  - 长海县 is an island county (长山群岛) under 大连市
  - Current core leadership (县委书记 & 县长): UNKNOWN — could not be identified
    from any accessible source in this investigation

Confidence notes:
  - All current officeholders marked as unknown/待查
  - Only confirmed data point: 陆凯's former role as 长海县委副书记
  - No biographical data available for any current leaders
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
for p_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[p_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "长海县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
CURRENT_DIR = Path(__file__).parent.resolve()
STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "liaoning_长海县"
if CURRENT_DIR.name == "liaoning_长海县":
    STAGING = CURRENT_DIR
elif STAGING_CANDIDATE.exists():
    STAGING = STAGING_CANDIDATE
else:
    STAGING = CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-2 core leadership (待查), 3 former县委副书记, 10+ organizations

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership — NOT IDENTIFIED in this investigation
    # ══════════════════════════════════════════════════════════════════════
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
        "current_post": "长海县委书记",
        "current_org": "中共长海县委员会",
        "source": "未能确认 — 所有网络搜索工具（Exa、百度、搜狗、Jina）均被限制或超时",
        "notes": "2026年7月调查时所有搜索引擎/政府网站均无法访问，未能确认现任县委书记身份"
    },
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
        "current_post": "长海县委副书记、县长",
        "current_org": "长海县人民政府",
        "source": "未能确认 — 所有网络搜索工具均被限制或超时",
        "notes": "2026年7月调查时所有搜索引擎/政府网站均无法访问，未能确认现任县长身份"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Known Former Leader
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "陆凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年4月",
        "birthplace": "",
        "education": "研究生学历，博士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "苏家屯区委副书记、代区长（原长海县委副书记）",
        "current_org": "苏家屯区人民政府",
        "source": "data/persons/20260725-辽宁省-沈阳市-区长-陆凯.json (repo cross-reference)",
        "notes": "曾任长海县委副书记（副厅级）、大连长山群岛海洋生态经济区党工委副书记，2026年4月前在任，后调任苏家屯区代区长"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共长海县委员会", "type": "党委", "level": "县级", "parent": "中共大连市委", "location": "长海县"},
    {"id": 2, "name": "长海县人民政府", "type": "政府", "level": "县级", "parent": "大连市人民政府", "location": "长海县"},
    {"id": 3, "name": "大连长山群岛海洋生态经济区党工委", "type": "开发区", "level": "副厅级", "parent": "中共大连市委", "location": "长海县"},
    {"id": 4, "name": "中共长海县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共大连市纪委", "location": "长海县"},
    {"id": 5, "name": "长海县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "大连市人大常委会", "location": "长海县"},
    {"id": 6, "name": "中国人民政治协商会议长海县委员会", "type": "政协", "level": "县级", "parent": "大连市政协", "location": "长海县"},
    {"id": 7, "name": "中共大连市委", "type": "党委", "level": "副省级", "parent": "中共辽宁省委", "location": "大连"},
    {"id": 8, "name": "大连市人民政府", "type": "政府", "level": "副省级", "parent": "辽宁省人民政府", "location": "大连"},
]

# ── Positions ─────────────────────────────────────────────────────────────────
positions = [
    # 县委书记 (待查)
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "待确认身份"},
    # 县长 (待查)
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "待确认身份"},
    # 陆凯 — 前长海县委副书记，大连长山群岛海洋生态经济区党工委副书记
    {"person_id": 3, "org_id": 1, "title": "长海县委副书记", "start_date": "", "end_date": "2026-04", "rank": "副厅级", "note": "2026年4月前离任调往苏家屯区"},
    {"person_id": 3, "org_id": 3, "title": "大连长山群岛海洋生态经济区党工委副书记", "start_date": "", "end_date": "2026-04", "rank": "副厅级", "note": "兼任"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 县委书记 — 县长 (presumed)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记—县长（党政一把手）", "overlap_org": "中共长海县委员会/长海县人民政府", "overlap_period": "至今"},
    # 陆凯 — 县委书记 (former subordinate)
    {"person_a": 3, "person_b": 1, "type": "superior_subordinate", "context": "县委副书记—县委书记（陆凯曾任长海县委副书记）", "overlap_org": "中共长海县委员会", "overlap_period": "至2026年4月"},
    # 陆凯 — 县长 (former peer)
    {"person_a": 3, "person_b": 2, "type": "peer", "context": "县委副书记—县长（陆凯曾任副书记）", "overlap_org": "中共长海县委员会/长海县人民政府", "overlap_period": "至2026年4月"},
]


# ── Build ─────────────────────────────────────────────────────────────────────
def main() -> None:
    print(f"Building {SLUG} network...")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

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

    # ── Write person JSONs ───────────────────────────────────────────────
    pjson_paths = []
    for pjson_data in [person_secretary, person_mayor, person_lukai]:
        pjson_path = PJSON_DIR / pjson_data["_filename"]
        with open(pjson_path, "w", encoding="utf-8") as f:
            json.dump(pjson_data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {pjson_path}")
        pjson_paths.append(pjson_path)
        json.dumps(pjson_data, ensure_ascii=False)  # validate

    # ── Print summary ───────────────────────────────────────────────────
    print(f"\n{SLUG} build complete!")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Person JSONs: {len(pjson_paths)}")
    print(f"\n⚠️  NOTE: Current 县委书记 and 县长 identity UNKNOWN due to web access degradation.")
    print(f"  Verify with manual check of 长海县政府网站 (www.changhai.gov.cn) when accessible.")


# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON: 县委书记 (unknown)
# ═══════════════════════════════════════════════════════════════════════════════
person_secretary = {
    "_filename": f"{TODAY}-辽宁省-大连市-县委书记-待查.json",
    "schema_version": "1.0",
    "generated_at": AS_OF,
    "investigation_scope": {
        "province": "辽宁省",
        "city": "大连市",
        "region": "长海县",
        "job": "县委书记",
        "task_id": "liaoning_长海县",
        "time_focus": "2025-2026"
    },
    "identity": {
        "person_id": "changhai_secretary_unknown",
        "name": "待查",
        "aliases": [],
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": [],
        "party_join": "",
        "work_start": "",
        "dedupe_keys": {
            "name_birth": "",
            "name_birthplace": "",
            "official_profile_url": ""
        }
    },
    "current_status": {
        "current_post": "长海县委书记",
        "current_org": "中共长海县委员会",
        "administrative_rank": "正处级",
        "as_of": "2026-07-25",
        "is_current_confirmed": False,
        "source_ids": []
    },
    "career_timeline": [
        {
            "start": "unknown",
            "end": "present",
            "org": "中共长海县委员会",
            "title": "长海县委书记",
            "level": "正处级",
            "location": "大连市长海县",
            "system": "party",
            "rank": "正处级",
            "is_key_promotion": False,
            "notes": "2026年7月调查时所有网络搜索工具均被限制，未能确认县委书记身份",
            "confidence": "unverified",
            "source_ids": []
        }
    ],
    "organizations": ["中共长海县委员会"],
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
        "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
    },
    "network_metrics": {},
    "risk_and_integrity_signals": [
        {
            "type": "none_found",
            "description": "因无法访问网络，未找到任何风险信号相关信息",
            "date": "",
            "confidence": "unverified",
            "source_ids": []
        }
    ],
    "source_register": [],
    "confidence_summary": {
        "identity": "unverified",
        "current_role": "unverified",
        "career_completeness": "thin",
        "relationship_confidence": "low",
        "biggest_gap": "县委书记姓名、身份、履历完全未知"
    },
    "open_questions": [
        {
            "priority": "critical",
            "question": "长海县现任县委书记是谁？",
            "why_it_matters": "核心目标人物",
            "suggested_queries": [
                "长海县 县委书记 现任",
                "长海县委书记 任前公示",
                "site:changhai.gov.cn 县委书记"
            ],
            "last_attempted": "2026-07-25"
        },
        {
            "priority": "critical",
            "question": "县委书记的履历、教育背景是什么？",
            "why_it_matters": "完整的人物分析",
            "suggested_queries": [
                "长海县委书记 简历"
            ],
            "last_attempted": "2026-07-25"
        },
        {
            "priority": "high",
            "question": "前任长海县委书记是谁？去向如何？",
            "why_it_matters": "了解人事变动链条",
            "suggested_queries": [
                "前任长海县委书记 去向"
            ],
            "last_attempted": "2026-07-25"
        }
    ]
}

# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON: 县长 (unknown)
# ═══════════════════════════════════════════════════════════════════════════════
person_mayor = {
    "_filename": f"{TODAY}-辽宁省-大连市-县长-待查.json",
    "schema_version": "1.0",
    "generated_at": AS_OF,
    "investigation_scope": {
        "province": "辽宁省",
        "city": "大连市",
        "region": "长海县",
        "job": "县长",
        "task_id": "liaoning_长海县",
        "time_focus": "2025-2026"
    },
    "identity": {
        "person_id": "changhai_mayor_unknown",
        "name": "待查",
        "aliases": [],
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": [],
        "party_join": "",
        "work_start": "",
        "dedupe_keys": {
            "name_birth": "",
            "name_birthplace": "",
            "official_profile_url": ""
        }
    },
    "current_status": {
        "current_post": "长海县委副书记、县长",
        "current_org": "长海县人民政府",
        "administrative_rank": "正处级",
        "as_of": "2026-07-25",
        "is_current_confirmed": False,
        "source_ids": []
    },
    "career_timeline": [
        {
            "start": "unknown",
            "end": "present",
            "org": "长海县人民政府",
            "title": "长海县委副书记、县长",
            "level": "正处级",
            "location": "大连市长海县",
            "system": "government",
            "rank": "正处级",
            "is_key_promotion": False,
            "notes": "2026年7月调查时所有网络搜索工具均被限制，未能确认县长身份",
            "confidence": "unverified",
            "source_ids": []
        }
    ],
    "organizations": ["长海县人民政府"],
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
        "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
    },
    "network_metrics": {},
    "risk_and_integrity_signals": [
        {
            "type": "none_found",
            "description": "因无法访问网络，未找到任何风险信号相关信息",
            "date": "",
            "confidence": "unverified",
            "source_ids": []
        }
    ],
    "source_register": [],
    "confidence_summary": {
        "identity": "unverified",
        "current_role": "unverified",
        "career_completeness": "thin",
        "relationship_confidence": "low",
        "biggest_gap": "县长姓名、身份、履历完全未知"
    },
    "open_questions": [
        {
            "priority": "critical",
            "question": "长海县现任县长是谁？",
            "why_it_matters": "核心目标人物",
            "suggested_queries": [
                "长海县 县长 现任",
                "长海县长 任前公示",
                "site:changhai.gov.cn 县长"
            ],
            "last_attempted": "2026-07-25"
        },
        {
            "priority": "critical",
            "question": "县长的履历、教育背景是什么？",
            "why_it_matters": "完整的人物分析",
            "suggested_queries": [
                "长海县长 简历"
            ],
            "last_attempted": "2026-07-25"
        },
        {
            "priority": "high",
            "question": "前任长海县长是谁？去向如何？",
            "why_it_matters": "了解人事变动链条",
            "suggested_queries": [
                "前任长海县长 去向"
            ],
            "last_attempted": "2026-07-25"
        },
        {
            "priority": "high",
            "question": "陆凯离任长海县委副书记后，新的县委副书记是谁？是否即现任县长？",
            "why_it_matters": "确认县领导班子的变动",
            "suggested_queries": [
                "长海县委副书记 2026"
            ],
            "last_attempted": "2026-07-25"
        }
    ]
}

# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON: 陆凯 (former 长海县委副书记, now 苏家屯区代区长)
# Reference: data/persons/20260725-辽宁省-沈阳市-区长-陆凯.json
# ═══════════════════════════════════════════════════════════════════════════════
person_lukai = {
    "_filename": f"{TODAY}-辽宁省-大连市-前县委副书记-陆凯.json",
    "schema_version": "1.0",
    "generated_at": AS_OF,
    "investigation_scope": {
        "province": "辽宁省",
        "city": "大连市",
        "region": "长海县",
        "job": "长海县委副书记（已离任）",
        "task_id": "liaoning_长海县",
        "time_focus": "至2026年4月"
    },
    "identity": {
        "person_id": "changhai_lu_kai",
        "name": "陆凯",
        "aliases": [],
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年4月",
        "birthplace": "",
        "native_place": "",
        "education": [
            {
                "period": "",
                "institution": "",
                "major": "",
                "degree": "研究生学历，博士学位",
                "study_type": "unknown",
                "source_ids": ["S001"]
            }
        ],
        "party_join": "中共党员",
        "work_start": "",
        "dedupe_keys": {
            "name_birth": "陆凯_1979年4月",
            "name_birthplace": "陆凯_",
            "official_profile_url": ""
        }
    },
    "current_status": {
        "current_post": "苏家屯区委副书记、代区长",
        "current_org": "苏家屯区人民政府",
        "administrative_rank": "正处级",
        "as_of": "2026-07-25",
        "is_current_confirmed": True,
        "source_ids": ["S001", "S002"]
    },
    "career_timeline": [
        {
            "start": "",
            "end": "",
            "org": "大连理工大学",
            "title": "大连理工大学团委书记",
            "level": "副厅级",
            "location": "大连",
            "system": "party",
            "rank": "副厅级",
            "is_key_promotion": False,
            "notes": "前期任职",
            "confidence": "plausible",
            "source_ids": ["S001"]
        },
        {
            "start": "",
            "end": "",
            "org": "共青团大连市委员会",
            "title": "共青团大连市委副书记",
            "level": "副厅级",
            "location": "大连",
            "system": "party",
            "rank": "副厅级",
            "is_key_promotion": False,
            "notes": "",
            "confidence": "plausible",
            "source_ids": ["S001"]
        },
        {
            "start": "",
            "end": "",
            "org": "共青团大连市委员会",
            "title": "共青团大连市委书记",
            "level": "正局级",
            "location": "大连",
            "system": "party",
            "rank": "正局级",
            "is_key_promotion": False,
            "notes": "",
            "confidence": "plausible",
            "source_ids": ["S001"]
        },
        {
            "start": "",
            "end": "2026-04",
            "org": "中共长海县委员会",
            "title": "长海县委副书记（副厅级）",
            "level": "副厅级",
            "location": "大连市长海县",
            "system": "party",
            "rank": "副厅级",
            "is_key_promotion": False,
            "notes": "大连长山群岛海洋生态经济区党工委副书记",
            "confidence": "plausible",
            "source_ids": ["S001"]
        },
        {
            "start": "2026-06",
            "end": "present",
            "org": "苏家屯区人民政府",
            "title": "苏家屯区委副书记、代区长",
            "level": "正处级",
            "location": "沈阳市苏家屯区",
            "system": "government",
            "rank": "正处级",
            "is_key_promotion": True,
            "notes": "2026年6月任代区长",
            "confidence": "plausible",
            "source_ids": ["S001"]
        }
    ],
    "organizations": ["中共长海县委员会", "大连长山群岛海洋生态经济区党工委", "共青团大连市委员会", "大连理工大学"],
    "relationships": [
        {
            "person": "待查（县委书记）",
            "person_id": "changhai_secretary_unknown",
            "relationship_type": "superior_subordinate",
            "strength": "strong",
            "evidence": "陆凯曾任长海县委副书记，受县委书记领导",
            "overlap_org": "中共长海县委员会",
            "overlap_period": "至2026年4月",
            "direction": "other_to_person",
            "confidence": "plausible",
            "source_ids": []
        },
        {
            "person": "待查（县长）",
            "person_id": "changhai_mayor_unknown",
            "relationship_type": "peer",
            "strength": "strong",
            "evidence": "陆凯任县委副书记时与县长为党政副手关系",
            "overlap_org": "长海县人民政府",
            "overlap_period": "至2026年4月",
            "direction": "undirected",
            "confidence": "plausible",
            "source_ids": []
        }
    ],
    "governance_record": [],
    "professional_profile": {
        "primary_specializations": ["共青团工作", "党务管理"],
        "secondary_specializations": [],
        "career_pattern": "cross_county_rotation",
        "systems_experience": ["party", "government"],
        "geographic_pattern": ["大连", "沈阳"],
        "promotion_velocity": {
            "summary": "从大连团市委书记转任长海县委副书记（副厅级），后调任苏家屯区代区长，属于跨市调任",
            "notable_fast_promotions": []
        }
    },
    "work_style_and_personality": {
        "public_style_indicators": [
            {
                "trait": "unknown",
                "evidence": "公开信息有限",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "speech_themes": [],
        "management_signals": [],
        "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
    },
    "network_metrics": {},
    "risk_and_integrity_signals": [
        {
            "type": "none_found",
            "description": "无公开的纪律处分或负面媒体报道",
            "date": "",
            "confidence": "plausible",
            "source_ids": []
        }
    ],
    "source_register": [
        {
            "id": "S001",
            "title": "陆凯人物JSON（苏家屯区调查）",
            "url": "",
            "publisher": "gov-relation repo - data/persons/20260725-辽宁省-沈阳市-区长-陆凯.json",
            "published_at": "2026-07-25",
            "accessed_at": "2026-07-25",
            "source_type": "database",
            "reliability": "medium",
            "notes": "从苏家屯区调查中交叉引用"
        },
        {
            "id": "S002",
            "title": "苏家屯区代区长任命报道",
            "url": "",
            "publisher": "辽宁发布",
            "published_at": "2026-06",
            "accessed_at": "2026-07-25",
            "source_type": "appointment_notice",
            "reliability": "high",
            "notes": "确认陆凯由长海县委副书记调任苏家屯区代区长"
        }
    ],
    "confidence_summary": {
        "identity": "plausible",
        "current_role": "confirmed",
        "career_completeness": "partial",
        "relationship_confidence": "medium",
        "biggest_gap": "陆凯在大连理工大学至大连团市委期间的详细履历不完整"
    },
    "open_questions": [
        {
            "priority": "medium",
            "question": "陆凯在长海县委副书记任期的具体起止时间？",
            "why_it_matters": "精确化时间线",
            "suggested_queries": ["陆凯 长海县委副书记 任命"],
            "last_attempted": "2026-07-25"
        },
        {
            "priority": "medium",
            "question": "陆凯的具体出生地（籍贯）？",
            "why_it_matters": "人物去重和地域分析",
            "suggested_queries": ["陆凯 籍贯"],
            "last_attempted": "2026-07-25"
        }
    ]
}


if __name__ == "__main__":
    main()
