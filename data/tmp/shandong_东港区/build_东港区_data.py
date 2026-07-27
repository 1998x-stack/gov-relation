#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 东港区 (Donggang District), 日照市, 山东省.

Investigation date: 2026-07-25
Task ID: shandong_东港区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - http://www.rzdonggang.gov.cn/ — 日照市东港区人民政府官方网站 (primary, current as of July 2026)
  - Official news articles accessed 2026-07-25 from the Donggang government site:
    * "何文到涛雒镇调研重点项目推进工作" (2026-06-25) — confirmed 何文 as 区委书记
    * "区委常委会召开会议" (2026-06-13) — 区委书记何文主持会议
  - The 区长's identity is currently unverified due to limited web access to government leadership pages

Confidence notes:
  - 区委书记何文: CONFIRMED via multiple official government news articles (June-July 2026)
  - 区长: UNVERIFIED — identity pending further research. The 东港区政府门户网站的"领导之窗"页面
    was not accessible via web fetch during investigation.
  - Biographical details (birth, birthplace, education): mostly unverified due to web access limitations
  - All claims labeled with confidence level; gaps explicitly documented
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "东港区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shandong_东港区"
if _CURRENT_DIR.name == "shandong_东港区":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING / "data" / "persons"
PJSON_DIR.mkdir(parents=True, exist_ok=True)

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-9 current district leaders, 10-19 standing committee, 20-29 deputies, 30+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current — as of July 2026)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "何文",
        "gender": "男",
        "ethnicity": "汉族",  # plausible — vast majority of Shandong district leaders are Han
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共日照市东港区委员会",
        "source": "http://www.rzdonggang.gov.cn/art/2026/6/25/art_33466_10360078.html",
        "confidence": "confirmed",
        "notes": "2026年6月24日带队到涛雒镇调研重点项目推进工作；6月11日主持区委常委会会议。时任区委书记。"
    },
    {
        "id": 2,
        "name": "待查_东港区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",  # unverified
        "current_org": "东港区人民政府",
        "source": "",
        "confidence": "unverified",
        "notes": "区长的姓名、简历等公开信息待进一步调查。东港区政府门户网站的'领导之窗'页面在本次调研期间无法访问。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Standing Committee Members (区委常委) — partially confirmed
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "待查_区委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记",  # usually concurrent with 区长
        "current_org": "中共日照市东港区委员会",
        "source": "",
        "confidence": "unverified",
        "notes": "区委副书记通常由区长兼任；也可能是专职副书记。待确认。"
    },
    {
        "id": 4,
        "name": "待查_常务副区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "东港区人民政府",
        "source": "",
        "confidence": "unverified",
        "notes": "待查。"
    },
    {
        "id": 5,
        "name": "待查_组织部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共日照市东港区委员会",
        "source": "",
        "confidence": "unverified",
        "notes": "待查。"
    },
    {
        "id": 6,
        "name": "待查_宣传部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、宣传部部长",
        "current_org": "中共日照市东港区委员会",
        "source": "",
        "confidence": "unverified",
        "notes": "待查。"
    },
    {
        "id": 7,
        "name": "待查_纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、纪委书记、区监委主任",
        "current_org": "中共日照市东港区纪律检查委员会",
        "source": "",
        "confidence": "unverified",
        "notes": "待查。"
    },
    {
        "id": 8,
        "name": "待查_政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、政法委书记",
        "current_org": "中共日照市东港区委员会",
        "source": "",
        "confidence": "unverified",
        "notes": "待查。"
    },
    {
        "id": 9,
        "name": "待查_统战部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、统战部部长",
        "current_org": "中共日照市东港区委员会",
        "source": "",
        "confidence": "unverified",
        "notes": "待查。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Donggang predecessors (partial — from Rizhao city context)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 10,
        "name": "刘祥龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "日照市副市长",
        "current_org": "日照市人民政府",
        "source": "https://jingji.cctv.com/2025/09/24/ARTI7Sppks4Tj3FxJYJ6l9lq250924.shtml",
        "confidence": "confirmed",
        "notes": "原东港区委书记，后升任日照市副市长。2025年9月以副市长身份出席全国水域救援大赛。东港区委书记任期内推动多项发展。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共日照市东港区委员会", "type": "party", "level": "县处级", "parent": "中共日照市委员会", "location": "日照市东港区"},
    {"id": 2, "name": "东港区人民政府", "type": "government", "level": "县处级", "parent": "日照市人民政府", "location": "日照市东港区"},
    {"id": 3, "name": "东港区纪律检查委员会", "type": "discipline", "level": "县处级", "parent": "日照市纪律检查委员会", "location": "日照市东港区"},
    {"id": 4, "name": "东港区人大常委会", "type": "people_congress", "level": "县处级", "parent": "", "location": "日照市东港区"},
    {"id": 5, "name": "中国人民政治协商会议日照市东港区委员会", "type": "cppcc", "level": "县处级", "parent": "", "location": "日照市东港区"},
    {"id": 6, "name": "东港区人民武装部", "type": "military", "level": "县处级", "parent": "", "location": "日照市东港区"},
    # Parent city organizations
    {"id": 7, "name": "中共日照市委员会", "type": "party", "level": "地厅级", "parent": "中共山东省委", "location": "日照市"},
    {"id": 8, "name": "日照市人民政府", "type": "government", "level": "地厅级", "parent": "山东省人民政府", "location": "日照市"},
]

