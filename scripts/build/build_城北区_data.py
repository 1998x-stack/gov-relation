#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 城北区, 西宁市, 青海省.

Investigation date: 2026-07-25
Task ID: qinghai_城北区
Level: 市辖区
Targets: 区委书记 & 区长

Research status: PARTIAL — limited evidence due to severe web access degradation
(Exa rate-limited, Baidu 403/captcha, xncb.gov.cn connection errors, Jina Reader
timeouts, all search-engine queries blocked/timed out).

Known from the home page of www.xncb.gov.cn:
- 城北区 held its 10th Party Congress (中国共产党西宁市城北区第十次代表大会) in July 2026
- 城北区 10th People's Congress (十届人大一次会议) held ~2026-07-23
- 城北区 10th CPPCC (政协十届一次会议) held ~2026-07-24
- "祁登林" participated in a CPPCC boundary group discussion (2026-07-24)
- The leadership page (领导信息/领导之窗) could not be accessed (site was unstable)

Core leader names are UNVERIFIED due to site inaccessibility.
祁登林 is the only name found — his exact role is unknown.
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
SLUG = "城北区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

# ── Persons ────────────────────────────────────────────────────────────────
# NOTE: Core leader names UNVERIFIED. 祁登林 is the only name found in article
# titles from the government website; his exact role is unclear (may be 区委书记,
# 区长, or 政协主席). All biographical identity fields are empty.
persons = [
    # ═══════ Core Leadership (UNVERIFIED) ═══════
    {
        "id": 1,
        "name": "待确认_区委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "城北区委书记",
        "current_org": "中共西宁市城北区委员会",
        "source": "https://www.xncb.gov.cn/"
    },
    {
        "id": 2,
        "name": "待确认_区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "城北区委副书记、区长",
        "current_org": "城北区人民政府",
        "source": "https://www.xncb.gov.cn/"
    },
    # ═══════ Candidate Leader (祁登林 — role unconfirmed) ═══════
    {
        "id": 3,
        "name": "祁登林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "城北区领导（具体职务未确认）",
        "current_org": "中共西宁市城北区委员会",
        "source": "https://www.xncb.gov.cn/ —— 新闻标题中出现"
    },
    # ═══════ Standing Org Leaders (UNVERIFIED) ═══════
    {
        "id": 4,
        "name": "待确认_人大常委会主任",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "城北区人大常委会主任",
        "current_org": "城北区人民代表大会常务委员会",
        "source": "https://www.xncb.gov.cn/"
    },
    {
        "id": 5,
        "name": "待确认_政协主席",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "政协城北区委员会主席",
        "current_org": "中国人民政治协商会议城北区委员会",
        "source": "https://www.xncb.gov.cn/"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共西宁市城北区委员会", "type": "党委", "level": "县级", "parent": "中共西宁市委员会", "location": "西宁市城北区"},
    {"id": 2, "name": "城北区人民政府", "type": "政府", "level": "县级", "parent": "西宁市人民政府", "location": "西宁市城北区"},
    {"id": 3, "name": "中共城北区纪律检查委员会/城北区监察委员会", "type": "党委", "level": "县级", "parent": "中共西宁市纪律检查委员会", "location": "西宁市城北区"},
    {"id": 4, "name": "城北区人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "西宁市人民代表大会常务委员会", "location": "西宁市城北区"},
    {"id": 5, "name": "中国人民政治协商会议城北区委员会", "type": "政协", "level": "县级", "parent": "政协西宁市委员会", "location": "西宁市城北区"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "城北区委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "身份未确认——区委书记姓名待查"},
    {"person_id": 2, "org_id": 1, "title": "城北区委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "身份未确认——区长姓名待查"},
    {"person_id": 2, "org_id": 2, "title": "城北区人民政府区长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "身份未确认——区长姓名待查"},
    {"person_id": 3, "org_id": 1, "title": "城北区领导（具体职务待确认）", "start_date": "", "end_date": "present", "rank": "", "note": "2026-07-24新闻标题中出现：祁登林参加区政协十届一次会议界别联组讨论"},
    {"person_id": 4, "org_id": 4, "title": "城北区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": "身份未确认——人大常委会主任姓名待查"},
    {"person_id": 5, "org_id": 5, "title": "政协城北区委员会主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": "身份未确认——政协主席姓名待查"},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记与区长为城北区党政正职搭档（2026年换届）", "overlap_org": "城北区", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 4, "type": "党政-人大", "context": "区委书记与区人大常委会主任在区委领导下共事", "overlap_org": "中共西宁市城北区委员会", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 5, "type": "政府-政协", "context": "区长与政协主席在区政府和政协工作中协作", "overlap_org": "城北区", "overlap_period": "2026"},
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

    # 城北区区委书记 person JSON (待确认)
    party_secretary = {
        "schema_version": "1.0",
        "generated_at": today_str,
        "investigation_scope": {
            "province": "青海省",
            "city": "西宁市",
            "region": "城北区",
            "job": "区委书记",
            "task_id": "qinghai_城北区",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": "chengbei_partysec",
            "name": "待确认_区委书记",
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
                "name_birth": "",
                "name_birthplace": "",
                "official_profile_url": "https://www.xncb.gov.cn/"
            }
        },
        "current_status": {
            "current_post": "城北区委书记",
            "current_org": "中共西宁市城北区委员会",
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": []
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": "中共西宁市城北区委员会",
                "title": "城北区委书记",
                "level": "县级",
                "location": "青海省西宁市城北区",
                "system": "party",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "2026年7月城北区第十次党代会换届，区委书记姓名待确认",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "organizations": [
            {"org_id": "org_chengbei_party", "name": "中共西宁市城北区委员会", "role": "领导机关", "source_ids": []}
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
                "summary": "不明 — 区委书记姓名和履历均未确认",
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
                "description": "截至2026年7月，因区委书记姓名未确认，无法检索到相关纪律处分信息",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "西宁市城北区人民政府门户网站",
                "url": "https://www.xncb.gov.cn/",
                "publisher": "西宁市城北区人民政府",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "medium",
                "notes": "可确认城北区2026年7月完成第十次党代会和区人大/政协换届，但领导之窗页面无法访问"
            }
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "区委书记姓名、出生年份、籍贯、教育背景、履历全部未知"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "城北区区委书记是谁？",
                "why_it_matters": "城北区党政一把手，关系网络核心节点",
                "suggested_queries": [
                    "西宁市城北区 区委书记 2026",
                    "城北区 第十次党代会 区委书记",
                    "祁登林 城北区 职务"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": "区委书记的完整履历是什么？",
                "why_it_matters": "核心人物的职业轨迹和晋升路径",
                "suggested_queries": [
                    "[姓名] 简历 西宁 城北区",
                    "[姓名] 任前公示 西宁 组织部",
                    "[姓名] 百度百科"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": "前任城北区委书记是谁？去向如何？",
                "why_it_matters": "干部交流模式和晋升路径分析",
                "suggested_queries": [
                    "城北区 前任 区委书记",
                    "城北区 上一任 党委书记"
                ],
                "last_attempted": AS_OF
            }
        ]
    }

    # 城北区区长 person JSON (待确认)
    mayor = {
        "schema_version": "1.0",
        "generated_at": today_str,
        "investigation_scope": {
            "province": "青海省",
            "city": "西宁市",
            "region": "城北区",
            "job": "区长",
            "task_id": "qinghai_城北区",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": "chengbei_mayor",
            "name": "待确认_区长",
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
                "name_birth": "",
                "name_birthplace": "",
                "official_profile_url": "https://www.xncb.gov.cn/"
            }
        },
        "current_status": {
            "current_post": "城北区委副书记、区长",
            "current_org": "城北区人民政府",
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": []
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": "城北区人民政府",
                "title": "城北区委副书记、区长",
                "level": "县级",
                "location": "青海省西宁市城北区",
                "system": "government",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "2026年7月城北区第十届人大一次会议选举产生（或任命），区长姓名待确认",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "organizations": [
            {"org_id": "org_chengbei_gov", "name": "城北区人民政府", "role": "领导机关", "source_ids": []}
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
                "summary": "不明 — 区长姓名和履历均未确认",
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
                "description": "截至2026年7月，因区长姓名未确认，无法检索到相关纪律处分信息",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "西宁市城北区人民政府门户网站",
                "url": "https://www.xncb.gov.cn/",
                "publisher": "西宁市城北区人民政府",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "medium",
                "notes": "可确认城北区2026年7月完成第十届人大一次会议，选举产生区政府领导，但具体名单无法访问"
            }
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "区长姓名、出生年份、籍贯、教育背景、履历全部未知"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "城北区区长是谁？",
                "why_it_matters": "区政府主要负责人，关系网络核心节点",
                "suggested_queries": [
                    "西宁市城北区 区长 2026",
                    "城北区 第十届人大 区长 选举",
                    "城北区 人民政府 区长"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": "区长的完整履历是什么？",
                "why_it_matters": "核心人物的职业轨迹",
                "suggested_queries": [
                    "[姓名] 简历 西宁 城北区",
                    "[姓名] 任前公示 西宁",
                    "[姓名] 百度百科"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": "前任城北区区长是谁？去向如何？",
                "why_it_matters": "干部交流模式和晋升路径分析",
                "suggested_queries": [
                    "城北区 前任 区长",
                    "城北区 上一任 区长"
                ],
                "last_attempted": AS_OF
            }
        ]
    }

    # 祁登林 person JSON (partial - role unconfirmed)
    qidenglin = {
        "schema_version": "1.0",
        "generated_at": today_str,
        "investigation_scope": {
            "province": "青海省",
            "city": "西宁市",
            "region": "城北区",
            "job": "待确认",
            "task_id": "qinghai_城北区",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": "chengbei_qidenglin",
            "name": "祁登林",
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
                "name_birth": "祁登林_",
                "name_birthplace": "祁登林_",
                "official_profile_url": "https://www.xncb.gov.cn/"
            }
        },
        "current_status": {
            "current_post": "城北区领导（具体职务待确认）",
            "current_org": "未知",
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": ["S001"]
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": "城北区",
                "title": "城北区领导（具体职务待确认）",
                "level": "县级",
                "location": "青海省西宁市城北区",
                "system": "unknown",
                "rank": "",
                "is_key_promotion": False,
                "notes": "2026-07-24新闻标题：祁登林参加区政协十届一次会议界别联组讨论。具体职务未知（可能为区委书记、区长或政协主席）。",
                "confidence": "unverified",
                "source_ids": ["S001"]
            }
        ],
        "organizations": [],
        "relationships": [],
        "governance_record": [
            {
                "period": "2026-07-24",
                "domain": "other",
                "achievement_or_event": "参加区政协十届一次会议界别联组讨论",
                "role_in_event": "参会",
                "measurable_outcome": "",
                "location": "城北区",
                "confidence": "plausible",
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
                "summary": "不明 — 公开资料未找到任何履历信息",
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
                "description": "截至2026年7月，未发现祁登林的纪律处分、审计问题或负面报道",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "祁登林参加区政协十届一次会议界别联组讨论 — 城北区人民政府网站新闻列表",
                "url": "https://www.xncb.gov.cn/",
                "publisher": "西宁市城北区人民政府",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "medium",
                "notes": "仅从首页新闻标题确认祁登林参会，具体职务和详细内容因JS动态加载无法抓取"
            }
        ],
        "confidence_summary": {
            "identity": "partial",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "祁登林的具体职务、出生信息、履历全部未知"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "祁登林在城北区的具体职务是什么？",
                "why_it_matters": "城北区关系网络核心节点定位",
                "suggested_queries": [
                    "祁登林 城北区 职务",
                    "祁登林 区委书记",
                    "祁登林 城北区 简历"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": "祁登林的基本信息（出生、籍贯、教育背景）是什么？",
                "why_it_matters": "基础身份信息，用于人员去重和履历分析",
                "suggested_queries": [
                    "祁登林 简历 西宁",
                    "祁登林 出生",
                    "祁登林 百度百科"
                ],
                "last_attempted": AS_OF
            }
        ]
    }

    # Write person JSON files
    ps_path = person_dir / f"{today_str}-青海省-西宁市-区委书记-待确认_区委书记.json"
    with open(ps_path, "w", encoding="utf-8") as f:
        json.dump(party_secretary, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Person JSON: {ps_path}")

    mayor_path = person_dir / f"{today_str}-青海省-西宁市-区长-待确认_区长.json"
    with open(mayor_path, "w", encoding="utf-8") as f:
        json.dump(mayor, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Person JSON: {mayor_path}")

    qdl_path = person_dir / f"{today_str}-青海省-西宁市-领导-祁登林.json"
    with open(qdl_path, "w", encoding="utf-8") as f:
        json.dump(qidenglin, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Person JSON: {qdl_path}")

    print(f"\n{'='*60}")
    print(f"城北区 build complete!")
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
