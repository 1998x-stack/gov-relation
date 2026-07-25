#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 德城区 (Decheng District), 德州市, 山东省.

Level: 市辖区
Province: 山东省
Parent city: 德州市
Targets: 区委书记 (Party Secretary: 张旗), 区长 (Mayor: 张因忠)
Task ID: shandong_德城区

Research date: 2026-07-25
Official source: http://www.decheng.gov.cn/ (德城区人民政府)

Current status (as of 2026-07-23, verified via 德城区人民政府 website 领导之窗):
- 区委书记: 张旗 (confirmed via news article 全区安全生产工作会议召开 on 2026-07-23)
- 区委副书记、区长: 张因忠 (男，汉族，1979年6月生，研究生学历，中共党员)
- 区委副书记: 盛慧
- 区委常委、副区长(常务): 王春波 (男，1980年4月生，汉族，本科，中共党员)
- 区委常委、副区长: 刘桂芝 (女，1975年7月生，汉族，研究生，中共党员)
- 副区长: 郑志永 (男，1971年9月生，汉族，研究生，中共党员)
- 副区长: 孙茜茜 (女，1984年10月生，汉族，研究生，中共党员)

Leadership roster sourced from:
  - http://www.decheng.gov.cn/n55004251/n55004287/n55004541/n55004814/c68116788/content.html (区长张因忠)
  - http://www.decheng.gov.cn/n55004251/n55004287/n55004541/n55004814/c69397192/content.html (常务副区长王春波)
  - http://www.decheng.gov.cn/n55004251/n55004287/n55004541/n55004814/c61458570/content.html (副区长刘桂芝)
  - http://www.decheng.gov.cn/n55004251/n55004287/n55004541/n55004814/c84301485/content.html (副区长郑志永)
  - http://www.decheng.gov.cn/n55004251/n55004287/n55004541/n55004814/c92493501/content.html (副区长孙茜茜)
  - http://www.decheng.gov.cn/n55840578/n55840678/c101060536/content.html (区委书记张旗 confirmed)

Confidence notes:
  - 张因忠 identity confirmed via official government bio page with name, gender, birth, education.
  - 张旗 identity confirmed via official news report mentioning role; full bio not available on public page.
  - 区委副书记 盛慧 confirmed via official news article.
  - Full government leadership roster confirmed via official leadership window pages.
  - Detailed career histories before current roles not fully available.
  - Web search tools (Exa) were rate-limited; primary source was direct government website access.
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

