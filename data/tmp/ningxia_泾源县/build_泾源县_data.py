#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 泾源县 (Jingyuan County), 固原市, 宁夏回族自治区.

Investigation date: 2026-07-25
Task ID: ningxia_泾源县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - Web access was severely degraded during investigation:
    - Exa search API rate-limited
    - Baidu Baike returned HTTP 403
    - Chinese government websites (泾源县, 固原市) unreachable via HTTP(S)
    - Google/Bing search results timed out via Jina Reader
    - Wikipedia and cached versions also timed out
  - Due to the above constraints, specific leader names could NOT be verified
    from current primary sources in this session.

Confidence notes:
  - Administrative structure (organizations, levels) is confirmed from standard
    administrative division records in training data.
  - Current officeholder names are marked as "待查" (to be checked) — verifying
    from the 泾源县 government website's 领导之窗 page is required.
  - All biographical fields for persons are left empty with appropriate
    confidence markers.
  - The build script is structurally complete but requires populating specific
    leader names when official sources become accessible.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Module path setup ─────────────────────────────────────────────────
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

# ── Metadata ──────────────────────────────────────────────────────────
SLUG = "泾源县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ─────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "ningxia_泾源县"
if _CURRENT_DIR.name == "ningxia_泾源县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ────────────────────────────────────────────────────────────
# NOTE: Specific officeholder names could NOT be verified due to complete
# web access degradation. All person-level biographic data requires manual
# verification from official sources.
# Expected government website domain: www.nxjingyuan.gov.cn or similar
# Expected leadership page: /xxgk/ldzc/ or /zwgk/ldzc/

persons = [
    # ════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ════════════════════════════════════════════════════════════════════
    # --- 县委书记 (Party Secretary) ---
    {
        "id": 1,
        "name": "待查_县委书记",
        "gender": "",           # unverified
        "ethnicity": "",        # unverified
        "birth": "",            # unverified
        "birthplace": "",       # unverified
        "education": "",        # unverified
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "泾源县委书记",
        "current_org": "中共泾源县委员会",
        "source": "Web access degraded — name unverified. Check 泾源县领导之窗.",
    },
    # --- 县长 (County Chief) ---
    {
        "id": 2,
        "name": "待查_县长",
        "gender": "",           # unverified
        "ethnicity": "",        # unverified
        "birth": "",            # unverified
        "birthplace": "",       # unverified
        "education": "",        # unverified
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "泾源县委副书记、县长",
        "current_org": "泾源县人民政府",
        "source": "Web access degraded — name unverified. Check 泾源县领导之窗.",
    },
    # ════════════════════════════════════════════════════════════════════
    # County Standing Committee (县委常委)
    # ════════════════════════════════════════════════════════════════════
    # --- 县委副书记 (Deputy Party Secretary, typically 3rd-ranking) ---
    {
        "id": 3,
        "name": "待查_副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "泾源县委副书记",
        "current_org": "中共泾源县委员会",
        "source": "Web access degraded — name unverified.",
    },
    # --- 常务副县长 (Executive Deputy County Chief) ---
    {
        "id": 4,
        "name": "待查_常务副县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "泾源县委常委、常务副县长",
        "current_org": "泾源县人民政府",
        "source": "Web access degraded — name unverified.",
    },
    # --- 纪委书记 (Discipline Inspection Secretary) ---
    {
        "id": 5,
        "name": "待查_纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "泾源县委常委、县纪委书记、县监委主任",
        "current_org": "中共泾源县纪律检查委员会",
        "source": "Web access degraded — name unverified.",
    },
    # --- 组织部部长 (Organization Department Head) ---
    {
        "id": 6,
        "name": "待查_组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "泾源县委常委、组织部部长",
        "current_org": "中共泾源县委组织部",
        "source": "Web access degraded — name unverified.",
    },
    # --- 宣传部部长 (Propaganda Department Head) ---
    {
        "id": 7,
        "name": "待查_宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "泾源县委常委、宣传部部长",
        "current_org": "中共泾源县委员会",
        "source": "Web access degraded — name unverified.",
    },
    # --- 政法委书记 (Political-Legal Affairs Secretary) ---
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
        "current_post": "泾源县委常委、政法委书记",
        "current_org": "中共泾源县委员会",
        "source": "Web access degraded — name unverified.",
    },
    # --- 统战部部长 (United Front Work Department Head) ---
    {
        "id": 9,
        "name": "待查_统战部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "泾源县委常委、统战部部长",
        "current_org": "中共泾源县委员会",
        "source": "Web access degraded — name unverified.",
    },
    # ════════════════════════════════════════════════════════════════════
    # County Government Deputies (副县长)
    # ════════════════════════════════════════════════════════════════════
    {
        "id": 10,
        "name": "待查_副县长1",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "泾源县副县长",
        "current_org": "泾源县人民政府",
        "source": "Web access degraded — name unverified.",
    },
    {
        "id": 11,
        "name": "待查_副县长2",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "泾源县副县长",
        "current_org": "泾源县人民政府",
        "source": "Web access degraded — name unverified.",
    },
    # ════════════════════════════════════════════════════════════════════
    # 县级领导 (County-level leaders — 人大、政协)
    # ════════════════════════════════════════════════════════════════════
    {
        "id": 12,
        "name": "待查_人大主任",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "泾源县人大常委会主任",
        "current_org": "泾源县人民代表大会常务委员会",
        "source": "Web access degraded — name unverified.",
    },
    {
        "id": 13,
        "name": "待查_政协主席",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "政协泾源县委员会主席",
        "current_org": "政协泾源县委员会",
        "source": "Web access degraded — name unverified.",
    },
]

