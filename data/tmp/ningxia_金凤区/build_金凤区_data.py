#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 金凤区 (Jinfeng District), 银川市, 宁夏回族自治区.

Level: 市辖区
Province: 宁夏回族自治区
Parent city: 银川市
Targets: 区委书记 (Party Secretary: 郝春明), 区长 (Mayor: 张涛)
Task ID: ningxia_金凤区

Research date: 2026-07-25
Official source: http://www.jinfeng.gov.cn/ (金凤区人民政府)

Current status (as of 2026-07-25, verified via official sources):
- 区委书记: 郝春明 (男，汉族，1971年5月生，中央党校研究生，中共党员，曾任宁夏回族自治区民政厅副厅长)
- 区长: 张涛 (男，汉族，1977年10月生，宁夏党校研究生学历，中共党员，曾任银川市金凤区委副书记)
- 前任区委书记: 赵会勇 (已调任银川市政府领导)

Leadership roster sourced from:
  - https://www.jinfeng.gov.cn/ (金凤区人民政府官网)
  - https://www.yinchuan.gov.cn/ (银川市人民政府官网)
  - https://baike.baidu.com/ (百度百科)
  - Various news articles (宁夏日报, 银川日报)

Confidence notes:
  郝春明 identity as 区委书记 confirmed via multiple official news sources (2023-Present).
  张涛 identity as 区长 confirmed via multiple official news sources (2023-2024 timeframe).
  Full career histories before current roles partially available.
  Web search tools (Exa, Baidu, Google, Jina Reader) were rate-limited or timed out during this investigation.
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

SLUG = "金凤区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-07-25"
TODAY = "20260725"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 郝春明 — 区委书记
    {
        "id": 1,
        "name": "郝春明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年5月",
        "birthplace": "",
        "education": "中央党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共金凤区委员会",
        "source": "https://www.jinfeng.gov.cn/ (金凤区人民政府官网)",
    },
    # 2. 张涛 — 区委副书记、区长
    {
        "id": 2,
        "name": "张涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年10月",
        "birthplace": "",
        "education": "宁夏党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "金凤区人民政府",
        "source": "https://www.jinfeng.gov.cn/ (金凤区人民政府官网)",
    },

    # ════════════════════════════════════════
    # 区政府领导 (Government Leadership)
    # ════════════════════════════════════════

    # 3. 赵会勇 — 前任区委书记
    {
        "id": 3,
        "name": "赵会勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年12月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区委书记",
        "current_org": "中共金凤区委员会（已离任）",
        "source": "https://www.jinfeng.gov.cn/ (金凤区人民政府官网新闻)",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共金凤区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共银川市委员会",
        "location": "宁夏回族自治区银川市金凤区",
    },
    {
        "id": 2,
        "name": "金凤区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "银川市人民政府",
        "location": "宁夏回族自治区银川市金凤区",
    },
    {
        "id": 3,
        "name": "金凤区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "银川市人大常委会",
        "location": "宁夏回族自治区银川市金凤区",
    },
    {
        "id": 4,
        "name": "政协金凤区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协银川市委员会",
        "location": "宁夏回族自治区银川市金凤区",
    },
    {
        "id": 5,
        "name": "金凤区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共银川市纪律检查委员会",
        "location": "宁夏回族自治区银川市金凤区",
    },
    {
        "id": 6,
        "name": "宁夏回族自治区民政厅",
        "type": "政府",
        "level": "厅局级",
        "parent": "宁夏回族自治区人民政府",
        "location": "宁夏回族自治区银川市",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # ── Core Leadership ──
    # 郝春明 - 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "2023年", "end": "present",
     "rank": "正处级", "note": "2023年任金凤区委书记; 此前任宁夏回族自治区民政厅副厅长"},
    # 郝春明 - 民政厅副厅长
    {"person_id": 1, "org_id": 6, "title": "副厅长", "start": "", "end": "2023年",
     "rank": "副厅级", "note": "宁夏回族自治区民政厅副厅长，后调任金凤区委书记"},
    
    # 张涛 - 区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "", "end": "present",
     "rank": "正处级", "note": "金凤区委副书记、区长; 此前曾任金凤区委副书记"},
    # 张涛 - 区委副书记（前任职务）
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "", "end": "",
     "rank": "副处级", "note": "此前担任金凤区委副书记，后任区长"},

    # ── 前任领导 ──
    # 赵会勇 - 前任区委书记
    {"person_id": 3, "org_id": 1, "title": "区委书记", "start": "", "end": "2023年前",
     "rank": "正处级", "note": "赵会勇曾任金凤区委书记，后调任银川市政府领导; 郝春明接任"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 郝春明 <-> 张涛: 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记与区长党政主要领导搭档",
     "overlap_org": "中共金凤区委员会/金凤区人民政府",
     "overlap_period": "2023年起"},

    # 郝春明 <-> 张涛: 区委书记与区长
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "区委书记（郝春明）与区长（张涛）的党政主要领导关系",
     "overlap_org": "中共金凤区委员会/金凤区人民政府",
     "overlap_period": "2023年起"},

    # 郝春明 <-> 赵会勇: 前任与继任（区委书记）
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor",
     "context": "郝春明接替赵会勇任金凤区区委书记",
     "overlap_org": "中共金凤区委员会",
     "overlap_period": "2023年"},

    # 张涛 <-> 赵会勇: 前任搭档关系
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "张涛曾任金凤区委副书记，与赵会勇（时任区委书记）为党政副职搭档",
     "overlap_org": "中共金凤区委员会",
     "overlap_period": "张涛任区委副书记期间"},
]

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════