SLUG = "德城区"

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

    # 1. 张旗 — 区委书记
    {
        "id": 1,
        "name": "张旗",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共德城区委员会",
        "source": "http://www.decheng.gov.cn/n55840578/n55840678/c101060536/content.html",
    },
    # 2. 张因忠 — 区委副书记、区长
    {
        "id": 2,
        "name": "张因忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年6月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "德城区人民政府",
        "source": "http://www.decheng.gov.cn/n55004251/n55004287/n55004541/n55004814/c68116788/content.html",
    },

    # ════════════════════════════════════════
    # 区委领导 (Party Committee)
    # ════════════════════════════════════════

    # 3. 盛慧 — 区委副书记
    {
        "id": 3,
        "name": "盛慧",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共德城区委员会",
        "source": "http://www.decheng.gov.cn/n55840578/n55840678/c101060536/content.html",
    },

    # ════════════════════════════════════════
    # 政府领导 (Government)
    # ════════════════════════════════════════

    # 4. 王春波 — 区委常委、副区长（常务）
    {
        "id": 4,
        "name": "王春波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年4月",
        "birthplace": "",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "德城区人民政府",
        "source": "http://www.decheng.gov.cn/n55004251/n55004287/n55004541/n55004814/c69397192/content.html",
    },
    # 5. 刘桂芝 — 区委常委、副区长
    {
        "id": 5,
        "name": "刘桂芝",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1975年7月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "德城区人民政府",
        "source": "http://www.decheng.gov.cn/n55004251/n55004287/n55004541/n55004814/c61458570/content.html",
    },
    # 6. 郑志永 — 副区长
    {
        "id": 6,
        "name": "郑志永",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年9月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "德城区人民政府",
        "source": "http://www.decheng.gov.cn/n55004251/n55004287/n55004541/n55004814/c84301485/content.html",
    },
    # 7. 孙茜茜 — 副区长
    {
        "id": 7,
        "name": "孙茜茜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1984年10月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "德城区人民政府",
        "source": "http://www.decheng.gov.cn/n55004251/n55004287/n55004541/n55004814/c92493501/content.html",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共德城区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共德州市委员会",
        "location": "山东省德州市德城区",
    },
    {
        "id": 2,
        "name": "德城区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "德州市人民政府",
        "location": "山东省德州市德城区",
    },
    {
        "id": 3,
        "name": "德城区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "德州市人大常委会",
        "location": "山东省德州市德城区",
    },
    {
        "id": 4,
        "name": "政协德城区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协德州市委员会",
        "location": "山东省德州市德城区",
    },
    {
        "id": 5,
        "name": "德城区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共德州市纪律检查委员会",
        "location": "山东省德州市德城区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # ── Core Leadership ──
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "", "end": "present",
     "rank": "正处级", "note": "Confirmed active as of 2026-07-23 (出席全区安全生产工作会议报道)"},
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "", "end": "present",
     "rank": "正处级", "note": "Confirmed active as of 2026-07-23 (官网简历于2026-06-11更新)"},

    # ── 区委领导 ──
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start": "", "end": "present",
     "rank": "副处级", "note": "Confirmed active as of 2026-07-23"},

    # ── 区政府领导 ──
    {"person_id": 4, "org_id": 2, "title": "区委常委、副区长（常务）", "start": "", "end": "present",
     "rank": "副处级", "note": "三级调研员；协助区长负责区政府常务工作"},
    {"person_id": 5, "org_id": 2, "title": "区委常委、副区长", "start": "", "end": "present",
     "rank": "副处级", "note": "三级调研员；兼区红十字会会长"},
    {"person_id": 6, "org_id": 2, "title": "副区长", "start": "", "end": "present",
     "rank": "副处级", "note": "区政府党组成员"},
    {"person_id": 7, "org_id": 2, "title": "副区长", "start": "", "end": "present",
     "rank": "副处级", "note": "区政府党组成员"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 张旗 <-> 张因忠: 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记与区长党政主要领导搭档; 共同负责德城区全面工作",
     "overlap_org": "中共德城区委员会/德城区人民政府",
     "overlap_period": "截至2026年7月"},

    # 张旗 <-> 盛慧: 书记与副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "区委书记与专职副书记; 区委领导班子搭档",
     "overlap_org": "中共德城区委员会",
     "overlap_period": "截至2026年7月"},

    # 张因忠 <-> 王春波: 区长与常务副区长
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "区长与常务副区长工作搭档; 协助区长分管财政、税务、审计",
     "overlap_org": "德城区人民政府",
     "overlap_period": "截至2026年7月"},

    # 张因忠 <-> 刘桂芝: 区长与副区长
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "区长与副区长工作搭档",
     "overlap_org": "德城区人民政府",
     "overlap_period": "截至2026年7月"},

    # 张因忠 <-> 郑志永: 区长与副区长
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "区长与副区长工作搭档",
     "overlap_org": "德城区人民政府",
     "overlap_period": "截至2026年7月"},

    # 张因忠 <-> 孙茜茜: 区长与副区长
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "区长与副区长工作搭档",
     "overlap_org": "德城区人民政府",
     "overlap_period": "截至2026年7月"},

    # 区委常委会成员间的工作关系
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "区委书记与区委常委常务副区长; 区委常委会搭档",
     "overlap_org": "中共德城区委员会",
     "overlap_period": "截至2026年7月"},
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "区委书记与区委常委副区长; 区委常委会搭档",
     "overlap_org": "中共德城区委员会",
     "overlap_period": "截至2026年7月"},
]


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════


