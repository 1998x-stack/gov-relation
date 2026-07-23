#!/usr/bin/env python3
"""
竞秀区领导班子工作关系网络 — Build script
河北省保定市竞秀区

Confirmed sources:
- 保定市竞秀区人民政府门户网站 (https://www.jingxiu.gov.cn/): confirms 刘相伟 as 区委书记, 付建宾 as 区长
- News items on government site: "区委书记刘相伟带队开展一线慰问和大气污染防治督导检查",
  "区长付建宾主持召开规范成品油流通市场经营行为专项行动推进会"

Research date: 2026-07-23
"""

import json
import os
import sys
from datetime import date

# Add repo root to path
_REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

import sqlite3  # noqa: used by gov_relation.runner

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

AS_OF = "2026-07-23"
DB_PATH = None  # Will be set in main()
GEXF_PATH = None  # Will be set in main()

# ── PERSONS ──
persons = [
    # ── 区委书记 (Party Secretary) ──
    {
        "id": 1,
        "name": "刘相伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "保定市竞秀区委书记",
        "current_org": "中共保定市竞秀区委员会",
        "source": "https://www.jingxiu.gov.cn/",
    },
    # ── 区长 (District Mayor) ──
    {
        "id": 2,
        "name": "付建宾",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "保定市竞秀区委副书记、区长",
        "current_org": "保定市竞秀区人民政府/中共保定市竞秀区委员会",
        "source": "https://www.jingxiu.gov.cn/",
    },
]

# ── ORGANIZATIONS ──
organizations = [
    {
        "id": 1,
        "name": "中共保定市竞秀区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共保定市委员会",
        "location": "保定市竞秀区",
    },
    {
        "id": 2,
        "name": "保定市竞秀区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "保定市人民政府",
        "location": "保定市竞秀区",
    },
]

# ── POSITIONS (current roles) ──
positions = [
    {
        "person_id": 1,
        "org_id": 1,
        "title": "保定市竞秀区委书记",
        "start_date": "待查",
        "end_date": "present",
        "rank": "正处级",
        "note": "当前区委书记，来源：竞秀区政府官网",
    },
    {
        "person_id": 2,
        "org_id": 1,
        "title": "保定市竞秀区委副书记",
        "start_date": "待查",
        "end_date": "present",
        "rank": "正处级",
        "note": "区委副书记、区长",
    },
    {
        "person_id": 2,
        "org_id": 2,
        "title": "保定市竞秀区人民政府区长",
        "start_date": "待查",
        "end_date": "present",
        "rank": "正处级",
        "note": "区政府主要负责人",
    },
]

# ── RELATIONSHIPS ──
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记与区长：党委和政府主要领导工作关系",
        "overlap_org": "中共保定市竞秀区委员会",
        "overlap_period": "共同任职期间（待查至今）",
    },
]

# ── BUILD ──
def main():
    # When run from staging, derive paths relative to script location
    staging_dir = os.path.dirname(os.path.abspath(__file__))

    global DB_PATH, GEXF_PATH
    DB_PATH = os.path.join(staging_dir, "竞秀区_network.db")
    GEXF_PATH = os.path.join(staging_dir, "竞秀区_network.gexf")

    run_build(
        slug="竞秀区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Also write person JSON files
    write_person_json(staging_dir)

    print(f"Build complete. DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"Person JSONs in: {staging_dir}")


def write_person_json(staging_dir: str):
    """Write person graph JSON files into staging dir."""
    for person in persons:
        pid = person["id"]
        name = person["name"]
        job_slug = "区委书记" if pid == 1 else "区长"

        filename = f"{AS_OF}-河北省-保定市-{job_slug}-{name}.json"

        person_json = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河北省",
                "city": "保定市",
                "region": "竞秀区",
                "job": job_slug,
                "task_id": "hebei_竞秀区",
                "time_focus": "当前任职",
            },
            "identity": {
                "person_id": f"hebei_baoding_jingxiu_{name}_{pid}",
                "name": name,
                "aliases": [],
                "gender": person.get("gender", ""),
                "ethnicity": person.get("ethnicity", ""),
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "",
                    "name_birthplace": "",
                    "official_profile_url": "",
                },
            },
            "current_status": {
                "current_post": person.get("current_post", ""),
                "current_org": person.get("current_org", ""),
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"],
            },
            "career_timeline": [
                {
                    "start": "待查",
                    "end": "present",
                    "org": person.get("current_org", ""),
                    "title": person.get("current_post", ""),
                    "level": "县处级",
                    "location": "保定市竞秀区",
                    "system": "party" if pid == 1 else "government",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "当前任职，确认来源：竞秀区政府官网新闻",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                }
            ],
            "organizations": [
                {
                    "org_id": 1,
                    "name": "中共保定市竞秀区委员会",
                    "type": "党委",
                    "level": "县处级",
                },
                {
                    "org_id": 2,
                    "name": "保定市竞秀区人民政府",
                    "type": "政府",
                    "level": "县处级",
                },
            ],
            "relationships": [
                {
                    "person": "付建宾" if pid == 1 else "刘相伟",
                    "person_id": f"hebei_baoding_jingxiu_{'付建宾' if pid == 1 else '刘相伟'}_{2 if pid == 1 else 1}",
                    "relationship_type": "superior_subordinate",
                    "strength": "strong",
                    "evidence": "区委书记与区长，党委和政府主要领导工作关系",
                    "overlap_org": "中共保定市竞秀区委员会",
                    "overlap_period": "共同任职期间",
                    "direction": "person_to_other" if pid == 1 else "other_to_person",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                }
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "公开资料不足，无法判断", "notable_fast_promotions": []},
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "当前公开资料不足，无法推断工作风格和个性特征。",
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "目前未发现公开的纪律处分、审计问题或负面媒体报道",
                    "date": "",
                    "confidence": "unverified",
                    "source_ids": [],
                }
            ],
            "source_register": [
                {
                    "id": "S001",
                    "title": "保定市竞秀区人民政府门户网站",
                    "url": "https://www.jingxiu.gov.cn/",
                    "publisher": "保定市竞秀区人民政府",
                    "published_at": "",
                    "accessed_at": AS_OF,
                    "source_type": "official",
                    "reliability": "high",
                    "notes": "政府官网新闻栏目确认区委书记和区长姓名",
                }
            ],
            "confidence_summary": {
                "identity": "plausible",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "缺乏详细履历：出生年月、籍贯、教育背景、工作经历、任现职时间均不详",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": f"{name}的完整履历（出生年月、籍贯、教育背景、工作经历）",
                    "why_it_matters": "关系网络分析的核心信息",
                    "suggested_queries": [
                        f"{name} 简历 保定 竞秀区",
                        f"{name} 任前公示 保定",
                        f"{name} 百度百科",
                    ],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": f"{name}的任现职时间",
                    "why_it_matters": "确定领导班子的共同工作时间起点",
                    "suggested_queries": [
                        f"竞秀区 人大 任命 {name} 区长" if pid == 2 else f"保定市委 任命 {name} 区委书记",
                        f"{name} 任职 竞秀区",
                    ],
                    "last_attempted": AS_OF,
                },
            ],
        }

        filepath = os.path.join(staging_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(person_json, f, ensure_ascii=False, indent=2)
        print(f"Person JSON written: {filepath}")


if __name__ == "__main__":
    main()
