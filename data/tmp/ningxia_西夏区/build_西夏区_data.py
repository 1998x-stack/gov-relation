#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 西夏区 (Xixia District), 银川市, 宁夏回族自治区.

Investigation date: 2026-07-25
Task ID: ningxia_西夏区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - local.cctv.com — 央视网地方频道新闻报道（primary source, current as of July 2026）
    - https://local.cctv.com/2026/05/08/ARTILRcbSbVRVZTd44jd3Z6M260508.shtml (教育发展联盟大会，确认庞子杰为区委书记)
    - https://local.cctv.com/2026/03/13/ARTIYn93joPHo7ucc1M5Hwsk260313.shtml (一季度项目推进)
    - https://local.cctv.com/2026/06/16/ARTIKA3JXCuq9bSsZHkYdxIe260616.shtml (城中村改造)
    - https://local.cctv.com/2026/01/21/ARTIIn5UFhcDwhMoZKGDuYtZ260121.shtml (招商赋能)
  - Web search was degraded: Exa rate-limited, Baidu Baike 403, Jina Reader timeouts, government sites WAF-blocked

Confidence notes:
  - 区委书记庞子杰: confirmed via CCTV news article (2026-05-08), also serves as 银川市人大常委会副主任
  - 区长: unverified — web access limitations prevented confirmation from available sources
  - All claims labeled with confidence level; gaps explicitly documented
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "西夏区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "ningxia_西夏区"
if _CURRENT_DIR.name == "ningxia_西夏区":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-9 current party/government leaders

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "庞子杰",
        "gender": "男",
        "ethnicity": "", # unverified
        "birth": "",      # unverified
        "birthplace": "", # unverified
        "education": "",  # unverified
        "party_join": "中共党员",
        "work_start": "", # unverified
        "current_post": "区委书记",
        "current_org": "中共银川市西夏区委员会",
        "source": "https://local.cctv.com/2026/05/08/ARTILRcbSbVRVZTd44jd3Z6M260508.shtml",
    },
    {
        "id": 2,
        "name": "（待确认）",  # Placeholder - 区长 name not confirmed via available web sources
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "西夏区人民政府",
        "source": "",
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Leaders identified from news (partial)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "西夏区人民政府",
        "source": "",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共银川市西夏区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共银川市委员会",
        "location": "宁夏回族自治区银川市西夏区",
    },
    {
        "id": 2,
        "name": "西夏区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "银川市人民政府",
        "location": "宁夏回族自治区银川市西夏区",
    },
    {
        "id": 3,
        "name": "银川市人大常委会",
        "type": "人大",
        "level": "地市级",
        "parent": "宁夏回族自治区人大常委会",
        "location": "宁夏回族自治区银川市",
    },
    {
        "id": 4,
        "name": "西夏区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "银川市人大常委会",
        "location": "宁夏回族自治区银川市西夏区",
    },
    {
        "id": 5,
        "name": "西夏区政协",
        "type": "政协",
        "level": "县处级",
        "parent": "银川市政协",
        "location": "宁夏回族自治区银川市西夏区",
    },
    {
        "id": 6,
        "name": "西夏区纪委监委",
        "type": "党委",
        "level": "县处级",
        "parent": "中共银川市西夏区委员会",
        "location": "宁夏回族自治区银川市西夏区",
    },
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 庞子杰
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "兼任银川市人大常委会副主任（副厅级）"},
    {"person_id": 1, "org_id": 3, "title": "银川市人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "据央视网2026年5月报道"},
]

# ── Relationships ────────────────────────────────────────────────────────────
relationships = [
    # Person-Organization edges: 庞子杰 at 区委
    {"person_a": 100001, "person_b": 1, "type": "worked_at", "context": "区委书记", "overlap_org": "中共银川市西夏区委员会", "overlap_period": "present"},
    # 庞子杰 at 人大常委会
    {"person_a": 100003, "person_b": 1, "type": "worked_at", "context": "银川市人大常委会副主任", "overlap_org": "银川市人大常委会", "overlap_period": "present"},
]

# ═══════════════════════════════════════════════════════════════════════════
# Person JSON writer
# ═══════════════════════════════════════════════════════════════════════════

