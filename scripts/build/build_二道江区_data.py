#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 二道江区 (Erdaojiang District), 通化市, 吉林省.

Level: 市辖区
Province: 吉林省
Parent city: 通化市
Targets: 区委书记 (Party Secretary: 张峰), 区长 (Mayor: 班兆龙)
Task ID: jilin_二道江区

Research date: 2026-07-25
Official source: http://www.edj.gov.cn/ (二道江区人民政府)

Current status (as of 2026-07-25, verified via 二道江区人民政府 news articles):
- 区委书记: 张峰 (男，2026年5月以区委书记身份公开出席环保调研)
- 区委副书记、区长: 班兆龙 (2026年多次以区长身份主持区政府常务会议)
- 区人大常委会主任: 关宝峰
- 区政协主席: 王树东
- 区委常委、统战部部长: 徐薇翔
- 王坤 (参加张峰调研，具体职务待确认—可能是分管生态环境的副区长或区委办负责人)

Leadership roster sourced from:
  - http://www.edj.gov.cn/zfxx/yw/202605/t20260529_774423.html (张峰调研生态环境)
  - http://www.edj.gov.cn/zfxx/yw/202606/t20260609_775274.html (班兆龙主持区政府常务会议)
  - http://www.edj.gov.cn/zfxx/yw/202605/t20260519_773650.html (区委常委班子学习会: 张峰、关宝峰、班兆龙、王树东)
  - http://www.edj.gov.cn/zfxx/tpxw/202604/t20260424_771805.html (徐薇翔—区委常委、统战部部长)

Confidence notes:
  张峰 as 区委书记 confirmed via May 2026 news article.
  班兆龙 as 区委副书记、区长 confirmed via multiple June 2026 meeting reports.
  关宝峰 as 区人大常委会主任 and 王树东 as 区政协主席 confirmed via April-May 2026 news articles.
  徐薇翔 as 区委常委、统战部部长 confirmed via March 2026 article.
  Full career histories before current roles not publicly available on government website.
  Government website (edj.gov.cn) does not have a dedicated 领导之窗/领导分工 page.
  Web search tools (Exa, Baidu, Google, Jina Reader) were rate-limited or timed out during this investigation.
  Baidu Baike blocked by captcha.
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

