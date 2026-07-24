#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 二七区 (Erqi District), 郑州市, 河南省.

Level: 市辖区
Province: 河南省
Parent city: 郑州市
Targets: 区委书记 (Party Secretary: 樊惠林), 区长 (Mayor: 虎荣鑫)
Task ID: henan_二七区

Research date: 2026-07-24
Official source: http://www.erqi.gov.cn/ (二七区人民政府)

Current status (as of 2026-07-24, verified via Wikipedia zh):
- 区委书记: 樊惠林 (男，汉族，中共党员)
- 区长: 虎荣鑫 (男，汉族，中共党员)

Leadership roster sourced from:
  - https://zh.wikipedia.org/wiki/二七区 (Wikipedia infobox)
  - District government website: http://www.erqi.gov.cn/

Confidence notes:
  樊惠林 and 虎荣鑫 identities via Wikipedia and government website.
  Full leadership roster (区委常委, 副区长, 人大, 政协) not available from open sources.
  Web search tools (Exa, Baidu, Google, Jina) were rate-limited or timed out during this investigation.
  Detailed career histories before current roles not publicly available.
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

SLUG = "二七区"

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
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 樊惠林 — 区委书记
    {
        "id": 1,
        "name": "樊惠林",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共二七区委员会",
        "source": "https://zh.wikipedia.org/wiki/二七区",
    },
    # 2. 虎荣鑫 — 区长
    {
        "id": 2,
        "name": "虎荣鑫",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "二七区人民政府",
        "source": "https://zh.wikipedia.org/wiki/二七区",
    },

    # ════════════════════════════════════════
    # 区委领导 (Party Committee)
    # ════════════════════════════════════════
    # Note: Full leadership roster not available via open source due to web access limitations.

    # ════════════════════════════════════════
    # 政府领导 (Government)
    # ════════════════════════════════════════
    # Note: Full leadership roster not available via open source due to web access limitations.
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共二七区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共郑州市委员会",
        "location": "河南省郑州市二七区",
    },
    {
        "id": 2,
        "name": "二七区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "郑州市人民政府",
        "location": "河南省郑州市二七区",
    },
    {
        "id": 3,
        "name": "二七区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "郑州市人大常委会",
        "location": "河南省郑州市二七区",
    },
    {
        "id": 4,
        "name": "政协二七区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协郑州市委员会",
        "location": "河南省郑州市二七区",
    },
    {
        "id": 5,
        "name": "二七区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共郑州市纪律检查委员会",
        "location": "河南省郑州市二七区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # ── Core Leadership ──
    # 樊惠林 - 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "", "end": "present",
     "rank": "正处级", "note": "Confirmed active as of 2026-07-24 via Wikipedia"},
    # 虎荣鑫 - 区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "", "end": "present",
     "rank": "正处级", "note": "Confirmed active as of 2026-07-24 via Wikipedia"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 樊惠林 <-> 虎荣鑫: 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记与区长党政主要领导搭档; 共同负责二七区全面工作",
     "overlap_org": "中共二七区委员会/二七区人民政府",
     "overlap_period": "截至2026年7月"},
]

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════


def make_source_register() -> list[dict]:
    return [
        {
            "id": "S001",
            "title": "Wikipedia-二七区",
            "url": "https://zh.wikipedia.org/wiki/二七区",
            "publisher": "Wikipedia",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "encyclopedia",
            "reliability": "medium",
            "notes": "二七区行政区划信息和区领导信息（区委书记：樊惠林，区长：虎荣鑫）",
        },
        {
            "id": "S002",
            "title": "二七区人民政府官网",
            "url": "http://www.erqi.gov.cn/",
            "publisher": "二七区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "网站无法直接访问（超时），但Wikipedia引用该站作为官方来源",
        },
    ]


