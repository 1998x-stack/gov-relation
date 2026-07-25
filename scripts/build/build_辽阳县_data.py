#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 辽阳县, 辽阳市, 辽宁省.

Level: 县
Province: 辽宁省
Parent city: 辽阳市
Targets: 县委书记 (Party Secretary: 王浩), 县长 (Mayor: 田相宇)
Task ID: liaoning_辽阳县

Research date: 2026-07-25
Official source: http://www.liaoyangxian.gov.cn/ (辽阳县人民政府)

Current status (as of 2026-07-25, verified via 辽阳县人民政府 website):
- 县委书记: 王浩 (男，2026年7月22日以县委书记身份到小北河镇、唐马寨镇防汛一线)
- 县委副书记、县长: 田相宇 (男，2026年7月23日以县长身份主持召开县政府党组、常务会议)
- 县委副书记: 张福海 (男，2026年7月19日参加防汛慰问活动)
- 县委常委: 关晟 (男，2026年7月9日出席县委常委议军会议)

Leadership roster sourced from:
  - http://www.liaoyangxian.gov.cn/ (辽阳县人民政府首页)
  - http://www.liaoyangxian.gov.cn/xwzx/002006/20260721/18166572-5334-44b6-bd25-08af7882a0b2.html (王浩防汛救灾)
  - http://www.liaoyangxian.gov.cn/xwzx/002006/20260724/fab4eaa0-5019-4952-946d-b983b10dc563.html (田相宇主持政府常务会议)
  - http://www.liaoyangxian.gov.cn/xwzx/002006/com_list.html (新闻列表，包含张福海、关晟信息)

Confidence notes:
  王浩 identity as 县委书记 confirmed via July 2026 news article on county website.
  田相宇 identity as 县长 confirmed via July 2026 news article on county website.
  Full career histories before current roles are unknown - only current roles confirmed.
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

SLUG = "辽阳县"

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

    # 1. 王浩 — 县委书记
    {
        "id": 1,
        "name": "王浩",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共辽阳县委员会",
        "source": "http://www.liaoyangxian.gov.cn/xwzx/002006/20260721/18166572-5334-44b6-bd25-08af7882a0b2.html",
    },
    # 2. 田相宇 — 县委副书记、县长
    {
        "id": 2,
        "name": "田相宇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县长",
        "current_org": "辽阳县人民政府",
        "source": "http://www.liaoyangxian.gov.cn/xwzx/002006/20260724/fab4eaa0-5019-4952-946d-b983b10dc563.html",
    },

    # ════════════════════════════════════════
    # 县领导 (County Leadership)
    # ════════════════════════════════════════

    # 3. 张福海 — 县委副书记
    {
        "id": 3,
        "name": "张福海",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共辽阳县委员会",
        "source": "http://www.liaoyangxian.gov.cn/xwzx/002006/20260721/18166572-5334-44b6-bd25-08af7882a0b2.html",
    },
    # 4. 关晟 — 县委常委
    {
        "id": 4,
        "name": "关晟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共辽阳县委员会",
        "source": "http://www.liaoyangxian.gov.cn/xwzx/002006/com_list.html",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共辽阳县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共辽阳市委员会",
        "location": "辽宁省辽阳市辽阳县",
    },
    {
        "id": 2,
        "name": "辽阳县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "辽阳市人民政府",
        "location": "辽宁省辽阳市辽阳县",
    },
    {
        "id": 3,
        "name": "辽阳县人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "辽阳市人大常委会",
        "location": "辽宁省辽阳市辽阳县",
    },
    {
        "id": 4,
        "name": "政协辽阳县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协辽阳市委员会",
        "location": "辽宁省辽阳市辽阳县",
    },
    {
        "id": 5,
        "name": "辽阳县纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共辽阳市纪律检查委员会",
        "location": "辽宁省辽阳市辽阳县",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # ── Core Leadership ──
    # 王浩 - 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "present",
     "rank": "正处级", "note": "2026年7月22日以县委书记身份深入防汛一线"},
    # 田相宇 - 县长
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "present",
     "rank": "正处级", "note": "2026年7月23日以县委副书记、县政府党组书记、县长身份主持召开县政府党组、常务会议"},
    # 田相宇 - 县委副书记
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "present",
     "rank": "副处级", "note": "辽阳县委副书记、县长"},

    # ── 县领导 ──
    # 张福海 - 县委副书记
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "", "end": "present",
     "rank": "副处级", "note": "2026年7月19日以县委副书记身份参加防汛慰问活动"},
    # 关晟 - 县委常委
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "present",
     "rank": "副处级", "note": "2026年7月9日出席县委常委议军会议"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 王浩 <-> 田相宇: 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "县委书记与县长党政主要领导搭档",
     "overlap_org": "中共辽阳县委员会/辽阳县人民政府",
     "overlap_period": "截至2026年7月"},

    # 王浩 <-> 张福海: 书记与副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "县委书记与县委副书记；县委领导班子搭档",
     "overlap_org": "中共辽阳县委员会",
     "overlap_period": "截至2026年7月"},

    # 王浩 <-> 关晟: 书记与常委
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "县委书记与县委常委；县委领导班子搭档",
     "overlap_org": "中共辽阳县委员会",
     "overlap_period": "截至2026年7月"},

    # 田相宇 <-> 张福海: 县长与副书记
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "县长与县委副书记；县领导班子同事",
     "overlap_org": "中共辽阳县委员会",
     "overlap_period": "截至2026年7月"},

    # 田相宇 <-> 关晟: 县长与常委
    {"person_a": 2, "person_b": 4, "type": "overlap",
     "context": "县长与县委常委",
     "overlap_org": "中共辽阳县委员会",
     "overlap_period": "截至2026年7月"},

    # 张福海 <-> 关晟: 县领导同事
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "县委领导班子同事",
     "overlap_org": "中共辽阳县委员会",
     "overlap_period": "截至2026年7月"},
]

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════