SLUG = "二道江区"

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

    # 1. 张峰 — 区委书记
    {
        "id": 1,
        "name": "张峰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共二道江区委员会",
        "source": "http://www.edj.gov.cn/zfxx/yw/202605/t20260529_774423.html",
    },
    # 2. 班兆龙 — 区委副书记、区长
    {
        "id": 2,
        "name": "班兆龙",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "二道江区人民政府",
        "source": "http://www.edj.gov.cn/zfxx/yw/202606/t20260609_775274.html",
    },

    # ════════════════════════════════════════
    # 区级领导 (District Leadership)
    # ════════════════════════════════════════

    # 3. 关宝峰 — 区人大常委会主任
    {
        "id": 3,
        "name": "关宝峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "二道江区人大常委会",
        "source": "http://www.edj.gov.cn/zfxx/yw/202605/t20260519_773650.html",
    },
    # 4. 王树东 — 区政协主席
    {
        "id": 4,
        "name": "王树东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "政协二道江区委员会",
        "source": "http://www.edj.gov.cn/zfxx/yw/202605/t20260519_773650.html",
    },
    # 5. 徐薇翔 — 区委常委、统战部部长
    {
        "id": 5,
        "name": "徐薇翔",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、统战部部长",
        "current_org": "中共二道江区委员会",
        "source": "http://www.edj.gov.cn/zfxx/tpxw/202604/t20260424_771805.html",
    },
    # 6. 王坤 — 参加张峰调研（推定副区长或区委办负责人）
    {
        "id": 6,
        "name": "王坤",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（推定）副区长/区委办负责人",
        "current_org": "二道江区人民政府（推定）",
        "source": "http://www.edj.gov.cn/zfxx/yw/202605/t20260529_774423.html",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共二道江区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共通化市委员会",
        "location": "吉林省通化市二道江区",
    },
    {
        "id": 2,
        "name": "二道江区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "通化市人民政府",
        "location": "吉林省通化市二道江区",
    },
    {
        "id": 3,
        "name": "二道江区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "通化市人大常委会",
        "location": "吉林省通化市二道江区",
    },
    {
        "id": 4,
        "name": "政协二道江区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协通化市委员会",
        "location": "吉林省通化市二道江区",
    },
    {
        "id": 5,
        "name": "二道江区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共通化市纪律检查委员会",
        "location": "吉林省通化市二道江区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # ── Core Leadership ──
    # 张峰 - 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "", "end": "present",
     "rank": "正处级", "note": "2026年5月21日以区委书记身份赴三道江村调研生态环境工作"},

    # 班兆龙 - 区委副书记、区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "", "end": "present",
     "rank": "正处级", "note": "2026年6月8日以区委副书记、区长身份主持区政府常务会议"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "", "end": "present",
     "rank": "副处级", "note": "兼任区委副书记"},

    # ── 区级领导 ──
    # 关宝峰 - 区人大常委会主任
    {"person_id": 3, "org_id": 3, "title": "区人大常委会主任", "start": "", "end": "present",
     "rank": "正处级", "note": "2026年5月15日出席区委理论学习中心组集体学习"},

    # 王树东 - 区政协主席
    {"person_id": 4, "org_id": 4, "title": "区政协主席", "start": "", "end": "present",
     "rank": "正处级", "note": "2026年5月15日出席区委理论学习中心组集体学习"},

    # 徐薇翔 - 区委常委、统战部部长
    {"person_id": 5, "org_id": 1, "title": "区委常委、统战部部长", "start": "", "end": "present",
     "rank": "副处级", "note": "2026年3月31日在全区统战工作会议上讲话"},

    # 王坤 - 推定副区长或区委办负责人
    {"person_id": 6, "org_id": 2, "title": "（推定）副区长/区委办负责人", "start": "", "end": "present",
     "rank": "副处级/正科级", "note": "2026年5月21日陪同张峰调研生态环境; 具体职务待确认"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 张峰 <-> 班兆龙: 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记与区长党政主要领导搭档",
     "overlap_org": "中共二道江区委员会/二道江区人民政府",
     "overlap_period": "截至2026年7月"},

    # 张峰 <-> 关宝峰: 区委书记与人大主任
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "区委书记与区人大常委会主任; 区委中心组共同学习",
     "overlap_org": "中共二道江区委员会",
     "overlap_period": "截至2026年7月"},

    # 张峰 <-> 王树东: 区委书记与政协主席
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "区委书记与区政协主席; 区委中心组共同学习",
     "overlap_org": "中共二道江区委员会",
     "overlap_period": "截至2026年7月"},

    # 班兆龙 <-> 关宝峰: 区长与人大主任
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "区长与区人大常委会主任; 区委中心组共同学习",
     "overlap_org": "二道江区人民政府/二道江区人大常委会",
     "overlap_period": "截至2026年7月"},

    # 班兆龙 <-> 王树东: 区长与政协主席
    {"person_a": 2, "person_b": 4, "type": "overlap",
     "context": "区长与区政协主席; 区委中心组共同学习",
     "overlap_org": "二道江区人民政府/政协二道江区委员会",
     "overlap_period": "截至2026年7月"},

    # 张峰 <-> 徐薇翔: 区委书记与统战部长
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "区委书记与区委常委、统战部部长",
     "overlap_org": "中共二道江区委员会",
     "overlap_period": "截至2026年7月"},

    # 张峰 <-> 王坤: 区委书记与陪同调研干部
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "王坤陪同张峰调研生态环境",
     "overlap_org": "二道江区人民政府（推定）",
     "overlap_period": "截至2026年5月"},
]

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════