def make_source_register() -> list[dict]:
    return [
        {
            "id": "S001",
            "title": "德城区人民政府官网-区政府领导-张因忠",
            "url": "http://www.decheng.gov.cn/n55004251/n55004287/n55004541/n55004814/c68116788/content.html",
            "publisher": "德城区人民政府",
            "published_at": "2026-06-11",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "张因忠: 区委副书记、区长，1979年6月生，男，汉族，研究生，中共党员",
        },
        {
            "id": "S002",
            "title": "德城区人民政府官网-区政府领导-王春波",
            "url": "http://www.decheng.gov.cn/n55004251/n55004287/n55004541/n55004814/c69397192/content.html",
            "publisher": "德城区人民政府",
            "published_at": "2026-06-11",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "王春波: 区委常委、副区长（常务），1980年4月生，男，汉族，本科，中共党员",
        },
        {
            "id": "S003",
            "title": "德城区人民政府官网-区政府领导-刘桂芝",
            "url": "http://www.decheng.gov.cn/n55004251/n55004287/n55004541/n55004814/c61458570/content.html",
            "publisher": "德城区人民政府",
            "published_at": "2026-06-11",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "刘桂芝: 区委常委、副区长，1975年7月生，女，汉族，研究生，中共党员",
        },
        {
            "id": "S004",
            "title": "德城区人民政府官网-区政府领导-郑志永",
            "url": "http://www.decheng.gov.cn/n55004251/n55004287/n55004541/n55004814/c84301485/content.html",
            "publisher": "德城区人民政府",
            "published_at": "2026-06-11",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "郑志永: 副区长，1971年9月生，男，汉族，研究生，中共党员",
        },
        {
            "id": "S005",
            "title": "德城区人民政府官网-区政府领导-孙茜茜",
            "url": "http://www.decheng.gov.cn/n55004251/n55004287/n55004541/n55004814/c92493501/content.html",
            "publisher": "德城区人民政府",
            "published_at": "2026-06-11",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "孙茜茜: 副区长，1984年10月生，女，汉族，研究生，中共党员",
        },
        {
            "id": "S006",
            "title": "德城区要闻-全区安全生产工作会议召开",
            "url": "http://www.decheng.gov.cn/n55840578/n55840678/c101060536/content.html",
            "publisher": "德城区人民政府",
            "published_at": "2026-07-23",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认张旗为区委书记、张因忠为区长、盛慧为区委副书记",
        },
        {
            "id": "S007",
            "title": "德城区人民政府官网-机构职能-领导信息",
            "url": "http://www.decheng.gov.cn/n55004251/n55004287/n55004541/n55004814/index.html",
            "publisher": "德城区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "区政府领导完整名册",
        },
    ]


