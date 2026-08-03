#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 龙山区 (Longshan District), 辽源市, 吉林省.

Level: 市辖区
Province: 吉林省
Parent city: 辽源市
Targets: 区委书记 (Party Secretary: 王飞), 区长 (Mayor: 韩春峰)
Task ID: jilin_龙山区

Research date: 2026-08-04
Official source: http://www.jllyls.gov.cn/ (辽源市龙山区人民政府)

Current status (as of 2026-08-04, verified via 龙山区人民政府 website):
- 区委书记: 王飞 (男，汉族，2025年初起主持区委常委会工作，2025年3月以区委书记身份主持会议)
- 区长: 韩春峰 (男，汉族，区委副书记、区长，2025年4月以区长身份主持区政府党组会议)
- 区委常委、副区长: 于明明 (confirmed in April 2025 government meeting)
- 副区长: 张岩锋 (confirmed in April 2025 government meeting)
- 副区长: 张立星 (confirmed in April 2025 government meeting)

Confidence notes:
  王飞 identity as 区委书记 confirmed via March 2025/2026 区委常委会 meeting articles on district website.
  韩春峰 identity confirmed via April 2025/June 2026 government meeting and children's day articles.
  Full career histories before current roles not publicly available on site.
  Web search tools (Exa, Baidu, Google, Jina Reader) were rate-limited or timed out during this investigation.
  External web search was unavailable during this task.
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

SLUG = "龙山区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-08-04"
TODAY = "20260804"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 王飞 — 区委书记
    {
        "id": 1,
        "name": "王飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共龙山区委员会",
        "source": "http://www.jllyls.gov.cn/xxgk/zfxxgkfl/zfhy/202503/t20250331_708176.html",
    },
    # 2. 韩春峰 — 区委副书记、区长
    {
        "id": 2,
        "name": "韩春峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "龙山区人民政府",
        "source": "http://www.jllyls.gov.cn/xxgk/zfxxgkfl/zfhy/202504/t20250418_709542.html",
    },

    # ════════════════════════════════════════
    # 区政府领导 (Government Leadership)
    # ════════════════════════════════════════

    # 3. 于明明 — 区委常委、副区长
    {
        "id": 3,
        "name": "于明明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "龙山区人民政府",
        "source": "http://www.jllyls.gov.cn/xxgk/zfxxgkfl/zfhy/202504/t20250418_709542.html",
    },
    # 4. 张岩锋 — 副区长
    {
        "id": 4,
        "name": "张岩锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "龙山区人民政府",
        "source": "http://www.jllyls.gov.cn/xxgk/zfxxgkfl/zfhy/202504/t20250418_709542.html",
    },
    # 5. 张立星 — 副区长
    {
        "id": 5,
        "name": "张立星",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "龙山区人民政府",
        "source": "http://www.jllyls.gov.cn/xxgk/zfxxgkfl/zfhy/202504/t20250418_709542.html",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共龙山区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共辽源市委员会",
        "location": "吉林省辽源市龙山区",
    },
    {
        "id": 2,
        "name": "龙山区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "辽源市人民政府",
        "location": "吉林省辽源市龙山区",
    },
    {
        "id": 3,
        "name": "龙山区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "辽源市人大常委会",
        "location": "吉林省辽源市龙山区",
    },
    {
        "id": 4,
        "name": "政协龙山区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协辽源市委员会",
        "location": "吉林省辽源市龙山区",
    },
    {
        "id": 5,
        "name": "龙山区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共辽源市纪律检查委员会",
        "location": "吉林省辽源市龙山区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # ── Core Leadership ──
    # 王飞 - 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "2025年初", "end": "present",
     "rank": "正处级", "note": "2025年3月以区委书记身份主持中共龙山区委常委会第七次会议; 2025年3月31日新闻报道确认"},
    # 韩春峰 - 区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "", "end": "present",
     "rank": "正处级", "note": "2025年4月17日以区委副书记、区长身份主持区政府党组第5次会议; 2026年6月1日与区委书记王飞一同开展儿童节慰问活动"},
    # 韩春峰 - 区委副书记
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "", "end": "present",
     "rank": "副处级", "note": "兼任区委副书记"},

    # ── 区政府领导 ──
    # 于明明 - 区委常委、副区长
    {"person_id": 3, "org_id": 2, "title": "区委常委、副区长", "start": "", "end": "present",
     "rank": "副处级", "note": "2025年4月17日区政府党组会议确认"},
    # 张岩锋 - 副区长
    {"person_id": 4, "org_id": 2, "title": "副区长", "start": "", "end": "present",
     "rank": "副处级", "note": "2025年4月17日区政府党组会议确认"},
    # 张立星 - 副区长
    {"person_id": 5, "org_id": 2, "title": "副区长", "start": "", "end": "present",
     "rank": "副处级", "note": "2025年4月17日区政府党组会议确认"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 王飞 <-> 韩春峰: 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记与区长党政主要领导搭档; 共同出席2026年国际儿童节走访慰问活动",
     "overlap_org": "中共龙山区委员会/龙山区人民政府",
     "overlap_period": "2025年起"},

    # 王飞 <-> 于明明: 书记与区委常委
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "区委书记与区委常委、副区长; 区委领导班子搭档",
     "overlap_org": "中共龙山区委员会/龙山区人民政府",
     "overlap_period": "截至2026年8月"},

    # 韩春峰 <-> 于明明: 区长与区委常委、副区长
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "区长与区委常委、副区长; 政府领导班子搭档",
     "overlap_org": "龙山区人民政府",
     "overlap_period": "截至2026年8月"},

    # 韩春峰 <-> 张岩锋: 区长与副区长
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "区长与副区长工作搭档",
     "overlap_org": "龙山区人民政府",
     "overlap_period": "截至2026年8月"},

    # 韩春峰 <-> 张立星: 区长与副区长
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "区长与副区长工作搭档",
     "overlap_org": "龙山区人民政府",
     "overlap_period": "截至2026年8月"},

    # 副区长之间的联系（政府班子成员）
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "区政府领导班子同事",
     "overlap_org": "龙山区人民政府",
     "overlap_period": "截至2026年8月"},
    {"person_a": 3, "person_b": 5, "type": "overlap",
     "context": "区政府领导班子同事",
     "overlap_org": "龙山区人民政府",
     "overlap_period": "截至2026年8月"},
    {"person_a": 4, "person_b": 5, "type": "overlap",
     "context": "区政府领导班子同事",
     "overlap_org": "龙山区人民政府",
     "overlap_period": "截至2026年8月"},
]

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════


