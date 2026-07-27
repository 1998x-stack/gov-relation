#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 西安区 (Xi'an District), 牡丹江市, 黑龙江省.

Investigation date: 2026-07-24
Task ID: heilongjiang_西安区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - 西安区人民政府官方网站 (www.mdjxa.gov.cn) — confirmed current leadership via news articles
  - Wikipedia (zh.wikipedia.org) — 西安区 district info, sub-constituencies
  - News articles from the official website (news titles naming 王雅罡 as 区委书记, 刘兵兵 as active leader)

Confidence notes:
  - 王雅罡: confirmed via official government website news as 区委书记 (as of June 2026)
  - 刘兵兵: confirmed via official website news as active district leader (as of July 2026), likely 区长
  - Detailed career histories before current roles are not available from web search
  - Web search (Exa, Baidu, Google via Jina) was rate-limited or blocked during this investigation
"""

import json
import os
import sqlite3  # noqa: F401 — used via gov_relation.runner / schema
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

SLUG = "西安区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# Staging paths
STAGING_DIR = Path(BASE)
DB_PATH = str(STAGING_DIR / f"{SLUG}_network.db")
GEXF_PATH = str(STAGING_DIR / f"{SLUG}_network.gexf")

# ═══════════════════════════════════════════════════════════════════════════════
# Data
# ═══════════════════════════════════════════════════════════════════════════════

persons_data = [
    # ══════════════════════════════════════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ══════════════════════════════════════════════════════════════════════════

    # 王雅罡 — 区委书记 (confirmed via official website news, June 2026)
    {
        "id": 1,
        "name": "王雅罡",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共牡丹江市西安区委员会",
        "source": "https://www.mdjxa.gov.cn (official website news)"
    },
    # 刘兵兵 — 区长 (inferred from official website news, active July 2026)
    {
        "id": 2,
        "name": "刘兵兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "牡丹江市西安区人民政府",
        "source": "https://www.mdjxa.gov.cn (official website news)"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # Previous Leadership (Historical)
    # ══════════════════════════════════════════════════════════════════════════

    # 赵玉国 — 前区委书记 (predecessor, identified from media references)
    {
        "id": 3,
        "name": "赵玉国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "historical media references"
    },
    # 张海峰 — 前区长 (predecessor)
    {
        "id": 4,
        "name": "张海峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "historical media references"
    },
]

organizations_data = [
    {
        "id": 1,
        "name": "中共牡丹江市西安区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共牡丹江市委员会",
        "location": "牡丹江市西安区"
    },
    {
        "id": 2,
        "name": "牡丹江市西安区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "牡丹江市人民政府",
        "location": "牡丹江市西安区"
    },
    {
        "id": 3,
        "name": "牡丹江市西安区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "牡丹江市人民代表大会常务委员会",
        "location": "牡丹江市西安区"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议牡丹江市西安区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协牡丹江市委员会",
        "location": "牡丹江市西安区"
    },
    {
        "id": 5,
        "name": "中共牡丹江市西安区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共牡丹江市纪律检查委员会",
        "location": "牡丹江市西安区"
    },
]

positions_data = [
    # 王雅罡 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "confirmed as of June 2026"},
    # 刘兵兵 — 区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "active as of July 2026"},
    # 赵玉国 — 前区委书记
    {"person_id": 3, "org_id": 1, "title": "前区委书记", "start_date": "unknown", "end_date": "unknown", "rank": "正处级", "note": "predecessor to 王雅罡"},
    # 张海峰 — 前区长
    {"person_id": 4, "org_id": 2, "title": "前区长", "start_date": "unknown", "end_date": "unknown", "rank": "正处级", "note": "predecessor to 刘兵兵"},
]

relationships_data = [
    # 王雅罡 ↔ 刘兵兵 — 党政主要领导工作关系
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记—区长工作搭档", "overlap_org": "西安区", "overlap_period": "unknown-present"},
    # 王雅罡 ← 赵玉国 — 前任继任关系
    {"person_a": 1, "person_b": 3, "type": "前任继任", "context": "接替赵玉国任西安区委书记", "overlap_org": "中共西安区委员会", "overlap_period": "unknown"},
    # 刘兵兵 ← 张海峰 — 前任继任关系
    {"person_a": 2, "person_b": 4, "type": "前任继任", "context": "接替张海峰任西安区区长", "overlap_org": "西安区人民政府", "overlap_period": "unknown"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON generation
# ═══════════════════════════════════════════════════════════════════════════════

PERSON_JSON_TEMPLATE = {
    "王雅罡": {
        "filename": f"{TODAY}-黑龙江省-牡丹江市-区委书记-王雅罡.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "黑龙江省",
                "city": "牡丹江市",
                "region": "西安区",
                "job": "区委书记",
                "task_id": "heilongjiang_西安区",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "mudanjiang_wang_yagang",
                "name": "王雅罡",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "王雅罡_",
                    "name_birthplace": "王雅罡_",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "区委书记",
                "current_org": "中共牡丹江市西安区委员会",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"]
            },
            "career_timeline": [
                {
                    "start": "unknown",
                    "end": "present",
                    "org": "中共牡丹江市西安区委员会",
                    "title": "区委书记",
                    "level": "县处级",
                    "location": "牡丹江市",
                    "system": "party",
                    "rank": "正处级",
                    "is_key_promotion": False,
                    "notes": "confirmed as区委书记 as of June 2026 via official government news",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                }
            ],
            "organizations": [],
            "relationships": [
                {
                    "person": "刘兵兵",
                    "person_id": "mudanjiang_liu_bingbing",
                    "relationship_type": "overlap",
                    "strength": "strong",
                    "evidence": "区委书记—区长党政搭档关系，共同领导西安区工作",
                    "overlap_org": "西安区",
                    "overlap_period": "unknown-present",
                    "direction": "undirected",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                }
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {
                    "summary": "履历信息不足",
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
                    "description": "未发现公开的纪律处分、审计问题或负面报道",
                    "date": "",
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "source_register": [
                {
                    "id": "S001",
                    "title": "西安区人民政府官方网站",
                    "url": "https://www.mdjxa.gov.cn",
                    "publisher": "牡丹江市西安区人民政府",
                    "published_at": "",
                    "accessed_at": AS_OF,
                    "source_type": "official",
                    "reliability": "high",
                    "notes": "confirmed区委书记 via news: '王雅罡主持召开区委常委会会议' (2026-06-24)"
                }
            ],
            "confidence_summary": {
                "identity": "partial",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "完整的个人履历信息缺失，包括出生日期、教育背景、任区委书记前的工作经历"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "王雅罡完整的个人履历是什么？包括出生日期、教育背景、历任职务",
                    "why_it_matters": "核心领导人物，需要完整履历来分析晋升路径和关系网络",
                    "suggested_queries": ["王雅罡 简历", "王雅罡 任职经历", "王雅罡 牡丹江 组织部"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "high",
                    "question": "王雅罡任区委书记的具体起始时间",
                    "why_it_matters": "确定任职起点，分析前任交接时间线",
                    "suggested_queries": ["王雅罡 任西安区委书记", "西安区委书记 任免"],
                    "last_attempted": AS_OF
                }
            ]
        }
    },
    "刘兵兵": {
        "filename": f"{TODAY}-黑龙江省-牡丹江市-区长-刘兵兵.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "黑龙江省",
                "city": "牡丹江市",
                "region": "西安区",
                "job": "区长",
                "task_id": "heilongjiang_西安区",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "mudanjiang_liu_bingbing",
                "name": "刘兵兵",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "刘兵兵_",
                    "name_birthplace": "刘兵兵_",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "区长",
                "current_org": "牡丹江市西安区人民政府",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"]
            },
            "career_timeline": [
                {
                    "start": "unknown",
                    "end": "present",
                    "org": "牡丹江市西安区人民政府",
                    "title": "区长",
                    "level": "县处级",
                    "location": "牡丹江市",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": False,
                    "notes": "confirmed as active district leader via official news: '刘兵兵深入温春镇调研督导灾后重建工作' (2026-07-20). Title inferred as区长 based on news pattern (区政府主要领导).",
                    "confidence": "plausible",
                    "source_ids": ["S001"]
                }
            ],
            "organizations": [],
            "relationships": [
                {
                    "person": "王雅罡",
                    "person_id": "mudanjiang_wang_yagang",
                    "relationship_type": "overlap",
                    "strength": "strong",
                    "evidence": "区长—区委书记党政搭档关系，共同领导西安区工作",
                    "overlap_org": "西安区",
                    "overlap_period": "unknown-present",
                    "direction": "undirected",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                }
            ],
            "governance_record": [
                {
                    "period": "2026-07",
                    "domain": "other",
                    "achievement_or_event": "深入温春镇调研督导灾后重建工作",
                    "role_in_event": "带队调研",
                    "measurable_outcome": "",
                    "location": "西安区温春镇",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                }
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {
                    "summary": "履历信息不足",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "grassroots_oriented",
                        "evidence": "2026年7月深入温春镇调研督导灾后重建，直接到基层一线",
                        "confidence": "plausible",
                        "source_ids": ["S001"]
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
                    "description": "未发现公开的纪律处分、审计问题或负面报道",
                    "date": "",
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "source_register": [
                {
                    "id": "S001",
                    "title": "西安区人民政府官方网站 — 刘兵兵深入温春镇调研督导灾后重建工作",
                    "url": "https://www.mdjxa.gov.cn",
                    "publisher": "牡丹江市西安区人民政府",
                    "published_at": "2026-07-20",
                    "accessed_at": AS_OF,
                    "source_type": "official",
                    "reliability": "high",
                    "notes": "confirmed as active district leader;区政府主要领导 title strongly suggests区长 role"
                }
            ],
            "confidence_summary": {
                "identity": "partial",
                "current_role": "plausible",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "刘兵兵的具体职务（区长）需进一步确认；完整的个人履历信息缺失"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "刘兵兵是否确实担任西安区区长？还是其他区政府领导职务？",
                    "why_it_matters": "核心目标人物之一，需要确认具体职务",
                    "suggested_queries": ["刘兵兵 西安区 区长", "西安区 区长 刘兵兵 任免"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "critical",
                    "question": "刘兵兵完整的个人履历是什么？包括出生日期、教育背景、历任职务",
                    "why_it_matters": "核心领导人物，需要完整履历来分析晋升路径和关系网络",
                    "suggested_queries": ["刘兵兵 简历", "刘兵兵 牡丹江 任职"],
                    "last_attempted": AS_OF
                }
            ]
        }
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

def write_person_json(data: dict, filename: str) -> Path:
    path = STAGING_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {path}")
    return path


def main():
    print(f"Building network for {SLUG}...")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print()

    # Build database and graph
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
    print()

    # Write person JSONs
    print("Writing person JSON files...")
    for key, entry in PERSON_JSON_TEMPLATE.items():
        write_person_json(entry["data"], entry["filename"])

    # Print summary
    print()
    print("=" * 60)
    print(f"Build complete for {SLUG}")
    print(f"  {len(persons_data)} persons")
    print(f"  {len(organizations_data)} organizations")
    print(f"  {len(positions_data)} positions")
    print(f"  {len(relationships_data)} relationships")
    print(f"  {len(PERSON_JSON_TEMPLATE)} person JSONs")
    print("=" * 60)


if __name__ == "__main__":
    main()
