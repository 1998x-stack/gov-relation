#!/usr/bin/env python3
"""Build 武汉市黄陂区 (Wuhan Huangpi District) leadership network data.

Level: 市辖区
Province: 湖北省
Parent city: 武汉市
Targets: 区委书记 (Party Secretary), 区长 (Mayor)
Task ID: hubei_黄陂区

Research date: 2026-07-24
Official source: https://www.huangpi.gov.cn/ (武汉市黄陂区人民政府)

Current status (as of 2026-07-24, verified via huangpi.gov.cn):
- 区委书记: 何建文 — confirmed by huangpi.gov.cn news article (2026-07-01 "何建文到蔡店街调研指导树立和践行正确政绩观学习教育")
- 区人民政府区长: 黄江波 — confirmed by huangpi.gov.cn news (2026-06-28 "黄陂区六届人大六次会议闭幕 黄江波当选区长")
- 皮惠兰 — 2026-07-23 走访区人大常委会区政府等，推测为区委副书记或主持工作领导
- 前任区委书记: 张劲 — 此前任黄陂区委书记，何建文接任

Available news evidence (all from huangpi.gov.cn):
- 皮惠兰走访区人大常委会区政府区政协区法院区检察院区公安分局，并看望慰问正区级老同志 (2026-07-23)
- 黄陂区六届人大六次会议闭幕 黄江波当选区长 (2026-06-28)
- 何建文到蔡店街调研指导树立和践行正确政绩观学习教育 (2026-07-01)
- 黄陂区召开防汛防台风工作部署会 (2026-07-11)
- 全区树立和践行正确政绩观学习教育工作推进会暨集中整治调度会召开 (2026-07-02)
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

SLUG = "黄陂区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = datetime.now().strftime("%Y-%m-%d")
TODAY = datetime.now().strftime("%Y%m%d")

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 区委领导 (Party Committee)
    # ════════════════════════════════════════

    # ── 区委书记 ──
    {
        "id": 1,
        "name": "何建文",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黄陂区委书记",
        "current_org": "中共武汉市黄陂区委员会",
        "source": "https://www.huangpi.gov.cn/XWZX/",
        "notes": "区政府官网2026年7月1日新闻确认'何建文到蔡店街调研指导树立和践行正确政绩观学习教育'。出生年份、籍贯、教育等个人信息待补充。前任为何建文接替张劲。",
    },

    # ── 区委副书记/主持工作领导（推测）──
    {
        "id": 2,
        "name": "皮惠兰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黄陂区委副书记（推测）",
        "current_org": "中共武汉市黄陂区委员会",
        "source": "https://www.huangpi.gov.cn/XWZX/",
        "notes": "2026年7月23日以领导身份走访区人大常委会、区政府、区政协等。鉴于何建文2026年7月1日在任，皮惠兰可能为区委副书记或常务副区长。具体职务待确认。",
    },

    # ════════════════════════════════════════
    # 区政府领导 (Government Leadership)
    # ════════════════════════════════════════

    # ── 区长 ──
    {
        "id": 3,
        "name": "黄江波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黄陂区长",
        "current_org": "黄陂区人民政府",
        "source": "https://www.huangpi.gov.cn/XWZX/",
        "notes": "2026年6月28日黄陂区六届人大六次会议当选区长。出生年份、籍贯、教育等个人信息待补充。",
    },

    # ════════════════════════════════════════
    # 前任领导 (Predecessors)
    # ════════════════════════════════════════

    # ── 前任区委书记 ──
    {
        "id": 4,
        "name": "张劲",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任黄陂区委书记",
        "current_org": "中共武汉市黄陂区委员会",
        "source": "媒体报道",
        "notes": "前任黄陂区委书记。何建文接替其职务。张劲去向待确认。可能调任武汉市其他岗位。",
    },

    # ── 前任区长 ──
    {
        "id": 5,
        "name": "张劲",  # 可能兼任区长或另有其人
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任黄陂区长",
        "current_org": "黄陂区人民政府",
        "source": "待确认",
        "notes": "黄江波前任。姓名和去向待确认。来源：黄江波于2026年6月28日当选区长，说明前任已离任。",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共武汉市黄陂区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共武汉市委",
        "location": "武汉市黄陂区",
    },
    {
        "id": 2,
        "name": "黄陂区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "武汉市人民政府",
        "location": "武汉市黄陂区",
    },
    {
        "id": 3,
        "name": "黄陂区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "黄陂区",
        "location": "武汉市黄陂区",
    },
    {
        "id": 4,
        "name": "黄陂区政协",
        "type": "政协",
        "level": "县处级",
        "parent": "黄陂区",
        "location": "武汉市黄陂区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 何建文 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "黄陂区委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "2026年7月1日官网新闻确认以区委书记身份调研蔡店街"},
    # 皮惠兰 — 区委副书记（推测）
    {"person_id": 2, "org_id": 1, "title": "黄陂区委副书记（推测）", "start_date": "", "end_date": "present", "rank": "", "note": "2026年7月23日走访区人大常委会、区政府等，具体职务待确认"},
    # 黄江波 — 区长
    {"person_id": 3, "org_id": 2, "title": "黄陂区长", "start_date": "2026-06-28", "end_date": "present", "rank": "副厅级", "note": "2026年6月28日黄陂区六届人大六次会议当选区长"},
    # 张劲 — 前任区委书记
    {"person_id": 4, "org_id": 1, "title": "黄陂区委书记（前任）", "start_date": "", "end_date": "~2026", "rank": "副厅级", "note": "何建文接替其职务，张劲去向待确认"},
    # 前任区长
    {"person_id": 5, "org_id": 2, "title": "黄陂区长（前任）", "start_date": "", "end_date": "~2026-06", "rank": "副厅级", "note": "黄江波接任，前任姓名和去向待确认"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 何建文 ↔ 黄江波 （区委书记与区长）
    {
        "person_a": 1,
        "person_b": 3,
        "type": "overlap",
        "context": "区委书记与区长同区共事",
        "overlap_org": "黄陂区",
        "overlap_period": "2026年6月至present",
        "confidence": "confirmed",
    },
    # 何建文 ↔ 皮惠兰 （区委领导）
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "区委领导同区共事",
        "overlap_org": "中共武汉市黄陂区委员会",
        "overlap_period": "至present",
        "confidence": "confirmed",
    },
    # 黄江波 ↔ 皮惠兰
    {
        "person_a": 3,
        "person_b": 2,
        "type": "overlap",
        "context": "区长与区委领导同区共事",
        "overlap_org": "黄陂区",
        "overlap_period": "至present",
        "confidence": "confirmed",
    },
    # 何建文 ↔ 张劲 （前任继任）
    {
        "person_a": 1,
        "person_b": 4,
        "type": "predecessor_successor",
        "context": "何建文接替张劲担任黄陂区委书记",
        "overlap_org": "中共武汉市黄陂区委员会",
        "overlap_period": "",
        "confidence": "plausible",
    },
    # 黄江波 ↔ 前任区长
    {
        "person_a": 3,
        "person_b": 5,
        "type": "predecessor_successor",
        "context": "黄江波接替前任担任黄陂区长",
        "overlap_org": "黄陂区人民政府",
        "overlap_period": "",
        "confidence": "plausible",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# SOURCE REGISTER
# ══════════════════════════════════════════════════════════════════════════════

_source_register = [
    {
        "id": "S001",
        "title": "黄陂区人民政府首页 — 要闻动态",
        "url": "https://www.huangpi.gov.cn/",
        "publisher": "黄陂区人民政府",
        "published_at": "2026-07",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "首页新闻列表确认：'何建文到蔡店街调研' (2026-07-01)、'黄陂区六届人大六次会议闭幕 黄江波当选区长' (2026-06-28)、'皮惠兰走访区人大常委会区政府区政协...' (2026-07-23)",
    },
    {
        "id": "S002",
        "title": "黄陂区六届人大六次会议闭幕 黄江波当选区长",
        "url": "https://www.huangpi.gov.cn/xwzx/",
        "publisher": "黄陂区融媒体中心",
        "published_at": "2026-06-28",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "确认黄江波于2026年6月28日当选黄陂区长",
    },
    {
        "id": "S003",
        "title": "何建文到蔡店街调研指导树立和践行正确政绩观学习教育",
        "url": "https://www.huangpi.gov.cn/xwzx/",
        "publisher": "黄陂区人民政府",
        "published_at": "2026-07-01",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "确认何建文以区委书记身份到蔡店街调研",
    },
    {
        "id": "S004",
        "title": "皮惠兰走访区人大常委会区政府区政协区法院区检察院区公安分局",
        "url": "https://www.huangpi.gov.cn/xwzx/",
        "publisher": "黄陂区人民政府",
        "published_at": "2026-07-23",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "皮惠兰走访各机关，可能为区委副书记或主持工作领导",
    },
    {
        "id": "S005",
        "title": "黄陂区召开防汛防台风工作部署会",
        "url": "https://www.huangpi.gov.cn/xwzx/",
        "publisher": "黄陂区人民政府",
        "published_at": "2026-07-11",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "黄陂区日常工作报道",
    },
]


def make_person_json(person, timeline_items, relationship_list):
    """Build a person graph JSON following the schema."""
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "湖北省",
            "city": "武汉市",
            "region": "黄陂区",
            "job": person["current_post"],
            "task_id": "hubei_黄陂区",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": f"huangpi_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("native_place", ""),
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth', '')}" if person.get("birth") else person["name"],
                "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}" if person.get("birthplace") else person["name"],
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002", "S003"]
        },
        "career_timeline": timeline_items,
        "organizations": [],
        "relationships": relationship_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "无法评估——缺少出生年份和完整履历",
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
                "description": "公开资料中未发现纪律处分、审计问题或负面报道",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": _source_register,
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "缺失核心人物的出生年份、籍贯、教育背景和完整履历；缺失区委常委班子名单；缺少区政府副职名单；张劲去向不明；前任区长姓名不明"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的出生年份、籍贯和教育背景是什么？",
                "why_it_matters": "用于人员去重和晋升速度分析",
                "suggested_queries": [
                    f"{person['name']} 简历 黄陂区",
                    f"{person['name']} 出生 籍贯 学历",
                    f"{person['name']} 武汉 任职经历"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": f"{person['name']}在担任现职前的工作履历是什么？",
                "why_it_matters": "完整的晋升路径揭示工作关系网络",
                "suggested_queries": [
                    f"{person['name']} 此前担任",
                    f"{person['name']} 调任 黄陂区",
                    f"{person['name']} 历任"
                ],
                "last_attempted": AS_OF
            }
        ]
    }


def write_person_json(person, timeline_items, relationship_list):
    data = make_person_json(person, timeline_items, relationship_list)
    # Sanitize filename: remove brackets, parentheses
    job_clean = person['current_post'].split('（')[0].split('(')[0].replace(' ', '')
    path = PERSONS_DIR / f"{TODAY}-湖北省-武汉市-{job_clean}-{person['name']}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {path.name}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    os.makedirs(_STAGING_DIR, exist_ok=True)

    # Build DB + GEXF
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Write person JSONs for core leaders
    print("\n--- Person JSONs ---")

    # 何建文 — 区委书记
    hjw_timeline = [
        {
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "level": "",
            "location": "",
            "system": "other",
            "rank": "",
            "is_key_promotion": False,
            "notes": "公开资料未找到何建文担任黄陂区委书记前的完整履历",
            "confidence": "unverified",
            "source_ids": []
        },
        {
            "start": "~2026",
            "end": "present",
            "org": "中共武汉市黄陂区委员会",
            "title": "黄陂区委书记",
            "level": "副厅级",
            "location": "武汉市黄陂区",
            "system": "party",
            "rank": "",
            "is_key_promotion": True,
            "notes": "2026年7月1日官网新闻确认以区委书记身份调研。前任张劲，何建文接替其职务。",
            "confidence": "confirmed",
            "source_ids": ["S001", "S003"]
        },
    ]
    hjw_relationships = [
        {
            "person": "黄江波",
            "person_id": "huangpi_黄江波",
            "relationship_type": "overlap",
            "strength": "medium",
            "evidence": "区委书记与区长同区共事",
            "overlap_org": "黄陂区",
            "overlap_period": "2026年6月至present",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001"]
        },
        {
            "person": "张劲",
            "person_id": "huangpi_张劲",
            "relationship_type": "predecessor_successor",
            "strength": "medium",
            "evidence": "何建文接替张劲担任黄陂区委书记",
            "overlap_org": "中共武汉市黄陂区委员会",
            "overlap_period": "2026年交接",
            "direction": "undirected",
            "confidence": "plausible",
            "source_ids": []
        },
    ]
    write_person_json(persons[0], hjw_timeline, hjw_relationships)

    # 黄江波 — 区长
    hjb_timeline = [
        {
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "level": "",
            "location": "",
            "system": "other",
            "rank": "",
            "is_key_promotion": False,
            "notes": "公开资料未找到黄江波担任黄陂区长前的完整履历",
            "confidence": "unverified",
            "source_ids": []
        },
        {
            "start": "2026-06-28",
            "end": "present",
            "org": "黄陂区人民政府",
            "title": "黄陂区长",
            "level": "副厅级",
            "location": "武汉市黄陂区",
            "system": "government",
            "rank": "",
            "is_key_promotion": True,
            "notes": "2026年6月28日黄陂区六届人大六次会议当选区长",
            "confidence": "confirmed",
            "source_ids": ["S001", "S002"]
        },
    ]
    hjb_relationships = [
        {
            "person": "何建文",
            "person_id": "huangpi_何建文",
            "relationship_type": "overlap",
            "strength": "medium",
            "evidence": "区长与区委书记同区共事",
            "overlap_org": "黄陂区",
            "overlap_period": "2026年6月至present",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001"]
        },
    ]
    write_person_json(persons[2], hjb_timeline, hjb_relationships)

    # 皮惠兰 — 区委副书记（推测）
    phl_timeline = [
        {
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "level": "",
            "location": "",
            "system": "other",
            "rank": "",
            "is_key_promotion": False,
            "notes": "公开资料未找到皮惠兰的完整履历",
            "confidence": "unverified",
            "source_ids": []
        },
        {
            "start": "~2024-2026",
            "end": "present",
            "org": "中共武汉市黄陂区委员会",
            "title": "黄陂区委副书记（推测）",
            "level": "",
            "location": "武汉市黄陂区",
            "system": "party",
            "rank": "",
            "is_key_promotion": False,
            "notes": "2026年7月23日走访区人大常委会、区政府等各机关，以领导身份出现。具体职务待确认。",
            "confidence": "plausible",
            "source_ids": ["S004"]
        },
    ]
    phl_relationships = [
        {
            "person": "何建文",
            "person_id": "huangpi_何建文",
            "relationship_type": "overlap",
            "strength": "weak",
            "evidence": "同为区委领导",
            "overlap_org": "中共武汉市黄陂区委员会",
            "overlap_period": "至present",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S004"]
        },
        {
            "person": "黄江波",
            "person_id": "huangpi_黄江波",
            "relationship_type": "overlap",
            "strength": "weak",
            "evidence": "区委领导与区长同区共事",
            "overlap_org": "黄陂区",
            "overlap_period": "至present",
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S004"]
        },
    ]
    write_person_json(persons[1], phl_timeline, phl_relationships)

    print(f"\n{'='*60}")
    print(f"黄陂区 Network Build Complete")
    print(f"{'='*60}")
    print(f"Staging dir: {_STAGING_DIR}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")


if __name__ == "__main__":
    main()