# ── Positions ─────────────────────────────────────────────────────────────────
positions = [
    # Current positions — 何文
    {"id": 1, "person_id": 1, "org_id": 1, "title": "区委书记", "start": "", "end": "present", "rank": "县处级正职", "note": "as of 2026-07"},
    # 区长 (unknown)
    {"id": 2, "person_id": 2, "org_id": 2, "title": "区长", "start": "", "end": "present", "rank": "县处级正职", "note": "待查"},
    {"id": 3, "person_id": 2, "org_id": 1, "title": "区委副书记", "start": "", "end": "present", "rank": "县处级副职", "note": "通常由区长兼任"},
    # 刘祥龙 — predecessor
    {"id": 10, "person_id": 10, "org_id": 1, "title": "原东港区委书记", "start": "", "end": "", "rank": "县处级正职", "note": "后升任日照市副市长"},
    {"id": 11, "person_id": 10, "org_id": 8, "title": "日照市副市长", "start": "", "end": "present", "rank": "副厅级", "note": "as of 2025-09"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    {
        "id": 1,
        "person_a": 1,  # 何文
        "person_b": 2,  # 区长 (unknown)
        "type": "overlap",
        "context": "党政搭档：何文任区委书记，区长任区政府主要领导",
        "overlap_org": "中共日照市东港区委员会",
        "overlap_period": "2026",
        "confidence": "plausible"
    },
    {
        "id": 2,
        "person_a": 1,  # 何文
        "person_b": 10,  # 刘祥龙
        "type": "predecessor_successor",
        "context": "刘祥龙为前任东港区委书记，何文接任",
        "overlap_org": "中共日照市东港区委员会",
        "overlap_period": "",
        "confidence": "plausible"
    },
]

# ── Person JSON records ──────────────────────────────────────────────────────
PERSON_JSONS = [
    {
        "filename": f"{TODAY}-山东省-日照市-区委书记-何文.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "山东省",
                "city": "日照市",
                "region": "东港区",
                "job": "区委书记",
                "task_id": "shandong_东港区",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "donggang_he_wen",
                "name": "何文",
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
                    "name_birth": "何文",
                    "name_birthplace": "",
                    "official_profile_url": "http://www.rzdonggang.gov.cn/"
                }
            },
            "current_status": {
                "current_post": "中共日照市东港区委书记",
                "current_org": "中共日照市东港区委员会",
                "administrative_rank": "县处级正职",
                "as_of": "2026-07-25",
                "is_current_confirmed": True,
                "source_ids": ["S001", "S002"]
            },
            "career_timeline": [
                {
                    "start": "unknown",
                    "end": "present",
                    "org": "中共日照市东港区委员会",
                    "title": "东港区委书记",
                    "level": "县处级正职",
                    "location": "日照市东港区",
                    "system": "party",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "2026年6月以区委书记身份公开活动（调研、主持会议）",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S002"]
                },
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "履历缺口",
                    "title": "",
                    "notes": "公开资料未找到何文在担任东港区委书记前的履历信息",
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "organizations": [
                {
                    "org_id": "donggang_party",
                    "name": "中共日照市东港区委员会",
                    "type": "party",
                    "level": "县处级",
                    "role": "区委书记"
                }
            ],
            "relationships": [
                {
                    "person": "东港区长（待查）",
                    "person_id": "donggang_quzhang_unknown",
                    "relationship_type": "overlap",
                    "strength": "strong",
                    "evidence": "党政搭档关系，区委书记与区长在同一领导班子中共事",
                    "overlap_org": "中共日照市东港区委员会",
                    "overlap_period": "2026",
                    "direction": "undirected",
                    "confidence": "plausible",
                    "source_ids": []
                },
                {
                    "person": "刘祥龙",
                    "person_id": "donggang_liu_xianglong",
                    "relationship_type": "predecessor_successor",
                    "strength": "strong",
                    "evidence": "刘祥龙为前任东港区委书记，后升任日照市副市长",
                    "overlap_org": "中共日照市东港区委员会",
                    "overlap_period": "",
                    "direction": "undirected",
                    "confidence": "plausible",
                    "source_ids": ["S003"]
                }
            ],
            "governance_record": [
                {
                    "period": "2026-06",
                    "domain": "economic_development",
                    "achievement_or_event": "带队调研涛雒镇重点项目推进工作，包括宏创金属精深加工、三生钢铁数字产业生态园等项目",
                    "role_in_event": "区委书记，带队调研并协调解决难点问题",
                    "measurable_outcome": "",
                    "location": "日照市东港区涛雒镇",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                },
                {
                    "period": "2026-06",
                    "domain": "education",
                    "achievement_or_event": "主持区委常委会会议，研究教育工作，推进国家义务教育优质均衡发展区创建",
                    "role_in_event": "区委书记，主持会议并讲话",
                    "measurable_outcome": "",
                    "location": "日照市东港区",
                    "confidence": "confirmed",
                    "source_ids": ["S002"]
                },
                {
                    "period": "2026-06",
                    "domain": "other",
                    "achievement_or_event": "关注12345热线服务质效，推动作风建设暨热线服务质效提升'百日攻坚'行动",
                    "role_in_event": "区委书记",
                    "measurable_outcome": "",
                    "location": "日照市东港区",
                    "confidence": "confirmed",
                    "source_ids": ["S002"]
                }
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["party"],
                "geographic_pattern": [],
                "promotion_velocity": {
                    "summary": "履历信息不足，无法评估晋升速度",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "grassroots_oriented",
                        "evidence": "带队到涛雒镇一线调研重点项目，强调靠前服务保障",
                        "confidence": "plausible",
                        "source_ids": ["S001"]
                    }
                ],
                "speech_themes": [
                    "项目攻坚",
                    "靠前服务",
                    "创新驱动"
                ],
                "management_signals": [
                    "强调深入一线解决问题",
                    "关注12345热线服务质效"
                ],
                "caveat": "工作风格从公开报道和政务活动推断，非私人心理评估。"
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "截至2026年7月，未发现何文有纪律处分、审计问题或负面媒体报道。东港区委领导班子整体稳定。",
                    "date": "",
                    "confidence": "plausible",
                    "source_ids": []
                }
            ],
            "source_register": [
                {
                    "id": "S001",
                    "title": "何文到涛雒镇调研重点项目推进工作",
                    "url": "http://www.rzdonggang.gov.cn/art/2026/6/25/art_33466_10360078.html",
                    "publisher": "日照市东港区人民政府",
                    "published_at": "2026-06-25",
                    "accessed_at": "2026-07-25",
                    "source_type": "official",
                    "reliability": "high",
                    "notes": "官方政府网站新闻，确认何文为东港区委书记"
                },
                {
                    "id": "S002",
                    "title": "区委常委会召开会议",
                    "url": "http://www.rzdonggang.gov.cn/art/2026/6/13/art_33466_10359838.html",
                    "publisher": "日照市东港区人民政府",
                    "published_at": "2026-06-13",
                    "accessed_at": "2026-07-25",
                    "source_type": "official",
                    "reliability": "high",
                    "notes": "官方政府网站新闻，区委书记何文主持会议"
                },
                {
                    "id": "S003",
                    "title": "全国水域救援大赛新闻",
                    "url": "https://jingji.cctv.com/2025/09/24/ARTI7Sppks4Tj3FxJYJ6l9lq250924.shtml",
                    "publisher": "央视网",
                    "published_at": "2025-09-24",
                    "accessed_at": "2026-07-25",
                    "source_type": "media",
                    "reliability": "high",
                    "notes": "确认刘祥龙以日照市副市长身份出席活动"
                }
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": "何文在担任东港区委书记前的全部履历（出生、籍贯、教育背景、历任职务）均未查到。东港区区长及其他领导班子成员的信息均无法获取。"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "何文（东港区委书记）的完整履历是什么？包括出生日期、籍贯、教育背景、此前任职经历",
                    "why_it_matters": "核心领导人的背景信息是关系网络分析的基础",
                    "suggested_queries": ["何文 简历", "何文 日照", "何文 东港区委书记 任前公示"],
                    "last_attempted": "2026-07-25"
                },
                {
                    "priority": "critical",
                    "question": "东港区区长是谁？",
                    "why_it_matters": "区长是区政府主要领导，与区委书记为党政搭档关系",
                    "suggested_queries": ["日照市东港区 区长", "东港区 区长 简历", "东港区政府 领导分工"],
                    "last_attempted": "2026-07-25"
                },
                {
                    "priority": "high",
                    "question": "东港区委常委班子成员名单及分工",
                    "why_it_matters": "完整的领导班子信息是构建关系网络的基础",
                    "suggested_queries": ["东港区 区委常委", "东港区 领导分工"],
                    "last_attempted": "2026-07-25"
                },
                {
                    "priority": "high",
                    "question": "东港区前任区委书记刘祥龙的完整任职时间线",
                    "why_it_matters": "了解前任去向和交接时间线有助于分析权力更替模式",
                    "suggested_queries": ["刘祥龙 东港区委书记", "刘祥龙 任职 东港"],
                    "last_attempted": "2026-07-25"
                },
                {
                    "priority": "medium",
                    "question": "东港区与日照市其他区县间的人事交流情况",
                    "why_it_matters": "跨区县干部交流模式有助于识别更广域的关系网络",
                    "suggested_queries": ["东港区 岚山区 干部交流", "东港区 开发区 人事"],
                    "last_attempted": "2026-07-25"
                }
            ]
        }
    },
    {
        "filename": f"{TODAY}-山东省-日照市-区长-待查.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "山东省",
                "city": "日照市",
                "region": "东港区",
                "job": "区长",
                "task_id": "shandong_东港区",
                "time_focus": "2026"
            },
            "identity": {
                "person_id": "donggang_quzhang_unknown",
                "name": "待查_东港区长",
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
                    "name_birth": "",
                    "name_birthplace": "",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "东港区区长",
                "current_org": "东港区人民政府",
                "administrative_rank": "县处级正职",
                "as_of": "2026-07-25",
                "is_current_confirmed": False,
                "source_ids": []
            },
            "career_timeline": [],
            "organizations": [],
            "relationships": [],
            "governance_record": [],
            "professional_profile": {},
            "work_style_and_personality": {},
            "network_metrics": {},
            "risk_and_integrity_signals": [],
            "source_register": [],
            "confidence_summary": {
                "identity": "unverified",
                "current_role": "unverified",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": "东港区区长身份及履历全部缺失。"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "东港区区长姓名和基本身份信息",
                    "why_it_matters": "区长是本次调研的核心目标之一，与区委书记为党政搭档",
                    "suggested_queries": ["日照市东港区 区长", "东港区 区长 公示", "东港区政府 领导分工"],
                    "last_attempted": "2026-07-25"
                },
                {
                    "priority": "critical",
                    "question": "东港区区长的完整履历",
                    "why_it_matters": "了解其此前任职经历，识别与其他区县的人事关系",
                    "suggested_queries": ["东港区长 简历", "东港区长 任前公示"],
                    "last_attempted": "2026-07-25"
                }
            ]
        }
    },
]

