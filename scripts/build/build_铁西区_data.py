#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 铁西区 (Tiexi District), 鞍山市, 辽宁省.

Level: 市辖区
Province: 辽宁省
Parent city: 鞍山市
Targets: 区委书记 (District Party Secretary), 区长 (District Mayor)
Task ID: liaoning_铁西区

Research date: 2026-07-25
Official source: http://www.astxq.gov.cn/ (鞍山市铁西区人民政府 — UNREACHABLE during investigation)

Current status (as of 2026-07-25):
- 区委书记: **待查** — All web search tools (Exa rate-limited, Baidu 403/CAPTCHA,
  Jina Reader timeout, Google blocked) and government sites (www.astxq.gov.cn DNS/timeout)
  were unreachable or timed out during this investigation.
- 区长: **待查** — Same constraints.

Confidence notes:
  Due to complete web access degradation, the current leadership names could not be confirmed
  from any official source. This build script uses placeholder records ("待查_区委书记" and
  "待查_区长") to establish the structural framework.

  NOTE: Existing 铁西区_network.db and 铁西区_network.gexf in data/ directory cover
  **沈阳市**铁西区, NOT 鞍山市铁西区. These are distinct regions.
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

SLUG = "铁西区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-07-25"
TODAY = "20260725"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

# NOTE: Due to complete web search degradation, all leader names are placeholder records.
# Future updates should replace these with confirmed names and biographies.

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 待查_区委书记 — 区委书记 (Party Secretary of Tiexi District)
    {
        "id": 1,
        "name": "待查_区委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共鞍山市铁西区委员会",
        "source": "未确认 — 区委书记姓名、履历均待查。政府网站 www.astxq.gov.cn 在调查期间无法访问。",
    },
    # 2. 待查_区长 — 区委副书记、区长
    {
        "id": 2,
        "name": "待查_区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "鞍山市铁西区人民政府",
        "source": "未确认 — 区长姓名、履历均待查。政府网站 www.astxq.gov.cn 在调查期间无法访问。",
    },

    # ════════════════════════════════════════
    # 区委常委 (District Party Standing Committee)
    # ════════════════════════════════════════

    # 3. 待查_区委副书记
    {
        "id": 3,
        "name": "待查_区委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共鞍山市铁西区委员会",
        "source": "未确认 — 待查",
    },
    # 4. 待查_常务副区长
    {
        "id": 4,
        "name": "待查_常务副区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "鞍山市铁西区人民政府",
        "source": "未确认 — 待查",
    },
    # 5. 待查_纪委书记
    {
        "id": 5,
        "name": "待查_纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区纪委书记、区监委主任",
        "current_org": "中共鞍山市铁西区纪律检查委员会",
        "source": "未确认 — 待查",
    },
    # 6. 待查_组织部部长
    {
        "id": 6,
        "name": "待查_组织部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共鞍山市铁西区委组织部",
        "source": "未确认 — 待查",
    },
    # 7. 待查_宣传部部长
    {
        "id": 7,
        "name": "待查_宣传部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、宣传部部长",
        "current_org": "中共鞍山市铁西区委宣传部",
        "source": "未确认 — 待查",
    },
    # 8. 待查_政法委书记
    {
        "id": 8,
        "name": "待查_政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、政法委书记",
        "current_org": "中共鞍山市铁西区委政法委员会",
        "source": "未确认 — 待查",
    },
    # 9. 待查_统战部部长
    {
        "id": 9,
        "name": "待查_统战部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、统战部部长",
        "current_org": "中共鞍山市铁西区委统战部",
        "source": "未确认 — 待查",
    },

    # ════════════════════════════════════════
    # 前任领导 (Predecessors)
    # ════════════════════════════════════════

    # 10. 待查_前任区委书记
    {
        "id": 10,
        "name": "待查_前任区委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区委书记（已离任）",
        "current_org": "中共鞍山市铁西区委员会（已离任）",
        "source": "未确认 — 待查",
    },
    # 11. 待查_前任区长
    {
        "id": 11,
        "name": "待查_前任区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区长（已离任）",
        "current_org": "鞍山市铁西区人民政府（已离任）",
        "source": "未确认 — 待查",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共鞍山市铁西区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共鞍山市委员会",
        "location": "辽宁省鞍山市铁西区",
    },
    {
        "id": 2,
        "name": "鞍山市铁西区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "鞍山市人民政府",
        "location": "辽宁省鞍山市铁西区",
    },
    {
        "id": 3,
        "name": "中共鞍山市铁西区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共鞍山市铁西区委员会",
        "location": "辽宁省鞍山市铁西区",
    },
    {
        "id": 4,
        "name": "中共鞍山市铁西区委组织部",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共鞍山市铁西区委员会",
        "location": "辽宁省鞍山市铁西区",
    },
    {
        "id": 5,
        "name": "中共鞍山市铁西区委宣传部",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共鞍山市铁西区委员会",
        "location": "辽宁省鞍山市铁西区",
    },
    {
        "id": 6,
        "name": "中共鞍山市铁西区委政法委员会",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共鞍山市铁西区委员会",
        "location": "辽宁省鞍山市铁西区",
    },
    {
        "id": 7,
        "name": "中共鞍山市铁西区委统战部",
        "type": "党委",
        "level": "乡科级",
        "parent": "中共鞍山市铁西区委员会",
        "location": "辽宁省鞍山市铁西区",
    },
    {
        "id": 8,
        "name": "鞍山市铁西区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "鞍山市人民代表大会常务委员会",
        "location": "辽宁省鞍山市铁西区",
    },
    {
        "id": 9,
        "name": "政协鞍山市铁西区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协鞍山市委员会",
        "location": "辽宁省鞍山市铁西区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # ── Core Leadership ──
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "", "end": "present",
     "rank": "正处级", "note": "姓名、任职时间均待查"},
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "", "end": "present",
     "rank": "正处级", "note": "姓名、任职时间均待查"},

    # ── 区委常委 ──
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start": "", "end": "present",
     "rank": "副处级", "note": "待查"},
    {"person_id": 4, "org_id": 2, "title": "区委常委、副区长", "start": "", "end": "present",
     "rank": "副处级", "note": "负责区政府常务工作"},
    {"person_id": 5, "org_id": 3, "title": "区委常委、区纪委书记、区监委主任", "start": "", "end": "present",
     "rank": "副处级", "note": "待查"},
    {"person_id": 6, "org_id": 4, "title": "区委常委、组织部部长", "start": "", "end": "present",
     "rank": "副处级", "note": "待查"},
    {"person_id": 7, "org_id": 5, "title": "区委常委、宣传部部长", "start": "", "end": "present",
     "rank": "副处级", "note": "待查"},
    {"person_id": 8, "org_id": 6, "title": "区委常委、政法委书记", "start": "", "end": "present",
     "rank": "副处级", "note": "待查"},
    {"person_id": 9, "org_id": 7, "title": "区委常委、统战部部长", "start": "", "end": "present",
     "rank": "副处级", "note": "待查"},

    # ── 前任领导 ──
    {"person_id": 10, "org_id": 1, "title": "前任区委书记", "start": "", "end": "",
     "rank": "正处级", "note": "姓名、任职时间均待查"},
    {"person_id": 11, "org_id": 2, "title": "前任区长", "start": "", "end": "",
     "rank": "正处级", "note": "姓名、任职时间均待查"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记与区长党政主要领导搭档（姓名待确认）",
     "overlap_org": "中共鞍山市铁西区委员会/鞍山市铁西区人民政府",
     "overlap_period": "待查"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "区委书记与区委副书记",
     "overlap_org": "中共鞍山市铁西区委员会",
     "overlap_period": "待查"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "区长与常务副区长",
     "overlap_org": "鞍山市铁西区人民政府",
     "overlap_period": "待查"},
    {"person_a": 1, "person_b": 10, "type": "predecessor_successor",
     "context": "现任与前任区委书记交接（姓名待确认）",
     "overlap_org": "中共鞍山市铁西区委员会",
     "overlap_period": "待查"},
    {"person_a": 2, "person_b": 11, "type": "predecessor_successor",
     "context": "现任与前任区长交接（姓名待确认）",
     "overlap_org": "鞍山市铁西区人民政府",
     "overlap_period": "待查"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "区委书记与纪委书记",
     "overlap_org": "中共鞍山市铁西区委员会",
     "overlap_period": "待查"},
]

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════