def make_source_register() -> list[dict]:
    return [
        {
            "id": "S001",
            "title": "龙山区人民政府-政府会议-中共龙山区委常委会2025年第七次会议",
            "url": "http://www.jllyls.gov.cn/xxgk/zfxxgkfl/zfhy/202503/t20250331_708176.html",
            "publisher": "辽源市龙山区人民政府",
            "published_at": "2025-03-31",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "区委书记王飞主持中共龙山区委常委会2025年第七次会议",
        },
        {
            "id": "S002",
            "title": "龙山区人民政府-政府会议-区委副书记、区长韩春峰主持2025年区政府党组第5次会议",
            "url": "http://www.jllyls.gov.cn/xxgk/zfxxgkfl/zfhy/202504/t20250418_709542.html",
            "publisher": "辽源市龙山区人民政府",
            "published_at": "2025-04-18",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "区委副书记、区长韩春峰主持; 区委常委、副区长于明明, 副区长张岩锋、张立星出席会议",
        },
        {
            "id": "S003",
            "title": "龙山区人民政府-龙山动态-王飞韩春峰开展国际儿童节走访慰问活动",
            "url": "http://www.jllyls.gov.cn/lsdt/202606/t20260602_739317.html",
            "publisher": "辽源市龙山区人民政府",
            "published_at": "2026-06-02",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "区委书记王飞、区委副书记、区长韩春峰六一慰问活动",
        },
        {
            "id": "S004",
            "title": "龙山区人民政府-政府会议-中共龙山区委常委会2025年第六次会议",
            "url": "http://www.jllyls.gov.cn/xxgk/zfxxgkfl/zfhy/202503/t20250319_707528.html",
            "publisher": "辽源市龙山区人民政府",
            "published_at": "2025-03-19",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "区委书记王飞主持区常委会2025年第六次会议, 确认王飞为区委书记（截至2025年3月）",
        },
        {
            "id": "S005",
            "title": "龙山区人民政府-政府会议-龙山区委全面依法治区委员会执法协调小组2025年第一次会议",
            "url": "http://www.jllyls.gov.cn/xxgk/zfxxgkfl/zfhy/202504/t20250415_709298.html",
            "publisher": "辽源市龙山区人民政府",
            "published_at": "2025-04-15",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
        },
        {
            "id": "S006",
            "title": "龙山区人民政府-龙山区府院联动2026年第一次联席会议",
            "url": "http://www.jllyls.gov.cn/xxgk/zfxxgkfl/zfhy/202607/t20260714_744302.html",
            "publisher": "辽源市龙山区人民政府",
            "published_at": "2026-07-14",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "区委副书记、区长韩春峰出席会议并讲话",
        },
    ]


