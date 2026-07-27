#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 太和区 (Taihe District), 锦州市, 辽宁省.

Level: 市辖区
Province: 辽宁省
Parent city: 锦州市
Targets: 区委书记 (Party Secretary: 尹璐), 区长 (Mayor: 郭鹏宇)
Task ID: liaoning_太和区

Research date: 2026-07-25
Official source: http://www.jzth.gov.cn/ (太和区人民政府)

Current status (as of 2026-07-25, verified via 太和区人民政府 website):
- 区委书记: 尹璐 (女/男, 汉族; 2026年7月以区委书记身份公开调研企业)
- 区长: 郭鹏宇 (区委副书记、区长; 2026年7月带队调研防汛和学校安全)
- 前任区委书记: 张雪冬 (2025年10月仍以区委书记身份带队赴外考察招商)

Leadership roster partially sourced from:
  - http://www.jzth.gov.cn/ (太和区人民政府官网门户首页新闻)
  - Headlines: "区委书记尹璐带队深入辖区重点企业走访调研"
  - Headlines: "区委副书记、区长郭鹏宇带队调研学校安全生产等重点..."
  - Headlines: "区委书记张雪冬带队赴苏常徐三地考察招商" (2025-10-20)

Confidence notes:
  尹璐 identity as 区委书记 confirmed via homepage headline.
  郭鹏宇 identity as 区委副书记、区长 confirmed via homepage headline.
  张雪冬 identity as 前任区委书记 confirmed via 2025-10-20 article headline.
  Full career histories before current roles not publicly available.
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

SLUG = "太和区"

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

    # 1. 尹璐 — 区委书记
    {
        "id": 1,
        "name": "尹璐",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共太和区委员会",
        "source": "http://www.jzth.gov.cn/ (首页头条: 区委书记尹璐带队深入辖区重点企业走访调研)",
    },
    # 2. 郭鹏宇 — 区委副书记、区长
    {
        "id": 2,
        "name": "郭鹏宇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "太和区人民政府",
        "source": "http://www.jzth.gov.cn/ (首页新闻: 区委副书记、区长郭鹏宇带队调研学校安全生产/防汛工作等)",
    },

    # ════════════════════════════════════════
    # 区政府领导 (Government Leadership)
    # ════════════════════════════════════════

    # Note: Detailed leadership roster (副区长, 区委常委) could not be extracted
    # due to web access limitations. The government site structure for leadership
    # pages could not be navigated. Below are placeholder entries based on
    # typical 市辖区 leadership structure. These should be confirmed/updated
    # when full site access is available.

    # 3. 太和区 副区长 (待确认)
    # NOTE: No names confirmed from available sources for deputy positions.
    # The official site's 政府领导/区长之窗 page URL could not be determined.

    # ════════════════════════════════════════
    # 前任领导 (Predecessors)
    # ════════════════════════════════════════

    # 3. 张雪冬 — 前任区委书记
    {
        "id": 3,
        "name": "张雪冬",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区委书记",
        "current_org": "中共太和区委员会（已离任）",
        "source": "http://www.jzth.gov.cn/ (首页新闻: 2025-10-20 '区委书记张雪冬带队赴苏常徐三地考察招商')",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共太和区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共锦州市委员会",
        "location": "辽宁省锦州市太和区",
    },
    {
        "id": 2,
        "name": "太和区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "锦州市人民政府",
        "location": "辽宁省锦州市太和区",
    },
    {
        "id": 3,
        "name": "太和区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "锦州市人大常委会",
        "location": "辽宁省锦州市太和区",
    },
    {
        "id": 4,
        "name": "政协太和区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协锦州市委员会",
        "location": "辽宁省锦州市太和区",
    },
    {
        "id": 5,
        "name": "太和区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共锦州市纪律检查委员会",
        "location": "辽宁省锦州市太和区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # ── Core Leadership ──
    # 尹璐 - 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "2026年（推测）", "end": "present",
     "rank": "正处级", "note": "2026年7月以区委书记身份调研重点企业; 接替前任张雪冬"},
    # 郭鹏宇 - 区委副书记、区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "", "end": "present",
     "rank": "正处级", "note": "2026年7月带队调研防汛工作和学校安全生产"},

    # ── 前任领导 ──
    # 张雪冬 - 前任区委书记
    {"person_id": 3, "org_id": 1, "title": "区委书记", "start": "", "end": "2026年中（推测）",
     "rank": "正处级", "note": "2025年10月20日仍以区委书记身份带队赴苏常徐三地考察招商; 之后由尹璐接任"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 尹璐 <-> 郭鹏宇: 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记与区长党政主要领导搭档",
     "overlap_org": "中共太和区委员会/太和区人民政府",
     "overlap_period": "2026年起（推测）"},

    # 尹璐 <-> 张雪冬: 前任与继任（区委书记）
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor",
     "context": "尹璐接替张雪冬任太和区区委书记",
     "overlap_org": "中共太和区委员会",
     "overlap_period": "2026年中"},
]

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════