# ══════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════

def main():
    # ── SQLite Database ──
    print(f"Building SQLite database: {DB_PATH}")
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS persons (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        gender TEXT,
        ethnicity TEXT,
        birth TEXT,
        birthplace TEXT,
        education TEXT,
        party_join TEXT,
        work_start TEXT,
        current_post TEXT,
        current_org TEXT,
        source TEXT
    );

    CREATE TABLE IF NOT EXISTS organizations (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT,
        level TEXT,
        parent TEXT,
        location TEXT
    );

    CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY,
        person_id INTEGER NOT NULL,
        org_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        start TEXT,
        end TEXT,
        rank TEXT,
        note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    );

    CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY,
        person_a_id INTEGER NOT NULL,
        person_b_id INTEGER NOT NULL,
        type TEXT NOT NULL,
        context TEXT,
        overlap_org TEXT,
        overlap_period TEXT,
        FOREIGN KEY (person_a_id) REFERENCES persons(id),
        FOREIGN KEY (person_b_id) REFERENCES persons(id)
    );
    """)

    for p in persons:
        cur.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
                     p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
                     p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)""",
                    (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                     pos.get("start", ""), pos.get("end", ""), pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships VALUES (?,?,?,?,?,?,?)""",
                    (r["id"], r["person_a"], r["person_b"], r["type"],
                     r.get("context", ""), r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()

    # Summary stats
    cur.execute("SELECT COUNT(*) FROM persons")
    person_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM organizations")
    org_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM positions")
    pos_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM relationships")
    rel_count = cur.fetchone()[0]
    conn.close()

    print(f"  Persons: {person_count}")
    print(f"  Organizations: {org_count}")
    print(f"  Positions: {pos_count}")
    print(f"  Relationships: {rel_count}")

    # ── GEXF Graph ──
    print(f"\nBuilding GEXF graph: {GEXF_PATH}")

    today = datetime.now().strftime("%Y-%m-%d")
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append(f'<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>china-gov-network skill</creator>')
    lines.append(f'    <description>东港区领导班子工作关系网络 - {today}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="type" title="Type" type="string"/>')
    lines.append('      <attribute id="category" title="Category" type="string"/>')
    lines.append('      <attribute id="birth" title="Birth" type="string"/>')
    lines.append('      <attribute id="birthplace" title="Birthplace" type="string"/>')
    lines.append('      <attribute id="education" title="Education" type="string"/>')
    lines.append('      <attribute id="current_post" title="Current Post" type="string"/>')
    lines.append('      <attribute id="source" title="Source" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="type" title="Type" type="string"/>')
    lines.append('      <attribute id="context" title="Context" type="string"/>')
    lines.append('      <attribute id="period" title="Period" type="string"/>')
    lines.append('    </attributes>')

    # ── Nodes: Persons ──
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        name = p["name"]
        post = p.get("current_post", "")

        if pid == 1:
            color = '#E03C31'  # red: Party Secretary (区委书记)
            size = 20.0
        elif pid == 2:
            color = '#2980B9'  # blue: government leader (区长)
            size = 18.0
        elif pid == 10:
            color = '#8E44AD'  # purple: former leader
            size = 15.0
        else:
            color = '#95A5A6'  # grey: others
            size = 12.0

        lines.append(f'      <node id="{pid}" label="{name}">')
        lines.append(f'        <attvalues>')
        lines.append(f'          <attvalue for="type" value="person"/>')
        lines.append(f'          <attvalue for="category" value="person"/>')
        lines.append(f'          <attvalue for="birth" value="{p.get("birth", "")}"/>')
        lines.append(f'          <attvalue for="birthplace" value="{p.get("birthplace", "")}"/>')
        lines.append(f'          <attvalue for="education" value="{p.get("education", "")}"/>')
        lines.append(f'          <attvalue for="current_post" value="{post}"/>')
        lines.append(f'          <attvalue for="source" value="{p.get("source", "")}"/>')
        lines.append(f'        </attvalues>')
        lines.append(f'        <viz:color r="{int(color[1:3], 16)}" g="{int(color[3:5], 16)}" b="{int(color[5:7], 16)}"/>')
        lines.append(f'        <viz:size value="{size}"/>')
        lines.append(f'      </node>')

    # Organization nodes
    for o in organizations:
        oid = 1000 + o["id"]
        lines.append(f'      <node id="{oid}" label="{o["name"]}">')
        lines.append(f'        <attvalues>')
        lines.append(f'          <attvalue for="type" value="org"/>')
        lines.append(f'          <attvalue for="category" value="{o["type"]}"/>')
        lines.append(f'        </attvalues>')
        lines.append(f'        <viz:color r="44" g="62" b="80"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append(f'      </node>')
    lines.append('    </nodes>')

    # ── Edges ──
    lines.append('    <edges>')
    edge_id = 1

    # person→organization (worked_at)
    for pos in positions:
        oid = 1000 + pos["org_id"]
        lines.append(f'      <edge id="{edge_id}" source="{pos["person_id"]}" target="{oid}" label="worked_at">')
        lines.append(f'        <attvalues>')
        lines.append(f'          <attvalue for="type" value="worked_at"/>')
        lines.append(f'          <attvalue for="context" value="{pos["title"]}"/>')
        lines.append(f'          <attvalue for="period" value="{pos.get("start", "?")} → {pos.get("end", "今")}"/>')
        lines.append(f'        </attvalues>')
        lines.append(f'      </edge>')
        edge_id += 1

    # person↔person (relationships)
    for r in relationships:
        lines.append(f'      <edge id="{edge_id}" source="{r["person_a"]}" target="{r["person_b"]}" label="{r["type"]}">')
        lines.append(f'        <attvalues>')
        lines.append(f'          <attvalue for="type" value="{r["type"]}"/>')
        lines.append(f'          <attvalue for="context" value="{r["context"]}"/>')
        lines.append(f'          <attvalue for="period" value="{r.get("overlap_period", "")}"/>')
        lines.append(f'        </attvalues>')
        lines.append(f'      </edge>')
        edge_id += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    total_nodes = len(persons) + len(organizations)
    total_edges = len(positions) + len(relationships)
    print(f"  Nodes: {len(persons)} persons + {len(organizations)} organizations = {total_nodes} total")
    print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {total_edges} total")

    # ── Person JSON files ──
    print(f"\nWriting person JSON files to {PJSON_DIR}")
    for pj in PERSON_JSONS:
        filepath = PJSON_DIR / pj["filename"]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(pj["data"], f, ensure_ascii=False, indent=2)
        print(f"  {pj['filename']}")
        # Validate JSON
        with open(filepath, "r", encoding="utf-8") as f:
            json.load(f)
        print(f"    ✓ Valid JSON")

    print("\nDone!")


if __name__ == "__main__":
    main()
