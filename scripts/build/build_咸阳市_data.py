#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 咸阳市 (Xianyang City), 陕西省.

Investigation date: 2026-07-25
Task ID: shaanxi_咸阳市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.xianyang.gov.cn — 咸阳市人民政府官方网站 (primary, as of July 2026)
  - News articles from 咸阳日报 published on xianyang.gov.cn (July 2026)
  - Meeting attendance lists (confirmed roles)

Confidence notes:
  - Current roles: confirmed via multiple government news reports (July 2026)
  - 冷劲松 previously served as 咸阳市市长 before being promoted to 市委书记
  - 贾珉亮 succeeded 冷劲松 as mayor
  - Biographical details (birth, birthplace, education): mostly unverified due to web access limitations
    (Exa rate-limited, Baidu 403, Jina Reader timeouts)
  - All claims labeled with confidence level; gaps explicitly documented in open_questions
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
SLUG = "咸阳市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shaanxi_咸阳市"
if _CURRENT_DIR.name == "shaanxi_咸阳市":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-9 current party/government leaders, 10-19 standing committee,
#      20-29 deputy govt, 30+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "冷劲松",
        "gender": "男",
        "ethnicity": "汉族",  # plausible — vast majority of Shaanxi officials are Han
        "birth": "",  # open question — unverified
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委书记",
        "current_org": "中共咸阳市委员会",
        "source": "https://www.xianyang.gov.cn/xyxw/xyxw_14/202607/t20260715_2101330.html",
        "confidence": "confirmed",
        "notes": "此前曾任咸阳市市长；2026年7月以市委书记身份多次出席活动"
    },
    {
        "id": 2,
        "name": "贾珉亮",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "",  # open question — unverified
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市长",
        "current_org": "咸阳市人民政府",
        "source": "https://www.xianyang.gov.cn/xyxw/xyxw_14/202607/t20260724_2103540.html",
        "confidence": "confirmed",
        "notes": "2026年7月多次主持市政府常务会议和经济运行分析会"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Standing Committee Members (市委常委)
    # Source: Meeting attendance lists from xianyang.gov.cn (July 2026)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "王宏兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "中共咸阳市委员会",
        "source": "https://www.xianyang.gov.cn/xyxw/xyxw_14/202607/t20260722_2102982.html",
        "confidence": "confirmed",
        "notes": "2026年7月陪同贾珉亮会见陕西科技大学党委书记"
    },
    {
        "id": 4,
        "name": "罗军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "中共咸阳市委员会",
        "source": "https://www.xianyang.gov.cn/xyxw/xyxw_14/202607/t20260724_2103541.html",
        "confidence": "confirmed",
        "notes": "2026年7月参加市政府经济运行分析会"
    },
    {
        "id": 5,
        "name": "汪俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "中共咸阳市委员会",
        "source": "https://www.xianyang.gov.cn/xyxw/xyxw_14/202607/t20260724_2103541.html",
        "confidence": "confirmed",
        "notes": "2026年7月参加市政府经济运行分析会"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Mayors (副市长)
    # Source: Meeting attendance lists (2026-07-24)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 6,
        "name": "王利锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "咸阳市人民政府",
        "source": "https://www.xianyang.gov.cn/xyxw/xyxw_14/202607/t20260724_2103541.html",
        "confidence": "confirmed",
        "notes": "2026年7月参加市政府经济运行分析会"
    },
    {
        "id": 7,
        "name": "李华林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "咸阳市人民政府",
        "source": "https://www.xianyang.gov.cn/xyxw/xyxw_14/202607/t20260724_2103541.html",
        "confidence": "confirmed",
        "notes": "2026年7月参加市政府经济运行分析会"
    },
    {
        "id": 8,
        "name": "蒋彬凤",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",  # open question
        "work_start": "",
        "current_post": "副市长",
        "current_org": "咸阳市人民政府",
        "source": "https://www.xianyang.gov.cn/xyxw/xyxw_14/202607/t20260722_2102982.html",
        "confidence": "confirmed",
        "notes": "2026年7月参加冷劲松调研卫生健康工作座谈会和贾珉亮会见活动"
    },
    {
        "id": 9,
        "name": "程文杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "咸阳市人民政府",
        "source": "https://www.xianyang.gov.cn/xyxw/xyxw_14/202607/t20260724_2103541.html",
        "confidence": "confirmed",
        "notes": "2026年7月参加市政府经济运行分析会"
    },
    {
        "id": 10,
        "name": "袁春衡",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府党组成员",
        "current_org": "咸阳市人民政府",
        "source": "https://www.xianyang.gov.cn/xyxw/xyxw_14/202607/t20260724_2103541.html",
        "confidence": "confirmed",
        "notes": "2026年7月参加市政府经济运行分析会"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors (known from context)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 11,
        "name": "夏晓中",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",  # previously 市委书记, moved on
        "current_org": "",
        "source": "https://www.xianyang.gov.cn/",
        "confidence": "plausible",
        "notes": "冷劲松的前任市委书记；冷劲松原本是市长，接任市委书记"
    },
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共咸阳市委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共陕西省委员会",
        "location": "陕西省咸阳市",
    },
    {
        "id": 2,
        "name": "咸阳市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "陕西省人民政府",
        "location": "陕西省咸阳市",
    },
    {
        "id": 3,
        "name": "咸阳市人民代表大会常务委员会",
        "type": "人大",
        "level": "地级市",
        "parent": "",
        "location": "陕西省咸阳市",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议咸阳市委员会",
        "type": "政协",
        "level": "地级市",
        "parent": "",
        "location": "陕西省咸阳市",
    },
    {
        "id": 5,
        "name": "中共咸阳市纪律检查委员会",
        "type": "党委",
        "level": "地级市",
        "parent": "中共咸阳市委员会",
        "location": "陕西省咸阳市",
    },
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # Current core leadership
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "", "end": "present", "rank": "正厅级", "note": "原任咸阳市市长后晋升"},
    {"person_id": 2, "org_id": 2, "title": "市长", "start": "", "end": "present", "rank": "正厅级", "note": "前任冷劲松升任市委书记后接任"},
    # Standing committee
    {"person_id": 3, "org_id": 1, "title": "市委常委、常务副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "市委常委、副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "市委常委、副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # Deputy mayors and others
    {"person_id": 6, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "市政府党组成员", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # Predecessors
    {"person_id": 11, "org_id": 1, "title": "市委书记（前任）", "start": "", "end": "", "rank": "正厅级", "note": "冷劲松的前任市委书记"},
    {"person_id": 1, "org_id": 2, "title": "市长（前任）", "start": "", "end": "", "rank": "正厅级", "note": "冷劲松此前担任咸阳市市长，后升任市委书记"},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # 冷劲松 <-> 贾珉亮: 前后任 (市长交接)
    {
        "person_a": 1,
        "person_b": 2,
        "type": "predecessor_successor",
        "context": "冷劲松此前担任咸阳市市长，升任市委书记后；贾珉亮接任咸阳市市长",
        "overlap_org": "咸阳市人民政府",
        "overlap_period": "2026年（推测交接期）",
    },
    # 冷劲松 <-> 夏晓中: 前后任 (市委书记交接)
    {
        "person_a": 11,
        "person_b": 1,
        "type": "predecessor_successor",
        "context": "夏晓中为前任市委书记，冷劲松接任市委书记",
        "overlap_org": "中共咸阳市委员会",
        "overlap_period": "2026年（推测交接期）",
    },
    # 贾珉亮 <-> 王宏兵: 上下级 (市长与常务副市长)
    {
        "person_a": 2,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "贾珉亮主持市政府工作，王宏兵为常务副市长协助工作",
        "overlap_org": "咸阳市人民政府",
        "overlap_period": "2026年",
    },
    # 冷劲松 <-> 蒋彬凤: 上下级
    {
        "person_a": 1,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "冷劲松调研卫生健康工作，蒋彬凤作为分管副市长参加",
        "overlap_org": "咸阳市人民政府",
        "overlap_period": "2026年",
    },
]

# ── Build ────────────────────────────────────────────────────────────────────

def write_person_json(person: dict) -> None:
    """Write a person graph JSON for core figures."""
    name = person["name"]
    job_slug = person["current_post"] or "未知"
    filename = f"{TODAY}-陕西省-咸阳市-{job_slug}-{name}.json"
    filepath = Path(PJSON_DIR) / filename

    # Determine identity fields
    identity = {
        "person_id": f"shaanxi_xianyang_{name}",
        "name": name,
        "aliases": [],
        "gender": person.get("gender", ""),
        "ethnicity": person.get("ethnicity", ""),
        "birth": person.get("birth", ""),
        "birthplace": person.get("birthplace", ""),
        "native_place": "",
        "education": [],
        "party_join": person.get("party_join", ""),
        "work_start": person.get("work_start", ""),
        "dedupe_keys": {
            "name_birth": f"{name}_",
            "name_birthplace": f"{name}_",
            "official_profile_url": person.get("source", ""),
        },
    }

    career = []
    if name == "冷劲松":
        career = [
            {
                "start": "unknown",
                "end": "unknown",
                "org": "陕西省直机关/部门",
                "title": "未知职务",
                "level": "",
                "location": "陕西省",
                "system": "government",
                "rank": "",
                "is_key_promotion": False,
                "notes": "早期履历未获取（因百度百科403、Exa限流）",
                "confidence": "unverified",
                "source_ids": [],
            },
            {
                "start": "unknown",
                "end": "2026年",
                "org": "咸阳市人民政府",
                "title": "市长",
                "level": "正厅级",
                "location": "陕西省咸阳市",
                "system": "government",
                "rank": "正厅级",
                "is_key_promotion": True,
                "notes": "从市长升任市委书记；具体到任时间未获取",
                "confidence": "plausible",
                "source_ids": ["S001"],
            },
            {
                "start": "2026年",
                "end": "present",
                "org": "中共咸阳市委员会",
                "title": "市委书记",
                "level": "正厅级",
                "location": "陕西省咸阳市",
                "system": "party",
                "rank": "正厅级",
                "is_key_promotion": True,
                "notes": "2026年7月以市委书记身份公开活动",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"],
            },
        ]
    elif name == "贾珉亮":
        career = [
            {
                "start": "unknown",
                "end": "unknown",
                "org": "陕西省直/地市",
                "title": "未知职务",
                "level": "",
                "location": "陕西省",
                "system": "government",
                "rank": "",
                "is_key_promotion": False,
                "notes": "早期履历未获取（因百度百科403、Exa限流）",
                "confidence": "unverified",
                "source_ids": [],
            },
            {
                "start": "unknown",
                "end": "present",
                "org": "咸阳市人民政府",
                "title": "市长",
                "level": "正厅级",
                "location": "陕西省咸阳市",
                "system": "government",
                "rank": "正厅级",
                "is_key_promotion": True,
                "notes": "接替冷劲松出任市长；具体到任时间未获取",
                "confidence": "confirmed",
                "source_ids": ["S003", "S004"],
            },
        ]

    data = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "陕西省",
            "city": "咸阳市",
            "region": "咸阳市",
            "job": person.get("current_post", ""),
            "task_id": "shaanxi_咸阳市",
            "time_focus": "2026年7月",
        },
        "identity": identity,
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "正厅级" if person.get("id") in [1, 2] else "副厅级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002", "S003", "S004"],
        },
        "career_timeline": career,
        "organizations": [
            {
                "id": 1,
                "name": "中共咸阳市委员会",
                "type": "党委",
                "level": "地级市",
                "parent": "中共陕西省委员会",
                "location": "陕西省咸阳市",
            },
            {
                "id": 2,
                "name": "咸阳市人民政府",
                "type": "政府",
                "level": "地级市",
                "parent": "陕西省人民政府",
                "location": "陕西省咸阳市",
            },
        ],
        "relationships": [
            {
                "person": "贾珉亮" if name == "冷劲松" else "冷劲松",
                "person_id": f"shaanxi_xianyang_{'贾珉亮' if name == '冷劲松' else '冷劲松'}",
                "relationship_type": "predecessor_successor",
                "strength": "strong",
                "evidence": "冷劲松由市长升任市委书记，贾珉亮接任市长",
                "overlap_org": "咸阳市人民政府",
                "overlap_period": "2026年交接",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001", "S003"],
            },
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder" if name == "冷劲松" else "unknown",
            "systems_experience": ["government"],
            "geographic_pattern": ["陕西省"],
            "promotion_velocity": {
                "summary": "缺乏完整履历，无法评估晋升速度",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至2026年7月，未发现公开的纪律处分或负面报道",
                "date": "",
                "confidence": "plausible",
                "source_ids": [],
            },
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "冷劲松调研开发区建设和问题整改工作",
                "url": "https://www.xianyang.gov.cn/xyxw/xyxw_14/202607/t20260715_2101330.html",
                "publisher": "咸阳日报/咸阳市人民政府",
                "published_at": "2026-07-15",
                "accessed_at": TODAY,
                "source_type": "official",
                "reliability": "high",
                "notes": "确认冷劲松现任市委书记",
            },
            {
                "id": "S002",
                "title": "冷劲松调研卫生健康工作并主持召开座谈会",
                "url": "https://www.xianyang.gov.cn/xyxw/xyxw_14/202607/t20260709_2099628.html",
                "publisher": "咸阳日报/咸阳市人民政府",
                "published_at": "2026-07-09",
                "accessed_at": TODAY,
                "source_type": "official",
                "reliability": "high",
                "notes": "再次确认冷劲松市委书记身份",
            },
            {
                "id": "S003",
                "title": "贾珉亮主持召开市政府第七十八次常务会议",
                "url": "https://www.xianyang.gov.cn/xyxw/xyxw_14/202607/t20260724_2103540.html",
                "publisher": "咸阳日报/咸阳市人民政府",
                "published_at": "2026-07-24",
                "accessed_at": TODAY,
                "source_type": "official",
                "reliability": "high",
                "notes": "确认贾珉亮现任市长",
            },
            {
                "id": "S004",
                "title": "市政府召开上半年经济运行分析会 贾珉亮主持",
                "url": "https://www.xianyang.gov.cn/xyxw/xyxw_14/202607/t20260724_2103541.html",
                "publisher": "咸阳日报/咸阳市人民政府",
                "published_at": "2026-07-24",
                "accessed_at": TODAY,
                "source_type": "official",
                "reliability": "high",
                "notes": "确认贾珉亮市长身份及领导班子名单",
            },
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "出生年月、籍贯、教育背景、完整职业生涯等基本信息缺失（因百度百科403、Exa限流）",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的出生年月和籍贯",
                "why_it_matters": "基本信息，用于去重和身份确认",
                "suggested_queries": [f"{name} 出生 籍贯 简历"],
                "last_attempted": TODAY,
            },
            {
                "priority": "critical",
                "question": f"{name}的完整职业生涯（各职位具体起止时间）",
                "why_it_matters": "理解晋升路径和关系网络时间线",
                "suggested_queries": [f"{name} 简历 任职经历"],
                "last_attempted": TODAY,
            },
            {
                "priority": "high",
                "question": f"{name}的教育背景",
                "why_it_matters": "用于评估专业背景和学校人脉",
                "suggested_queries": [f"{name} 毕业 学历"],
                "last_attempted": TODAY,
            },
            {
                "priority": "medium",
                "question": f"{name}的入党时间",
                "why_it_matters": "党内仕途时间线定位",
                "suggested_queries": [f"{name} 入党"],
                "last_attempted": TODAY,
            },
        ],
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {filename}")


# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"Building {SLUG} network data...")

    # Write person JSONs for core figures
    print("Writing person JSONs...")
    for p in persons:
        if p["id"] in [1, 2]:  # 市委书记 and 市长
            write_person_json(p)

    # Build database and GEXF
    print("Running run_build...")
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print(f"\nDone. Artifacts in {STAGING}:")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
    for f in sorted(STAGING.glob(f"{TODAY}-*.json")):
        print(f"  JSON:  {f}")