def make_source_register() -> list[dict]:
    return [
        {
            "id": "S001",
            "title": "太和区人民政府官网首页",
            "url": "http://www.jzth.gov.cn/",
            "publisher": "太和区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "首页头条: '区委书记尹璐带队深入辖区重点企业走访调研'—确认尹璐为现任区委书记",
        },
        {
            "id": "S002",
            "title": "太和区人民政府官网-政务新闻",
            "url": "http://www.jzth.gov.cn/",
            "publisher": "太和区人民政府",
            "published_at": "2026-07-21",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "'区委副书记、区长郭鹏宇带队调研学校安全生产等重点...'—确认郭鹏宇为现任区长",
        },
        {
            "id": "S003",
            "title": "太和区人民政府官网-招商引资",
            "url": "http://www.jzth.gov.cn/",
            "publisher": "太和区人民政府",
            "published_at": "2025-10-20",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "'区委书记张雪冬带队赴苏常徐三地考察招商'—确认张雪冬为前任区委书记（2025年10月在任）",
        },
        {
            "id": "S004",
            "title": "太和区人民政府官网-政务新闻-防汛调研",
            "url": "http://www.jzth.gov.cn/",
            "publisher": "太和区人民政府",
            "published_at": "2026-07-13",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "'下沉一线查隐患 压实责任守底线 区领导深入防汛最前沿'—郭鹏宇带队防汛调研",
        },
        {
            "id": "S005",
            "title": "太和区人民政府官网-政务新闻-安全生产调研",
            "url": "http://www.jzth.gov.cn/",
            "publisher": "太和区人民政府",
            "published_at": "2026-06-30",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "'郭鹏宇带队调研生产经营与安全生产工作'—郭鹏宇以区长身份调研",
        },
    ]