def make_source_register() -> list[dict]:
    return [
        {
            "id": "S001",
            "title": "鞍山市铁西区人民政府（官方域名）",
            "url": "http://www.astxq.gov.cn/",
            "publisher": "鞍山市铁西区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "unknown",
            "notes": "政府网站在调查期间无法访问（DNS超时/连接失败）",
        },
        {
            "id": "S002",
            "title": "鞍山市人民政府官网",
            "url": "http://www.anshan.gov.cn/",
            "publisher": "鞍山市人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "鞍山市政府网站可访问，但未直接列出铁西区领导信息",
        },
        {
            "id": "S003",
            "title": "百度百科 - 铁西区（鞍山）",
            "url": "https://baike.baidu.com/item/%E9%93%81%E8%A5%BF%E5%8C%BA/2620282",
            "publisher": "百度百科",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "encyclopedia",
            "reliability": "unknown",
            "notes": "百度百科在调查期间返回CAPTCHA验证，无法获取页面内容",
        },
    ]


def generate_person_json(job: str, name: str) -> dict:
    """Generate per-person graph JSON following person_graph_json.md schema."""
    person_id_str = f"tiexi_anshan_{name}"

    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "鞍山市",
            "region": "铁西区",
            "job": job,
            "task_id": "liaoning_铁西区",
            "time_focus": "2025–2026",
        },
        "identity": {
            "person_id": person_id_str,
            "name": name,
            "aliases": [],
            "gender": "",
            "ethnicity": "",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": f"{name}_",
                "name_birthplace": f"{name}_",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": job,
            "current_org": "中共鞍山市铁西区委员会" if "书记" in job else "鞍山市铁西区人民政府",
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": [],
        },
        "career_timeline": [],
        "organizations": [
            {"org_id": 1, "name": "中共鞍山市铁西区委员会", "type": "党委",
             "level": "县处级", "location": "辽宁省鞍山市铁西区"},
            {"org_id": 2, "name": "鞍山市铁西区人民政府", "type": "政府",
             "level": "县处级", "location": "辽宁省鞍山市铁西区"},
        ],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "完全未知 — 政府网站不可访问，搜索工具均受限",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style cannot be assessed without public records.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至2026年7月，由于搜索工具严重受限，无法进行有效搜索。未发现公开的纪律处分、审计问题或负面报道。",
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
            "biggest_gap": f"铁西区{job}的姓名、出生年月、籍贯、教育背景、完整履历全部未知",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"鞍山市铁西区{job}的姓名是什么？",
                "why_it_matters": "这是最基本的身份信息，是所有后续研究的基础",
                "suggested_queries": [
                    f"鞍山市铁西区 {job}",
                    f"鞍山市铁西区 领导 分工",
                    f"site:astxq.gov.cn {job}",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"鞍山市铁西区{job}的出生年月、籍贯、教育背景？",
                "why_it_matters": "身份去重和档案建库的基础信息",
                "suggested_queries": [
                    f"鞍山市铁西区 {job} 简历",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"鞍山市铁西区{job}的完整职业生涯履历？",
                "why_it_matters": "评估专业背景和职业发展路径",
                "suggested_queries": [
                    f"鞍山市铁西区 {job} 任前公示",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"鞍山市铁西区{job}何时开始担任现职？接替哪位前任？",
                "why_it_matters": "确认任职时间节点和前任/继任关系",
                "suggested_queries": [
                    f"鞍山 市委组织部 铁西区 任免",
                ],
                "last_attempted": AS_OF,
            },
        ],
    }


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    # 1. Build database and GEXF
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
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

    # 2. Write person JSONs for core leaders
    core_people = [
        ("区委书记", "待查_区委书记"),
        ("区长", "待查_区长"),
        ("区委副书记", "待查_区委副书记"),
        ("常务副区长", "待查_常务副区长"),
        ("纪委书记", "待查_纪委书记"),
        ("组织部部长", "待查_组织部部长"),
        ("宣传部部长", "待查_宣传部部长"),
        ("政法委书记", "待查_政法委书记"),
        ("统战部部长", "待查_统战部部长"),
    ]

    for job, name in core_people:
        person_data = generate_person_json(job, name)
        filename = f"{TODAY}-辽宁省-鞍山市-{job}-{name}.json"
        filepath = PERSONS_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(person_data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {filepath}")

    print("\nBuild complete.")


if __name__ == "__main__":
    main()
