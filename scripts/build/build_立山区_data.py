#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 立山区 (Lishan District), 鞍山市, 辽宁省.

Investigation date: 2026-07-25
Task ID: liaoning_立山区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - Web search (Exa) was rate-limited during this investigation
  - Direct fetches to baike.baidu.com returned 403
  - Direct fetches to zh.wikipedia.org timed out
  - Jina Reader timed out for known URLs
  - Google search via direct fetch returned CAPTCHA
  - All remote sources were inaccessible during this session

Confidence notes:
  - Current 区委书记 and 区长 names could not be independently verified via web sources
  - All person data in this build is marked "unverified" — requires confirmation from
    official sources (www.anshan.gov.cn leadership page, 鞍山市委组织部任前公示)
  - Previous leadership and detailed career timelines are not available
  - Generated under "partial evidence artifact mode" per source_fallbacks.md
"""

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Add project root to sys.path
BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

SLUG = "立山区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# Staging paths
STAGING_DIR = Path(BASE)
DB_PATH = str(STAGING_DIR / f"{SLUG}_network.db")
GEXF_PATH = str(STAGING_DIR / f"{SLUG}_network.gexf")

# ═══════════════════════════════════════════════════════════════════════════════
# Data — NOTE: Due to degraded web access, names and roles are unverified.
# All data requires source confirmation before use in analysis.
# ═══════════════════════════════════════════════════════════════════════════════

# ── Core leadership targets ──
# Research status: Web sources inaccessible (Exa rate-limited, Baidu 403,
#   Wikipedia timeout, Jina Reader timeout, Google CAPTCHA).
# These entries represent the KNOWN structure (区委书记 + 区长 as the two
# core targets) but actual current officeholder names were not verifiable.
#
# Next step: Access https://www.anshan.gov.cn or search for "鞍山市立山区
# 领导班子" or "立山区 领导之窗" to confirm the current holders.

persons_data = [
    # ══════════════════════════════════════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ══════════════════════════════════════════════════════════════════════════

    # 【待查】区委书记 — 立山区
    # Source: none verified — placeholder pending web access restoration
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
        "current_org": "中共鞍山市立山区委员会",
        "source": "未确认 — 需访问鞍山市人民政府网站或搜索确认"
    },
    # 【待查】区长 — 立山区
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
        "current_org": "鞍山市立山区人民政府",
        "source": "未确认 — 需访问鞍山市人民政府网站或搜索确认"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # Other Key Leadership (placeholder slots)
    # ══════════════════════════════════════════════════════════════════════════
    # These represent known structural roles in a standard county/district
    # leadership team. Names are not yet known.

    # 区人大常委会主任
    {
        "id": 3,
        "name": "待查_人大主任",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "鞍山市立山区人民代表大会常务委员会",
        "source": "未确认 — 结构占位"
    },
    # 区政协主席
    {
        "id": 4,
        "name": "待查_政协主席",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议鞍山市立山区委员会",
        "source": "未确认 — 结构占位"
    },
    # 区委副书记
    {
        "id": 5,
        "name": "待查_副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共鞍山市立山区委员会",
        "source": "未确认 — 结构占位"
    },
    # 常务副区长
    {
        "id": 6,
        "name": "待查_常务副区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "常务副区长",
        "current_org": "鞍山市立山区人民政府",
        "source": "未确认 — 结构占位"
    },
    # 区纪委书记
    {
        "id": 7,
        "name": "待查_纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区纪委书记、监委主任",
        "current_org": "中共鞍山市立山区纪律检查委员会",
        "source": "未确认 — 结构占位"
    },
    # 区委组织部部长
    {
        "id": 8,
        "name": "待查_组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委组织部部长",
        "current_org": "中共鞍山市立山区委组织部",
        "source": "未确认 — 结构占位"
    },
    # 区委政法委书记
    {
        "id": 9,
        "name": "待查_政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委政法委书记",
        "current_org": "中共鞍山市立山区委政法委",
        "source": "未确认 — 结构占位"
    },
    # 区委宣传部部长
    {
        "id": 10,
        "name": "待查_宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委宣传部部长",
        "current_org": "中共鞍山市立山区委宣传部",
        "source": "未确认 — 结构占位"
    },
]

organizations_data = [
    {
        "id": 1,
        "name": "中共鞍山市立山区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共鞍山市委员会",
        "location": "鞍山市立山区"
    },
    {
        "id": 2,
        "name": "鞍山市立山区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "鞍山市人民政府",
        "location": "鞍山市立山区"
    },
    {
        "id": 3,
        "name": "鞍山市立山区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "鞍山市人民代表大会常务委员会",
        "location": "鞍山市立山区"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议鞍山市立山区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协鞍山市委员会",
        "location": "鞍山市立山区"
    },
    {
        "id": 5,
        "name": "中共鞍山市立山区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共鞍山市纪律检查委员会",
        "location": "鞍山市立山区"
    },
    {
        "id": 6,
        "name": "中共鞍山市立山区委组织部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共鞍山市立山区委员会",
        "location": "鞍山市立山区"
    },
    {
        "id": 7,
        "name": "中共鞍山市立山区委政法委",
        "type": "党委",
        "level": "县处级",
        "parent": "中共鞍山市立山区委员会",
        "location": "鞍山市立山区"
    },
    {
        "id": 8,
        "name": "中共鞍山市立山区委宣传部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共鞍山市立山区委员会",
        "location": "鞍山市立山区"
    },
]

positions_data = [
    # 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "待确认 — 需搜索确认现任职"},
    # 区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "待确认 — 需搜索确认现任职"},
    # 人大主任
    {"person_id": 3, "org_id": 3, "title": "区人大常委会主任", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "待确认"},
    # 政协主席
    {"person_id": 4, "org_id": 4, "title": "区政协主席", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "待确认"},
    # 区委副书记
    {"person_id": 5, "org_id": 1, "title": "区委副书记", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "通常由区长兼任或设专职副书记"},
    # 常务副区长
    {"person_id": 6, "org_id": 2, "title": "常务副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "待确认"},
    # 区纪委书记
    {"person_id": 7, "org_id": 5, "title": "区纪委书记、监委主任", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "待确认"},
    # 组织部长
    {"person_id": 8, "org_id": 6, "title": "区委组织部部长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "通常兼任区委常委"},
    # 政法委书记
    {"person_id": 9, "org_id": 7, "title": "区委政法委书记", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "通常兼任区委常委"},
    # 宣传部长
    {"person_id": 10, "org_id": 8, "title": "区委宣传部部长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "通常兼任区委常委"},
]

relationships_data = [
    # 区委书记 ↔ 区长 — 党政搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记—区长工作搭档，共同主持立山区党政工作", "overlap_org": "立山区", "overlap_period": "unknown-present"},
    # 区委书记 ↔ 区委副书记
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "书记—副书记工作关系", "overlap_org": "中共立山区委员会", "overlap_period": "unknown-present"},
    # 区长 ↔ 常务副区长
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "区长—常务副区长工作关系", "overlap_org": "立山区人民政府", "overlap_period": "unknown-present"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON generation
# ═══════════════════════════════════════════════════════════════════════════════

PERSON_JSON_TEMPLATES = {
    "区委书记": {
        "filename": f"{TODAY}-辽宁省-鞍山市-区委书记-待查_区委书记.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "辽宁省",
                "city": "鞍山市",
                "region": "立山区",
                "job": "区委书记",
                "task_id": "liaoning_立山区",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "anshan_lishan_district_secretary",
                "name": "待查_区委书记",
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
                    "name_birth": "",
                    "name_birthplace": "",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "区委书记",
                "current_org": "中共鞍山市立山区委员会",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": False,
                "source_ids": []
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
                "promotion_velocity": {
                    "summary": "履历信息完全未知",
                    "notable_fast_promotions": []
                }
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
                    "description": "因网络访问受限，未能在本调查周期内确认身份信息或搜索到任何风险信号",
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
                "biggest_gap": "现任区委书记姓名及所有履历信息均未确认"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "立山区现任区委书记是谁？请确认姓名、性别、民族、出生年月等基本信息",
                    "why_it_matters": "核心调查目标，关乎整份调查的完整性",
                    "suggested_queries": [
                        "鞍山市立山区 区委书记",
                        "立山区 领导之窗",
                        "www.anshan.gov.cn 立山区 领导分工"
                    ],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "critical",
                    "question": "现任区委书记的完整简历（教育背景、历任职务、晋升时间线）",
                    "why_it_matters": "理解其晋升路径和可能的工作关系网络",
                    "suggested_queries": [
                        "{名称} 简历 立山区",
                        "{名称} 任前公示",
                        "{名称} 百度百科"
                    ],
                    "last_attempted": AS_OF
                }
            ]
        }
    },
    "区长": {
        "filename": f"{TODAY}-辽宁省-鞍山市-区长-待查_区长.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "辽宁省",
                "city": "鞍山市",
                "region": "立山区",
                "job": "区长",
                "task_id": "liaoning_立山区",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "anshan_lishan_district_mayor",
                "name": "待查_区长",
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
                    "name_birth": "",
                    "name_birthplace": "",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "区长",
                "current_org": "鞍山市立山区人民政府",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": False,
                "source_ids": []
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
                "promotion_velocity": {
                    "summary": "履历信息完全未知",
                    "notable_fast_promotions": []
                }
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
                    "description": "因网络访问受限，未能在本调查周期内确认身份信息或搜索到任何风险信号",
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
                "biggest_gap": "现任区长姓名及所有履历信息均未确认"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "立山区现任区长是谁？请确认姓名、性别、民族、出生年月等基本信息",
                    "why_it_matters": "核心调查目标，关乎整份调查的完整性",
                    "suggested_queries": [
                        "鞍山市立山区 区长",
                        "立山区 区长 分工",
                        "鞍山市 组织部 任前公示 立山区"
                    ],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "critical",
                    "question": "现任区长的完整简历（教育背景、历任职务、晋升时间线）",
                    "why_it_matters": "理解其晋升路径和可能的工作关系网络",
                    "suggested_queries": [
                        "{名称} 简历 立山区",
                        "{名称} 任前公示 鞍山"
                    ],
                    "last_attempted": AS_OF
                }
            ]
        }
    }
}


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

def write_person_json(data: dict, filename: str) -> None:
    """Write a person JSON file to the staging directory."""
    filepath = STAGING_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {filepath}")


def main() -> None:
    print(f"Building {SLUG} network data...")
    print(f"  DB path: {DB_PATH}")
    print(f"  GEXF path: {GEXF_PATH}")
    print()

    # Build database and GEXF
    run_build(
        slug=SLUG,
        persons=persons_data,
        organizations=organizations_data,
        positions=positions_data,
        relationships=relationships_data,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    # Write person JSONs
    print(f"\nWriting person JSON files to {STAGING_DIR}")
    for key, template in PERSON_JSON_TEMPLATES.items():
        write_person_json(template["data"], template["filename"])

    print(f"\n{'=' * 60}")
    print(f"Build complete for {SLUG}")
    print(f"{'=' * 60}")
    print(f"\nFiles created:")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")
    for key, template in PERSON_JSON_TEMPLATES.items():
        print(f"  Person:   {STAGING_DIR / template['filename']}")
    print(f"\n⚠  WARNING: All person names are placeholders (待查_xxx).")
    print(f"   Web search was completely unavailable during this investigation.")
    print(f"   Update this file with real names from official sources before use.")
    print(f"\n   Priority sources to check:")
    print(f"   - https://www.anshan.gov.cn (鞍山市人民政府)")
    print(f"   - Search: '立山区 领导班子 领导分工'")
    print(f"   - Search: '鞍山市 区委书记 立山区'")
    print(f"   - 鞍山市委组织部 任前公示")
    print()


if __name__ == "__main__":
    main()