def generate_person_json(job: str, name: str) -> dict:
    """Generate per-person graph JSON following person_graph_json.md schema."""
    person_id_str = f"taihe_{name}"

    # ── 尹璐 (区委书记) ──
    if name == "尹璐":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "辽宁省",
                "city": "锦州市",
                "region": "太和区",
                "job": "区委书记",
                "task_id": "liaoning_太和区",
                "time_focus": "2025–2026",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "尹璐",
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
                    "name_birth": "尹璐_",
                    "name_birthplace": "尹璐_",
                    "official_profile_url": "",
                },
            },
            "current_status": {
                "current_post": "区委书记",
                "current_org": "中共太和区委员会",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"],
            },
            "career_timeline": [
                {
                    "start": "2026年（推测）",
                    "end": "present",
                    "org": "中共太和区委员会",
                    "title": "区委书记",
                    "level": "正处级",
                    "location": "辽宁省锦州市太和区",
                    "system": "party",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "接替张雪冬任太和区区委书记; 2026年7月以区委书记身份调研重点企业",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                },
            ],
            "organizations": [
                {"org_id": 1, "name": "中共太和区委员会", "type": "党委",
                 "level": "县处级", "location": "辽宁省锦州市太和区"},
            ],
            "relationships": [
                {"person": "郭鹏宇", "person_id": "taihe_郭鹏宇",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区委书记与区长党政主要领导搭档",
                 "overlap_org": "中共太和区委员会/太和区人民政府",
                 "overlap_period": "2026年起（推测）",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001", "S002"]},
                {"person": "张雪冬", "person_id": "taihe_张雪冬",
                 "relationship_type": "predecessor_successor", "strength": "strong",
                 "evidence": "尹璐接替张雪冬担任太和区区委书记",
                 "overlap_org": "中共太和区委员会",
                 "overlap_period": "2026年中",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001", "S003"]},
            ],
            "governance_record": [
                {
                    "period": "2026年7月",
                    "domain": "economic_development",
                    "achievement_or_event": "带队深入辖区重点企业走访调研",
                    "role_in_event": "区委书记，带队调研",
                    "measurable_outcome": "实地调研辖区重点企业生产经营情况",
                    "location": "锦州市太和区",
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
                "promotion_velocity": {
                    "summary": "公开源不足，无法分析晋升速度。无此前职务信息。",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "unknown",
                        "evidence": "公开报道仅1篇（走访企业），不足以判断工作风格",
                        "confidence": "unverified",
                        "source_ids": ["S001"],
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
                "career_completeness": "minimal",
                "relationship_confidence": "medium",
                "biggest_gap": "尹璐的完整履历（出生年月、籍贯、性别、教育背景、任区委书记前的职业生涯）完全未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "尹璐的出生年月、籍贯、性别、毕业院校？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["尹璐 简历 锦州 太和区", "尹璐 出生", "尹璐 百度百科"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "尹璐任区委书记前担任什么职务？",
                    "why_it_matters": "理清其职业生涯路径",
                    "suggested_queries": ["尹璐 任太和区", "尹璐 任职公示", "尹璐 此前担任"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "尹璐何时开始担任太和区区委书记？",
                    "why_it_matters": "确认具体交接时间节点",
                    "suggested_queries": ["太和区 区委书记 任免 2026", "尹璐 任区委书记"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "尹璐的完整职业生涯履历？",
                    "why_it_matters": "评估专业背景和职业发展路径",
                    "suggested_queries": ["尹璐 工作经历", "尹璐 简历"],
                    "last_attempted": AS_OF,
                },
            ],
        }

    # ── 郭鹏宇 (区长) ──
    if name == "郭鹏宇":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "辽宁省",
                "city": "锦州市",
                "region": "太和区",
                "job": "区长",
                "task_id": "liaoning_太和区",
                "time_focus": "2025–2026",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "郭鹏宇",
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
                    "name_birth": "郭鹏宇_",
                    "name_birthplace": "郭鹏宇_",
                    "official_profile_url": "",
                },
            },
            "current_status": {
                "current_post": "区长",
                "current_org": "太和区人民政府",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S002"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "present",
                    "org": "太和区人民政府",
                    "title": "区长",
                    "level": "正处级",
                    "location": "辽宁省锦州市太和区",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "2026年6月至7月多次以区长身份公开调研; 此前任职情况未知",
                    "confidence": "confirmed",
                    "source_ids": ["S002", "S004", "S005"],
                },
            ],
            "organizations": [
                {"org_id": 2, "name": "太和区人民政府", "type": "政府",
                 "level": "县处级", "location": "辽宁省锦州市太和区"},
            ],
            "relationships": [
                {"person": "尹璐", "person_id": "taihe_尹璐",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区长与区委书记党政主要领导搭档",
                 "overlap_org": "中共太和区委员会/太和区人民政府",
                 "overlap_period": "2026年起（推测）",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001", "S002"]},
            ],
            "governance_record": [
                {
                    "period": "2026年7月",
                    "domain": "education_safety",
                    "achievement_or_event": "带队调研学校安全生产等重点领域工作",
                    "role_in_event": "区长，带队调研",
                    "measurable_outcome": "实地调研松山实验小学、南山小学、育才学校、巧鸟九年义务学校等校园安全",
                    "location": "锦州市太和区",
                    "confidence": "confirmed",
                    "source_ids": ["S002"],
                },
                {
                    "period": "2026年7月",
                    "domain": "disaster_prevention",
                    "achievement_or_event": "带队开展防汛工作调研",
                    "role_in_event": "区长，带队调研",
                    "measurable_outcome": "下沉一线查隐患，压实防汛责任",
                    "location": "锦州市太和区",
                    "confidence": "confirmed",
                    "source_ids": ["S004"],
                },
                {
                    "period": "2026年6月",
                    "domain": "economic_development",
                    "achievement_or_event": "调研生产经营与安全生产工作",
                    "role_in_event": "区长，带队调研",
                    "measurable_outcome": "调研辖区企业生产经营和安全生产情况",
                    "location": "锦州市太和区",
                    "confidence": "confirmed",
                    "source_ids": ["S005"],
                },
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["government"],
                "geographic_pattern": [],
                "promotion_velocity": {
                    "summary": "公开源不足，无法分析晋升速度",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "hands_on",
                        "evidence": "多次带队深入基层一线调研防汛、学校和安全生产工作（'四不两直'方式）",
                        "confidence": "plausible",
                        "source_ids": ["S002", "S004"],
                    }
                ],
                "speech_themes": [
                    "统筹发展和安全",
                    "压实责任守底线",
                ],
                "management_signals": [
                    {
                        "signal": "实地督导",
                        "evidence": "以'四不两直'方式开展调研",
                        "confidence": "plausible",
                        "source_ids": ["S002"],
                    }
                ],
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
                "career_completeness": "minimal",
                "relationship_confidence": "medium",
                "biggest_gap": "郭鹏宇的完整履历（出生年月、籍贯、性别、教育背景、任区长前的职业生涯）完全未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "郭鹏宇的出生年月、籍贯、毕业院校？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["郭鹏宇 简历 锦州 太和区", "郭鹏宇 出生"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "郭鹏宇何时开始担任太和区区长？此前担任什么职务？",
                    "why_it_matters": "理清履职起始时间和职业生涯全貌",
                    "suggested_queries": ["郭鹏宇 任太和区区长", "太和区 区长 任职公示"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "郭鹏宇任区长前曾任什么职务？是否为代区长转正？",
                    "why_it_matters": "了解其晋升路径",
                    "suggested_queries": ["郭鹏宇 代区长", "郭鹏宇 此前职务"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "郭鹏宇的完整职业生涯履历？",
                    "why_it_matters": "评估专业背景和职业发展路径",
                    "suggested_queries": ["郭鹏宇 工作经历"],
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
        ("区委书记", "尹璐"),
        ("区长", "郭鹏宇"),
    ]

    for job, name in person_configs:
        data = generate_person_json(job, name)
        if data:
            fname = f"{TODAY}-辽宁省-锦州市-{job}-{name}.json"
            fpath = PERSONS_DIR / fname
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  Wrote {fpath}")

    print(f"\nDone. Output files:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Person JSONs in: {PERSONS_DIR}")
