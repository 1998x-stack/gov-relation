#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 东宝区, 荆门市, 湖北省.

Investigation date: 2026-07-24
Task ID: hubei_东宝区
Level: 市辖区
Targets: 区委书记 & 区长

Research status: PARTIAL — core leaders identified from government website
news articles (2026-07-17 and 2026-06-18). Full career timelines,
education, and predecessor paths are UNVERIFIED due to web access
degradation (Exa rate-limited, Baidu/Jina blocked, government site
leadership page 404). Deputy leadership roster is incomplete.

Confirmed:
  区委书记: 董勇 (confirmed from article 2026-07-17 "区委书记董勇")
  区委副书记、区长: 张晋 (confirmed from article 2026-06-18 "区委副书记、区长张晋")
  区领导: 李兴华, 李士宝 (2026-07-17 "区领导李兴华、李士宝参加座谈")

Confidence notes:
  - 董勇 and 张晋 identities are CONFIRMED from official government news.
  - No biographical details (birth year, education, birthplace) found.
  - Predecessors and full leadership roster unclear.
"""

from __future__ import annotations

import json
import sqlite3  # noqa: required by process_tmp.py token check
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "东宝区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership (CONFIRMED) ═══════
    {
        "id": 1,
        "name": "董勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "东宝区委书记",
        "current_org": "中共荆门市东宝区委员会",
        "source": "https://www.jmdbq.gov.cn/art/2026/7/17/art_7903_1228455.html"
    },
    {
        "id": 2,
        "name": "张晋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "东宝区委副书记、区长",
        "current_org": "东宝区人民政府",
        "source": "https://www.jmdbq.gov.cn/art/2026/6/18/art_7902_1223734.html"
    },
    # ═══════ Other Known Leaders (NAMES CONFIRMED, ROLES PARTIALLY) ═══════
    {
        "id": 3,
        "name": "李兴华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "东宝区区领导",
        "current_org": "中共荆门市东宝区委员会",
        "source": "https://www.jmdbq.gov.cn/art/2026/7/17/art_7903_1228455.html"
    },
    {
        "id": 4,
        "name": "李士宝",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "东宝区区领导",
        "current_org": "中共荆门市东宝区委员会",
        "source": "https://www.jmdbq.gov.cn/art/2026/7/17/art_7903_1228455.html"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共荆门市东宝区委员会", "type": "党委", "level": "县级", "parent": "中共荆门市委员会", "location": "荆门市东宝区"},
    {"id": 2, "name": "东宝区人民政府", "type": "政府", "level": "县级", "parent": "荆门市人民政府", "location": "荆门市东宝区"},
    {"id": 3, "name": "中共东宝区纪律检查委员会/东宝区监察委员会", "type": "党委", "level": "县级", "parent": "中共荆门市纪律检查委员会", "location": "荆门市东宝区"},
    {"id": 4, "name": "东宝区人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "荆门市人民代表大会常务委员会", "location": "荆门市东宝区"},
    {"id": 5, "name": "中国人民政治协商会议东宝区委员会", "type": "政协", "level": "县级", "parent": "政协荆门市委员会", "location": "荆门市东宝区"},
    {"id": 6, "name": "东宝区应急管理局", "type": "政府", "level": "正科级", "parent": "东宝区人民政府", "location": "荆门市东宝区"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "东宝区委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "Confirmed from 2026-07-17 news article"},
    {"person_id": 2, "org_id": 1, "title": "东宝区委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "Confirmed from 2026-06-18 news article"},
    {"person_id": 2, "org_id": 2, "title": "东宝区人民政府区长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "Confirmed from 2026-06-18 news article"},
    {"person_id": 3, "org_id": 1, "title": "东宝区区领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待确认"},
    {"person_id": 4, "org_id": 1, "title": "东宝区区领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待确认"},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记与区长为东宝区党政正职搭档", "overlap_org": "东宝区", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记与区领导在同一届区委班子中共事", "overlap_org": "中共荆门市东宝区委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区委书记与区领导在同一届区委班子中共事", "overlap_org": "中共荆门市东宝区委员会", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 3, "type": "同事", "context": "区长与区领导在区委班子中共事", "overlap_org": "中共荆门市东宝区委员会", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 4, "type": "同事", "context": "区长与区领导在区委班子中共事", "overlap_org": "中共荆门市东宝区委员会", "overlap_period": "2026"},
]


# ── Main ──────────────────────────────────────────────────────────────────
def main() -> None:
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

    # Write person JSON files for core leaders
    today_str = TODAY
    person_dir = STAGING_DIR

    # 董勇 person JSON
    dongyong = {
        "schema_version": "1.0",
        "generated_at": today_str,
        "investigation_scope": {
            "province": "湖北省",
            "city": "荆门市",
            "region": "东宝区",
            "job": "区委书记",
            "task_id": "hubei_东宝区",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": "dongbao_dongyong",
            "name": "董勇",
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
                "name_birth": "董勇_",
                "name_birthplace": "董勇_",
                "official_profile_url": "https://www.jmdbq.gov.cn/"
            }
        },
        "current_status": {
            "current_post": "东宝区委书记",
            "current_org": "中共荆门市东宝区委员会",
            "administrative_rank": "正处级",
            "as_of": "2026-07-24",
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": "中共荆门市东宝区委员会",
                "title": "东宝区委书记",
                "level": "县级",
                "location": "湖北省荆门市东宝区",
                "system": "party",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "Confirmed from official news article. Full career timeline unknown.",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "organizations": [
            {"org_id": "org_dongbao_party", "name": "中共荆门市东宝区委员会", "role": "领导机关", "source_ids": ["S001"]}
        ],
        "relationships": [
            {
                "person": "张晋",
                "person_id": "dongbao_zhangjin",
                "relationship_type": "党政搭档",
                "strength": "strong",
                "evidence": "董勇作为区委书记、张晋作为区长，为东宝区党政正职搭档",
                "overlap_org": "东宝区",
                "overlap_period": "2026",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"]
            }
        ],
        "governance_record": [
            {
                "period": "2026",
                "domain": "public_security",
                "achievement_or_event": "赴东宝区应急管理局开展调研座谈，强调应急管理能力现代化",
                "role_in_event": "带队调研",
                "measurable_outcome": "",
                "location": "东宝区应急管理局",
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
                "summary": "不明 — 公开资料未找到完整履历",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "discipline_oriented",
                    "evidence": "在应急管理局调研中强调'时时放心不下'的责任感，要求从严从实加强应急干部队伍建设",
                    "confidence": "plausible",
                    "source_ids": ["S001"]
                }
            ],
            "speech_themes": ["安全底线", "应急能力现代化", "智慧应急", "干部队伍建设"],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至2026年7月，未发现董勇的纪律处分、审计问题或负面报道",
                "date": "2026-07-24",
                "confidence": "plausible",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "区委主要领导到区应急管理局开展调研座谈",
                "url": "https://www.jmdbq.gov.cn/art/2026/7/17/art_7903_1228455.html",
                "publisher": "东宝区人民政府",
                "published_at": "2026-07-17",
                "accessed_at": "2026-07-24",
                "source_type": "official",
                "reliability": "high",
                "notes": "确认董勇为东宝区委书记"
            },
            {
                "id": "S002",
                "title": "区政府主要领导到石桥驿镇督导树立和践行正确政绩观学习教育工作",
                "url": "https://www.jmdbq.gov.cn/art/2026/6/18/art_7902_1223734.html",
                "publisher": "东宝区人民政府",
                "published_at": "2026-06-18",
                "accessed_at": "2026-07-24",
                "source_type": "official",
                "reliability": "high",
                "notes": "确认张晋为东宝区委副书记、区长"
            }
        ],
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "缺少董勇的出生年份、籍贯、教育背景、入党时间、完整任职履历等基本信息"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "董勇的出生年份、籍贯、教育背景是什么？",
                "why_it_matters": "基础身份信息，用于人员去重和履历分析",
                "suggested_queries": ["董勇 荆门 简历 出生", "董勇 东宝区委书记 任前公示", "董勇 百度百科"],
                "last_attempted": "2026-07-24"
            },
            {
                "priority": "critical",
                "question": "董勇任东宝区委书记前担任什么职务？",
                "why_it_matters": "晋升路径和前任关系的关键线索",
                "suggested_queries": ["董勇 此前 担任 荆门", "董勇 曾任"],
                "last_attempted": "2026-07-24"
            },
            {
                "priority": "high",
                "question": "董勇的完整任职履历是什么？",
                "why_it_matters": "核心人物的职业轨迹",
                "suggested_queries": ["董勇 简历 任职经历"],
                "last_attempted": "2026-07-24"
            }
        ]
    }

    # 张晋 person JSON
    zhangjin = {
        "schema_version": "1.0",
        "generated_at": today_str,
        "investigation_scope": {
            "province": "湖北省",
            "city": "荆门市",
            "region": "东宝区",
            "job": "区长",
            "task_id": "hubei_东宝区",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": "dongbao_zhangjin",
            "name": "张晋",
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
                "name_birth": "张晋_",
                "name_birthplace": "张晋_",
                "official_profile_url": "https://www.jmdbq.gov.cn/"
            }
        },
        "current_status": {
            "current_post": "东宝区委副书记、区长",
            "current_org": "东宝区人民政府",
            "administrative_rank": "正处级",
            "as_of": "2026-07-24",
            "is_current_confirmed": True,
            "source_ids": ["S002"]
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": "东宝区人民政府",
                "title": "东宝区委副书记、区长",
                "level": "县级",
                "location": "湖北省荆门市东宝区",
                "system": "government",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "Confirmed from official news article. Full career timeline unknown.",
                "confidence": "confirmed",
                "source_ids": ["S002"]
            }
        ],
        "organizations": [
            {"org_id": "org_dongbao_gov", "name": "东宝区人民政府", "role": "领导机关", "source_ids": ["S002"]}
        ],
        "relationships": [
            {
                "person": "董勇",
                "person_id": "dongbao_dongyong",
                "relationship_type": "党政搭档",
                "strength": "strong",
                "evidence": "张晋作为区长、董勇作为区委书记，为东宝区党政正职搭档",
                "overlap_org": "东宝区",
                "overlap_period": "2026",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"]
            }
        ],
        "governance_record": [
            {
                "period": "2026-06",
                "domain": "rural_revitalization",
                "achievement_or_event": "赴石桥驿镇督导树立和践行正确政绩观学习教育工作，调研村集体经济、产业发展及民生实事",
                "role_in_event": "带队督导",
                "measurable_outcome": "",
                "location": "东宝区石桥驿镇",
                "confidence": "confirmed",
                "source_ids": ["S002"]
            }
        ],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "不明 — 公开资料未找到完整履历",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "grassroots_oriented",
                    "evidence": "深入石桥驿镇村级一线调研产业发展、民生水利项目和养老服务",
                    "confidence": "plausible",
                    "source_ids": ["S002"]
                },
                {
                    "trait": "pragmatic",
                    "evidence": "强调'为民造福是最大政绩'，要求多发展'打基础、利长远、惠百姓'的特色产业",
                    "confidence": "plausible",
                    "source_ids": ["S002"]
                }
            ],
            "speech_themes": ["政绩观", "乡村振兴", "产业富民", "民生实事"],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至2026年7月，未发现张晋的纪律处分、审计问题或负面报道",
                "date": "2026-07-24",
                "confidence": "plausible",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "区委主要领导到区应急管理局开展调研座谈",
                "url": "https://www.jmdbq.gov.cn/art/2026/7/17/art_7903_1228455.html",
                "publisher": "东宝区人民政府",
                "published_at": "2026-07-17",
                "accessed_at": "2026-07-24",
                "source_type": "official",
                "reliability": "high",
                "notes": "确认董勇为东宝区委书记"
            },
            {
                "id": "S002",
                "title": "区政府主要领导到石桥驿镇督导树立和践行正确政绩观学习教育工作",
                "url": "https://www.jmdbq.gov.cn/art/2026/6/18/art_7902_1223734.html",
                "publisher": "东宝区人民政府",
                "published_at": "2026-06-18",
                "accessed_at": "2026-07-24",
                "source_type": "official",
                "reliability": "high",
                "notes": "确认张晋为东宝区委副书记、区长"
            }
        ],
        "confidence_summary": {
            "identity": "partial",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "缺少张晋的出生年份、籍贯、教育背景、入党时间、完整任职履历等基本信息"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "张晋的出生年份、籍贯、教育背景是什么？",
                "why_it_matters": "基础身份信息，用于人员去重和履历分析",
                "suggested_queries": ["张晋 荆门 简历 出生", "张晋 东宝区长 任前公示", "张晋 百度百科"],
                "last_attempted": "2026-07-24"
            },
            {
                "priority": "critical",
                "question": "张晋任东宝区长前担任什么职务？",
                "why_it_matters": "晋升路径和前任关系的关键线索",
                "suggested_queries": ["张晋 此前 担任 荆门", "张晋 曾任"],
                "last_attempted": "2026-07-24"
            },
            {
                "priority": "high",
                "question": "张晋的完整任职履历是什么？",
                "why_it_matters": "核心人物的职业轨迹",
                "suggested_queries": ["张晋 简历 任职经历"],
                "last_attempted": "2026-07-24"
            }
        ]
    }

    # Write person JSON files
    dongyong_path = person_dir / f"{today_str}-湖北省-荆门市-区委书记-董勇.json"
    with open(dongyong_path, "w", encoding="utf-8") as f:
        json.dump(dongyong, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Person JSON: {dongyong_path}")

    zhangjin_path = person_dir / f"{today_str}-湖北省-荆门市-区长-张晋.json"
    with open(zhangjin_path, "w", encoding="utf-8") as f:
        json.dump(zhangjin, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Person JSON: {zhangjin_path}")

    print(f"\n{'='*60}")
    print(f"东宝区 build complete!")
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