def write_person_json(person: dict, job: str, open_questions: list | None = None) -> Path:
    """Write a person graph JSON file to the staging directory."""
    person_id = f"xixia_{person['name']}"
    path = PJSON_DIR / f"{TODAY}-宁夏回族自治区-银川市-{job}-{person['name']}.json"
    if open_questions is None:
        open_questions = []

    doc = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "宁夏回族自治区",
            "city": "银川市",
            "region": "西夏区",
            "job": job,
            "task_id": "ningxia_西夏区",
            "time_focus": "2026-07 (current)"
        },
        "identity": {
            "person_id": person_id,
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth','')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace','')}",
                "official_profile_url": person.get("source", "")
            }
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "正处级" if job in ["区委书记", "区长"] else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True if person["name"] != "（待确认）" else False,
            "source_ids": ["S001"] if person["source"] else []
        },
        "career_timeline": [],
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
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "No disciplinary or integrity red flags found in publicly available sources during investigation.",
                "date": "",
                "confidence": "plausible",
                "source_ids": []
            }
        ],
        "source_register": [],
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "partial",
            "current_role": "confirmed" if person["name"] != "（待确认）" else "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "Complete career history, birth year, birthplace, education"
        },
        "open_questions": open_questions
    }

    # Add career timeline entries
    if person["name"] != "（待确认）":
        doc["career_timeline"].append({
            "start": "unknown",
            "end": "present",
            "org": person.get("current_org", ""),
            "title": person.get("current_post", ""),
            "level": "县处级",
            "location": "宁夏回族自治区银川市西夏区",
            "system": "party" if "书记" in person.get("current_post", "") else "government",
            "rank": "副厅级" if "副主任" in person.get("current_post", "") else "正处级",
            "is_key_promotion": True,
            "notes": "Current role confirmed by CCTV news reports (May 2026)",
            "confidence": "confirmed",
            "source_ids": ["S001"]
        })
        if "市人大常委会" in person.get("current_post", "") or job == "区委书记":
            doc["career_timeline"].append({
                "start": "unknown",
                "end": "present",
                "org": "银川市人大常委会",
                "title": "银川市人大常委会副主任",
                "level": "地市级",
                "location": "宁夏回族自治区银川市",
                "system": "party",
                "rank": "副厅级",
                "is_key_promotion": True,
                "notes": "Concurrent role confirmed by CCTV news",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            })
        doc["organizations"] = [
            {"id": 1, "name": "中共银川市西夏区委员会", "type": "党委"},
            {"id": 2, "name": "西夏区人民政府", "type": "政府"},
            {"id": 3, "name": "银川市人大常委会", "type": "人大"},
        ]
        doc["source_register"].append({
            "id": "S001",
            "title": "2026年西夏区教育发展联盟大会顺利召开 - 央视网",
            "url": "https://local.cctv.com/2026/05/08/ARTILRcbSbVRVZTd44jd3Z6M260508.shtml",
            "publisher": "央视网",
            "published_at": "2026-05-08",
            "accessed_at": AS_OF,
            "source_type": "media",
            "reliability": "high",
            "notes": "CCTV news report confirming 庞子杰 as 西夏区委书记 and 银川市人大常委会副主任"
        })

    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {path.name}")
    return path


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    print(f"Building {SLUG} dataset (staging: {STAGING})")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    # Run build (DB + GEXF)
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Write person JSONs for the core targets
    print("\nWriting person JSONs ...")

    # 庞子杰 - confirmed 区委书记
    write_person_json(persons[0], "区委书记", open_questions=[
        {
            "priority": "critical",
            "question": "庞子杰的完整履历（出生年月、籍贯、学历、入党时间、参加工作时间和历任职务）",
            "why_it_matters": "核心领导的身份信息和晋升路径是关系网络分析的基础",
            "suggested_queries": ["庞子杰 简历 西夏区", "庞子杰 任前公示", "庞子杰 出生年月", "庞子杰 银川 人大"],
            "last_attempted": AS_OF
        },
        {
            "priority": "critical",
            "question": "庞子杰何时开始担任西夏区委书记？此前职务是什么？",
            "why_it_matters": "理解干部交流模式和晋升路径",
            "suggested_queries": ["庞子杰 西夏区 区委书记 任职", "庞子杰 调任"],
            "last_attempted": AS_OF
        },
        {
            "priority": "high",
            "question": "西夏区现任区长姓名",
            "why_it_matters": "党政一把手是关系网络的核心节点，缺少区长信息无法构建完整网络",
            "suggested_queries": ["银川市西夏区 区长", "西夏区 人民政府 区长", "西夏区 人大 任命 区长"],
            "last_attempted": AS_OF
        },
        {
            "priority": "high",
            "question": "西夏区区委常委班子构成（常务副区长、纪委书记、组织部长、宣传部长、政法委书记等）",
            "why_it_matters": "完整的常委会构成是区级权力结构分析的基础",
            "suggested_queries": ["西夏区 区委常委", "西夏区 领导分工"],
            "last_attempted": AS_OF
        },
        {
            "priority": "medium",
            "question": "西夏区前任区委书记去向",
            "why_it_matters": "了解干部交流模式和区域班子成员变动趋势",
            "suggested_queries": ["西夏区 原区委书记", "西夏区 前任 区委书记 调任"],
            "last_attempted": AS_OF
        }
    ])

    # Note: since 区长 name is not confirmed, we try to write a placeholder
    # for documentation purposes. The --apply promotion will include files
    # that exist; we can create the placeholder file too.
    write_person_json(
        {
            "id": 2,
            "name": "（待确认-区长姓名）",
            "gender": "",
            "ethnicity": "",
            "birth": "",
            "birthplace": "",
            "education": "",
            "party_join": "",
            "work_start": "",
            "current_post": "区委副书记、区长",
            "current_org": "西夏区人民政府",
            "source": ""
        },
        "区长",
        open_questions=[
            {
                "priority": "critical",
                "question": "西夏区现任区长姓名",
                "why_it_matters": "区政府主要负责人，关系网络的核心节点",
                "suggested_queries": ["银川市西夏区 区长", "西夏区 人民政府 区长", "西夏区 人大 任命 区长 2025 2026"],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": "西夏区现任区长的完整履历（出生年月、籍贯、学历、入党时间、工作经历）",
                "why_it_matters": "核心领导的身份信息和晋升路径是关系网络分析的基础",
                "suggested_queries": ["西夏区 区长 简历", "西夏区 区长 任前公示"],
                "last_attempted": AS_OF
            }
        ]
    )

    # Verify outputs
    print("\nOutput verification:")
    for path in [DB_PATH, GEXF_PATH]:
        if path.exists():
            size_kb = path.stat().st_size / 1024
            print(f"  ✅ {path.name} ({size_kb:.1f} KB)")
        else:
            print(f"  ❌ {path.name} MISSING")

    json_count = len(list(PJSON_DIR.glob(f"{TODAY}-*.json")))
    print(f"  ✅ Person JSON files: {json_count}")

    print(f"\n{SLUG} build complete.")
    print(f"\n⚠️  NOTE: 区长 name was not confirmed due to web access limitations.")
    print(f"  See open_questions in person JSONs and report/open_gaps.md for details.")


if __name__ == "__main__":
    main()
