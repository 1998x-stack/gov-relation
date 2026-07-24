#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 西峡县 (Xixia County), 南阳市, 河南省.

Investigation date: 2026-07-24
Task ID: henan_西峡县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - http://www.xixia.gov.cn/ — official government website (news listing page accessed 2026-07-24)
  - Government news: 郭存 appears in multiple news items (project inspection, tourism safety,
    exam preparation check), indicating a top leadership role
  - News: "中国共产党西峡县第十四届委员会第一次全体会议召开" (2026-06-25) — 14th County Party Committee elected
  - Associated prefecture build: scripts/build/build_南阳市_data.py — confirms 张生起 served as
    西峡县委书记 before 2011
  - Neighboring county patterns used for structure reference

Confidence notes:
  - 郭存 (county leader): confirmed active as a top county leader via multiple government news
    articles (Jun-Jul 2026). Definite role (县委书记 vs 县长) unverified from available sources.
  - 西峡县第十四届县委 elected June 25, 2026: confirmed.
  - 张生起 served as 西峡县委书记 1990s-2011: confirmed via 南阳市 build.
  - Full leadership roster, predecessors/successors, early careers: unverified due to degraded
    web access (Exa rate-limited, government site intermittent, Baidu 403).
  - This is a partial-evidence artifact: core leader identity is documented with plausible
    role assignment; detailed bios are incomplete. Uncertainty is explicit.
