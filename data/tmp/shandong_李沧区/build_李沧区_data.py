#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 青岛市李沧区 leadership network.

Investigation date: 2026-07-25
Task ID: shandong_李沧区
Level: 市辖区（副厅级）
Targets: 区委书记 & 区长

Research sources:
  - Web search was completely blocked: Exa rate-limited, Baidu 403, government sites
    DNS failures (qingdaolicang.gov.cn, licang.gov.cn NXDOMAIN), Wikipedia timed out,
    Google/Bing blocked automated access.
  - No existing artifacts for 李沧区 found in the repository.
  - The parent-city 青岛市 build script (scripts/build/build_青岛市_data.py) does not
    contain 李沧区-specific leadership info.

Confidence notes:
  - All leadership info is marked as unverified due to zero web access.
  - The 李沧区 government website (qingdaolicang.gov.cn) DNS does not resolve,
    suggesting the domain may have changed or the site is offline.
  - 李沧区 is confirmed to be a district of 青岛市 (from Wikipedia Qingdao page).
  - All specific officeholder names, biographies, and relationships are UNVERIFIED
    and need to be filled in when web access is available.
"""

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
for parent_count in [3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "山东省青岛市李沧区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shandong_李沧区"
if _CURRENT_DIR.name == "shandong_李沧区":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / "李沧区_network.db"
GEXF_PATH = STAGING / "李沧区_network.gexf"
PJSON_DIR = STAGING

# ═══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ═══════════════════════════════════════════════════════════════════════════════
# Due to complete web access degradation, all officeholder names are unverified.
# Key: 1-5 current leadership, 6-10 deputies, 11+ predecessors
persons = [
    # ══════════════════════════════════════════════════
    # Current Leadership (区委 — Party Committee)
    # ══════════════════════════════════════════════════
    {
        "id": 1,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共青岛市李沧区委书记",
        "current_org": "中共青岛市李沧区委员会",
        "source": "待确认——李沧区政府官网 (qingdaolicang.gov.cn) 无法访问。建议通过青岛市政府官网或青岛市委组织部任前公示查询",
        "confidence": "unverified",
        "notes": "李沧区委书记。因政府网站DNS解析失败，具体姓名未能获取。建议搜索'李沧区委书记'或查阅青岛市委组织部公告",
    },
    {
        "id": 2,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共青岛市李沧区委副书记、区长",
        "current_org": "青岛市李沧区人民政府",
        "source": "待确认——李沧区政府官网 (qingdaolicang.gov.cn) 无法访问。建议通过青岛市政府官网或李沧区人大常委会任命公告查询",
        "confidence": "unverified",
        "notes": "李沧区长。因政府网站DNS解析失败，具体姓名未能获取。建议搜索'李沧区长'或查阅李沧区人大常委会公告",
    },
    {
        "id": 3,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共青岛市李沧区委副书记",
        "current_org": "中共青岛市李沧区委员会",
        "source": "待确认",
        "confidence": "unverified",
        "notes": "区委副书记（通常兼任区长或专职副书记）",
    },
    # ══════════════════════════════════════════════════
    # Key Deputies (常委 — Standing Committee)
    # ══════════════════════════════════════════════════
    {
        "id": 4,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "李沧区纪委书记、监委主任",
        "current_org": "中共青岛市李沧区纪律检查委员会",
        "source": "待确认",
        "confidence": "unverified",
        "notes": "区纪委书记（区委常委）",
    },
    {
        "id": 5,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "李沧区委组织部部长",
        "current_org": "中共青岛市李沧区委组织部",
        "source": "待确认",
        "confidence": "unverified",
        "notes": "区委组织部长（区委常委）",
    },
    {
        "id": 6,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "李沧区委政法委书记",
        "current_org": "中共青岛市李沧区委政法委员会",
        "source": "待确认",
        "confidence": "unverified",
        "notes": "区委政法委书记（区委常委）",
    },
    {
        "id": 7,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "李沧区委宣传部部长",
        "current_org": "中共青岛市李沧区委宣传部",
        "source": "待确认",
        "confidence": "unverified",
        "notes": "区委宣传部长（区委常委）",
    },
    # ══════════════════════════════════════════════════
    # Government Deputy Heads
    # ══════════════════════════════════════════════════
    {
        "id": 8,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "李沧区常务副区长",
        "current_org": "青岛市李沧区人民政府",
        "source": "待确认",
        "confidence": "unverified",
        "notes": "常务副区长",
    },
    {
        "id": 9,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "李沧区副区长",
        "current_org": "青岛市李沧区人民政府",
        "source": "待确认",
        "confidence": "unverified",
        "notes": "副区长之一",
    },
    # ══════════════════════════════════════════════════
    # People's Congress & Political Consultative
    # ══════════════════════════════════════════════════
    {
        "id": 10,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "李沧区人大常委会主任",
        "current_org": "青岛市李沧区人大常委会",
        "source": "待确认",
        "confidence": "unverified",
        "notes": "区人大常委会主任",
    },
    {
        "id": 11,
        "name": "待确认",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "李沧区政协主席",
        "current_org": "中国人民政治协商会议青岛市李沧区委员会",
        "source": "待确认",
        "confidence": "unverified",
        "notes": "区政协主席",
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ═══════════════════════════════════════════════════════════════════════════════
organizations = [
    {"id": 1, "name": "中共青岛市李沧区委员会", "type": "党委", "level": "副厅级", "parent": "中共青岛市委", "location": "山东省青岛市李沧区"},
    {"id": 2, "name": "青岛市李沧区人民政府", "type": "政府", "level": "副厅级", "parent": "青岛市人民政府", "location": "山东省青岛市李沧区"},
    {"id": 3, "name": "中共青岛市李沧区纪律检查委员会", "type": "党委", "level": "副厅级", "parent": "中共青岛市纪委", "location": "山东省青岛市李沧区"},
    {"id": 4, "name": "中共青岛市李沧区委组织部", "type": "党委", "level": "正处级", "parent": "中共青岛市李沧区委员会", "location": "山东省青岛市李沧区"},
    {"id": 5, "name": "中共青岛市李沧区委政法委员会", "type": "党委", "level": "正处级", "parent": "中共青岛市李沧区委员会", "location": "山东省青岛市李沧区"},
    {"id": 6, "name": "中共青岛市李沧区委宣传部", "type": "党委", "level": "正处级", "parent": "中共青岛市李沧区委员会", "location": "山东省青岛市李沧区"},
    {"id": 7, "name": "青岛市李沧区人大常委会", "type": "人大", "level": "副厅级", "parent": "青岛市人大常委会", "location": "山东省青岛市李沧区"},
    {"id": 8, "name": "中国人民政治协商会议青岛市李沧区委员会", "type": "政协", "level": "副厅级", "parent": "青岛市政协", "location": "山东省青岛市李沧区"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ═══════════════════════════════════════════════════════════════════════════════
positions = [
    # 区委书记（待确认）
    {"person_id": 1, "org_id": 1, "title": "中共青岛市李沧区委书记",
     "start_date": "", "end_date": "", "rank": "副厅级",
     "note": "主持区委全面工作，因web访问受限，具体姓名待确认"},
    # 区长（待确认）
    {"person_id": 2, "org_id": 1, "title": "中共青岛市李沧区委副书记",
     "start_date": "", "end_date": "", "rank": "副厅级",
     "note": "兼任区政府党组书记"},
    {"person_id": 2, "org_id": 2, "title": "青岛市李沧区区长",
     "start_date": "", "end_date": "", "rank": "副厅级",
     "note": "主持区政府全面工作"},
    # 区委副书记（待确认）
    {"person_id": 3, "org_id": 1, "title": "中共青岛市李沧区委副书记",
     "start_date": "", "end_date": "", "rank": "副厅级",
     "note": "专职副书记"},
    # 纪委书记（待确认）
    {"person_id": 4, "org_id": 3, "title": "李沧区纪委书记、监委主任",
     "start_date": "", "end_date": "", "rank": "副厅级",
     "note": "区委常委"},
    # 组织部长（待确认）
    {"person_id": 5, "org_id": 4, "title": "李沧区委组织部部长",
     "start_date": "", "end_date": "", "rank": "正处级",
     "note": "区委常委"},
    # 政法委书记（待确认）
    {"person_id": 6, "org_id": 5, "title": "李沧区委政法委书记",
     "start_date": "", "end_date": "", "rank": "正处级",
     "note": "区委常委"},
    # 宣传部长（待确认）
    {"person_id": 7, "org_id": 6, "title": "李沧区委宣传部部长",
     "start_date": "", "end_date": "", "rank": "正处级",
     "note": "区委常委"},
    # 常务副区长（待确认）
    {"person_id": 8, "org_id": 2, "title": "李沧区常务副区长",
     "start_date": "", "end_date": "", "rank": "副厅级",
     "note": "区委常委、区政府党组副书记"},
    # 副区长（待确认）
    {"person_id": 9, "org_id": 2, "title": "李沧区副区长",
     "start_date": "", "end_date": "", "rank": "副局级",
     "note": ""},
    # 人大主任（待确认）
    {"person_id": 10, "org_id": 7, "title": "李沧区人大常委会主任",
     "start_date": "", "end_date": "", "rank": "副厅级",
     "note": ""},
    # 政协主席（待确认）
    {"person_id": 11, "org_id": 8, "title": "李沧区政协主席",
     "start_date": "", "end_date": "", "rank": "副厅级",
     "note": ""},
]

# ═══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ═══════════════════════════════════════════════════════════════════════════════
relationships = [
    # 区委书记 ↔ 区长
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记与区长党政工作搭档关系",
     "overlap_org": "中共青岛市李沧区委员会", "overlap_period": "当前"},
    # 区委书记 ↔ 区委副书记
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "区委书记与专职副书记工作关系",
     "overlap_org": "中共青岛市李沧区委员会", "overlap_period": "当前"},
    # 区委书记 ↔ 纪委书记
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "区委书记与纪委书记——党委与纪检系统关系",
     "overlap_org": "中共青岛市李沧区委员会", "overlap_period": "当前"},
    # 区委书记 ↔ 组织部长
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "区委书记与组织部长——干部管理工作关系",
     "overlap_org": "中共青岛市李沧区委员会", "overlap_period": "当前"},
    # 区长 ↔ 常务副区长
    {"person_a": 2, "person_b": 8, "type": "overlap",
     "context": "区长与常务副区长——政府日常工作搭档",
     "overlap_org": "青岛市李沧区人民政府", "overlap_period": "当前"},
    # 区长 ↔ 副区长
    {"person_a": 2, "person_b": 9, "type": "overlap",
     "context": "区长与副区长上下级工作关系",
     "overlap_org": "青岛市李沧区人民政府", "overlap_period": "当前"},
    # 政法委书记 ↔ 纪委书记
    {"person_a": 4, "person_b": 6, "type": "overlap",
     "context": "纪委书记与政法委书记——法治与纪律工作关系",
     "overlap_org": "中共青岛市李沧区委员会", "overlap_period": "当前"},
]


# ═══════════════════════════════════════════════════════════════════════════════
# PERSON JSONS
# ═══════════════════════════════════════════════════════════════════════════════

def write_person_jsons():
    """Write individual person graph JSON files for core figures."""

    # ── 区委书记 ──
    party_secretary = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "山东省",
            "city": "青岛市",
            "region": "李沧区",
            "job": "区委书记",
            "task_id": "shandong_李沧区",
            "time_focus": "2024-2026",
        },
        "identity": {
            "person_id": "licang_party_secretary_unknown",
            "name": "待确认",
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
                "name_birth": "待确认_",
                "name_birthplace": "待确认_",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": "中共青岛市李沧区委书记",
            "current_org": "中共青岛市李沧区委员会",
            "administrative_rank": "副厅级",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": [],
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "unknown",
                "org": "",
                "title": "全部履历",
                "level": "",
                "location": "",
                "system": "other",
                "rank": "",
                "is_key_promotion": False,
                "notes": "因web搜索完全受限（Exa限速、Baidu 403、政府网站DNS失效），无法获取当前区委书记姓名及履历",
                "confidence": "unverified",
                "source_ids": [],
            },
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
                "summary": "完全未知——web访问完全受限",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "无法获取任何公开资料",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "因web访问受限，无法搜索到任何关于李沧区委书记的纪律处分或负面报道信息",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": [],
            },
        ],
        "source_register": [],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "全部——因web访问完全受限，无法获取李沧区委书记的姓名、出生信息、教育背景、履历等任何资料",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "现任李沧区委书记是谁？",
                "why_it_matters": "核心调查目标——区委书记是李沧区最高领导",
                "suggested_queries": [
                    "李沧区委书记",
                    "青岛市李沧区 区委书记 2025 2026",
                    "李沧区 领导之窗 区委书记",
                    "site:qingdao.gov.cn 李沧区 区委书记",
                    "青岛市 李沧区 区委书记 任命",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": "李沧区委书记的出生年月、籍贯、教育背景是什么？",
                "why_it_matters": "核心身份信息",
                "suggested_queries": ["李沧区委书记 简历", "李沧区委书记 出生"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": "李沧区委书记的早期履历（区委书记之前）是什么？",
                "why_it_matters": "了解晋升路径和人脉网络",
                "suggested_queries": ["李沧区委书记 任职经历", "李沧区委书记 前任职务"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "李沧区前任区委书记是谁？调任何处？",
                "why_it_matters": "掌握区委书记的权力交接链条",
                "suggested_queries": ["李沧区 前任区委书记", "李沧区委书记 卸任"],
                "last_attempted": AS_OF,
            },
        ],
    }

    party_path = STAGING / f"{TODAY}-山东省-青岛市-区委书记-待确认.json"
    with open(party_path, "w", encoding="utf-8") as f:
        json.dump(party_secretary, f, ensure_ascii=False, indent=2)
    print(f"  ✅ Person JSON: {party_path}")

    # ── 区长 ──
    mayor = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "山东省",
            "city": "青岛市",
            "region": "李沧区",
            "job": "区长",
            "task_id": "shandong_李沧区",
            "time_focus": "2024-2026",
        },
        "identity": {
            "person_id": "licang_mayor_unknown",
            "name": "待确认",
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
                "name_birth": "待确认_",
                "name_birthplace": "待确认_",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": "中共青岛市李沧区委副书记、区长",
            "current_org": "青岛市李沧区人民政府",
            "administrative_rank": "副厅级",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": [],
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "unknown",
                "org": "",
                "title": "全部履历",
                "level": "",
                "location": "",
                "system": "other",
                "rank": "",
                "is_key_promotion": False,
                "notes": "因web搜索完全受限（Exa限速、Baidu 403、政府网站DNS失效），无法获取当前区长姓名及履历",
                "confidence": "unverified",
                "source_ids": [],
            },
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
                "summary": "完全未知——web访问完全受限",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "无法获取任何公开资料",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "因web访问受限，无法搜索到任何关于李沧区区长的纪律处分或负面报道信息",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": [],
            },
        ],
        "source_register": [],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "全部——因web访问完全受限，无法获取李沧区区长的姓名、出生信息、教育背景、履历等任何资料",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "现任李沧区长是谁？",
                "why_it_matters": "核心调查目标——区长是李沧区政府最高领导",
                "suggested_queries": [
                    "李沧区长",
                    "青岛市李沧区 区长 2025 2026",
                    "李沧区人大常委会 区长 任命",
                    "site:qingdao.gov.cn 李沧区 区长",
                    "青岛市 李沧区 区长 姓名",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": "李沧区区长的出生年月、籍贯、教育背景是什么？",
                "why_it_matters": "核心身份信息",
                "suggested_queries": ["李沧区长 简历", "李沧区长 出生"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": "李沧区区长的早期履历（区长之前）是什么？",
                "why_it_matters": "了解晋升路径和人脉网络",
                "suggested_queries": ["李沧区长 任职经历", "李沧区长 前任职务"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "李沧区前任区长是谁？调任何处？",
                "why_it_matters": "掌握区长的权力交接链条",
                "suggested_queries": ["李沧区 前任区长", "李沧区长 卸任"],
                "last_attempted": AS_OF,
            },
        ],
    }

    mayor_path = STAGING / f"{TODAY}-山东省-青岛市-区长-待确认.json"
    with open(mayor_path, "w", encoding="utf-8") as f:
        json.dump(mayor, f, ensure_ascii=False, indent=2)
    print(f"  ✅ Person JSON: {mayor_path}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
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

    write_person_jsons()

    print(f"\n✅ Build complete: {DB_PATH}")
    print(f"✅ GEXF complete: {GEXF_PATH}")
    print("\n⚠️  NOTE: All leadership data is marked as '待确认' (unverified) due to")
    print("   complete web access degradation (Exa rate-limited, Baidu 403,")
    print("   government sites DNS failure, Wikipedia/Google/Bing blocked).")
    print("   Please re-run with functioning web access to fill in actual names.")


if __name__ == "__main__":
    main()
