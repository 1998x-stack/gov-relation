#!/usr/bin/env python3
"""Build 盘锦市大洼区 (Panjin Dawa District) leadership network data.

Level: 市辖区
Province: 辽宁省
Parent city: 盘锦市
Targets: 区委书记 (Party Secretary), 区长 (District Mayor)
Task ID: liaoning_大洼区

Research date: 2026-07-25
Official source: http://www.dawa.gov.cn/ (大洼区人民政府)

Current status (as of 2026-07-25, verified via official government website news):

区委领导:
- 林学玮 — 区委书记。主持区委常委会工作，调研水稻插秧工作(2026-07),
  督导检查辽河沿线防汛(2026-07-20), 到田庄台镇开展工作调研(2026-07-21).
  来源: http://www.dawa.gov.cn/ 新闻动态

- 胡楠 — 区委副书记、区长。调研项目建设情况(2026-07),
  赴盘锦帅乡工业园区开展工作(2026-07-23).
  主持大洼区第三届人民政府会议(2026-07-22).
  来源: http://www.dawa.gov.cn/ 新闻动态

区政府领导 (来源: 区政府新闻):
- 胡楠  区委副书记、区长 — 主持区政府全面工作

其他区级领导 (从区委常委会/人大/政协新闻推断):
- 区人大常委会主任 — 待进一步核实
- 区政协主席 — 待进一步核实

Predecessor info:
- Note: 林学玮和胡楠的详细履历和前任信息目前因网络搜索受限无法确认
  （Exa API 限流、百度 403 屏蔽、Jina Reader 超时等）。
  仅能从大洼区政府官方网站新闻动态确认两人当前职务。

Organizations:
- 中共盘锦市大洼区委员会  (区委)
- 盘锦市大洼区人民政府   (区政府)
- 盘锦市大洼区人大常委会 (人大)
- 政协盘锦市大洼区委员会 (政协)
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

SLUG = "大洼区"

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
    {
        "id": 1,
        "name": "林学玮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "大洼区委书记",
        "current_org": "中共盘锦市大洼区委员会",
        "source": ("大洼区政府新闻: http://www.dawa.gov.cn/ "
                   "林学玮调研水稻插秧工作(2026-07), "
                   "督导检查辽河沿线防汛(2026-07-20), "
                   "到田庄台镇开展工作调研(2026-07-21)"),
    },
    {
        "id": 2,
        "name": "胡楠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "大洼区委副书记、区长",
        "current_org": "盘锦市大洼区人民政府",
        "source": ("大洼区政府新闻: http://www.dawa.gov.cn/ "
                   "胡楠调研项目建设情况(2026-07), "
                   "赴盘锦帅乡工业园区开展工作(2026-07-23), "
                   "大洼区第三届人民政府会议(2026-07-22)"),
    },
    # ════════════════════════════════════════
    # 区人大常委会 (People's Congress)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "大洼区人大常委会主任",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "大洼区人大常委会主任",
        "current_org": "盘锦市大洼区人大常委会",
        "source": "大洼区政府新闻: 区人大召开专题调研座谈会(2026-07-16) — 姓名待确认",
    },
    # ════════════════════════════════════════
    # 区政协 (CPPCC)
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "大洼区政协主席",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "大洼区政协主席",
        "current_org": "政协盘锦市大洼区委员会",
        "source": "大洼区政府新闻: 政协盘锦市大洼区第十一届委员会会议(2026-07-22) — 姓名待确认",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共盘锦市大洼区委员会",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共盘锦市委员会",
        "location": "辽宁省盘锦市大洼区",
    },
    {
        "id": 2,
        "name": "盘锦市大洼区人民政府",
        "type": "政府",
        "level": "市辖区",
        "parent": "盘锦市人民政府",
        "location": "辽宁省盘锦市大洼区",
    },
    {
        "id": 3,
        "name": "盘锦市大洼区人大常委会",
        "type": "人大",
        "level": "市辖区",
        "parent": "盘锦市人民代表大会常务委员会",
        "location": "辽宁省盘锦市大洼区",
    },
    {
        "id": 4,
        "name": "政协盘锦市大洼区委员会",
        "type": "政协",
        "level": "市辖区",
        "parent": "政协盘锦市委员会",
        "location": "辽宁省盘锦市大洼区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 林学玮 — 区委书记
    {
        "person_id": 1,
        "org_id": 1,
        "title": "大洼区委书记",
        "start_date": "",
        "end_date": "present",
        "rank": "正处级",
        "note": "区委书记，主持区委全面工作。来源: 大洼区政府官网新闻",
    },
    # 胡楠 — 区委副书记、区长
    {
        "person_id": 2,
        "org_id": 1,
        "title": "大洼区委副书记",
        "start_date": "",
        "end_date": "present",
        "rank": "副处级",
        "note": "区委副书记。来源: 大洼区政府官网新闻",
    },
    {
        "person_id": 2,
        "org_id": 2,
        "title": "大洼区区长",
        "start_date": "",
        "end_date": "present",
        "rank": "正处级",
        "note": "区长，主持区政府全面工作。来源: 大洼区政府官网新闻",
    },
    # 人大主任
    {
        "person_id": 3,
        "org_id": 3,
        "title": "大洼区人大常委会主任",
        "start_date": "",
        "end_date": "present",
        "rank": "正处级",
        "note": "姓名待确认",
    },
    # 政协主席
    {
        "person_id": 4,
        "org_id": 4,
        "title": "大洼区政协主席",
        "start_date": "",
        "end_date": "present",
        "rank": "正处级",
        "note": "姓名待确认",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 林学玮 ↔ 胡楠: 区委书记-区长搭档关系
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记与区长，党委和政府主要负责人搭档关系",
        "overlap_org": "中共盘锦市大洼区委员会 / 盘锦市大洼区人民政府",
        "overlap_period": "2026 (当前)",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# EXECUTION
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Building {SLUG} network data...")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

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

    print(f"\nDatabase: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("Done.")

    # Write person JSON files
    person_files = []

    # Person 1: 林学玮
    p1 = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "盘锦市",
            "region": "大洼区",
            "job": "大洼区委书记",
            "task_id": "liaoning_大洼区",
            "time_focus": "2026年7月",
        },
        "identity": {
            "person_id": "dawa_林学玮",
            "name": "林学玮",
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
                "name_birth": "林学玮_",
                "name_birthplace": "林学玮_",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": "大洼区委书记",
            "current_org": "中共盘锦市大洼区委员会",
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": [],
        "organizations": [],
        "relationships": [
            {
                "person": "胡楠",
                "person_id": "dawa_胡楠",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "区委书记与区长搭档，共同主持大洼区工作",
                "overlap_org": "中共盘锦市大洼区委员会",
                "overlap_period": "2026",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            }
        ],
        "governance_record": [
            {
                "period": "2026-07",
                "domain": "rural_revitalization",
                "achievement_or_event": "调研水稻插秧工作",
                "role_in_event": "带队调研",
                "measurable_outcome": "",
                "location": "大洼区",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "period": "2026-07-20",
                "domain": "public_security",
                "achievement_or_event": "督导检查辽河沿线防汛工作",
                "role_in_event": "带队督导",
                "measurable_outcome": "",
                "location": "大洼区辽河沿线",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "period": "2026-07-21",
                "domain": "rural_revitalization",
                "achievement_or_event": "到田庄台镇开展工作调研",
                "role_in_event": "带队调研",
                "measurable_outcome": "",
                "location": "大洼区田庄台镇",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
        ],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["party"],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "未发现公开的纪律处分、审计问题或负面报道",
                "date": "",
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "大洼区人民政府官方网站",
                "url": "http://www.dawa.gov.cn/",
                "publisher": "大洼区人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "新闻动态中的区委书记活动报道",
            }
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "完整履历（出生年月、籍贯、教育背景、早期任职经历）因网络搜索受限无法获取",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "林学玮的出生年月、籍贯、教育背景",
                "why_it_matters": "核心人物身份信息缺失",
                "suggested_queries": ["林学玮 简历 大洼区", "林学玮 百度百科", "林学玮 任前公示"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": "林学玮的完整任职履历",
                "why_it_matters": "无法构建完整的职业发展路径",
                "suggested_queries": ["林学玮 任职经历", "林学玮 此前 担任"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "林学玮的前任区委书记是谁，现任何处",
                "why_it_matters": "前任-继任关系是关系网络的重要连接",
                "suggested_queries": ["大洼区 前任 区委书记", "大洼区委书记 卸任 去向"],
                "last_attempted": AS_OF,
            },
        ],
    }

    p1_path = PERSONS_DIR / f"{TODAY}-辽宁省-盘锦市-大洼区委书记-林学玮.json"
    with open(p1_path, "w", encoding="utf-8") as f:
        json.dump(p1, f, ensure_ascii=False, indent=2)
    person_files.append(p1_path)
    print(f"  Person JSON: {p1_path.name}")

    # Person 2: 胡楠
    p2 = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "盘锦市",
            "region": "大洼区",
            "job": "大洼区委副书记、区长",
            "task_id": "liaoning_大洼区",
            "time_focus": "2026年7月",
        },
        "identity": {
            "person_id": "dawa_胡楠",
            "name": "胡楠",
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
                "name_birth": "胡楠_",
                "name_birthplace": "胡楠_",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": "大洼区委副书记、区长",
            "current_org": "盘锦市大洼区人民政府",
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": [],
        "organizations": [],
        "relationships": [
            {
                "person": "林学玮",
                "person_id": "dawa_林学玮",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "区长与区委书记搭档，共同主持大洼区工作",
                "overlap_org": "中共盘锦市大洼区委员会",
                "overlap_period": "2026",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            }
        ],
        "governance_record": [
            {
                "period": "2026-07",
                "domain": "economic_development",
                "achievement_or_event": "调研项目建设情况",
                "role_in_event": "带队调研",
                "measurable_outcome": "",
                "location": "大洼区",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "period": "2026-07-23",
                "domain": "economic_development",
                "achievement_or_event": "赴盘锦帅乡工业园区开展工作",
                "role_in_event": "带队工作",
                "measurable_outcome": "",
                "location": "大洼区盘锦帅乡工业园区",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "period": "2026-07-22",
                "domain": "economic_development",
                "achievement_or_event": "主持大洼区第三届人民政府会议",
                "role_in_event": "主持",
                "measurable_outcome": "",
                "location": "大洼区",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
        ],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["government"],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "未发现公开的纪律处分、审计问题或负面报道",
                "date": "",
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "大洼区人民政府官方网站",
                "url": "http://www.dawa.gov.cn/",
                "publisher": "大洼区人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "新闻动态中的区长活动报道",
            }
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "完整履历（出生年月、籍贯、教育背景、早期任职经历）因网络搜索受限无法获取",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "胡楠的出生年月、籍贯、教育背景",
                "why_it_matters": "核心人物身份信息缺失",
                "suggested_queries": ["胡楠 简历 大洼区", "胡楠 百度百科", "胡楠 任前公示"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": "胡楠的完整任职履历",
                "why_it_matters": "无法构建完整的职业发展路径",
                "suggested_queries": ["胡楠 任职经历", "胡楠 此前 担任"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "胡楠的前任区长是谁",
                "why_it_matters": "前任-继任关系是关系网络的重要连接",
                "suggested_queries": ["大洼区 前任 区长"],
                "last_attempted": AS_OF,
            },
        ],
    }

    p2_path = PERSONS_DIR / f"{TODAY}-辽宁省-盘锦市-区长-胡楠.json"
    with open(p2_path, "w", encoding="utf-8") as f:
        json.dump(p2, f, ensure_ascii=False, indent=2)
    person_files.append(p2_path)
    print(f"  Person JSON: {p2_path.name}")

    print(f"\nTotal person JSON files: {len(person_files)}")
    print("Build complete.")