# ── Organizations ──────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共泾源县委员会", "type": "党委",
     "level": "县处级", "parent": "中共固原市委员会",
     "location": "宁夏回族自治区固原市泾源县"},
    {"id": 2, "name": "泾源县人民政府", "type": "政府",
     "level": "县处级", "parent": "固原市人民政府",
     "location": "宁夏回族自治区固原市泾源县"},
    {"id": 3, "name": "中共泾源县纪律检查委员会", "type": "党委",
     "level": "县处级", "parent": "中共泾源县委员会",
     "location": "宁夏回族自治区固原市泾源县"},
    {"id": 4, "name": "中共泾源县委组织部", "type": "党委",
     "level": "县处级", "parent": "中共泾源县委员会",
     "location": "宁夏回族自治区固原市泾源县"},
    {"id": 5, "name": "泾源县人民代表大会常务委员会", "type": "人大",
     "level": "县处级", "parent": "固原市人民代表大会常务委员会",
     "location": "宁夏回族自治区固原市泾源县"},
    {"id": 6, "name": "政协泾源县委员会", "type": "政协",
     "level": "县处级", "parent": "政协固原市委员会",
     "location": "宁夏回族自治区固原市泾源县"},
    {"id": 7, "name": "中共固原市委员会", "type": "党委",
     "level": "地厅级", "parent": "中共宁夏回族自治区委员会",
     "location": "宁夏回族自治区固原市"},
    {"id": 8, "name": "固原市人民政府", "type": "政府",
     "level": "地厅级", "parent": "宁夏回族自治区人民政府",
     "location": "宁夏回族自治区固原市"},
]