def make_source_register() -> list[dict]:
    return [
        {
            "id": "S001",
            "title": "二道江区人民政府-政务要闻-张峰调研生态环境工作",
            "url": "http://www.edj.gov.cn/zfxx/yw/202605/t20260529_774423.html",
            "publisher": "二道江区人民政府",
            "published_at": "2026-05-29",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认张峰为二道江区委书记（2026年5月21日调研）; 王坤参加调研",
        },
        {
            "id": "S002",
            "title": "二道江区人民政府-政务要闻-区政府召开常务会议",
            "url": "http://www.edj.gov.cn/zfxx/yw/202606/t20260609_775274.html",
            "publisher": "二道江区人民政府",
            "published_at": "2026-06-09",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认班兆龙为区委副书记、区长（2026年6月8日）",
        },
        {
            "id": "S003",
            "title": "二道江区人民政府-政务要闻-区委常委班子学习会",
            "url": "http://www.edj.gov.cn/zfxx/yw/202605/t20260519_773650.html",
            "publisher": "二道江区人民政府",
            "published_at": "2026-05-19",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认张峰（区委书记）、关宝峰（区人大常委会主任）、班兆龙（区委副书记、区长）、王树东（区政协主席）",
        },
        {
            "id": "S004",
            "title": "二道江区人民政府-政务要闻-全区统战工作会议召开",
            "url": "http://www.edj.gov.cn/zfxx/tpxw/202604/t20260424_771805.html",
            "publisher": "二道江区人民政府",
            "published_at": "2026-04-24",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认徐薇翔为区委常委、统战部部长（2026年3月31日讲话）",
        },
        {
            "id": "S005",
            "title": "二道江区人民政府-政务要闻-树立和践行正确政绩观学习教育读书班",
            "url": "http://www.edj.gov.cn/zfxx/yw/202604/t20260415_770886.html",
            "publisher": "二道江区人民政府",
            "published_at": "2026-04-15",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "张峰作开班动员; 关宝峰、班兆龙、王树东出席",
        },
        {
            "id": "S006",
            "title": "二道江区人民政府-政务要闻-区政府召开常务会议（第2次）",
            "url": "http://www.edj.gov.cn/zfxx/yw/202604/t20260407_769961.html",
            "publisher": "二道江区人民政府",
            "published_at": "2026-04-07",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "班兆龙以区委副书记、区长身份主持区政府第2次常务会议",
        },
        {
            "id": "S007",
            "title": "二道江区人民政府-政务要闻-区政府召开常务会议（第3次）",
            "url": "http://www.edj.gov.cn/zfxx/yw/202604/t20260430_772283.html",
            "publisher": "二道江区人民政府",
            "published_at": "2026-04-30",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "班兆龙以区委副书记、区长身份主持区政府第3次常务会议",
        },
    ]