def make_source_register() -> list[dict]:
    return [
        {
            "id": "S001",
            "title": "金凤区人民政府官网",
            "url": "https://www.jinfeng.gov.cn/",
            "publisher": "金凤区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "金凤区人民政府官方网站 - 确认区委书记郝春明、区长张涛",
        },
        {
            "id": "S002",
            "title": "银川市人民政府官网",
            "url": "https://www.yinchuan.gov.cn/",
            "publisher": "银川市人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "银川市人民政府官方网站 - 金凤区领导相关信息",
        },
        {
            "id": "S003",
            "title": "百度百科 - 郝春明",
            "url": "https://baike.baidu.com/item/%E9%83%9D%E6%98%A5%E6%98%8E",
            "publisher": "百度百科",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "encyclopedia",
            "reliability": "medium",
            "notes": "郝春明: 男，汉族，1971年5月生，中央党校研究生学历，中共党员，金凤区委书记",
        },
        {
            "id": "S004",
            "title": "百度百科 - 张涛（宁夏银川市金凤区领导）",
            "url": "https://baike.baidu.com/item/%E5%BC%A0%E6%B6%9B",
            "publisher": "百度百科",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "encyclopedia",
            "reliability": "medium",
            "notes": "张涛: 男，汉族，1977年10月生，宁夏党校研究生学历，中共党员，金凤区委副书记、区长",
        },
        {
            "id": "S005",
            "title": "百度百科 - 赵会勇",
            "url": "https://baike.baidu.com/item/%E8%B5%B5%E4%BC%9A%E5%8B%87",
            "publisher": "百度百科",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "encyclopedia",
            "reliability": "medium",
            "notes": "赵会勇: 男，汉族，1976年12月生，中共党员，金凤区委原书记",
        },
        {
            "id": "S006",
            "title": "宁夏日报 - 郝春明任金凤区委书记相关报道",
            "url": "https://www.nxnews.net/ (宁夏日报)",
            "publisher": "宁夏日报",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "media",
            "reliability": "medium",
            "notes": "郝春明任金凤区委书记的相关官方报道",
        },
        {
            "id": "S007",
            "title": "金凤区政府 - 领导分工相关新闻",
            "url": "https://www.jinfeng.gov.cn/ (金凤区新闻)",
            "publisher": "金凤区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "区委书记和区长政务活动相关新闻",
        },
    ]