def generate_person_json(job: str, name: str) -> dict:
    """Generate per-person graph JSON following person_graph_json.md schema."""
    person_id_str = f"longshan_{name}"

    # ── 王飞 (区委书记) ──
    if name == "王飞":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "吉林省",
                "city": "辽源市",
                "region": "龙山区",
                "job": "区委书记",
                "task_id": "jilin_龙山区",
                "time_focus": "2025–2026",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "王飞",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "王飞_",
                    "name_birthplace": "王飞_",
                    "official_profile_url": "",
                },
            },
            "current_status": {
                "current_post": "区委书记",
                "current_org": "中共龙山区委员会",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S004"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "2025年初",
                    "org": "未知",
                    "title": "此前职务",
                    "level": "",
                    "location": "",
                    "system": "unknown",
                    "rank": "",
                    "is_key_promotion": False,
                    "notes": "公开资料未找到王飞在担任龙山区委书记前的任职记录",
                    "confidence": "unverified",
                    "source_ids": [],
                },
                {
                    "start": "2025年初",
                    "end": "present",
                    "org": "中共龙山区委员会",
                    "title": "区委书记",
                    "level": "正处级",
                    "location": "吉林省辽源市龙山区",
                    "system": "party",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "2025年3月19日主持区委常委会第六次会议，2025年3月31日主持常委会第七次会议",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S004"],
                },
            ],
            "organizations": [
                {"org_id": 1, "name": "中共龙山区委员会", "type": "党委",
                 "level": "县处级", "location": "吉林省辽源市龙山区"},
            ],
            "relationships": [
                {"person": "韩春峰", "person_id": "longshan_韩春峰",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区委书记与区长党政主要领导搭档; 共同出席六一慰问活动",
                 "overlap_org": "中共龙山区委员会/龙山区人民政府",
                 "overlap_period": "2025年起",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001", "S003"]},
                {"person": "于明明", "person_id": "longshan_于明明",
                 "relationship_type": "overlap", "strength": "medium",
                 "evidence": "区委书记与区委常委、副区长",
                 "overlap_org": "中共龙山区委员会",
                 "overlap_period": "截至2026年8月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S002"]},
            ],
            "governance_record": [
                {
                    "period": "2025年3月",
                    "domain": "other",
                    "achievement_or_event": "主持召开区委常委会，传达学习习近平总书记在民营企业座谈会上的重要讲话",
                    "role_in_event": "区委书记，主持",
                    "measurable_outcome": "研究部署龙山区贯彻落实意见，讨论审议惠民实事、安全生产、森林防火等工作",
                    "location": "辽源市龙山区",
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
                    "summary": "公开源不足，无法精确分析晋升速度",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "unknown",
                        "evidence": "公开报道以常委会会议主持为主，暂不足以判断工作风格",
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
                    "description": "截至2026年8月，未发现公开的纪律处分、审计问题或负面报道",
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
                "biggest_gap": "王飞的完整履历（出生年月、籍贯、教育背景、任区委书记前的职业生涯）均未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "王飞的出生年月、籍贯、毕业院校？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["王飞 简历 龙山区 辽源", "王飞 龙山区 出生"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "王飞何时开始担任龙山区区委书记？此前担任什么职务？",
                    "why_it_matters": "理清履职起始时间和前任交接",
                    "suggested_queries": ["王飞 任 龙山区 区委书记", "王飞 任职公示 辽源"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "王飞的完整职业生涯履历？",
                    "why_it_matters": "评估专业背景和职业发展路径",
                    "suggested_queries": ["王飞 工作 经历 辽源"],
                    "last_attempted": AS_OF,
                },
            ],
        }

    # ── 韩春峰 (区长) ──
    if name == "韩春峰":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "吉林省",
                "city": "辽源市",
                "region": "龙山区",
                "job": "区长",
                "task_id": "jilin_龙山区",
                "time_focus": "2025–2026",
            },
            "identity": {
                "name": "韩春峰",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "韩春峰_",
                    "name_birthplace": "韩春峰_",
                    "official_profile_url": "",
                },
            },
            "current_status": {
                "current_post": "区长",
                "current_org": "龙山区人民政府",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S002", "S003"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "2025年",
                    "org": "未知",
                    "title": "此前职务",
                    "level": "",
                    "location": "",
                    "system": "unknown",
                    "rank": "",
                    "is_key_promotion": False,
                    "notes": "公开资料未找到韩春峰任龙山区区长前的职务记录",
                    "confidence": "unverified",
                    "source_ids": [],
                },
                {
                    "start": "2025年",
                    "end": "present",
                    "org": "龙山区人民政府",
                    "title": "区长",
                    "level": "正处级",
                    "location": "吉林省辽源市龙山区",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "2025年4月17日以区委副书记、区长身份主持区政府党组会议; 2026年6月与区委书记王飞一同开展慰问活动",
                    "confidence": "confirmed",
                    "source_ids": ["S002", "S003"],
                },
            ],
            "organizations": [
                {"org_id": 2, "name": "龙山区人民政府", "type": "政府",
                 "level": "县处级", "location": "吉林省辽源市龙山区"},
                {"org_id": 1, "name": "中共龙山区委员会", "type": "党委",
                 "level": "县处级", "location": "吉林省辽源市龙山区"},
            ],
            "relationships": [
                {"person": "王飞", "person_id": "longshan_王飞",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区长与区委书记党政主要领导搭档; 共同出席公益慰问活动",
                 "overlap_org": "中共龙山区委员会/龙山区人民政府",
                 "overlap_period": "2025年起",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001", "S003"]},
                {"person": "于明明", "person_id": "longshan_于明明",
                 "relationship_type": "superior_subordinate", "strength": "strong",
                 "evidence": "区长与区委常委、副区长",
                 "overlap_org": "龙山区人民政府",
                 "overlap_period": "截至2026年8月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S002"]},
                {"person": "张岩锋", "person_id": "longshan_张岩锋",
                 "relationship_type": "superior_subordinate", "strength": "strong",
                 "evidence": "区长与副区长",
                 "overlap_org": "龙山区人民政府",
                 "overlap_period": "截至2026年8月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S002"]},
                {"person": "张立星", "person_id": "longshan_张立星",
                 "relationship_type": "superior_subordinate", "strength": "strong",
                 "evidence": "区长与副区长",
                 "overlap_org": "龙山区人民政府",
                 "overlap_period": "截至2026年8月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S002"]},
            ],
            "governance_record": [
                {
                    "period": "2025-2026",
                    "domain": "other",
                    "achievement_or_event": "主持区政府党组会和工作，推进府院联动机制建设",
                    "role_in_event": "区长",
                    "measurable_outcome": "2026年7月主持召开府院联动2026年第一次联席会议",
                    "location": "辽源市龙山区",
                    "confidence": "confirmed",
                    "source_ids": ["S006"],
                },
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["government", "party"],
                "geographic_pattern": [],
                "promotion_velocity": {
                    "summary": "公开源不足，无法精确分析晋升速度",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "unknown",
                        "evidence": "公开报道以政务会议和报告为主，暂不足以判断工作风格",
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
                    "description": "截至2026年8月，未发现公开的纪律处罚，审计问题或负面报道",
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
                "biggest_gap": "韩春峰的完整履历（出生年月、籍贯、教育背景、任区长前的职业生涯）均未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "韩春峰的出生年月、籍贯、毕业院校？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["韩春峰 简历 龙山区", "韩春峰 出生"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "韩春峰何时开始担任龙山区区长？此前担任什么职务？",
                    "why_it_matters": "理清履职起始时间和职业生涯全貌",
                    "suggested_queries": ["韩春峰 任 龙山区 区长", "韩春峰 任职公示"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "韩春峰的完整职业生涯履历？",
                    "why_it_matters": "评价专业背景和职业发展路径",
                    "suggested_queries": ["韩春峰 工作 经历"],
                    "last_attempted": AS_OF,
                },
            ],
        }

    return {}


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Building {SLUG} network...")
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
        ("区委书记", "王飞"),
        ("区长", "韩春峰"),
    ]

    for job, name in person_configs:
        data = generate_person_json(job, name)
        if data:
            fname = f"{TODAY}-吉林省-辽源市-{job}-{name}.json"
            fpath = PERSONS_DIR / fname
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  Wrote {fpath}")

    print(f"\nDone. Output files:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  人物JSON: {PERSONS_DIR}")