def make_source_register() -> list[dict]:
    return [
        {
            "id": "S001",
            "title": "辽阳县人民政府官网-新闻-县委书记王浩深入防汛一线",
            "url": "http://www.liaoyangxian.gov.cn/xwzx/002006/20260721/18166572-5334-44b6-bd25-08af7882a0b2.html",
            "publisher": "辽阳县人民政府",
            "published_at": "2026-07-22",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认王浩为辽阳县县委书记（截至2026年7月19日）",
        },
        {
            "id": "S002",
            "title": "辽阳县人民政府官网-新闻-辽阳县政府召开党组、常务会议",
            "url": "http://www.liaoyangxian.gov.cn/xwzx/002006/20260724/fab4eaa0-5019-4952-946d-b983b10dc563.html",
            "publisher": "辽阳县人民政府",
            "published_at": "2026-07-24",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "田相宇: 县委副书记、县政府党组书记、县长",
        },
        {
            "id": "S003",
            "title": "辽阳县人民政府官网-新闻列表-今日辽阳县",
            "url": "http://www.liaoyangxian.gov.cn/xwzx/002006/com_list.html",
            "publisher": "辽阳县人民政府",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "包含张福海（县委副书记）、关晟（县委常委）等信息",
        },
    ]


def generate_person_json(job: str, name: str) -> dict:
    """Generate per-person graph JSON following person_graph_json.md schema."""
    person_id_str = f"liaoyangxian_{name}"

    # ── 王浩 (县委书记) ──
    if name == "王浩":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "辽宁省",
                "city": "辽阳市",
                "region": "辽阳县",
                "job": "县委书记",
                "task_id": "liaoning_辽阳县",
                "time_focus": "2026",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "王浩",
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
                    "name_birth": "王浩_",
                    "name_birthplace": "王浩_",
                    "official_profile_url": "",
                },
            },
            "current_status": {
                "current_post": "县委书记",
                "current_org": "中共辽阳县委员会",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "present",
                    "org": "中共辽阳县委员会",
                    "title": "县委书记",
                    "level": "正处级",
                    "location": "辽宁省辽阳市辽阳县",
                    "system": "party",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "2026年7月22日以县委书记身份深入防汛一线。此前履历公开信息不足",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                },
            ],
            "organizations": [
                {"org_id": 1, "name": "中共辽阳县委员会", "type": "党委",
                 "level": "县处级", "location": "辽宁省辽阳市辽阳县"},
            ],
            "relationships": [
                {"person": "田相宇", "person_id": "liaoyangxian_田相宇",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "县委书记与县长党政主要领导搭档",
                 "overlap_org": "中共辽阳县委员会/辽阳县人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001", "S002"]},
                {"person": "张福海", "person_id": "liaoyangxian_张福海",
                 "relationship_type": "superior_subordinate", "strength": "medium",
                 "evidence": "县委书记与县委副书记",
                 "overlap_org": "中共辽阳县委员会",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001"]},
                {"person": "关晟", "person_id": "liaoyangxian_关晟",
                 "relationship_type": "superior_subordinate", "strength": "medium",
                 "evidence": "县委书记与县委常委",
                 "overlap_org": "中共辽阳县委员会",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S003"]},
            ],
            "governance_record": [
                {
                    "period": "2026年7月",
                    "domain": "public_security",
                    "achievement_or_event": "深入小北河镇、唐马寨镇防汛救灾一线走访慰问，督导检查防汛减灾、群众转移安置、巡堤查险工作",
                    "role_in_event": "县委书记，深入一线指挥",
                    "measurable_outcome": "实地走访17个村庄，部署防汛减灾措施",
                    "location": "辽阳县小北河镇、唐马寨镇",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                },
                {
                    "period": "2026年6月",
                    "domain": "other",
                    "achievement_or_event": "深入河栏镇、甜水满族乡督导检查防汛备汛、调研产业发展",
                    "role_in_event": "县委书记，调研督导",
                    "measurable_outcome": "督促基层防汛备汛和产业调研",
                    "location": "辽阳县河栏镇、甜水满族乡",
                    "confidence": "confirmed",
                    "source_ids": ["S003"],
                },
                {
                    "period": "2026年7月",
                    "domain": "other",
                    "achievement_or_event": "讲授树立和践行正确政绩观学习教育专题党课",
                    "role_in_event": "县委书记，主讲",
                    "measurable_outcome": "组织全县干部学习教育",
                    "location": "辽阳县",
                    "confidence": "confirmed",
                    "source_ids": ["S003"],
                },
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["party"],
                "geographic_pattern": ["辽阳市"],
                "promotion_velocity": {
                    "summary": "公开源不足，无法精确分析晋升速度",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "grassroots_oriented",
                        "evidence": "亲自深入防汛一线17个村庄走访慰问，检查防汛减灾工作",
                        "confidence": "plausible",
                        "source_ids": ["S001"],
                    },
                    {
                        "trait": "stability_oriented",
                        "evidence": "强调'人民至上、生命至上'，要求'时时放心不下'的责任感",
                        "confidence": "plausible",
                        "source_ids": ["S001"],
                    },
                ],
                "speech_themes": ["坚持人民至上生命至上", "群防群控", "众志成城共护家园"],
                "management_signals": ["亲自深入一线督导", "强调正向激励", "要求各部门协同联动"],
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
                "identity": "plausible",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "王浩的完整履历（出生年月、籍贯、教育背景、任县委书记前的职业生涯）均未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "王浩的出生年月、籍贯、毕业院校？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["王浩 简历 辽阳县 辽阳", "王浩 出生"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "王浩何时开始担任辽阳县委书记？此前担任什么职务？",
                    "why_it_matters": "理清履职起始时间和职业生涯全貌",
                    "suggested_queries": ["王浩 任 辽阳县 县委书记 任职公示"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "王浩的完整职业生涯履历？",
                    "why_it_matters": "评估专业背景和职业发展路径",
                    "suggested_queries": ["王浩 工作 经历 辽阳"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "前任县委书记是谁？何时交接？",
                    "why_it_matters": "理清县委书记交接链条",
                    "suggested_queries": ["辽阳县 前任 县委书记"],
                    "last_attempted": AS_OF,
                },
            ],
        }

    # ── 田相宇 (县长) ──
    if name == "田相宇":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "辽宁省",
                "city": "辽阳市",
                "region": "辽阳县",
                "job": "县长",
                "task_id": "liaoning_辽阳县",
                "time_focus": "2026",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "田相宇",
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
                    "name_birth": "田相宇_",
                    "name_birthplace": "田相宇_",
                    "official_profile_url": "",
                },
            },
            "current_status": {
                "current_post": "县长",
                "current_org": "辽阳县人民政府",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S002"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "present",
                    "org": "辽阳县人民政府",
                    "title": "县长",
                    "level": "正处级",
                    "location": "辽宁省辽阳市辽阳县",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "2026年7月23日以县委副书记、县政府党组书记、县长身份主持召开县政府党组、常务会议。此前履历公开信息不足",
                    "confidence": "confirmed",
                    "source_ids": ["S002"],
                },
                {
                    "start": "未知",
                    "end": "present",
                    "org": "中共辽阳县委员会",
                    "title": "县委副书记",
                    "level": "副处级",
                    "location": "辽宁省辽阳市辽阳县",
                    "system": "party",
                    "rank": "副处级",
                    "is_key_promotion": False,
                    "notes": "兼任县委副书记",
                    "confidence": "confirmed",
                    "source_ids": ["S002"],
                },
            ],
            "organizations": [
                {"org_id": 2, "name": "辽阳县人民政府", "type": "政府",
                 "level": "县处级", "location": "辽宁省辽阳市辽阳县"},
                {"org_id": 1, "name": "中共辽阳县委员会", "type": "党委",
                 "level": "县处级", "location": "辽宁省辽阳市辽阳县"},
            ],
            "relationships": [
                {"person": "王浩", "person_id": "liaoyangxian_王浩",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "县长与县委书记党政主要领导搭档",
                 "overlap_org": "中共辽阳县委员会/辽阳县人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001", "S002"]},
                {"person": "张福海", "person_id": "liaoyangxian_张福海",
                 "relationship_type": "overlap", "strength": "medium",
                 "evidence": "县长与县委副书记；县领导班子同事",
                 "overlap_org": "中共辽阳县委员会",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S002", "S003"]},
                {"person": "关晟", "person_id": "liaoyangxian_关晟",
                 "relationship_type": "overlap", "strength": "medium",
                 "evidence": "县长与县委常委",
                 "overlap_org": "中共辽阳县委员会",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S003"]},
            ],
            "governance_record": [
                {
                    "period": "2026年7月",
                    "domain": "other",
                    "achievement_or_event": "主持召开县政府党组、常务会议，传达学习习近平总书记重要讲话精神、部署节能降碳工作",
                    "role_in_event": "县长，主持",
                    "measurable_outcome": "部署县政府系统贯彻习近平总书记七一讲话、节能降碳等工作",
                    "location": "辽阳县",
                    "confidence": "confirmed",
                    "source_ids": ["S002"],
                },
                {
                    "period": "2026年6月",
                    "domain": "public_security",
                    "achievement_or_event": "检查节前安全生产工作",
                    "role_in_event": "县长，检查督导",
                    "measurable_outcome": "督促节前安全生产落实",
                    "location": "辽阳县",
                    "confidence": "confirmed",
                    "source_ids": ["S003"],
                },
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["government", "party"],
                "geographic_pattern": ["辽阳市"],
                "promotion_velocity": {
                    "summary": "公开源不足，无法精确分析晋升速度",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "unknown",
                        "evidence": "公开报道以政务会议为主，暂不足以判断工作风格",
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
                "identity": "plausible",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": "田相宇的完整履历（出生年月、籍贯、教育背景、任县长前的职业生涯）均未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "田相宇的出生年月、籍贯、毕业院校？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["田相宇 简历 辽阳县", "田相宇 辽阳"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "田相宇何时开始担任辽阳县县长？此前担任什么职务？",
                    "why_it_matters": "理清履职起始时间和职业生涯全貌",
                    "suggested_queries": ["田相宇 任 辽阳县 县长 任职公示"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "田相宇的完整职业生涯履历？",
                    "why_it_matters": "评估专业背景和职业发展路径",
                    "suggested_queries": ["田相宇 工作 经历"],
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
        ("县委书记", "王浩"),
        ("县长", "田相宇"),
    ]

    for job, name in person_configs:
        data = generate_person_json(job, name)
        if data:
            fname = f"{TODAY}-辽宁省-辽阳市-{job}-{name}.json"
            fpath = PERSONS_DIR / fname
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  Wrote {fpath}")

    print(f"\nDone. Output files:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Person JSONs in: {PERSONS_DIR}")
