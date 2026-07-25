#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 原州区 (Yuanzhou District), 固原市, 宁夏回族自治区.

Investigation date: 2026-07-25
Task ID: ningxia_原州区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - Official government websites for 原州区 and 固原市 were unreachable during investigation.
  - DNS resolution: www.yuanzhouqu.gov.cn and www.guyuan.gov.cn failed to resolve.
  - Web search was degraded: Exa rate-limited, Baidu Baike 403, Jina Reader timeouts.
  - No existing artifacts for 原州区 or 固原市 found in the repository.

Confidence notes:
  - Current officeholders' names could NOT be verified from primary sources during this session
    due to complete web access degradation to Chinese government sites.
  - The build script is structurally complete but requires populating specific leader names
    when official sources become accessible.
  - All person-specific data marked as "unverified" — manual verification from official
    government leadership pages is required.
  - Generic administrative structure (organizations, administrative levels) is confirmed from
    standard administrative division records.
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
SLUG = "原州区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "ningxia_原州区"
if _CURRENT_DIR.name == "ningxia_原州区":
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
# NOTE: Specific officeholder names could not be verified due to complete web
# access degradation. The IDs below are structural placeholders. Populate from
# the 原州区 government website's 领导之窗 (leadership window) page when available.
# Official website (expected): www.yuanzhouqu.gov.cn
# Expected leadership page: /xxgk/ldzc/ or /zwgk/ldzc/

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "待查_区委书记",
        "gender": "",       # unverified
        "ethnicity": "",    # unverified
        "birth": "",        # unverified
        "birthplace": "",   # unverified
        "education": "",    # unverified
        "party_join": "中共党员",
        "work_start": "",   # unverified
        "current_post": "区委书记",
        "current_org": "中共固原市原州区委员会",
        "source": "https://www.yuanzhouqu.gov.cn (unreachable during investigation)",
    },
    {
        "id": 2,
        "name": "待查_区长",
        "gender": "",       # unverified
        "ethnicity": "",    # unverified
        "birth": "",        # unverified
        "birthplace": "",   # unverified
        "education": "",    # unverified
        "party_join": "中共党员",
        "work_start": "",   # unverified
        "current_post": "区委副书记、区长",
        "current_org": "原州区人民政府",
        "source": "https://www.yuanzhouqu.gov.cn (unreachable during investigation)",
    },
    # ══════════════════════════════════════════════════════════════════════
    # Standing Committee (区委常委) — names unknown, structural record
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "待查_常务副区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "原州区人民政府",
        "source": "https://www.yuanzhouqu.gov.cn (unreachable during investigation)",
    },
    {
        "id": 4,
        "name": "待查_区委常委1",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共固原市原州区委员会",
        "source": "https://www.yuanzhouqu.gov.cn (unreachable during investigation)",
    },
    {
        "id": 5,
        "name": "待查_区委常委2",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共固原市原州区委员会",
        "source": "https://www.yuanzhouqu.gov.cn (unreachable during investigation)",
    },
    {
        "id": 6,
        "name": "待查_区委常委3",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共固原市原州区委员会",
        "source": "https://www.yuanzhouqu.gov.cn (unreachable during investigation)",
    },
    {
        "id": 7,
        "name": "待查_区委常委4",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共固原市原州区委员会",
        "source": "https://www.yuanzhouqu.gov.cn (unreachable during investigation)",
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Government Leaders (副区长) — names unknown
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 8,
        "name": "待查_副区长1",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "原州区人民政府",
        "source": "https://www.yuanzhouqu.gov.cn (unreachable during investigation)",
    },
    {
        "id": 9,
        "name": "待查_副区长2",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长（公安分局局长）",
        "current_org": "原州区人民政府",
        "source": "https://www.yuanzhouqu.gov.cn (unreachable during investigation)",
    },
    {
        "id": 10,
        "name": "待查_副区长3",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "原州区人民政府",
        "source": "https://www.yuanzhouqu.gov.cn (unreachable during investigation)",
    },
    {
        "id": 11,
        "name": "待查_副区长4",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "原州区人民政府",
        "source": "https://www.yuanzhouqu.gov.cn (unreachable during investigation)",
    },
    {
        "id": 12,
        "name": "待查_副区长5",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "原州区人民政府",
        "source": "https://www.yuanzhouqu.gov.cn (unreachable during investigation)",
    },
    {
        "id": 13,
        "name": "待查_副区长6",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "原州区人民政府",
        "source": "https://www.yuanzhouqu.gov.cn (unreachable during investigation)",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共固原市原州区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共固原市委员会",
        "location": "宁夏回族自治区固原市原州区",
    },
    {
        "id": 2,
        "name": "原州区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "固原市人民政府",
        "location": "宁夏回族自治区固原市原州区",
    },
    {
        "id": 3,
        "name": "原州区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "固原市人大常委会",
        "location": "宁夏回族自治区固原市原州区",
    },
    {
        "id": 4,
        "name": "原州区政协",
        "type": "政协",
        "level": "县处级",
        "parent": "固原市政协",
        "location": "宁夏回族自治区固原市原州区",
    },
    {
        "id": 5,
        "name": "原州区纪委监委",
        "type": "党委",
        "level": "县处级",
        "parent": "中共固原市原州区委员会",
        "location": "宁夏回族自治区固原市原州区",
    },
    {
        "id": 6,
        "name": "原州区公安分局",
        "type": "政府",
        "level": "乡科级",
        "parent": "原州区人民政府",
        "location": "宁夏回族自治区固原市原州区",
    },
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "", "end": "present", "rank": "正处级", "note": "主持区政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 常务副区长
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start": "", "end": "present", "rank": "副处级", "note": "负责区政府常务工作"},
    # 其他区委常委
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 副区长
    {"person_id": 8, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": "负责公安、信访、司法"},
    {"person_id": 9, "org_id": 6, "title": "公安分局局长", "start": "", "end": "present", "rank": "正科级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────────
# Relationship types: overlap (same org/time), superior_subordinate, etc.

relationships = [
    # 区委书记 — 区长 (党政正职搭档)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "区委书记与区长党政正职搭档关系", "overlap_org": "中共固原市原州区委员会/原州区人民政府", "overlap_period": "present"},
    # 区委书记 — 区委常委 (领导关系)
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "区委书记领导常务副区长", "overlap_org": "中共固原市原州区委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "区委书记领导区委常委", "overlap_org": "中共固原市原州区委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "区委书记领导区委常委", "overlap_org": "中共固原市原州区委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "区委书记领导区委常委", "overlap_org": "中共固原市原州区委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "区委书记领导区委常委", "overlap_org": "中共固原市原州区委员会", "overlap_period": "present"},
    # 区长 — 副区长 (政府内部上下级)
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "区长领导常务副区长", "overlap_org": "原州区人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "区长领导副区长", "overlap_org": "原州区人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "区长领导副区长", "overlap_org": "原州区人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "区长领导副区长", "overlap_org": "原州区人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "区长领导副区长", "overlap_org": "原州区人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "区长领导副区长", "overlap_org": "原州区人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "区长领导副区长", "overlap_org": "原州区人民政府", "overlap_period": "present"},
]


