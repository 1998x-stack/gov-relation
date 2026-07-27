#!/usr/bin/env python3
"""
武汉市洪山区（湖北省武汉市）领导班子工作关系网络 — 2026-07-24
Build script for Hongshan District, Wuhan City, Hubei Province (市辖区).

TASK: hubei_洪山区
Province: 湖北省
Parent city: 武汉市
Region: 洪山区
Level: 市辖区
Targets: 区委书记 & 区长

Data sources:
- 武汉市洪山区人民政府官网: https://www.hongshan.gov.cn/
  - 政府领导栏目确认: 区长刘华珍, 副区长许永周/田燕/陈京
- 区委书记信息: 洪山区人民政府网站未公开党委领导信息,
  区委网站无法访问。此为已知缺口。

This script uses the gov_relation.runner module (modern pattern).
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

SLUG = "洪山区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = datetime.now().strftime("%Y-%m-%d")

STAGING_DB = _STAGING_DIR / f"{SLUG}_network.db"
STAGING_GEXF = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

DB_PATH = STAGING_DB
GEXF_PATH = STAGING_GEXF

import sqlite3  # noqa: F811


# ── Source Register ──────────────────────────────────────────────────────
SOURCES = {
    "S001": {"title": "洪山区人民政府门户网站",
             "url": "https://www.hongshan.gov.cn/",
             "type": "official", "reliability": "high"},
}


def make_source_register():
    return [{"id": k, **v} for k, v in SOURCES.items()]


# ══════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership
    # ══════════════════════════════════════════════════════════════════════

    # ── 1. Party Secretary (区委书记) — UNKNOWN ──
    {
        "id": 1,
        "name": "待确认 (区委书记)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共武汉市洪山区委员会",
        "source": "待查 — 洪山区政府网站未公开党委领导信息"
    },

    # ── 2. District Mayor (区长) — CONFIRMED ──
    {
        "id": 2,
        "name": "刘华珍",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "洪山区人民政府",
        "source": "https://www.hongshan.gov.cn/ — 区政府门户网站首页领导信息"
    },

    # ══════════════════════════════════════════════════════════════════════
    # Government Leadership (Deputy Mayors — CONFIRMED from hongshan.gov.cn)
    # ══════════════════════════════════════════════════════════════════════

    # ── 3. Deputy Mayor ──
    {
        "id": 3,
        "name": "许永周",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "洪山区人民政府",
        "source": "https://www.hongshan.gov.cn/ — 区政府门户网站首页领导信息"
    },

    # ── 4. Deputy Mayor ──
    {
        "id": 4,
        "name": "田燕",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "洪山区人民政府",
        "source": "https://www.hongshan.gov.cn/ — 区政府门户网站首页领导信息"
    },

    # ── 5. Deputy Mayor ──
    {
        "id": 5,
        "name": "陈京",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "洪山区人民政府",
        "source": "https://www.hongshan.gov.cn/ — 区政府门户网站首页领导信息"
    },

    # ══════════════════════════════════════════════════════════════════════
    # People's Congress & CPPCC (placeholder)
    # ══════════════════════════════════════════════════════════════════════

    # ── 6. NPC Standing Committee Chair ──
    {
        "id": 6,
        "name": "待确认 (区人大常委会主任)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "洪山区人民代表大会常务委员会",
        "source": "待查"
    },

    # ── 7. CPPCC Chair ──
    {
        "id": 7,
        "name": "待确认 (区政协主席)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议武汉市洪山区委员会",
        "source": "待查"
    },
]


# ══════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共武汉市洪山区委员会", "type": "党委", "level": "县处级",
     "parent": "中共武汉市委员会", "location": "湖北省武汉市洪山区"},
    {"id": 2, "name": "洪山区人民政府", "type": "政府", "level": "县处级",
     "parent": "武汉市人民政府", "location": "湖北省武汉市洪山区"},
    {"id": 3, "name": "洪山区人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "武汉市人民代表大会常务委员会", "location": "湖北省武汉市洪山区"},
    {"id": 4, "name": "中国人民政治协商会议武汉市洪山区委员会", "type": "政协", "level": "县处级",
     "parent": "中国人民政治协商会议武汉市委员会", "location": "湖北省武汉市洪山区"},
    {"id": 5, "name": "中共武汉市委员会", "type": "党委", "level": "副省级",
     "parent": "中共湖北省委", "location": "湖北省武汉市"},
    {"id": 6, "name": "武汉市人民政府", "type": "政府", "level": "副省级",
     "parent": "湖北省人民政府", "location": "湖北省武汉市"},
]


# ══════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════

positions = [
    # Core Leadership
    {"person_id": 1, "org_id": 1, "title": "洪山区委书记",
     "start_date": "", "end_date": "至今", "rank": "正处级",
     "note": "区委书记姓名待确认"},

    {"person_id": 2, "org_id": 2, "title": "洪山区区长",
     "start_date": "", "end_date": "至今", "rank": "正处级",
     "note": "主持区人民政府全面工作。分管区政府办公室、区审计局"},
    {"person_id": 2, "org_id": 1, "title": "洪山区委副书记",
     "start_date": "", "end_date": "至今", "rank": "正处级",
     "note": "兼任区委副书记"},

    # Deputy Mayors
    {"person_id": 3, "org_id": 2, "title": "洪山区副区长",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "洪山区副区长",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": "女"},
    {"person_id": 5, "org_id": 2, "title": "洪山区副区长",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},

    # NPC & CPPCC (placeholder)
    {"person_id": 6, "org_id": 3, "title": "洪山区人大常委会主任",
     "start_date": "", "end_date": "至今", "rank": "正处级",
     "note": "姓名待确认"},
    {"person_id": 7, "org_id": 4, "title": "洪山区政协主席",
     "start_date": "", "end_date": "至今", "rank": "正处级",
     "note": "姓名待确认"},
]


# ══════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════

relationships = [
    # Top leadership pair (党政搭档) — placeholder for party secretary
    {"person_a": 1, "person_b": 2, "type": "colleague",
     "context": "区委书记（待确认）与区长刘华珍党政搭档",
     "overlap_org": "洪山区", "overlap_period": "至今"},

    # Mayor → Deputy Mayors
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "区长刘华珍与副区长许永周",
     "overlap_org": "洪山区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "区长刘华珍与副区长田燕",
     "overlap_org": "洪山区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "区长刘华珍与副区长陈京",
     "overlap_org": "洪山区人民政府", "overlap_period": "至今"},
]


# ══════════════════════════════════════════════════════════════════════════
# PERSON GRAPH JSON HELPER
# ══════════════════════════════════════════════════════════════════════════

def make_person_json(person, timeline, person_relationships, source_register):
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "湖北省",
            "city": "武汉市",
            "region": "洪山区",
            "job": person["current_post"],
            "task_id": "hubei_洪山区",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": f"hongshan_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [{"period": "", "institution": person.get("education", ""), "major": "", "degree": "",
                           "study_type": "unknown", "source_ids": []}],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth','')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace','')}",
                "official_profile_url": person.get("source", "")
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if "书记" in person["current_post"] and "副" not in person["current_post"] else
                                   "正处级" if "区长" in person["current_post"] and "副" not in person["current_post"] else
                                   "正处级" if "主任" in person["current_post"] and "副" not in person["current_post"] else
                                   "正处级" if "主席" in person["current_post"] and "副" not in person["current_post"] else
                                   "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": "待确认" not in person["name"],
            "source_ids": ["S001"]
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": person_relationships,
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
            "caveat": "Work style is inferred from public records. No private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未在公开资料中发现负面信号",
                                         "date": AS_OF, "confidence": "confirmed", "source_ids": ["S001"]}],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if "待确认" not in person["name"] else "unverified",
            "current_role": "confirmed" if "待确认" not in person["name"] else "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "区委书记姓名及完整履历未知"
        },
        "open_questions": [
            {"priority": "critical", "question": f"{person['name']}当前担任{person['current_post']}的身份确认？",
             "why_it_matters": "核心领导身份是关系网络的基础",
             "suggested_queries": [f"洪山区 {person['current_post']} 任命", f"洪山区 {person['current_post']} 简历"],
             "last_attempted": AS_OF}
        ]
    }


# ══════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════

def build():
    print("=" * 60)
    print("  武汉市洪山区领导班子工作关系网络")
    print("  等级: 市辖区")
    print("  调查日期: 2026-07-24")
    print("  信息来源: 洪山区人民政府官网")
    print("=" * 60)

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=STAGING_DB,
        gexf_path=STAGING_GEXF,
        overwrite=True,
    )
    print(f"\n✅ 洪山区数据构建完成。")
    print(f"  DB: {STAGING_DB}")
    print(f"  GEXF: {STAGING_GEXF}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── Generate Person Graph JSONs ──
    print("\n--- Generating Person Graph JSONs ---")
    source_register = make_source_register()

    # 1. 刘华珍 (区长) — the only confirmed person with a name
    liu_timeline = [
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "公开资料仅可见现任洪山区区长身份，此前任职经历未在政府官网公布",
         "confidence": "unverified", "source_ids": []},
        {"start": "", "end": "至今", "org": "洪山区人民政府", "title": "洪山区区长",
         "notes": "主持区人民政府全面工作。分管区政府办公室、区审计局",
         "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    liu_relationships = [
        {"person": "待确认 (区委书记)", "person_id": "hongshan_待确认 (区委书记)", "relationship_type": "colleague",
         "strength": "strong",
         "evidence": "区长与区委书记党政搭档",
         "overlap_org": "洪山区", "overlap_period": "至今",
         "direction": "undirected", "confidence": "plausible", "source_ids": ["S001"]},
        {"person": "许永周", "person_id": "hongshan_许永周", "relationship_type": "superior_subordinate",
         "strength": "medium",
         "evidence": "区长与副区长",
         "overlap_org": "洪山区人民政府", "overlap_period": "至今",
         "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "田燕", "person_id": "hongshan_田燕", "relationship_type": "superior_subordinate",
         "strength": "medium",
         "evidence": "区长与副区长",
         "overlap_org": "洪山区人民政府", "overlap_period": "至今",
         "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "陈京", "person_id": "hongshan_陈京", "relationship_type": "superior_subordinate",
         "strength": "medium",
         "evidence": "区长与副区长",
         "overlap_org": "洪山区人民政府", "overlap_period": "至今",
         "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    liu_json = make_person_json(persons[1], liu_timeline, liu_relationships, source_register)
    liu_path = PERSONS_DIR / f"{TODAY}-湖北省-武汉市-区长-刘华珍.json"
    with open(liu_path, "w", encoding="utf-8") as f:
        json.dump(liu_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {liu_path.name}")

    # 2. 区委书记 — placeholder (name unknown)
    ps_timeline = [
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "区委书记姓名及履历完全未知。洪山区政府网站未公开区委领导信息。",
         "confidence": "unverified", "source_ids": []},
    ]
    ps_relationships = [
        {"person": "刘华珍", "person_id": "hongshan_刘华珍", "relationship_type": "colleague",
         "strength": "strong",
         "evidence": "区委书记（待确认）与区长刘华珍党政搭档",
         "overlap_org": "洪山区", "overlap_period": "至今",
         "direction": "undirected", "confidence": "plausible", "source_ids": ["S001"]},
    ]
    ps_json = make_person_json(persons[0], ps_timeline, ps_relationships, source_register)
    ps_path = PERSONS_DIR / f"{TODAY}-湖北省-武汉市-区委书记-待确认.json"
    with open(ps_path, "w", encoding="utf-8") as f:
        json.dump(ps_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {ps_path.name}")

    print(f"\n所有 Person Graph JSONs 已生成到: {PERSONS_DIR}")


if __name__ == "__main__":
    build()