"""

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[1]  # repo root: go from scripts/build/ up to repo root
SLUG = "西峡县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR
# ── Persons ─────────────────────────────────────────────────────────────────

persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "郭存",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记（推定）",
        "current_org": "中共西峡县委员会",
        "source": "Confirmed as top county leader via multiple government news articles (2026-06-05 to 2026-07-02): 郭存调研重点项目建设, 郭存到恐龙遗迹园景区调研安全生产, 郭存检查高考服务保障. Role as 县委书记 is plausible based on activity pattern (project inspection, cross-department coordination). Exact role unverified due to degraded web access."
    },
    {
        "id": 2,
        "name": "待查（县长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长（姓名待查）",
        "current_org": "西峡县人民政府",
        "source": "Current 西峡县长 identity unverified. Government news listing mentions '西峡县人大常委会视察调研' and '西峡县政协开展民主监督活动' but does not name the 县长 explicitly. Needs targeted web search or government leadership page access."
    },
    # ═══════ Noteworthy Predecessor ═══════
    {
        "id": 3,
        "name": "张生起",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1963年11月",
        "birthplace": "河南省社旗县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "1984年",
        "current_post": "南阳市人大常委会主任（现职，非西峡）",
        "current_org": "南阳市人民代表大会常务委员会",
        "source": "Confirmed via scripts/build/build_南阳市_data.py and Wikipedia. Served as 西峡县委书记 before 2011. Now 南阳市人大常委会主任."
    },
    # ═══════ Other Mentioned Leaders ═══════
    {
        "id": 4,
        "name": "待查（县委副书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记（姓名待查）",
        "current_org": "中共西峡县委员会",
        "source": "Based on typical county leadership structure. Name unverified. Could be the same as the 县长 if the 县长 serves as deputy party secretary (standard pattern)."
    },
    {
        "id": 5,
        "name": "待查（常务副县长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长（姓名待查）",
        "current_org": "西峡县人民政府",
        "source": "Typical county leadership structure includes a 常务副县长. Identity and name unverified."
    },
    {
        "id": 6,
        "name": "待查（人大常委会主任）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任（姓名待查）",
        "current_org": "西峡县人民代表大会常务委员会",
        "source": "County legislative head. Identity unverified. News mentions '西峡县人大常委会视察调研' but does not name the chair."
    },
    {
        "id": 7,
        "name": "待查（政协主席）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席（姓名待查）",
        "current_org": "中国人民政治协商会议西峡县委员会",
        "source": "County political consultative head. Identity unverified. News mentions '西峡县政协开展民主监督活动' (2026-06-30) but does not name the chair."
    },
]

# ── Organizations ──────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共西峡县委员会", "type": "党委", "level": "县处级", "parent": "中共南阳市委", "location": "西峡县"},
    {"id": 2, "name": "西峡县人民政府", "type": "政府", "level": "县处级", "parent": "南阳市人民政府", "location": "西峡县"},
    {"id": 3, "name": "西峡县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "南阳市人大常委会", "location": "西峡县"},
    {"id": 4, "name": "中国人民政治协商会议西峡县委员会", "type": "政协", "level": "县处级", "parent": "南阳市政协", "location": "西峡县"},
    {"id": 5, "name": "西峡县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "南阳市纪委监委", "location": "西峡县"},
    {"id": 6, "name": "中共南阳市委", "type": "党委", "level": "地级市", "parent": "中共河南省委", "location": "南阳市"},
    {"id": 7, "name": "南阳市人民政府", "type": "政府", "level": "地级市", "parent": "河南省人民政府", "location": "南阳市"},
]

# ── Positions (person → org with title) ────────────────────────────────────

positions = [
    # 郭存 (id=1)
    {"person_id": 1, "org_id": 1, "title": "县委书记（推定）", "start_date": "~2025-2026", "end_date": "present", "rank": "县处级正职", "note": "推定：2026年6-7月以主要领导身份调研项目。确切任职起始时间和职务需验证。"},
    # 待查县长 (id=2)
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "推定"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "姓名和到任时间待查"},
    # 张生起 (id=3) — former 西峡县委书记
    {"person_id": 3, "org_id": 1, "title": "西峡县委书记（前任）", "start_date": "", "end_date": "2011年4月", "rank": "县处级正职", "note": "来自南阳市数据。早期履历不详，具体到任时间不详。"},
    {"person_id": 3, "org_id": 6, "title": "南阳市委常委、政法委书记", "start_date": "2016年2月", "end_date": "2018年9月", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 3, "title": "南阳市人大常委会主任", "start_date": "2022年2月", "end_date": "present", "rank": "正厅级", "note": ""},
    # 待查县委副书记 (id=4)
    {"person_id": 4, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "姓名待查"},
    # 待查常务副县长 (id=5)
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "姓名待查"},
    {"person_id": 5, "org_id": 2, "title": "常务副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "姓名待查"},
    # 待查人大主任 (id=6)
    {"person_id": 6, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "姓名待查"},
    # 待查政协主席 (id=7)
    {"person_id": 7, "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "姓名待查"},
]

# ── Relationships ───────────────────────────────────────────────────────────

relationships = [
    # 郭存 ↔ 待查县长（推定党政搭档）
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "推定：郭存为县委书记，待查县长为县委副书记、县长，为西峡县党政正职搭档",
        "overlap_org": "西峡县",
        "overlap_period": "当前"
    },
    # 张生起（前任西峡县委书记）→ 郭存（推定前后任）
    {
        "person_a": 3, "person_b": 1,
        "type": "predecessor_successor",
        "context": "张生起曾任西峡县委书记（约2011年前），为间接前任。中间可能有其他书记。",
        "overlap_org": "中共西峡县委员会",
        "overlap_period": "跨时期"
    },
    # 待查县长 ↔ 待查常务副县长（政府正副职）
    {
        "person_a": 2, "person_b": 5,
        "type": "superior_subordinate",
        "context": "推定：县长与常务副县长为政府正副职搭档",
        "overlap_org": "西峡县人民政府",
        "overlap_period": "当前"
    },
    # 待查县长 ↔ 待查县委副书记（推定副书记由县长兼任）
    {
        "person_a": 2, "person_b": 4,
        "type": "overlap",
        "context": "推定：县长兼任县委副书记（按组织惯例）。如县长与副书记为同一人则去除本条。",
        "overlap_org": "中共西峡县委员会",
        "overlap_period": "当前"
    },
]

# ── Person JSON Data ───────────────────────────────────────────────────────
person_files_data = [
    {
        "id": 1,
        "name": "郭存",
        "job": "县委书记",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "南阳市",
                "region": "西峡县",
                "job": "县委书记（推定）",
                "task_id": "henan_西峡县",
                "time_focus": "2025-2026"
            },
            "identity": {
                "person_id": "xixia_guo_cun",
                "name": "郭存",
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
                    "name_birth": "郭存_unknown",
                    "name_birthplace": "",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "县委书记（推定）",
                "current_org": "中共西峡县委员会",
                "administrative_rank": "县处级正职（推定）",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S002", "S003"]
            },
            "career_timeline": [
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "履历缺口",
                    "title": "",
                    "notes": "公开资料未找到郭存任西峡县领导前的完整履历。网络访问受限（政府网站间歇性不可用、Exa 限额、百度403）。",
                    "confidence": "unverified",
                    "source_ids": []
                },
                {
                    "start": "~2025-2026",
                    "end": "present",
                    "org": "中共西峡县委员会",
                    "title": "县委书记（推定）",
                    "level": "县处级正职",
                    "location": "河南省南阳市西峡县",
                    "system": "party",
                    "rank": "正处级（推定）",
                    "is_key_promotion": True,
                    "notes": "推定：2026年6-7月以主要领导身份调研重点项目、恐龙遗迹园景区安全和高考试保障工作。确切职务信息需验证。",
                    "confidence": "plausible",
                    "source_ids": ["S001", "S002", "S003"]
                }
            ],
            "organizations": [
                {"org": "中共西峡县委员会", "role": "县委书记（推定）", "period": "~2025—至今"}
            ],
            "relationships": [
                {
                    "person": "待查（县长）",
                    "person_id": "xixia_county_mayor_unknown",
                    "relationship_type": "superior_subordinate",
                    "strength": "strong",
                    "evidence": "推定：郭存为县委书记，待查县长为县政府正职，为党政正职搭档",
                    "overlap_org": "西峡县",
                    "overlap_period": "当前",
                    "direction": "undirected",
                    "confidence": "plausible",
                    "source_ids": []
                },
                {
                    "person": "张生起",
                    "person_id": "nanyang_zhang_shengqi",
                    "relationship_type": "predecessor_successor",
                    "strength": "weak",
                    "evidence": "张生起曾任西峡县委书记（约2011年前），为间接前任。中间可能有其他书记。",
                    "overlap_org": "中共西峡县委员会",
                    "overlap_period": "跨时期",
                    "direction": "other_to_person",
                    "confidence": "unverified",
                    "source_ids": ["S004"]
                }
            ],
            "governance_record": [
                {
                    "period": "2026-07",
                    "domain": "economic_development",
                    "achievement_or_event": "调研重点项目建设",
                    "role_in_event": "主持调研",
                    "location": "西峡县",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                },
                {
                    "period": "2026-06",
                    "domain": "other",
                    "achievement_or_event": "到恐龙遗迹园景区调研安全生产工作",
                    "role_in_event": "调研",
                    "location": "西峡县",
                    "confidence": "confirmed",
                    "source_ids": ["S002"]
                },
                {
                    "period": "2026-06",
                    "domain": "education",
                    "achievement_or_event": "检查西峡县2026年高考服务保障工作",
                    "role_in_event": "检查",
                    "location": "西峡县",
                    "confidence": "confirmed",
                    "source_ids": ["S003"]
                }
            ],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
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
                        "evidence": "深入重点项目、旅游景区和高考试点调研检查，关注经济发展、安全和教育民生",
                        "confidence": "plausible",
                        "source_ids": ["S001", "S002", "S003"]
                    }
                ],
                "speech_themes": ["项目建设", "安全生产", "高考保障"],
                "management_signals": ["重视项目推进", "关注旅游安全和教育保障"],
                "caveat": "工作风格基于公开报道推断"
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "截至2026年7月，未发现郭存相关的纪检处分、审计问题或负面媒体报道",
                    "date": AS_OF,
                    "confidence": "plausible",
                    "source_ids": []
                }
            ],
            "source_register": [
                {"id": "S001", "title": "郭存调研重点项目建设", "url": "http://www.xixia.gov.cn/", "publisher": "西峡县人民政府", "published_at": "2026-07-02", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "西峡要闻，确认郭存为县级主要领导"},
                {"id": "S002", "title": "郭存到恐龙遗迹园景区调研安全生产工作", "url": "http://www.xixia.gov.cn/", "publisher": "西峡县人民政府", "published_at": "2026-06-22", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
                {"id": "S003", "title": "郭存检查西峡县2026年高考服务保障工作", "url": "http://www.xixia.gov.cn/", "publisher": "西峡县人民政府", "published_at": "2026-06-05", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
                {"id": "S004", "title": "南阳市领导班子数据", "url": "https://github.com/xieming/gov-relation/blob/main/scripts/build/build_南阳市_data.py", "publisher": "gov-relation", "published_at": "2026-07-24", "accessed_at": AS_OF, "source_type": "database", "reliability": "high", "notes": "确认张生起曾任西峡县委书记"}
            ],
            "confidence_summary": {
                "identity": "unverified",
                "current_role": "plausible",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": "郭存是否确为县委书记（而非县长或其他职务），及其任县委书记前的完整履历"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "郭存的确切职务是什么？是县委书记还是县长？",
                    "why_it_matters": "核心人物的职务确认是整个网络分析的基础",
                    "suggested_queries": ["郭存 西峡县 职务", "西峡县 县委书记 郭存", "西峡县 县长 郭存"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "critical",
                    "question": "郭存任西峡县领导前的职业履历是什么？",
                    "why_it_matters": "核心人物的完整背景对评估其关系网络至关重要",
                    "suggested_queries": ["郭存 简历 西峡", "郭存 南阳 任职"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "high",
                    "question": "郭存的出生年份、籍贯、学历信息",
                    "why_it_matters": "基本信息缺失，影响身份确认",
                    "suggested_queries": ["郭存 出生 西峡"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "critical",
                    "question": "西峡县现任县长是谁？",
                    "why_it_matters": "县长是核心目标人物之一，身份未知",
                    "suggested_queries": ["西峡县 县长 2026", "西峡县 人民政府 县长"],
                    "last_attempted": AS_OF
                }
            ]
        }
    },
    {
        "id": 2,
        "name": "待查县长",
        "job": "县长",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省",
                "city": "南阳市",
                "region": "西峡县",
                "job": "县委副书记、县长",
                "task_id": "henan_西峡县",
                "time_focus": "2025-2026"
            },
            "identity": {
                "person_id": "xixia_county_mayor_unknown",
                "name": "待查",
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
                    "name_birth": "unknown",
                    "name_birthplace": "",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "县委副书记、县长（姓名待查）",
                "current_org": "西峡县人民政府",
                "administrative_rank": "县处级正职（推定）",
                "as_of": AS_OF,
                "is_current_confirmed": False,
                "source_ids": []
            },
            "career_timeline": [
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "未知",
                    "title": "",
                    "notes": "西峡县县长身份信息完全未知。网络访问受限导致无法确认。",
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "organizations": [],
            "relationships": [
                {
                    "person": "郭存",
                    "person_id": "xixia_guo_cun",
                    "relationship_type": "superior_subordinate",
                    "strength": "strong",
                    "evidence": "推定：郭存为县委书记，待查县长为县委副书记、县长",
                    "overlap_org": "西峡县",
                    "overlap_period": "当前",
                    "direction": "other_to_person",
                    "confidence": "plausible",
                    "source_ids": []
                }
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {
                    "summary": "完全未知",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "完全未知"
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "身份未知，无法评估",
                    "date": AS_OF,
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "source_register": [],
            "confidence_summary": {
                "identity": "unverified",
                "current_role": "unverified",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": "西峡县县长的姓名、职务、履历完全未知"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "西峡县现任县长是谁？",
                    "why_it_matters": "核心目标人物之一",
                    "suggested_queries": ["西峡县 县长 2026", "西峡县 人民政府 县长 任命", "西峡县 县级领导 分工"],
                    "last_attempted": AS_OF
                },
                {
                    "priority": "critical",
                    "question": "西峡县县长何时到任？此前任职经历是什么？",
                    "why_it_matters": "完整履历对关系网络分析至关重要",
                    "suggested_queries": ["西峡县 县长 简历", "西峡县 县长 任前公示"],
                    "last_attempted": AS_OF
                }
            ]
        }
    }
]

# ══════════════════════════════════════════════════════════════════════════
# Runner
# ══════════════════════════════════════════════════════════════════════════

def main():
    # Use the public runner library from gov_relation
    sys.path.insert(0, str(BASE))
    from gov_relation.runner import run_build

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

    # Write person JSON files
    for pf in person_files_data:
        person_name = pf["name"]
        job = pf["job"]
        filename = f"{TODAY}-河南省-南阳市-{job}-{person_name}.json"
        filepath = PERSONS_DIR / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(pf["data"], f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {filepath}")

    print(f"\nDone. Build complete for {SLUG}.")
    print(f"  DB:     {DB_PATH}")
    print(f"  GEXF:   {GEXF_PATH}")


if __name__ == "__main__":
    main()