# ═══════════════════════════════════════════════════════════════════════════
# Person JSON writer
# ═══════════════════════════════════════════════════════════════════════════

def write_person_json(person: dict, job: str) -> Path:
    """Write a person graph JSON file to the staging directory."""
    person_id = f"yuanzhou_{person['name']}"
    name_display = person["name"].replace("待查_", "")  # cleaner display
    path = PJSON_DIR / f"{TODAY}-宁夏回族自治区-固原市-{job}-{person['name']}.json"
    doc = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "宁夏回族自治区",
            "city": "固原市",
            "region": "原州区",
            "job": job,
            "task_id": "ningxia_原州区",
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
            "is_current_confirmed": False,
            "source_ids": []
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": person.get("current_org", ""),
                "title": person.get("current_post", ""),
                "level": "县处级",
                "location": "宁夏回族自治区固原市原州区",
                "system": "party" if "书记" in person.get("current_post", "") else "government",
                "rank": "正处级" if job in ["区委书记", "区长"] else "副处级",
                "is_key_promotion": True if job in ["区委书记", "区长"] else False,
                "notes": "Current role — name and details not verified due to web access degradation",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "organizations": [
            {"id": 1, "name": "中共固原市原州区委员会", "type": "党委"},
            {"id": 2, "name": "原州区人民政府", "type": "政府"},
        ],
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
                "description": "No disciplinary or integrity red flags found — leader names not confirmed, so no search possible.",
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
            "biggest_gap": "All biographical data — complete web access degradation prevented any source verification"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"原州区现任区委书记姓名及完整履历",
                "why_it_matters": "区委书记是原州区最高领导，其身份信息是关系网络分析的基础",
                "suggested_queries": ["原州区 区委书记", "原州区 领导之窗", "原州区委书记"],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": f"原州区现任区长姓名及完整履历",
                "why_it_matters": "区长是区政府主要负责人，其身份信息是关系网络分析的基础",
                "suggested_queries": ["原州区 区长", "原州区人民政府 领导"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": "原州区党委常委完整名单",
                "why_it_matters": "完整领导层名单是构建区级权力关系网络的基础",
                "suggested_queries": ["原州区委常委", "原州区 领导分工"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": "原州区副区长完整名单及分工",
                "why_it_matters": "副区长分工能反映各部门工作关系网络",
                "suggested_queries": ["原州区 副区长 分工"],
                "last_attempted": AS_OF
            }
        ]
    }
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
    write_person_json(persons[0], "区委书记")   # 待查_区委书记
    write_person_json(persons[1], "区长")       # 待查_区长

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
    print(f"\n⚠️  IMPORTANT: All person names are placeholders. Run this script again after")
    print(f"   verifying actual officeholders from www.yuanzhouqu.gov.cn (领导之窗).")


if __name__ == "__main__":
    main()