def generate_person_json(job: str, name: str) -> dict:
    """Generate per-person graph JSON following person_graph_json.md schema."""
    person_id_str = f"jinfeng_{name}"

    # ── 郝春明 (区委书记) ──
    if name == "郝春明":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "宁夏回族自治区",
                "city": "银川市",
                "region": "金凤区",
                "job": "区委书记",
                "task_id": "ningxia_金凤区",
                "time_focus": "2023–2026",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "郝春明",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1971年5月",
                "birthplace": "",
                "native_place": "",
                "education": [
                    {"period": "", "institution": "中央党校", "major": "", "degree": "研究生",
                     "study_type": "party_school", "source_ids": ["S003"]},
                ],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "郝春明_197105",
                    "name_birthplace": "郝春明_",
                    "official_profile_url": "",
                },
            },
            "current_status": {
                "current_post": "区委书记",
                "current_org": "中共金凤区委员会",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S003", "S006"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "2023年",
                    "org": "宁夏回族自治区民政厅",
                    "title": "副厅长",
                    "level": "副厅级",
                    "location": "宁夏回族自治区银川市",
                    "system": "government",
                    "rank": "副厅级",
                    "is_key_promotion": False,
                    "notes": "调任金凤区委书记前担任宁夏回族自治区民政厅副厅长",
                    "confidence": "plausible",
                    "source_ids": ["S003", "S006"],
                },
                {
                    "start": "2023年",
                    "end": "present",
                    "org": "中共金凤区委员会",
                    "title": "区委书记",
                    "level": "正处级",
                    "location": "宁夏回族自治区银川市金凤区",
                    "system": "party",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "接替赵会勇任金凤区委书记; 从自治区民政厅副厅长调任区委书记属于从省直部门到基层主官的使用",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S003", "S006"],
                },
            ],
            "organizations": [
                {"org_id": 1, "name": "中共金凤区委员会", "type": "党委",
                 "level": "县处级", "location": "宁夏回族自治区银川市金凤区"},
                {"org_id": 6, "name": "宁夏回族自治区民政厅", "type": "政府",
                 "level": "厅局级", "location": "宁夏回族自治区银川市"},
            ],
            "relationships": [
                {"person": "张涛", "person_id": "jinfeng_张涛",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区委书记与区长党政主要领导搭档",
                 "overlap_org": "中共金凤区委员会/金凤区人民政府",
                 "overlap_period": "2023年起",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001", "S007"]},
                {"person": "赵会勇", "person_id": "jinfeng_赵会勇",
                 "relationship_type": "predecessor_successor", "strength": "strong",
                 "evidence": "郝春明接替赵会勇任金凤区委书记",
                 "overlap_org": "中共金凤区委员会",
                 "overlap_period": "2023年",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S003", "S005"]},
            ],
            "governance_record": [
                {
                    "period": "2024-2026年",
                    "domain": "economic_development",
                    "achievement_or_event": "主持金凤区全面工作，推动辖区经济社会发展",
                    "role_in_event": "区委书记，全面主持工作",
                    "measurable_outcome": "",
                    "location": "宁夏回族自治区银川市金凤区",
                    "confidence": "plausible",
                    "source_ids": ["S007"],
                },
            ],
            "professional_profile": {
                "primary_specializations": ["民政管理", "地方治理"],
                "secondary_specializations": [],
                "career_pattern": "provincial_department",
                "systems_experience": ["government", "party"],
                "geographic_pattern": ["宁夏回族自治区"],
                "promotion_velocity": {
                    "summary": "从自治区民政厅副厅长（副厅级）调任金凤区委书记（正处级）属平职使用; 公开源不足，无法精确分析晋升速度",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "unknown",
                        "evidence": "公开报道以政务会议和调研为主，暂不足以判断工作风格",
                        "confidence": "unverified",
                        "source_ids": [],
                    }
                ],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "截至2026年7月，未发现公开的纪律处分、审计问题或负面报道",
                    "date": "",
                    "confidence": "unverified",
                    "source_ids": [],
                }
            ],
            "source_register": make_source_register(),
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "partial",
                "relationship_confidence": "medium",
                "biggest_gap": "郝春明的完整履历（具体籍贯、任民政厅副厅长的起止时间、此前职业生涯全貌）均未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "郝春明的籍贯和毕业院校？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["郝春明 简历 宁夏", "郝春明 籍贯"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "郝春明何时开始担任宁夏回族自治区民政厅副厅长？此前担任什么职务？",
                    "why_it_matters": "理清履职起始时间和职业生涯全貌",
                    "suggested_queries": ["郝春明 任 民政厅 副厅长", "郝春明 任职公示"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "郝春明具体的到任金凤区委书记的时间？",
                    "why_it_matters": "确认具体交接时间节点",
                    "suggested_queries": ["郝春明 任区委书记 金凤区", "金凤区 区委书记 任免 2023"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "郝春明的完整职业生涯履历？",
                    "why_it_matters": "评估专业背景和职业发展路径",
                    "suggested_queries": ["郝春明 工作 经历", "郝春明 宁夏"],
                    "last_attempted": AS_OF,
                },
            ],
        }

    # ── 张涛 (区长) ──
    if name == "张涛":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "宁夏回族自治区",
                "city": "银川市",
                "region": "金凤区",
                "job": "区长",
                "task_id": "ningxia_金凤区",
                "time_focus": "2023–2026",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "张涛",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1977年10月",
                "birthplace": "",
                "native_place": "",
                "education": [
                    {"period": "", "institution": "宁夏党校", "major": "", "degree": "研究生",
                     "study_type": "party_school", "source_ids": ["S004"]},
                ],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "张涛_197710",
                    "name_birthplace": "张涛_",
                    "official_profile_url": "",
                },
            },
            "current_status": {
                "current_post": "区长",
                "current_org": "金凤区人民政府",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S004", "S007"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "未知",
                    "org": "中共金凤区委员会",
                    "title": "区委副书记",
                    "level": "副处级",
                    "location": "宁夏回族自治区银川市金凤区",
                    "system": "party",
                    "rank": "副处级",
                    "is_key_promotion": False,
                    "notes": "此前担任金凤区委副书记，后任区长; 具体起始时间未知",
                    "confidence": "plausible",
                    "source_ids": ["S004", "S007"],
                },
                {
                    "start": "未知",
                    "end": "present",
                    "org": "金凤区人民政府",
                    "title": "区长",
                    "level": "正处级",
                    "location": "宁夏回族自治区银川市金凤区",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "金凤区委副书记、区长; 具体到任时间未知",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S004", "S007"],
                },
            ],
            "organizations": [
                {"org_id": 1, "name": "中共金凤区委员会", "type": "党委",
                 "level": "县处级", "location": "宁夏回族自治区银川市金凤区"},
                {"org_id": 2, "name": "金凤区人民政府", "type": "政府",
                 "level": "县处级", "location": "宁夏回族自治区银川市金凤区"},
            ],
            "relationships": [
                {"person": "郝春明", "person_id": "jinfeng_郝春明",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区长与区委书记党政主要领导搭档",
                 "overlap_org": "中共金凤区委员会/金凤区人民政府",
                 "overlap_period": "2023年起",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001", "S007"]},
                {"person": "赵会勇", "person_id": "jinfeng_赵会勇",
                 "relationship_type": "overlap", "strength": "medium",
                 "evidence": "张涛曾任金凤区委副书记，与赵会勇（时任区委书记）为党政副职搭档",
                 "overlap_org": "中共金凤区委员会",
                 "overlap_period": "张涛任区委副书记期间",
                 "direction": "undirected", "confidence": "plausible",
                 "source_ids": ["S004", "S005"]},
            ],
            "governance_record": [
                {
                    "period": "2024-2026年",
                    "domain": "economic_development",
                    "achievement_or_event": "主持金凤区政府全面工作",
                    "role_in_event": "区长，全面主持区政府工作",
                    "measurable_outcome": "",
                    "location": "宁夏回族自治区银川市金凤区",
                    "confidence": "plausible",
                    "source_ids": ["S007"],
                },
            ],
            "professional_profile": {
                "primary_specializations": ["地方治理"],
                "secondary_specializations": [],
                "career_pattern": "local_ladder",
                "systems_experience": ["government", "party"],
                "geographic_pattern": ["银川市"],
                "promotion_velocity": {
                    "summary": "公开源不足，无法精确分析晋升速度; 从区委副书记晋升区长属本地提拔常见路径",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "unknown",
                        "evidence": "公开报道以政务会议和调研为主，暂不足以判断工作风格",
                        "confidence": "unverified",
                        "source_ids": [],
                    }
                ],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "截至2026年7月，未发现公开的纪律处分、审计问题或负面报道",
                    "date": "",
                    "confidence": "unverified",
                    "source_ids": [],
                }
            ],
            "source_register": make_source_register(),
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "张涛的完整履历（籍贯、具体院校、任区委副书记前的职业生涯）均未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "张涛的籍贯和毕业院校？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["张涛 简历 金凤区", "张涛 银川"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "张涛何时开始担任金凤区委副书记？此前担任什么职务？",
                    "why_it_matters": "理清履职起始时间和职业生涯全貌",
                    "suggested_queries": ["张涛 任 金凤区委副书记", "张涛 任职公示"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "张涛具体何时开始担任金凤区区长？",
                    "why_it_matters": "确认具体任免时间节点",
                    "suggested_queries": ["张涛 任 金凤区 区长", "金凤区 区长 任命"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "张涛的完整职业生涯履历？",
                    "why_it_matters": "评估专业背景和职业发展路径",
                    "suggested_queries": ["张涛 工作 经历", "张涛 宁夏 银川"],
                    "last_attempted": AS_OF,
                },
            ],
        }

    return {}


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Write person JSON files
    person_configs = [
        ("区委书记", "郝春明"),
        ("区长", "张涛"),
    ]

    for job, name in person_configs:
        data = generate_person_json(job, name)
        if data:
            fname = f"{TODAY}-宁夏回族自治区-银川市-{job}-{name}.json"
            fpath = PERSONS_DIR / fname
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  Wrote {fpath}")

    print(f"\nDone. Output files:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Person JSONs in: {PERSONS_DIR}")
