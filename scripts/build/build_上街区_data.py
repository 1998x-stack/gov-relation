#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 上街区 (Shangjie District), 郑州市, 河南省.

Level: 市辖区
Province: 河南省
Parent city: 郑州市
Targets: 区委书记 (Party Secretary: unknown from available sources), 区长 (Mayor: 时博)
Task ID: henan_上街区

Research date: 2026-07-24
Official source: http://www.zzsj.gov.cn/ (上街区人民政府)

Current status (as of 2026-07-24, verified via Wikipedia zh):
- 区委书记: 未知 (not listed in Wikipedia infobox; web search tools were rate-limited/timed out)
- 区长: 时博 (confirmed via Wikipedia)

Leadership roster sourced from:
  - https://zh.wikipedia.org/wiki/上街区 (Wikipedia infobox: 区长时博)
  - District government website: http://www.zzsj.gov.cn/

Confidence notes:
  时博 identity confirmed via Wikipedia.
  区委书记 identity unknown from open sources due to degraded web access (Exa rate-limited, Baidu 403, Google/DuckDuckGo timed out).
  Full leadership roster (区委常委, 副区长, 人大, 政协) not available.
  Detailed career histories before current roles not publicly available.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / "..").resolve()  # tmp/henan_上街区/../.. = repo root
# Fall back to locate correct root
if not (_REPO_ROOT / "gov_relation").exists():
    # Try going up more levels if this is nested tmp
    _REPO_ROOT = (_STAGING_DIR / "../../..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "上街区"

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

    # 1. 区委书记 — name unknown from open sources
    {
        "id": 1,
        "name": "（待查）区委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共上街区委员会",
        "source": "https://zh.wikipedia.org/wiki/上街区",
    },
    # 2. 时博 — 区长
    {
        "id": 2,
        "name": "时博",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "上街区人民政府",
        "source": "https://zh.wikipedia.org/wiki/上街区",
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
        "name": "中共上街区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共郑州市委员会",
        "location": "河南省郑州市上街区",
    },
    {
        "id": 2,
        "name": "上街区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "郑州市人民政府",
        "location": "河南省郑州市上街区",
    },
    {
        "id": 3,
        "name": "上街区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "郑州市人大常委会",
        "location": "河南省郑州市上街区",
    },
    {
        "id": 4,
        "name": "政协上街区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协郑州市委员会",
        "location": "河南省郑州市上街区",
    },
    {
        "id": 5,
        "name": "上街区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共郑州市纪律检查委员会",
        "location": "河南省郑州市上街区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # ── Core Leadership ──
    # 区委书记 (name TBD)
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "", "end": "present",
     "rank": "正处级", "note": "姓名待查; 现任区委书记未从公开来源确认"},
    # 时博 - 区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "", "end": "present",
     "rank": "正处级", "note": "Confirmed active as of 2026-07-24 via Wikipedia"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 区委书记 (TBD) <-> 时博: 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记与区长党政主要领导搭档; 共同负责上街区全面工作",
     "overlap_org": "中共上街区委员会/上街区人民政府",
     "overlap_period": "截至2026年7月"},
]

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════


def make_source_register() -> list[dict]:
    return [
        {
            "id": "S001",
            "title": "Wikipedia-上街区",
            "url": "https://zh.wikipedia.org/wiki/上街区",
            "publisher": "Wikipedia",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "encyclopedia",
            "reliability": "medium",
            "notes": "上街区行政区划信息和区长信息（区长：时博）；区委书记未列于信息框",
        },
        {
            "id": "S002",
            "title": "上街区人民政府官网",
            "url": "http://www.zzsj.gov.cn/",
            "publisher": "上街区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "网站可正常访问，但领导之窗页面无法直接访问（疑似动态页面）",
        },
    ]


