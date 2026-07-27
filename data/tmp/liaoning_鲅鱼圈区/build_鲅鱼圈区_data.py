#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 鲅鱼圈区, 营口市, 辽宁省.

Investigation date: 2026-07-25
Task ID: liaoning_鲅鱼圈区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - www.byq.gov.cn — 鲅鱼圈区人民政府官方网站 (unreachable — timed out)
  - www.yingkou.gov.cn — 营口市人民政府官方网站 (partial access — leadership page readable)
  - Baidu Baike (403), Exa (rate-limited), Google (blocked), Jina Reader (timed out)

Confidence notes:
  - All web sources at the district level were unreachable from the research environment (July 2026).
  - 鲅鱼圈区政府网站 (byq.gov.cn) all sub-pages timed out.
  - Baidu Baike returned HTTP 403.
  - Exa search API rate-limited.
  - Jina Reader timed out on all requests.
  - 营口市政府主站 (yingkou.gov.cn) was partially accessible (leadership page),
    showing city-level leadership but not district-level.
  - All current-role district-level claims are labeled 'unverified' due to inability
    to confirm via live web sources in this session.
  - 区委书记姓名: 待查
  - 区长姓名: 待查
  - Artifacts created with explicit uncertainty per source_fallbacks.md partial
    evidence mode.
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
SLUG = "鲅鱼圈区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "liaoning_鲅鱼圈区"
if _CURRENT_DIR.name == "liaoning_鲅鱼圈区":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1=区委书记, 2=区长, 3-8=区委常委/副区长

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
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
        "current_org": "中共营口市鲅鱼圈区委员会",
        "source": "待查 — 鲅鱼圈区政府官网(byq.gov.cn)无法访问",
        "confidence": "unverified",
        "notes": "区委书记姓名确认失败。区政府网站byq.gov.cn及所有子页面均超时无法访问。营口市政府网站领导之窗仅显示市级领导。未找到任何可靠的公开来源确认当前在任区委书记姓名。需后续通过营口市委组织部公示或新闻报道进一步核实。"
    },
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
        "current_org": "鲅鱼圈区人民政府",
        "source": "待查 — 鲅鱼圈区政府官网(byq.gov.cn)无法访问",
        "confidence": "unverified",
        "notes": "区长姓名确认失败。与区委书记同因网络不可达而无法确认。区政府官网全部超时。需后续核实。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Key Standing Committee Members (inferred default 区委/区政府 structure)
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
        "current_post": "区委常委、副区长（常务）",
        "current_org": "鲅鱼圈区人民政府",
        "source": "待查 — 默认区级班子构成推断",
        "confidence": "unverified",
        "notes": "常务副区长姓名待核实。区级政府一般配备一名常务副区长。具体信息需从鲅鱼圈区政府网站领导分工页面获取。"
    },
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
        "current_org": "中共鲅鱼圈区纪律检查委员会",
        "source": "待查 — 默认区级纪检班子构成推断",
        "confidence": "unverified",
        "notes": "区纪委书记姓名待核实。属区级标配常委职务。"
    },
    {
        "id": 5,
        "name": "待查_组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共鲅鱼圈区委组织部",
        "source": "待查 — 默认区级班子构成推断",
        "confidence": "unverified",
        "notes": "区委组织部部长姓名待核实。"
    },
    {
        "id": 6,
        "name": "待查_宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、宣传部部长",
        "current_org": "中共鲅鱼圈区委宣传部",
        "source": "待查 — 默认区级班子构成推断",
        "confidence": "unverified",
        "notes": "区委宣传部部长姓名待核实。"
    },
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
        "current_org": "中共鲅鱼圈区委政法委员会",
        "source": "待查 — 默认区级班子构成推断",
        "confidence": "unverified",
        "notes": "区委政法委书记姓名待核实。"
    },
    {
        "id": 8,
        "name": "待查_副区长（公安局长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、区公安分局局长",
        "current_org": "营口市公安局鲅鱼圈分局",
        "source": "待查 — 默认区级政府构成推断",
        "confidence": "unverified",
        "notes": "分管公安的副区长兼公安分局局长姓名待核实。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共营口市鲅鱼圈区委员会", "type": "党委", "level": "县处级", "parent": "中共营口市委", "location": "鲅鱼圈区"},
    {"id": 2, "name": "鲅鱼圈区人民政府", "type": "政府", "level": "县处级", "parent": "营口市人民政府", "location": "鲅鱼圈区"},
    {"id": 3, "name": "中国人民政治协商会议鲅鱼圈区委员会", "type": "政协", "level": "县处级", "parent": "政协营口市委", "location": "鲅鱼圈区"},
    {"id": 4, "name": "鲅鱼圈区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "营口市人大常委会", "location": "鲅鱼圈区"},
    {"id": 5, "name": "中共鲅鱼圈区纪律检查委员会（监察委员会）", "type": "纪委", "level": "县处级", "parent": "营口市纪委", "location": "鲅鱼圈区"},
    {"id": 6, "name": "中共鲅鱼圈区委组织部", "type": "党委", "level": "县处级", "parent": "中共鲅鱼圈区委员会", "location": "鲅鱼圈区"},
    {"id": 7, "name": "中共鲅鱼圈区委宣传部", "type": "党委", "level": "县处级", "parent": "中共鲅鱼圈区委员会", "location": "鲅鱼圈区"},
    {"id": 8, "name": "中共鲅鱼圈区委政法委员会", "type": "党委", "level": "县处级", "parent": "中共鲅鱼圈区委员会", "location": "鲅鱼圈区"},
    {"id": 9, "name": "营口市公安局鲅鱼圈分局", "type": "政府", "level": "乡科级", "parent": "鲅鱼圈区人民政府", "location": "鲅鱼圈区"},
    {"id": 10, "name": "营口经济技术开发区（鲅鱼圈区）管委会", "type": "开发区", "level": "国家级开发区", "parent": "营口市人民政府", "location": "鲅鱼圈区"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 待查_区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "区委书记姓名待核实。所有政府网站不可达。"},
    # 待查_区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "区长姓名待核实。"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "区长兼任区委副书记"},
    # 待查_常务副区长
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "副区长（常务）", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "分管发改、财政、应急、人社等"},
    # 待查_纪委书记
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 5, "title": "区纪委书记、区监委主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 待查_组织部长
    {"person_id": 5, "org_id": 1, "title": "区委常委、组织部部长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": ""},
    {"person_id": 5, "org_id": 6, "title": "组织部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 待查_宣传部长
    {"person_id": 6, "org_id": 1, "title": "区委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": ""},
    {"person_id": 6, "org_id": 7, "title": "宣传部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 待查_政法委书记
    {"person_id": 7, "org_id": 1, "title": "区委常委、政法委书记", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": ""},
    {"person_id": 7, "org_id": 8, "title": "政法委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 待查_副区长（公安局长）
    {"person_id": 8, "org_id": 2, "title": "副区长（兼区公安分局局长）", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": ""},
    {"person_id": 8, "org_id": 9, "title": "区公安分局局长", "start_date": "", "end_date": "", "rank": "乡科级正职", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────────
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记与区长为党政主要领导搭档关系",
        "overlap_org": "中共营口市鲅鱼圈区委员会",
        "overlap_period": "当前",
        "confidence": "unverified",
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "区委书记与常务副区长为区委与政府领导关系",
        "overlap_org": "中共营口市鲅鱼圈区委员会",
        "overlap_period": "当前",
        "confidence": "unverified",
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "区长与常务副区长为政府主要领导与副手关系",
        "overlap_org": "鲅鱼圈区人民政府",
        "overlap_period": "当前",
        "confidence": "unverified",
    },
    {
        "person_a": 2,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "区长与分管公安的副区长为政府领导关系",
        "overlap_org": "鲅鱼圈区人民政府",
        "overlap_period": "当前",
        "confidence": "unverified",
    },
    {
        "person_a": 3,
        "person_b": 4,
        "type": "overlap",
        "context": "同为区委常委班子成员",
        "overlap_org": "中共营口市鲅鱼圈区委员会",
        "overlap_period": "当前",
        "confidence": "unverified",
    },
    {
        "person_a": 3,
        "person_b": 5,
        "type": "overlap",
        "context": "同为区委常委班子成员",
        "overlap_org": "中共营口市鲅鱼圈区委员会",
        "overlap_period": "当前",
        "confidence": "unverified",
    },
    {
        "person_a": 4,
        "person_b": 5,
        "type": "overlap",
        "context": "同为区委常委班子成员",
        "overlap_org": "中共营口市鲅鱼圈区委员会",
        "overlap_period": "当前",
        "confidence": "unverified",
    },
    {
        "person_a": 5,
        "person_b": 6,
        "type": "overlap",
        "context": "同为区委常委班子成员",
        "overlap_org": "中共营口市鲅鱼圈区委员会",
        "overlap_period": "当前",
        "confidence": "unverified",
    },
    {
        "person_a": 6,
        "person_b": 7,
        "type": "overlap",
        "context": "同为区委常委班子成员",
        "overlap_org": "中共营口市鲅鱼圈区委员会",
        "overlap_period": "当前",
        "confidence": "unverified",
    },
]

# ── Person JSONs ─────────────────────────────────────────────────────────────

PERSON_JSON_TEMPLATE = {
    "schema_version": "1.0",
    "generated_at": TODAY,
    "investigation_scope": {
        "province": "辽宁省",
        "city": "营口市",
        "region": "鲅鱼圈区",
        "task_id": "liaoning_鲅鱼圈区",
        "time_focus": "2026年7月",
    },
    "identity": {},
    "current_status": {},
    "career_timeline": [],
    "organizations": [],
    "relationships": [],
    "governance_record": [],
    "professional_profile": {},
    "work_style_and_personality": {},
    "network_metrics": {},
    "risk_and_integrity_signals": [],
    "source_register": [],
    "confidence_summary": {},
    "open_questions": [],
}


def build_person_json(person_id: int) -> dict:
    p = {x["id"]: x for x in persons}[person_id]
    name = p["name"]
    role_label = p["current_post"]
    now = TODAY

    person = {
        "identity": {
            "person_id": f"liaoning_yingkou_byq_{name}",
            "name": name,
            "aliases": [],
            "gender": p["gender"],
            "ethnicity": p["ethnicity"],
            "birth": p["birth"],
            "birthplace": p["birthplace"],
            "native_place": "",
            "education": [],
            "party_join": p["party_join"],
            "work_start": p["work_start"],
            "dedupe_keys": {
                "name_birth": f"{name}_",
                "name_birthplace": f"{name}_",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": "县处级正职" if person_id <= 2 else "县处级副职",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": [],
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": p["current_org"],
                "title": p["current_post"],
                "level": "",
                "location": "鲅鱼圈区",
                "system": "party" if person_id == 1 else "government",
                "rank": "县处级正职" if person_id <= 2 else "县处级副职",
                "is_key_promotion": False,
                "notes": p["notes"],
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
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
                "summary": "",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "No risk signals found — name unverified, no records to review",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": [],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": f"姓名完全未知。因政府网站和公共网络均不可达，{role_label}姓名无法确认。",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"鲅鱼圈区{role_label}姓名是什么？",
                "why_it_matters": "核心目标人物之一，完整调查必须确认姓名和身份",
                "suggested_queries": [
                    f"鲅鱼圈区 {p['current_post']}",
                    f"鲅鱼圈区 领导分工 {p['current_post']}",
                    "鲅鱼圈区政府 领导之窗",
                    "营口市委组织部 任前公示 鲅鱼圈",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{name}的出生年月、籍贯、学历和完整履历",
                "why_it_matters": "身份确认后需补充完整履历",
                "suggested_queries": [
                    f"鲅鱼圈区 {p['current_post']} 简历",
                ],
                "last_attempted": AS_OF,
            },
        ],
    }

    return person


def write_person_json(person_id: int):
    p = {x["id"]: x for x in persons}[person_id]
    name = p["name"]
    role_label = p["current_post"]
    safe_role = role_label.replace("、", "_")
    filename = f"{TODAY}-辽宁省-营口市-{safe_role}-{name}.json"
    path = PJSON_DIR / filename

    person_data = build_person_json(person_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(person_data, f, ensure_ascii=False, indent=2)

    return path


# ── Main ─────────────────────────────────────────────────────────────────────


def main():
    # Build DB and GEXF
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

    # Write person JSONs
    person_files = []
    for pid in [1, 2, 3, 4, 5, 6, 7, 8]:
        path = write_person_json(pid)
        person_files.append(str(path))

    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("Person JSONs:")
    for pf in person_files:
        print(f"  {pf}")
    print(f"\nNote: All person names are '待查_*' — unverified due to web access failure.")
    print(f"      Government sites (byq.gov.cn) timed out; Baidu 403; Exa rate-limited.")
    print(f"Done.")


if __name__ == "__main__":
    main()