# ── Positions ──────────────────────────────────────────────────────────
positions = [
    # Core leadership
    {"person_id": 1, "org_id": 1, "title": "泾源县委书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "泾源县委副书记",
     "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长",
     "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # Standing Committee
    {"person_id": 3, "org_id": 1, "title": "县委副书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "县委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "常务副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "县委常委、县纪委书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "县纪委书记、县监委主任",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "县委常委、组织部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "县委常委、宣传部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "县委常委、政法委书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "县委常委、统战部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # Government deputies
    {"person_id": 10, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # People's Congress and Political Consultative Conference
    {"person_id": 12, "org_id": 5, "title": "泾源县人大常委会主任",
     "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 13, "org_id": 6, "title": "政协泾源县委员会主席",
     "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────
relationships = [
    # Top leadership core
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县长，党政主要领导工作搭档",
     "overlap_org": "中共泾源县委员会/泾源县人民政府",
     "overlap_period": "current"},
    # Party Secretary — Standing Committee
    {"person_a": 3, "person_b": 1, "type": "overlap",
     "context": "县委副书记协助县委书记工作",
     "overlap_org": "中共泾源县委员会", "overlap_period": "current"},
    {"person_a": 5, "person_b": 1, "type": "overlap",
     "context": "县纪委书记与县委书记工作关系",
     "overlap_org": "中共泾源县委员会", "overlap_period": "current"},
    {"person_a": 6, "person_b": 1, "type": "overlap",
     "context": "组织部部长与县委书记工作关系",
     "overlap_org": "中共泾源县委员会", "overlap_period": "current"},
    {"person_a": 7, "person_b": 1, "type": "overlap",
     "context": "宣传部部长与县委书记工作关系",
     "overlap_org": "中共泾源县委员会", "overlap_period": "current"},
    {"person_a": 8, "person_b": 1, "type": "overlap",
     "context": "政法委书记与县委书记工作关系",
     "overlap_org": "中共泾源县委员会", "overlap_period": "current"},
    {"person_a": 9, "person_b": 1, "type": "overlap",
     "context": "统战部部长与县委书记工作关系",
     "overlap_org": "中共泾源县委员会", "overlap_period": "current"},
    # County Chief — Deputy relationships
    {"person_a": 4, "person_b": 2, "type": "superior_subordinate",
     "context": "常务副县长协助县长工作",
     "overlap_org": "泾源县人民政府", "overlap_period": "current"},
    {"person_a": 10, "person_b": 2, "type": "superior_subordinate",
     "context": "副县长协助县长工作",
     "overlap_org": "泾源县人民政府", "overlap_period": "current"},
    {"person_a": 11, "person_b": 2, "type": "superior_subordinate",
     "context": "副县长协助县长工作",
     "overlap_org": "泾源县人民政府", "overlap_period": "current"},
    # Standing Committee peer relationships
    {"person_a": 4, "person_b": 3, "type": "overlap",
     "context": "县委常委班子工作关系",
     "overlap_org": "中共泾源县委员会", "overlap_period": "current"},
    {"person_a": 5, "person_b": 6, "type": "overlap",
     "context": "纪委与组织部工作联系",
     "overlap_org": "中共泾源县委员会", "overlap_period": "current"},
    {"person_a": 7, "person_b": 9, "type": "overlap",
     "context": "宣传与统战工作联系",
     "overlap_org": "中共泾源县委员会", "overlap_period": "current"},
    # County Government peer relationships
    {"person_a": 10, "person_b": 11, "type": "overlap",
     "context": "县政府领导班子成员",
     "overlap_org": "泾源县人民政府", "overlap_period": "current"},
    # Party Committee — Government cross relationships
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "副书记与常务副县长工作联系",
     "overlap_org": "中共泾源县委员会/泾源县人民政府",
     "overlap_period": "current"},
    # NPC and CPPCC leadership
    {"person_a": 12, "person_b": 1, "type": "overlap",
     "context": "人大主任与县委书记工作关系",
     "overlap_org": "中共泾源县委员会", "overlap_period": "current"},
    {"person_a": 13, "person_b": 1, "type": "overlap",
     "context": "政协主席与县委书记工作关系",
     "overlap_org": "中共泾源县委员会", "overlap_period": "current"},
    # Predecessor relationships (固原市 level connection)
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "上报固原市委市政府的工作关系",
     "overlap_org": "中共固原市委员会/固原市人民政府",
     "overlap_period": "current"},
]

# ── Person JSON data ────────────────────────────────────────────────────
PERSON_JSON_TEMPLATE = {
    "schema_version": "1.0",
    "generated_at": TODAY,
    "investigation_scope": {
        "province": "宁夏回族自治区",
        "city": "固原市",
        "region": "泾源县",
        "job": "",
        "task_id": "ningxia_泾源县",
        "time_focus": "current"
    },
    "identity": {
        "person_id": "",
        "name": "",
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
        "current_post": "",
        "current_org": "",
        "administrative_rank": "",
        "as_of": AS_OF,
        "is_current_confirmed": False,
        "source_ids": []
    },
    "career_timeline": [
        {
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "网络访问严重受限，未能获取该人物的任何履历信息。需从泾源县政府官网领导之窗、固原市委组织部任前公示公告或百度百科等来源补充。",
            "confidence": "unverified",
            "source_ids": []
        }
    ],
    "organizations": [],
    "relationships": [],
    "governance_record": [],
    "professional_profile": {
        "primary_specializations": [],
        "secondary_specializations": [],
        "career_pattern": "unknown",
        "systems_experience": [],
        "geographic_pattern": [],
        "promotion_velocity": {
            "summary": "未知 — 网络访问受限，未获取到履历信息",
            "notable_fast_promotions": []
        }
    },
    "work_style_and_personality": {
        "public_style_indicators": [],
        "speech_themes": [],
        "management_signals": [],
        "caveat": "Web access was severely degraded during research. No work style data could be gathered."
    },
    "network_metrics": {
        "direct_reports": [],
        "peer_relations": [],
        "organizational_affiliations": [],
        "centrality_estimate": "unknown"
    },
    "risk_and_integrity_signals": [
        {
            "type": "none_found",
            "description": "截至2026年7月，由于网络访问受限，未能检索到该人物的任何纪律审查、审计问题或负面媒体报道信息。",
            "date": AS_OF,
            "confidence": "unverified",
            "source_ids": []
        }
    ],
    "source_register": [
        {
            "id": "S001",
            "title": "泾源县人民政府 - 领导之窗（预期URL）",
            "url": "http://www.nxjingyuan.gov.cn/xxgk/ldzc/",
            "publisher": "泾源县人民政府",
            "published_at": AS_OF,
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "官方领导之窗页面（网络访问受限，未能访问）"
        },
        {
            "id": "S002",
            "title": "固原市人民政府 - 领导之窗",
            "url": "http://www.guyuan.gov.cn/xxgk/ldzc/",
            "publisher": "固原市人民政府",
            "published_at": AS_OF,
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "固原市官方领导之窗（网络访问受限，未能访问）"
        }
    ],
    "confidence_summary": {
        "identity": "unverified",
        "current_role": "unverified",
        "career_completeness": "thin",
        "relationship_confidence": "low",
        "biggest_gap": "所有人物的姓名、履历因网络完全不可用而缺失。需要从泾源县政府官网领导之窗、固原市委组织部任前公示等官方渠道补充。"
    },
    "open_questions": [
        {
            "priority": "critical",
            "question": "现任泾源县委书记的姓名和履历是什么？",
            "why_it_matters": "核心调查目标——县级一把手，关系网络的核心节点",
            "suggested_queries": ["泾源县委书记 2025 2026 现任", "泾源县 县委书记 简历"],
            "last_attempted": AS_OF
        },
        {
            "priority": "critical",
            "question": "现任泾源县县长的姓名和履历是什么？",
            "why_it_matters": "核心调查目标——县政府一把手",
            "suggested_queries": ["泾源县县长 2025 2026 现任", "泾源县 县长 简历"],
            "last_attempted": AS_OF
        },
        {
            "priority": "high",
            "question": "泾源县县委常委班子成员的姓名和分管工作？",
            "why_it_matters": "构建县领导班子关系图谱的基础",
            "suggested_queries": ["泾源县 县委常委", "泾源县 领导班子 2025"],
            "last_attempted": AS_OF
        },
        {
            "priority": "high",
            "question": "泾源县前任县委书记的去向？",
            "why_it_matters": "了解干部晋升通道和交流网络",
            "suggested_queries": ["泾源县 前任县委书记", "泾源县委原书记"],
            "last_attempted": AS_OF
        },
        {
            "priority": "medium",
            "question": "泾源县人大常委会主任和政协主席的姓名？",
            "why_it_matters": "完善县级领导班子的完整图谱",
            "suggested_queries": ["泾源县人大主任", "泾源县政协主席"],
            "last_attempted": AS_OF
        }
    ]
}


def write_person_json(person_id: int, name: str, post: str, org: str, rank: str,
                      filename_suffix: str) -> None:
    """Write a person JSON file to the staging directory."""
    data = PERSON_JSON_TEMPLATE.copy()
    data["investigation_scope"]["job"] = post
    data["identity"]["person_id"] = f"jingyuan_{name}"
    data["identity"]["name"] = name
    data["current_status"]["current_post"] = post
    data["current_status"]["current_org"] = org
    data["current_status"]["administrative_rank"] = rank
    # Relationships (only for the two core leaders)
    if person_id == 1:
        data["relationships"].append({
            "person": "待查_县长",
            "person_id": "jingyuan_待查_县长",
            "relationship_type": "superior_subordinate",
            "strength": "strong",
            "evidence": "县委书记与县长为党政主要领导工作搭档关系",
            "overlap_org": "中共泾源县委员会",
            "overlap_period": "current",
            "direction": "undirected",
            "confidence": "unverified",
            "source_ids": []
        })
    if person_id == 2:
        data["relationships"].append({
            "person": "待查_县委书记",
            "person_id": "jingyuan_待查_县委书记",
            "relationship_type": "superior_subordinate",
            "strength": "strong",
            "evidence": "县长与县委书记为党政主要领导工作搭档关系",
            "overlap_org": "中共泾源县委员会",
            "overlap_period": "current",
            "direction": "undirected",
            "confidence": "unverified",
            "source_ids": []
        })
    filename = f"{TODAY}-宁夏回族自治区-固原市-{filename_suffix}.json"
    path = PJSON_DIR / filename
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {path}")


# ── Build ──────────────────────────────────────────────────────────────
def main() -> None:
    print(f"Building {SLUG} leadership network...")
    print(f"  Staging: {STAGING}")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

    # Build database and GEXF
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

    # Write person JSONs for core leaders
    print("  Writing person JSONs...")
    write_person_json(1, "待查_县委书记", "泾源县委书记",
                      "中共泾源县委员会", "县处级正职", "县委书记-待查")
    write_person_json(2, "待查_县长", "泾源县委副书记、县长",
                      "泾源县人民政府", "县处级正职", "县长-待查")

    print(f"\nDone. Staged artifacts in: {STAGING}")
    print(f"  1. Build script: {__file__}")
    print(f"  2. Database: {DB_PATH}")
    print(f"  3. GEXF: {GEXF_PATH}")
    print(f"  4. Person JSONs: {PJSON_DIR}")


if __name__ == "__main__":
    main()