def generate_person_json(job: str, name: str) -> dict:
    """Generate per-person graph JSON following person_graph_json.md schema."""
    person_id_str = f"erdaojiang_{name}"

    # ── 张峰 (区委书记) ──
    if name == "张峰":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "吉林省",
                "city": "通化市",
                "region": "二道江区",
                "job": "区委书记",
                "task_id": "jilin_二道江区",
                "time_focus": "2026",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "张峰",
                "aliases": [],
                "gender": "男",
                "ethnicity": "",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "张峰_",
                    "name_birthplace": "张峰_",
                    "official_profile_url": "",
                },
            },
            "current_status": {
                "current_post": "区委书记",
                "current_org": "中共二道江区委员会",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "present",
                    "org": "中共二道江区委员会",
                    "title": "区委书记",
                    "level": "正处级",
                    "location": "吉林省通化市二道江区",
                    "system": "party",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "2026年5月21日以区委书记身份公开调研生态环境; 当前仍为区委书记",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                },
            ],
            "organizations": [
                {"org_id": 1, "name": "中共二道江区委员会", "type": "党委",
                 "level": "县处级", "location": "吉林省通化市二道江区"},
            ],
            "relationships": [
                {"person": "班兆龙", "person_id": "erdaojiang_班兆龙",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区委书记与区长党政主要领导搭档，共同出席区委理论学习中心组会议",
                 "overlap_org": "中共二道江区委员会/二道江区人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S001", "S002", "S003"]},
                {"person": "关宝峰", "person_id": "erdaojiang_关宝峰",
                 "relationship_type": "overlap", "strength": "medium",
                 "evidence": "区委书记与区人大常委会主任，共同出席区委理论学习中心组会议",
                 "overlap_org": "中共二道江区委员会",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S003"]},
                {"person": "王树东", "person_id": "erdaojiang_王树东",
                 "relationship_type": "overlap", "strength": "medium",
                 "evidence": "区委书记与区政协主席，共同出席区委理论学习中心组会议",
                 "overlap_org": "中共二道江区委员会",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S003"]},
                {"person": "徐薇翔", "person_id": "erdaojiang_徐薇翔",
                 "relationship_type": "superior_subordinate", "strength": "medium",
                 "evidence": "区委书记与区委常委、统战部部长",
                 "overlap_org": "中共二道江区委员会",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S004"]},
            ],
            "governance_record": [
                {
                    "period": "2026年4-5月",
                    "domain": "environment",
                    "achievement_or_event": "调研二道江区生态环境工作，推进钢渣堆生态修复等历史遗留问题整改",
                    "role_in_event": "区委书记，带队调研",
                    "measurable_outcome": "实地查看三道江村东平沟等重点点位，强调环保问题闭环整改",
                    "location": "通化市二道江区",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                },
                {
                    "period": "2026年4月",
                    "domain": "other",
                    "achievement_or_event": "作树立和践行正确政绩观学习教育读书班开班动员和专题辅导",
                    "role_in_event": "区委书记，开班主讲",
                    "measurable_outcome": "提出聚焦产业转型升级、服务通钢发展、培育医药健康等特色产业",
                    "location": "通化市二道江区",
                    "confidence": "confirmed",
                    "source_ids": ["S005"],
                },
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["party"],
                "geographic_pattern": ["通化市"],
                "promotion_velocity": {
                    "summary": "公开源不足，无法分析晋升速度",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "environment_oriented",
                        "evidence": "亲自调研生态环境工作，强调环保问题闭环整改和高质量发展",
                        "confidence": "plausible",
                        "source_ids": ["S001"],
                    },
                    {
                        "trait": "discipline_oriented",
                        "evidence": "正确政绩观读书班上强调纠治政绩观偏差、常态化警示教育",
                        "confidence": "plausible",
                        "source_ids": ["S005"],
                    },
                ],
                "speech_themes": [
                    "生态优先", "高质量发展", "正确政绩观", "民生福祉",
                ],
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
                "biggest_gap": "张峰的完整履历（出生年月、籍贯、教育背景、职业生涯全貌）均未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "张峰的出生年月、籍贯、毕业院校？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["张峰 通化 二道江 简历", "张峰 出生"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "张峰何时开始担任二道江区委书记？此前担任什么职务？",
                    "why_it_matters": "理清履职起始时间和职业生涯全貌",
                    "suggested_queries": ["张峰 任 二道江区 区委书记", "张峰 任职公示", "张峰 简历 通化"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "二道江区前任区委书记是谁？去向如何？",
                    "why_it_matters": "党政交接与人事变动分析",
                    "suggested_queries": ["二道江区 前任 区委书记", "二道江区 区委书记 任免 2025"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "张峰的完整职业生涯履历？",
                    "why_it_matters": "评估专业背景和职业发展路径",
                    "suggested_queries": ["张峰 工作 经历 通化"],
                    "last_attempted": AS_OF,
                },
            ],
        }

    # ── 班兆龙 (区长) ──
    if name == "班兆龙":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "吉林省",
                "city": "通化市",
                "region": "二道江区",
                "job": "区长",
                "task_id": "jilin_二道江区",
                "time_focus": "2026",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "班兆龙",
                "aliases": [],
                "gender": "男",
                "ethnicity": "",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "班兆龙_",
                    "name_birthplace": "班兆龙_",
                    "official_profile_url": "",
                },
            },
            "current_status": {
                "current_post": "区长",
                "current_org": "二道江区人民政府",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S002"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "present",
                    "org": "二道江区人民政府",
                    "title": "区长",
                    "level": "正处级",
                    "location": "吉林省通化市二道江区",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "2026年多次以区委副书记、区长身份主持区政府常务会议",
                    "confidence": "confirmed",
                    "source_ids": ["S002", "S006", "S007"],
                },
            ],
            "organizations": [
                {"org_id": 2, "name": "二道江区人民政府", "type": "政府",
                 "level": "县处级", "location": "吉林省通化市二道江区"},
                {"org_id": 1, "name": "中共二道江区委员会", "type": "党委",
                 "level": "县处级", "location": "吉林省通化市二道江区"},
            ],
            "relationships": [
                {"person": "张峰", "person_id": "erdaojiang_张峰",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区长与区委书记党政主要领导搭档",
                 "overlap_org": "中共二道江区委员会/二道江区人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S003"]},
                {"person": "关宝峰", "person_id": "erdaojiang_关宝峰",
                 "relationship_type": "overlap", "strength": "medium",
                 "evidence": "区长与区人大常委会主任",
                 "overlap_org": "二道江区人民政府/二道江区人大常委会",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S003"]},
                {"person": "王树东", "person_id": "erdaojiang_王树东",
                 "relationship_type": "overlap", "strength": "medium",
                 "evidence": "区长与区政协主席",
                 "overlap_org": "二道江区人民政府/政协二道江区委员会",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S003"]},
            ],
            "governance_record": [
                {
                    "period": "2026年",
                    "domain": "other",
                    "achievement_or_event": "主持多次区政府常务会议，部署防汛备汛、生态环保督察整改、经济运行、安全生产等工作",
                    "role_in_event": "区长，主持会议",
                    "measurable_outcome": "安排『十五五』规划分工、重点企业项目包保、春耕备耕、森林防火等工作",
                    "location": "通化市二道江区",
                    "confidence": "confirmed",
                    "source_ids": ["S002", "S006", "S007"],
                },
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["government", "party"],
                "geographic_pattern": ["通化市"],
                "promotion_velocity": {
                    "summary": "公开源不足，无法分析晋升速度",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "pragmatic",
                        "evidence": "多次主持常务会议部署具体工作，涉及防汛、经济、安全、乡村振兴等务实议题",
                        "confidence": "plausible",
                        "source_ids": ["S002", "S006", "S007"],
                    }
                ],
                "speech_themes": [
                    "安全生产", "生态环保", "经济稳增长", "乡村振兴",
                ],
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
                "biggest_gap": "班兆龙的完整履历（出生年月、籍贯、教育背景、任区长前的职业生涯）均未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "班兆龙的出生年月、籍贯、毕业院校？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["班兆龙 通化 简历", "班兆龙 二道江区"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "班兆龙何时开始担任二道江区区长？此前担任什么职务？",
                    "why_it_matters": "理清履职起始时间和前序岗位",
                    "suggested_queries": ["班兆龙 任 二道江区 区长", "班兆龙 任职公示"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "二道江区前任区长是谁？去向如何？",
                    "why_it_matters": "党政交接与人事变动分析",
                    "suggested_queries": ["二道江区 前任 区长", "二道江区 区长 任免"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "班兆龙的完整职业生涯履历？",
                    "why_it_matters": "评估专业背景和职业发展路径",
                    "suggested_queries": ["班兆龙 工作 经历"],
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
        ("区委书记", "张峰"),
        ("区长", "班兆龙"),
    ]

    for job, name in person_configs:
        data = generate_person_json(job, name)
        if data:
            fname = f"{TODAY}-吉林省-通化市-{job}-{name}.json"
            fpath = PERSONS_DIR / fname
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  Wrote {fpath}")

    print(f"\nDone. Output files:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Person JSONs in: {PERSONS_DIR}")