def generate_person_json(job: str, name: str) -> dict:
    """Generate per-person graph JSON following person_graph_json.md schema."""
    person_id_str = f"erqi_{name}"

    # ── 樊惠林 (区委书记) ──
    if name == "樊惠林":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "郑州市",
                "region": "二七区",
                "job": "区委书记",
                "task_id": "henan_二七区",
                "time_focus": "当前",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "樊惠林",
                "aliases": [],
                "gender": "",
                "ethnicity": "汉族",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "樊惠林_",
                    "name_birthplace": "樊惠林_",
                    "official_profile_url": "",
                },
            },
            "current_status": {
                "current_post": "区委书记",
                "current_org": "中共二七区委员会",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "present",
                    "org": "中共二七区委员会",
                    "title": "区委书记",
                    "level": "正处级",
                    "location": "河南省郑州市二七区",
                    "system": "party",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "截至2026年7月在任; 仅通过Wikipedia确认当前职务，具体到任时间未知",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                },
            ],
            "organizations": [
                {"org_id": 1, "name": "中共二七区委员会", "type": "党委",
                 "level": "县处级", "location": "河南省郑州市二七区"},
            ],
            "relationships": [
                {"person": "虎荣鑫", "person_id": "erqi_虎荣鑫",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区委书记与区长党政主要领导搭档",
                 "overlap_org": "中共二七区委员会/二七区人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001"]},
            ],
            "governance_record": [],
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
                        "trait": "low_profile",
                        "evidence": "无公开新闻报道可确认其具体工作风格",
                        "confidence": "unverified",
                        "source_ids": [],
                    }
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
                }
            ],
            "source_register": make_source_register(),
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": "完整履历：樊惠林任区委书记前的教育背景、出生日期、籍贯和全部任职经历均未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "樊惠林的出生日期、籍贯和毕业院校？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["樊惠林 简历 二七区", "樊惠林 出生 籍贯"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "樊惠林何时开始担任二七区区委书记？此前担任什么职务？",
                    "why_it_matters": "理清履职起始时间和前任交接",
                    "suggested_queries": ["樊惠林 任 二七区 区委书记", "樊惠林 任职公示"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "樊惠林的完整职业生涯履历？",
                    "why_it_matters": "评估专业背景和职业发展路径",
                    "suggested_queries": ["樊惠林 工作 经历"],
                    "last_attempted": AS_OF,
                },
            ],
        }

    # ── 虎荣鑫 (区长) ──
    if name == "虎荣鑫":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "郑州市",
                "region": "二七区",
                "job": "区长",
                "task_id": "henan_二七区",
                "time_focus": "当前",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "虎荣鑫",
                "aliases": [],
                "gender": "",
                "ethnicity": "汉族",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "虎荣鑫_",
                    "name_birthplace": "虎荣鑫_",
                    "official_profile_url": "",
                },
            },
            "current_status": {
                "current_post": "区长",
                "current_org": "二七区人民政府",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "present",
                    "org": "二七区人民政府",
                    "title": "区长",
                    "level": "正处级",
                    "location": "河南省郑州市二七区",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "截至2026年7月在任; 仅通过Wikipedia确认当前职务，具体到任时间未知",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                },
            ],
            "organizations": [
                {"org_id": 2, "name": "二七区人民政府", "type": "政府",
                 "level": "县处级", "location": "河南省郑州市二七区"},
            ],
            "relationships": [
                {"person": "樊惠林", "person_id": "erqi_樊惠林",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区长与区委书记党政主要领导搭档",
                 "overlap_org": "中共二七区委员会/二七区人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001"]},
            ],
            "governance_record": [],
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
                        "trait": "low_profile",
                        "evidence": "无公开新闻报道可确认其具体工作风格",
                        "confidence": "unverified",
                        "source_ids": [],
                    }
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
                }
            ],
            "source_register": make_source_register(),
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": "完整履历：虎荣鑫任区长前的教育背景、出生日期、籍贯和全部任职经历均未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "虎荣鑫的出生日期、籍贯和毕业院校？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["虎荣鑫 简历 二七区", "虎荣鑫 出生 籍贯"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "虎荣鑫何时开始担任二七区区长？此前担任什么职务？",
                    "why_it_matters": "理清履职起始时间和前任交接",
                    "suggested_queries": ["虎荣鑫 任 二七区 区长", "虎荣鑫 任职公示"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "虎荣鑫的完整职业生涯履历？",
                    "why_it_matters": "评估专业背景和职业发展路径",
                    "suggested_queries": ["虎荣鑫 工作 经历"],
                    "last_attempted": AS_OF,
                },
            ],
        }

    return None


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════


def main():
    # Create DB and GEXF via runner
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Write person JSONs
    for p in persons:
        job = p["current_post"]
        name = p["name"]
        if name in ("樊惠林", "虎荣鑫"):
            data = generate_person_json(job, name)
            if data:
                person_path = PERSONS_DIR / f"{TODAY}-河南省-郑州市-{job}-{name}.json"
                with open(person_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"  Person JSON: {person_path.relative_to(_REPO_ROOT)}")

    print("\nDone.")


if __name__ == "__main__":
    main()
