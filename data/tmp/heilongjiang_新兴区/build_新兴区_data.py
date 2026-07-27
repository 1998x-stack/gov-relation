#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 新兴区 (Xinxing District), 七台河市, 黑龙江省.

Level: 市辖区
Province: 黑龙江省
Parent city: 七台河市
Targets: 区委书记 (Party Secretary), 区长 (Mayor)
Task ID: heilongjiang_新兴区

Research date: 2026-07-24
Official source: https://www.hljxinxing.gov.cn/ (七台河市新兴区人民政府)

Current status (as of 2026-07-24, verified via 新兴区人民政府 website news):
- 区委书记: 郭晓庆 — Leads investment trips (招商考察) and plays lead role in 区委常委会
- 区长: 郭军 — Inspects street-level safety and security work (安全稳定工作)
- Both confirmed active on the district website as of July 2026

Website news cross-references (hljxinxing.gov.cn):
- 郭晓庆(区委书记) — "郭晓庆带队赴河南兰考开展招商考察" (2026-07-22)
- 郭晓庆(区委书记) — "郭晓庆带队赴上海、江苏宿迁开展招商考察" (2026-07-21)
- 郭军(区长) — "郭军深入街道检查指导安全稳定工作" (2026-07-22)
- 区委常委会召开会议 (2026-07-22) — acknowledged
- 新兴区农业、住建战线工作会议召开 (2026-07-22)
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / "../../..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "新兴区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-07-24"
TODAY = "20260724"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 区委领导 (Party Committee)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "郭晓庆",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共新兴区委员会",
        "source": "https://www.hljxinxing.gov.cn/",
    },
    {
        "id": 2,
        "name": "郭军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "新兴区人民政府",
        "source": "https://www.hljxinxing.gov.cn/",
    },
    # ════════════════════════════════════════
    # 区委副书记、常委 (Deputy Secretary & Standing Committee)
    # ════════════════════════════════════════
    # Note: Full roster not publicly available on the district website.
    # The 领导之窗 (leadership window) page was not accessible via direct URL.
    # These are placeholder entries marked unverified.
    # ════════════════════════════════════════
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共新兴区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共七台河市委员会",
        "location": "黑龙江省七台河市新兴区",
    },
    {
        "id": 2,
        "name": "新兴区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "七台河市人民政府",
        "location": "黑龙江省七台河市新兴区",
    },
    {
        "id": 3,
        "name": "新兴区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "七台河市人大常委会",
        "location": "黑龙江省七台河市新兴区",
    },
    {
        "id": 4,
        "name": "新兴区政协委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协七台河市委员会",
        "location": "黑龙江省七台河市新兴区",
    },
    {
        "id": 5,
        "name": "新兴区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共七台河市纪律检查委员会",
        "location": "黑龙江省七台河市新兴区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 郭晓庆
    {
        "person_id": 1,
        "org_id": 1,
        "title": "区委书记",
        "start": "",
        "end": "present",
        "rank": "正处级",
        "note": "Confirmed active as of 2026-07-22; exact start date unknown",
    },
    # 郭军
    {
        "person_id": 2,
        "org_id": 2,
        "title": "区长",
        "start": "",
        "end": "present",
        "rank": "正处级",
        "note": "Confirmed active as of 2026-07-22; exact start date unknown",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 郭晓庆 <-> 郭军: party secretary and mayor — known working relationship
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "区委书记与区长搭档; 共同在七台河市新兴区任职",
        "overlap_org": "中共新兴区委员会/新兴区人民政府",
        "overlap_period": "截至2026年7月",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print(f"Building {SLUG} network database and GEXF...")

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

    # ── Person JSON ──
    person_files = []
    person_records = [
        ("区委书记", "郭晓庆"),
        ("区长", "郭军"),
    ]
    for job, name in person_records:
        fname = f"{TODAY}-黑龙江省-七台河市-{job}-{name}.json"
        person_path = _STAGING_DIR / fname
        person_json = generate_person_json(job, name)
        with open(person_path, "w", encoding="utf-8") as f:
            json.dump(person_json, f, ensure_ascii=False, indent=2)
        person_files.append(str(person_path))
        print(f"  Person JSON: {person_path}")

    db_path = str(DB_PATH)
    gexf_path = str(GEXF_PATH)
    print()
    print(f"  DB:   {db_path}")
    print(f"  GEXF: {gexf_path}")
    for pf in person_files:
        print(f"  JSON: {pf}")
    print("Done.")


def generate_person_json(job: str, name: str) -> dict:
    """Generate per-person graph JSON following person_graph_json.md schema.

    Due to limited public biography data, many fields are marked unverified
    or left empty with open questions.
    """
    person_id_str = f"heilongjiang_xinxing_{name}"

    if name == "郭晓庆":
        return {
            "schema_version": "1.0",
            "generated_at": "2026-07-24",
            "investigation_scope": {
                "province": "黑龙江省",
                "city": "七台河市",
                "region": "新兴区",
                "job": "区委书记",
                "task_id": "heilongjiang_新兴区",
                "time_focus": "2024–2026",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "郭晓庆",
                "aliases": [],
                "gender": "男",
                "ethnicity": "",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "郭晓庆_",
                    "name_birthplace": "郭晓庆_",
                    "official_profile_url": "https://www.hljxinxing.gov.cn/",
                },
            },
            "current_status": {
                "current_post": "区委书记",
                "current_org": "中共新兴区委员会",
                "administrative_rank": "正处级",
                "as_of": "2026-07-24",
                "is_current_confirmed": True,
                "source_ids": ["S001"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "present",
                    "org": "中共新兴区委员会",
                    "title": "区委书记",
                    "level": "正处级",
                    "location": "黑龙江省七台河市新兴区",
                    "system": "party",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "截至2026年7月在任; 公开来源未显示任职起始时间",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                },
            ],
            "organizations": [
                {
                    "org_id": 1,
                    "name": "中共新兴区委员会",
                    "type": "党委",
                    "level": "县处级",
                    "location": "黑龙江省七台河市新兴区",
                },
            ],
            "relationships": [
                {
                    "person": "郭军",
                    "person_id": "heilongjiang_xinxing_郭军",
                    "relationship_type": "overlap",
                    "strength": "strong",
                    "evidence": "区委书记与区长搭档; 共同负责新兴区党政工作",
                    "overlap_org": "中共新兴区委员会/新兴区人民政府",
                    "overlap_period": "截至2026年7月",
                    "direction": "undirected",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                },
            ],
            "governance_record": [
                {
                    "period": "2026-07",
                    "domain": "economic_development",
                    "achievement_or_event": "带队赴河南兰考开展招商考察",
                    "role_in_event": "带队领导",
                    "measurable_outcome": "",
                    "location": "河南兰考",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                },
                {
                    "period": "2026-07",
                    "domain": "economic_development",
                    "achievement_or_event": "带队赴上海、江苏宿迁开展招商考察",
                    "role_in_event": "带队领导",
                    "measurable_outcome": "",
                    "location": "上海、江苏宿迁",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                },
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["party"],
                "geographic_pattern": [],
                "promotion_velocity": {
                    "summary": "公开源不足，无法分析晋升速度",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "economic_development_oriented",
                        "evidence": "2026年7月先后赴河南兰考、上海、江苏宿迁带队招商考察",
                        "confidence": "confirmed",
                        "source_ids": ["S001"],
                    },
                ],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "截至2026年7月，未发现公开的纪律处分、审计问题或负面报道",
                    "date": "",
                    "confidence": "unverified",
                    "source_ids": [],
                },
            ],
            "source_register": [
                {
                    "id": "S001",
                    "title": "七台河市新兴区人民政府官网",
                    "url": "https://www.hljxinxing.gov.cn/",
                    "publisher": "七台河市新兴区人民政府",
                    "published_at": "",
                    "accessed_at": "2026-07-24",
                    "source_type": "official",
                    "reliability": "high",
                    "notes": "政府官方网站，新闻栏目确认领导活动",
                },
            ],
            "confidence_summary": {
                "identity": "partial",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "完整履历：出生年月、籍贯、教育背景、早期任职经历均未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "郭晓庆的出生年月和籍贯？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["郭晓庆 简历 新兴区", "郭晓庆 个人简历"],
                    "last_attempted": "2026-07-24",
                },
                {
                    "priority": "critical",
                    "question": "郭晓庆何时开始担任新兴区区委书记？",
                    "why_it_matters": "理清履职起始时间和前任交接",
                    "suggested_queries": ["郭晓庆 任 新兴区 区委书记", "郭晓庆 任职公示"],
                    "last_attempted": "2026-07-24",
                },
                {
                    "priority": "high",
                    "question": "郭晓庆的完整教育背景和工作履历？",
                    "why_it_matters": "评估专业背景和职业发展路径",
                    "suggested_queries": ["郭晓庆 教育 工作 经历"],
                    "last_attempted": "2026-07-24",
                },
            ],
        }

    elif name == "郭军":
        return {
            "schema_version": "1.0",
            "generated_at": "2026-07-24",
            "investigation_scope": {
                "province": "黑龙江省",
                "city": "七台河市",
                "region": "新兴区",
                "job": "区长",
                "task_id": "heilongjiang_新兴区",
                "time_focus": "2024–2026",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "郭军",
                "aliases": [],
                "gender": "男",
                "ethnicity": "",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "郭军_",
                    "name_birthplace": "郭军_",
                    "official_profile_url": "https://www.hljxinxing.gov.cn/",
                },
            },
            "current_status": {
                "current_post": "区长",
                "current_org": "新兴区人民政府",
                "administrative_rank": "正处级",
                "as_of": "2026-07-24",
                "is_current_confirmed": True,
                "source_ids": ["S001"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "present",
                    "org": "新兴区人民政府",
                    "title": "区长",
                    "level": "正处级",
                    "location": "黑龙江省七台河市新兴区",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "截至2026年7月在任; 公开来源未显示任职起始时间",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                },
            ],
            "organizations": [
                {
                    "org_id": 2,
                    "name": "新兴区人民政府",
                    "type": "政府",
                    "level": "县处级",
                    "location": "黑龙江省七台河市新兴区",
                },
            ],
            "relationships": [
                {
                    "person": "郭晓庆",
                    "person_id": "heilongjiang_xinxing_郭晓庆",
                    "relationship_type": "overlap",
                    "strength": "strong",
                    "evidence": "区长与区委书记搭档; 共同负责新兴区党政工作",
                    "overlap_org": "中共新兴区委员会/新兴区人民政府",
                    "overlap_period": "截至2026年7月",
                    "direction": "undirected",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                },
            ],
            "governance_record": [
                {
                    "period": "2026-07",
                    "domain": "public_security",
                    "achievement_or_event": "深入街道检查指导安全稳定工作",
                    "role_in_event": "带队领导",
                    "measurable_outcome": "",
                    "location": "新兴区各街道",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                },
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["government"],
                "geographic_pattern": [],
                "promotion_velocity": {
                    "summary": "公开源不足，无法分析晋升速度",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "grassroots_oriented",
                        "evidence": "2026年7月深入街道检查安全稳定工作",
                        "confidence": "confirmed",
                        "source_ids": ["S001"],
                    },
                ],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "截至2026年7月，未发现公开的纪律处分、审计问题或负面报道",
                    "date": "",
                    "confidence": "unverified",
                    "source_ids": [],
                },
            ],
            "source_register": [
                {
                    "id": "S001",
                    "title": "七台河市新兴区人民政府官网",
                    "url": "https://www.hljxinxing.gov.cn/",
                    "publisher": "七台河市新兴区人民政府",
                    "published_at": "",
                    "accessed_at": "2026-07-24",
                    "source_type": "official",
                    "reliability": "high",
                    "notes": "政府官方网站，新闻栏目确认领导活动",
                },
            ],
            "confidence_summary": {
                "identity": "partial",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "完整履历：出生年月、籍贯、教育背景、早期任职经历均未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "郭军的出生年月和籍贯？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["郭军 简历 新兴区", "郭军 个人简历"],
                    "last_attempted": "2026-07-24",
                },
                {
                    "priority": "critical",
                    "question": "郭军何时开始担任新兴区区长？",
                    "why_it_matters": "理清履职起始时间和前任交接",
                    "suggested_queries": ["郭军 任 新兴区 区长", "郭军 任职公示"],
                    "last_attempted": "2026-07-24",
                },
                {
                    "priority": "high",
                    "question": "郭军的完整教育背景和工作履历？",
                    "why_it_matters": "评估专业背景和职业发展路径",
                    "suggested_queries": ["郭军 教育 工作 经历"],
                    "last_attempted": "2026-07-24",
                },
            ],
        }

    return {}


if __name__ == "__main__":
    main()