def generate_person_json(job: str, name: str) -> dict:
    """Generate per-person graph JSON following person_graph_json.md schema."""
    person_id_str = f"decheng_{name}"

    # ── 张旗 (区委书记) ──
    if name == "张旗":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "山东省",
                "city": "德州市",
                "region": "德城区",
                "job": "区委书记",
                "task_id": "shandong_德城区",
                "time_focus": "2024–2026",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "张旗",
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
                    "name_birth": "张旗_",
                    "name_birthplace": "张旗_",
                    "official_profile_url": "",
                },
            },
            "current_status": {
                "current_post": "区委书记",
                "current_org": "中共德城区委员会",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S006"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "present",
                    "org": "中共德城区委员会",
                    "title": "区委书记",
                    "level": "正处级",
                    "location": "山东省德州市德城区",
                    "system": "party",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "截至2026年7月在任；首次见于2026年7月23日官方报道",
                    "confidence": "confirmed",
                    "source_ids": ["S006"],
                },
            ],
            "organizations": [
                {"org_id": 1, "name": "中共德城区委员会", "type": "党委",
                 "level": "县处级", "location": "山东省德州市德城区"},
            ],
            "relationships": [
                {"person": "张因忠", "person_id": "decheng_张因忠",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区委书记与区长党政主要领导搭档",
                 "overlap_org": "中共德城区委员会/德城区人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S006", "S001"]},
                {"person": "盛慧", "person_id": "decheng_盛慧",
                 "relationship_type": "superior_subordinate", "strength": "strong",
                 "evidence": "区委书记与专职副书记",
                 "overlap_org": "中共德城区委员会",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S006"]},
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["party"],
                "geographic_pattern": [],
                "promotion_velocity": {
                    "summary": "公开源不足，无法分析晋升速度",
                    "notable_fast_promotions": [],
                },
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {
                        "trait": "unknown",
                        "evidence": "无公开新闻报道可确认其具体工作风格",
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
                "career_completeness": "partial",
                "relationship_confidence": "medium",
                "biggest_gap": "张旗的完整履历、出生日期、籍贯、教育背景和全部任职经历均未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "张旗的完整履历（出生日期、籍贯、毕业院校、工作经历）？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["张旗 简历 德城区", "张旗 德州市 区委书记"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "张旗何时开始担任德城区区委书记？此前担任什么职务？",
                    "why_it_matters": "理清履职起始时间和前任交接",
                    "suggested_queries": ["张旗 任 德城区 区委书记", "张旗 任职公示"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "张旗的党组织系统经历和分管工作详情？",
                    "why_it_matters": "评估其政治路线和专业背景",
                    "suggested_queries": ["张旗 德城区 党建工作"],
                    "last_attempted": AS_OF,
                },
            ],
        }

    # ── 张因忠 (区长) ──
    if name == "张因忠":
        return {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "山东省",
                "city": "德州市",
                "region": "德城区",
                "job": "区长",
                "task_id": "shandong_德城区",
                "time_focus": "2024–2026",
            },
            "identity": {
                "person_id": person_id_str,
                "name": "张因忠",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1979年6月",
                "birthplace": "",
                "native_place": "",
                "education": [
                    {"period": "", "institution": "", "major": "", "degree": "研究生",
                     "study_type": "unknown", "source_ids": ["S001"]},
                ],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "张因忠_197906",
                    "name_birthplace": "张因忠_",
                    "official_profile_url": "http://www.decheng.gov.cn/n55004251/n55004287/n55004541/n55004814/c68116788/content.html",
                },
            },
            "current_status": {
                "current_post": "区长",
                "current_org": "德城区人民政府",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"],
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "present",
                    "org": "德城区人民政府",
                    "title": "区长",
                    "level": "正处级",
                    "location": "山东省德州市德城区",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "截至2026年7月在任；官网简历于2026-06-11更新",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                },
            ],
            "organizations": [
                {"org_id": 2, "name": "德城区人民政府", "type": "政府",
                 "level": "县处级", "location": "山东省德州市德城区"},
            ],
            "relationships": [
                {"person": "张旗", "person_id": "decheng_张旗",
                 "relationship_type": "overlap", "strength": "strong",
                 "evidence": "区长与区委书记党政主要领导搭档",
                 "overlap_org": "中共德城区委员会/德城区人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S006", "S001"]},
                {"person": "王春波", "person_id": "decheng_王春波",
                 "relationship_type": "superior_subordinate", "strength": "strong",
                 "evidence": "区长与常务副区长工作搭档",
                 "overlap_org": "德城区人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S002"]},
                {"person": "刘桂芝", "person_id": "decheng_刘桂芝",
                 "relationship_type": "superior_subordinate", "strength": "strong",
                 "evidence": "区长与副区长工作搭档",
                 "overlap_org": "德城区人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S003"]},
                {"person": "郑志永", "person_id": "decheng_郑志永",
                 "relationship_type": "superior_subordinate", "strength": "medium",
                 "evidence": "区长与副区长工作搭档",
                 "overlap_org": "德城区人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S004"]},
                {"person": "孙茜茜", "person_id": "decheng_孙茜茜",
                 "relationship_type": "superior_subordinate", "strength": "medium",
                 "evidence": "区长与副区长工作搭档",
                 "overlap_org": "德城区人民政府",
                 "overlap_period": "截至2026年7月",
                 "direction": "undirected", "confidence": "confirmed",
                 "source_ids": ["S005"]},
            ],
            "governance_record": [],
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
                        "trait": "unknown",
                        "evidence": "无充分公开报道可确认其具体工作风格",
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
                "biggest_gap": "完整履历：张因忠任区长前的教育背景（具体院校/专业）和全部任职经历均未知",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "张因忠的籍贯和毕业院校？",
                    "why_it_matters": "身份去重和档案建库的基础信息",
                    "suggested_queries": ["张因忠 简历 德城区", "张因忠 出生 籍贯"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "critical",
                    "question": "张因忠何时开始担任德城区区长？此前担任什么职务？",
                    "why_it_matters": "理清履职起始时间和前任交接",
                    "suggested_queries": ["张因忠 任 德城区 区长", "张因忠 任职公示"],
                    "last_attempted": AS_OF,
                },
                {
                    "priority": "high",
                    "question": "张因忠的完整职业生涯履历？",
                    "why_it_matters": "评估专业背景和职业发展路径",
                    "suggested_queries": ["张因忠 工作 经历 德州"],
                    "last_attempted": AS_OF,
                },
            ],
        }

    return {}


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=f"Build {SLUG} network data")
    parser.add_argument("--db-path", default=str(DB_PATH))
    parser.add_argument("--gexf-path", default=str(GEXF_PATH))
    parser.add_argument("--persons-dir", default=str(PERSONS_DIR))
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    db_path = Path(args.db_path)
    gexf_path = Path(args.gexf_path)
    persons_dir = Path(args.persons_dir)

    # Build DB and GEXF
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=args.overwrite,
    )

    # Generate person JSONs for core leaders
    core_figures = [
        ("区委书记", "张旗"),
        ("区长", "张因忠"),
    ]
    for job, name in core_figures:
        data = generate_person_json(job, name)
        if data:
            filename = f"{TODAY}-山东省-德州市-{job}-{name}.json"
            filepath = persons_dir / filename
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  Wrote {filepath}")

    print(f"Done. DB: {db_path}, GEXF: {gexf_path}")