def generate_person_json(job: str, name: str) -> dict:
    """Generate per-person graph JSON following person_graph_json.md schema."""
    person_id_str = f"shangjie_{name}"

    # ── 区委书记 (待查) ──
    if name == "（待查）区委书记":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "郑州市",
                "region": "上街区",
                "job": "区委书记",
                "task_id": "henan_上街区",
                "time_focus": "当前",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "（待查）区委书记",
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
                    "name_birth": "待查__",
                    "name_birthplace": "待查__",
                    "official_profile_url": "",
                },
            },
            "current_status": {
                "current_post": "区委书记",
                "current_org": "中共上街区委员会",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": False,
                "source_ids": [],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "present",
                    "org": "中共上街区委员会",
                    "title": "区委书记",
                    "level": "正处级",
                    "location": "河南省郑州市上街区",
                    "system": "party",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "姓名未从公开来源确认；Wikipedia上街区信息框未列区委书记",
                    "confidence": "unverified",
                    "source_ids": [],
                },
            ],
            "organizations": [
                {"org_id": 1, "name": "中共上街区委员会", "type": "党委",
                 "level": "县处级", "location": "河南省郑州市上街区"},
            ],
            "relationships": [
                {"person": "时博", "person_id": "shangjie_时博",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区委书记与区长党政主要领导搭档（假定关系，因区委书记姓名未确证）",
                 "overlap_org": "中共上街区委员会/上街区人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "plausible",
                 "source_ids": []},
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["party"],
                "geographic_pattern": [],
                "promotion_velocity": {
                    "summary": "公开源不足，姓名未知，无法分析",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "unknown",
                        "evidence": "姓名未知，无法调研工作风格",
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
                    "description": "姓名未知，无法搜索风险信号",
                    "date": "",
                    "confidence": "unverified",
                    "source_ids": [],
                }
            ],
            "source_register": make_source_register(),
            "confidence_summary": {
                "identity": "unverified",
                "current_role": "unverified",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": "区委书记姓名完全未知——这是最重要的缺口",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "上街区现任区委书记是谁？",
                    "why_it_matters": "项目的核心目标人物（target）之一，全区工作的一把手",
                    "suggested_queries": ["上街区 区委书记", "上街区 书记 现任", "郑州 上街 区委书记"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "区委书记的出生日期、籍贯和毕业院校？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["上街区 区委书记 简历", "上街区 书记 出生"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "区委书记何时开始担任上街区区委书记？此前担任什么职务？",
                    "why_it_matters": "理清履职起始时间和前任交接",
                    "suggested_queries": ["上街区 区委书记 任前公示", "上街区 书记 任职 时间"],
                    "last_attempted": AS_OF,
                },
            ],
        }

    # ── 时博 (区长) ──
    if name == "时博":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "郑州市",
                "region": "上街区",
                "job": "区长",
                "task_id": "henan_上街区",
                "time_focus": "当前",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "时博",
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
                    "name_birth": "时博_",
                    "name_birthplace": "时博_",
                    "official_profile_url": "",
                },
            },
            "current_status": {
                "current_post": "区长",
                "current_org": "上街区人民政府",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "present",
                    "org": "上街区人民政府",
                    "title": "区长",
                    "level": "正处级",
                    "location": "河南省郑州市上街区",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "截至2026年7月在任; 仅通过Wikipedia确认当前职务，具体到任时间未知",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                },
            ],
            "organizations": [
                {"org_id": 2, "name": "上街区人民政府", "type": "政府",
                 "level": "县处级", "location": "河南省郑州市上街区"},
            ],
            "relationships": [
                {"person": "（待查）区委书记", "person_id": "shangjie_（待查）区委书记",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区长与区委书记党政主要领导搭档（区委书记姓名未确证）",
                 "overlap_org": "中共上街区委员会/上街区人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "plausible",
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
                "biggest_gap": "完整履历：时博任区长前的教育背景、出生日期、籍贯和全部任职经历均未知; 区委书记搭档姓名未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "时博的出生日期、籍贯和毕业院校？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["时博 简历 上街区", "时博 出生 籍贯"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "时博何时开始担任上街区区长？此前担任什么职务？",
                    "why_it_matters": "理清履职起始时间和前任交接",
                    "suggested_queries": ["时博 任 上街区 区长", "时博 任职公示"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "时博的完整职业生涯履历？",
                    "why_it_matters": "评估专业背景和职业发展路径",
                    "suggested_queries": ["时博 工作 经历"],
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
        if name in ("（待查）区委书记", "时博"):
            data = generate_person_json(job, name)
            if data:
                # Use a safe filename - if name has special chars, use job-based name
                safe_name = name.replace("（待查）", "unknown_")
                person_path = PERSONS_DIR / f"{TODAY}-河南省-郑州市-{job}-{safe_name}.json"
                with open(person_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"  Person JSON: {person_path.relative_to(_REPO_ROOT)}")

    print("\nDone.")


if __name__ == "__main__":
    main()
