#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 华州区, 渭南市, 陕西省.

Investigation date: 2026-07-25
Task ID: shaanxi_华州区
Level: 市辖区
Targets: 区委书记 & 区长

Research status:
  Web access to huaqu.gov.cn — transport timeout (all HTTPS and HTTP attempts)
  Web access to Baidu/Baidu Baike — HTTP 403
  Web access to Google — blocked
  Web access to Exa — rate-limited
  Unable to confirm current officeholder names via official sources.

  The 华州区 (Huazhou District) government official website at www.huaqu.gov.cn
  is unreachable from this environment. No alternative source provided
  leadership roster information.

  Person names for 区委书记 and 区长 are marked as "待查" (to be confirmed)
  pending successful web access in a future investigation pass.

  This artifact set follows the "partial evidence mode" as specified in
  source_fallbacks.md — structurally valid artifacts are created with
  explicit uncertainty in confidence labels and open_questions.

Confidence notes:
  - 华州区 administrative structure and organizations: confirmed (known from public records)
  - 区委书记 name: unverified (no accessible source)
  - 区长 name: unverified (no accessible source)
  - All career timelines: unverified (no source available)
"""

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "华州区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

STAGING_DIR = Path(BASE)
DB_PATH = str(STAGING_DIR / f"{SLUG}_network.db")
GEXF_PATH = str(STAGING_DIR / f"{SLUG}_network.gexf")

# ═══════════════════════════════════════════════════════════════════════════════
# Data
# ═══════════════════════════════════════════════════════════════════════════════

persons_data = [
    # ══════════════════════════════════════════════════════════════════════════
    # Party Committee (区委) Leadership
    # ══════════════════════════════════════════════════════════════════════════

    # 待查 — 区委书记（姓名待确认）
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
        "current_org": "中共渭南市华州区委员会",
        "source": "华州区官方网站无法访问，区委书记姓名待确认"
    },
    # 待查 — 区委副书记、区长（姓名待确认）
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
        "current_post": "区委副书记、区长",
        "current_org": "渭南市华州区人民政府",
        "source": "华州区官方网站无法访问，区长姓名待确认"
    },
    # 待查 — 区委常委、常务副区长
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
        "current_org": "渭南市华州区人民政府",
        "source": "公开报道推断，具体姓名待确认"
    },
    # 待查 — 区纪委书记
    {
        "id": 4,
        "name": "待查_纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区纪委书记、区监委主任",
        "current_org": "中共渭南市华州区纪律检查委员会",
        "source": "公开报道推断，具体姓名待确认"
    },
    # 待查 — 区委组织部部长
    {
        "id": 5,
        "name": "待查_组织部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共渭南市华州区委组织部",
        "source": "公开报道推断，具体姓名待确认"
    },
    # 待查 — 区委宣传部部长
    {
        "id": 6,
        "name": "待查_宣传部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、宣传部部长",
        "current_org": "中共渭南市华州区委宣传部",
        "source": "公开报道推断，具体姓名待确认"
    },
    # 待查 — 区委政法委书记
    {
        "id": 7,
        "name": "待查_政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、政法委书记",
        "current_org": "中共渭南市华州区委政法委",
        "source": "公开报道推断，具体姓名待确认"
    },
    # 区人大常委会主任（待确认）
    {
        "id": 8,
        "name": "待查_人大常委会主任",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "渭南市华州区人民代表大会常务委员会",
        "source": "公开报道推断，具体姓名待确认"
    },
    # 区政协主席（待确认）
    {
        "id": 9,
        "name": "待查_政协主席",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议渭南市华州区委员会",
        "source": "公开报道推断，具体姓名待确认"
    },
]

organizations_data = [
    {
        "id": 1,
        "name": "中共渭南市华州区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共渭南市委员会",
        "location": "渭南市华州区"
    },
    {
        "id": 2,
        "name": "渭南市华州区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "渭南市人民政府",
        "location": "渭南市华州区"
    },
    {
        "id": 3,
        "name": "渭南市华州区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "渭南市人民代表大会常务委员会",
        "location": "渭南市华州区"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议渭南市华州区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协渭南市委员会",
        "location": "渭南市华州区"
    },
    {
        "id": 5,
        "name": "中共渭南市华州区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共渭南市纪律检查委员会",
        "location": "渭南市华州区"
    },
    {
        "id": 6,
        "name": "中共渭南市华州区委组织部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共渭南市华州区委员会",
        "location": "渭南市华州区"
    },
    {
        "id": 7,
        "name": "中共渭南市华州区委宣传部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共渭南市华州区委员会",
        "location": "渭南市华州区"
    },
    {
        "id": 8,
        "name": "中共渭南市华州区委政法委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共渭南市华州区委员会",
        "location": "渭南市华州区"
    },
]

positions_data = [
    # 区委（党委系统）
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "姓名待确认"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "姓名待确认"},
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "姓名待确认"},
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "姓名待确认"},
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "姓名待确认"},
    {"person_id": 6, "org_id": 1, "title": "区委常委", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "姓名待确认"},
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "姓名待确认"},

    # 区政府
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "姓名待确认"},
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "姓名待确认"},

    # 纪委
    {"person_id": 4, "org_id": 5, "title": "区纪委书记、区监委主任", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "姓名待确认"},

    # 组织部
    {"person_id": 5, "org_id": 6, "title": "组织部部长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "姓名待确认"},

    # 宣传部
    {"person_id": 6, "org_id": 7, "title": "宣传部部长", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "姓名待确认"},

    # 政法委
    {"person_id": 7, "org_id": 8, "title": "政法委书记", "start_date": "unknown", "end_date": "present", "rank": "副处级", "note": "姓名待确认"},

    # 人大
    {"person_id": 8, "org_id": 3, "title": "区人大常委会主任", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "姓名待确认"},

    # 政协
    {"person_id": 9, "org_id": 4, "title": "区政协主席", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": "姓名待确认"},
]

relationships_data = [
    # 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记——区长党政搭档", "overlap_org": "中共华州区委/华州区人民政府", "overlap_period": "unknown-present"},

    # 区委书记与常委
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "区委书记与常务副区长在区委常委会共事", "overlap_org": "中共华州区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "区委书记与纪委书记在区委常委会共事", "overlap_org": "中共华州区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "区委书记与组织部部长在干部选拔任用方面密切协作", "overlap_org": "中共华州区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "区委书记与宣传部部长在区委常委会共事", "overlap_org": "中共华州区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "区委书记与政法委书记在区委常委会共事", "overlap_org": "中共华州区委", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "区委书记与区人大常委会主任在区级班子中共事", "overlap_org": "华州区", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "区委书记与区政协主席在区级班子中共事", "overlap_org": "华州区", "overlap_period": ""},

    # 区长与其他领导
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "区长与常务副区长在区政府班子中配合", "overlap_org": "华州区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "区长与纪委书记在区委常委会共事", "overlap_org": "中共华州区委", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "区长与组织部部长在区委常委会共事", "overlap_org": "中共华州区委", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "区长与宣传部部长在区委常委会共事", "overlap_org": "中共华州区委", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "区长与政法委书记在区委常委会共事", "overlap_org": "中共华州区委", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "区长与区人大常委会主任在区级班子中共事", "overlap_org": "华州区", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "区长与区政协主席在区级班子中共事", "overlap_org": "华州区", "overlap_period": ""},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON generation
# ═══════════════════════════════════════════════════════════════════════════════

PERSON_JSON_TEMPLATE = {
    "待查_区委书记": {
        "filename": f"{TODAY}-陕西省-渭南市-华州区-区委书记-待查_区委书记.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "陕西省",
                "city": "渭南市",
                "region": "华州区",
                "job": "区委书记",
                "task_id": "shaanxi_华州区",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "huazhou_party_secretary",
                "name": "待查_区委书记",
                "aliases": [],
                "gender": "",
                "ethnicity": "",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员（推测）",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "待查_未知",
                    "name_birthplace": "待查_未知",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "区委书记",
                "current_org": "中共渭南市华州区委员会",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": False,
                "source_ids": []
            },
            "career_timeline": [
                {"start": "unknown", "end": "present", "org": "渭南市华州区委员会", "title": "区委书记", "level": "县处级", "location": "陕西渭南", "system": "party", "rank": "正处级", "is_key_promotion": True, "notes": "当前在任（姓名待确认）", "confidence": "unverified", "source_ids": []},
                {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开资料未找到华州区区委书记姓名及履历", "confidence": "unverified", "source_ids": []},
            ],
            "organizations": [],
            "relationships": [
                {"person": "待查_区长", "person_id": "huazhou_district_mayor", "relationship_type": "overlap", "strength": "strong", "evidence": "区委书记——区长党政搭档（具体姓名待确认）", "overlap_org": "中共华州区委/华州区人民政府", "overlap_period": "unknown-present", "direction": "undirected", "confidence": "unverified", "source_ids": []},
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "全部信息待查", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "因姓名未知无法检索公开信息", "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": [],
            "confidence_summary": {"identity": "unverified", "current_role": "unverified", "career_completeness": "thin", "relationship_confidence": "low", "biggest_gap": "华州区区委书记完整的姓名、履历、身份信息全部缺失"},
            "open_questions": [
                {"priority": "critical", "question": "华州区现任区委书记的姓名", "why_it_matters": "核心目标人物，无姓名则无法进行任何关系网络分析", "suggested_queries": ["华州区 区委书记 2026", "华州区 领导之窗", "华州区 常委名单"], "last_attempted": AS_OF},
                {"priority": "critical", "question": "华州区区委书记的完整履历（出生年月、籍贯、教育背景、历任职务）", "why_it_matters": "关键人物，履历缺失严重影响关系网络分析", "suggested_queries": ["华州区 区委书记 简历", "华州区 区委书记 任前公示"], "last_attempted": AS_OF},
                {"priority": "high", "question": "华州区区委书记何时就任？前任是谁？", "why_it_matters": "确定任期起点和前任去向", "suggested_queries": ["华州区 前任区委书记", "华州区 区委书记 任命"], "last_attempted": AS_OF},
            ]
        }
    },
    "待查_区长": {
        "filename": f"{TODAY}-陕西省-渭南市-华州区-区长-待查_区长.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "陕西省",
                "city": "渭南市",
                "region": "华州区",
                "job": "区长",
                "task_id": "shaanxi_华州区",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "huazhou_district_mayor",
                "name": "待查_区长",
                "aliases": [],
                "gender": "",
                "ethnicity": "",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员（推测）",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "待查_未知",
                    "name_birthplace": "待查_未知",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "区委副书记、区长",
                "current_org": "渭南市华州区人民政府",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": False,
                "source_ids": []
            },
            "career_timeline": [
                {"start": "unknown", "end": "present", "org": "渭南市华州区人民政府", "title": "区长", "level": "县处级", "location": "陕西渭南", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "当前在任（姓名待确认）", "confidence": "unverified", "source_ids": []},
                {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开资料未找到华州区区长姓名及履历", "confidence": "unverified", "source_ids": []},
            ],
            "organizations": [],
            "relationships": [
                {"person": "待查_区委书记", "person_id": "huazhou_party_secretary", "relationship_type": "overlap", "strength": "strong", "evidence": "区长——区委书记党政搭档（具体姓名待确认）", "overlap_org": "中共华州区委/华州区人民政府", "overlap_period": "unknown-present", "direction": "undirected", "confidence": "unverified", "source_ids": []},
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "全部信息待查", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "因姓名未知无法检索公开信息", "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": [],
            "confidence_summary": {"identity": "unverified", "current_role": "unverified", "career_completeness": "thin", "relationship_confidence": "low", "biggest_gap": "华州区区长完整的姓名、履历、身份信息全部缺失"},
            "open_questions": [
                {"priority": "critical", "question": "华州区现任区长的姓名", "why_it_matters": "核心目标人物，无姓名则无法进行任何关系网络分析", "suggested_queries": ["华州区 区长 2026", "华州区 政府 领导", "华州区 区长 任命"], "last_attempted": AS_OF},
                {"priority": "critical", "question": "华州区区长的完整履历（出生年月、籍贯、教育背景、历任职务）", "why_it_matters": "关键人物，履历缺失严重影响关系网络分析", "suggested_queries": ["华州区 区长 简历", "华州区 区长 任前公示"], "last_attempted": AS_OF},
                {"priority": "high", "question": "华州区区长何时就任？前任是谁？去向何方？", "why_it_matters": "确定任期起点和前区长的去向", "suggested_queries": ["华州区 前任区长", "华州区 区长 任命 人大常委会"], "last_attempted": AS_OF},
            ]
        }
    },
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
    print(f"  ⚠ Web access degraded — all person names marked as 待查")
    print()

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

    print("Writing person JSON files...")
    for key, entry in PERSON_JSON_TEMPLATE.items():
        write_person_json(entry["data"], entry["filename"])

    print()
    print("=" * 60)
    print(f"Build complete for {SLUG}")
    print(f"  {len(persons_data)} persons")
    print(f"  {len(organizations_data)} organizations")
    print(f"  {len(positions_data)} positions")
    print(f"  {len(relationships_data)} relationships")
    print(f"  {len(PERSON_JSON_TEMPLATE)} person JSONs")
    print("  ⚠ All names are placeholders — needs follow-up investigation")
    print("=" * 60)

if __name__ == "__main__":
    main()
