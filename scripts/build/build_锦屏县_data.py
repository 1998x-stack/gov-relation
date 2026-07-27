#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 锦屏县 leadership network.

Task: guizhou_锦屏县
Province: 贵州省
Parent City: 黔东南苗族侗族自治州
Region: 锦屏县
Level: 县级
Targets: 县委书记 (Party Secretary), 县长 (County Mayor)

Investigation Date: 2026-07-23

Confirmed Findings (Phase 1 & 2 Research):
1. 唐标 (male) - Current 锦屏县委书记 (confirmed by multiple Jinping government
   news articles showing "唐标带队" activities alongside 张以东).
2. 张以东 (male) - Current 县委副书记、县长 (confirmed by official website leadership
   section at "领导之窗").
3. Government leadership team confirmed:
   - 莫昌良 - 县委常委、常务副县长
   - 谢枝清 - 县委常委、副县长
   - 卢秋米 - 副县长
   - 李作维 - 副县长
   - 黄万辉 - 副县长
   - 林少丛 - 副县长
4. Official source: https://www.jinping.gov.cn/zwgk/ (领导之窗 section)
5. 唐标 previously served as 锦屏县长 before being promoted to 县委书记.
6. Key news articles from July 2026 show active leadership.

Important notes:
- 唐标's identity details (birth year, birthplace, education) not found on official site
  — full biography needs deeper research.
- 张以东's identity details similarly sparse on official site.
- Predecessor names are not directly confirmed (舒勇 is a potential previous 县委书记,
  but unconfirmed as the immediate predecessor).
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

_HERE = os.path.dirname(os.path.abspath(__file__))
_BASE = os.path.normpath(os.path.join(_HERE, "..", "..", ".."))
if _BASE not in sys.path:
    sys.path.insert(0, _BASE)

from gov_relation.runner import run_build
from gov_relation.paths import REPO_ROOT

AS_OF = "2026-07-23"
STAGING_DIR = _HERE
DB_PATH = os.path.join(STAGING_DIR, "锦屏县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "锦屏县_network.gexf")
PERSONS_DIR = STAGING_DIR

# =========================================================================
# DATA
# =========================================================================

# ── Persons ──────────────────────────────────────────────────────────
persons = [
    # Current leadership
    {"id": 1, "name": "唐标", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "锦屏县委书记", "current_org": "中共锦屏县委员会",
     "source": "https://www.jinping.gov.cn/"},
    {"id": 2, "name": "张以东", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "锦屏县委副书记、县长", "current_org": "锦屏县人民政府",
     "source": "https://www.jinping.gov.cn/zwgk/"},

    # Government leadership team
    {"id": 3, "name": "莫昌良", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "锦屏县委常委、常务副县长", "current_org": "锦屏县人民政府",
     "source": "https://www.jinping.gov.cn/zwgk/"},
    {"id": 4, "name": "谢枝清", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "锦屏县委常委、副县长", "current_org": "锦屏县人民政府",
     "source": "https://www.jinping.gov.cn/zwgk/"},
    {"id": 5, "name": "卢秋米", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "锦屏县副县长", "current_org": "锦屏县人民政府",
     "source": "https://www.jinping.gov.cn/zwgk/"},
    {"id": 6, "name": "李作维", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "锦屏县副县长", "current_org": "锦屏县人民政府",
     "source": "https://www.jinping.gov.cn/zwgk/"},
    {"id": 7, "name": "黄万辉", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "锦屏县副县长", "current_org": "锦屏县人民政府",
     "source": "https://www.jinping.gov.cn/zwgk/"},
    {"id": 8, "name": "林少丛", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "锦屏县副县长", "current_org": "锦屏县人民政府",
     "source": "https://www.jinping.gov.cn/zwgk/"},
]

# ── Organizations ────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共锦屏县委员会", "type": "党委",
     "level": "县级", "parent": "中共黔东南苗族侗族自治州委员会",
     "location": "锦屏县三江镇"},
    {"id": 2, "name": "锦屏县人民政府", "type": "政府",
     "level": "县级", "parent": "黔东南苗族侗族自治州人民政府",
     "location": "锦屏县三江镇"},
    {"id": 3, "name": "锦屏县人大常委会", "type": "人大",
     "level": "县级", "parent": "黔东南州人大常委会",
     "location": "锦屏县三江镇"},
    {"id": 4, "name": "锦屏县政协", "type": "政协",
     "level": "县级", "parent": "黔东南州政协",
     "location": "锦屏县三江镇"},
    {"id": 5, "name": "锦屏县纪委监委", "type": "纪委",
     "level": "县级", "parent": "黔东南州纪委监委",
     "location": "锦屏县三江镇"},
    {"id": 6, "name": "贵州锦屏经济开发区管委会", "type": "开发区",
     "level": "县级", "parent": "锦屏县人民政府",
     "location": "锦屏县"},
    {"id": 7, "name": "中共黔东南苗族侗族自治州委员会", "type": "党委",
     "level": "地市级", "parent": "中共贵州省委员会",
     "location": "凯里市"},
    {"id": 8, "name": "黔东南苗族侗族自治州人民政府", "type": "政府",
     "level": "地市级", "parent": "贵州省人民政府",
     "location": "凯里市"},
    {"id": 9, "name": "黔东南州人大常委会", "type": "人大",
     "level": "地市级", "parent": "贵州省人大常委会",
     "location": "凯里市"},
    {"id": 10, "name": "黔东南州政协", "type": "政协",
     "level": "地市级", "parent": "贵州省政协",
     "location": "凯里市"},
    {"id": 11, "name": "黔东南州纪委监委", "type": "纪委",
     "level": "地市级", "parent": "贵州省纪委监委",
     "location": "凯里市"},
]

# ── Positions ────────────────────────────────────────────────────────
positions = [
    # 唐标 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "锦屏县委书记",
     "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "现任锦屏县委书记，具体到任时间待查。此前曾任锦屏县长。"},

    # 张以东 — 县长
    {"person_id": 2, "org_id": 2, "title": "锦屏县委副书记、县长",
     "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "现任锦屏县委副书记、县长。全面领导县人民政府和经开区管委会工作，分管财政、审计、粮食。"},
    {"person_id": 2, "org_id": 6, "title": "贵州锦屏经济开发区管委会主任（兼）",
     "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "领导经开区管委会全面工作"},

    # 莫昌良 — 常务副县长
    {"person_id": 3, "org_id": 2, "title": "锦屏县委常委、常务副县长",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "县委常委、常务副县长"},

    # 谢枝清 — 常委副县长
    {"person_id": 4, "org_id": 2, "title": "锦屏县委常委、副县长",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "县委常委、副县长"},

    # 卢秋米 — 副县长
    {"person_id": 5, "org_id": 2, "title": "锦屏县副县长",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "副县长"},

    # 李作维 — 副县长
    {"person_id": 6, "org_id": 2, "title": "锦屏县副县长",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "副县长"},

    # 黄万辉 — 副县长
    {"person_id": 7, "org_id": 2, "title": "锦屏县副县长",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "副县长"},

    # 林少丛 — 副县长
    {"person_id": 8, "org_id": 2, "title": "锦屏县副县长",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "副县长"},
]

# ── Relationships ────────────────────────────────────────────────────
relationships = [
    # 唐标 + 张以东 = 党政搭档
    {"person_a": 1, "person_b": 2,
     "type": "党政搭档",
     "context": "唐标（县委书记）与张以东（县委副书记、县长）为锦屏县党政主要领导搭档",
     "overlap_org": "锦屏县党政领导班子", "overlap_period": "现任"},

    # 莫昌良 — 在唐标领导下工作
    {"person_a": 3, "person_b": 1,
     "type": "上下级",
     "context": "莫昌良（县委常委、常务副县长）在唐标（县委书记）领导下工作",
     "overlap_org": "中共锦屏县委员会", "overlap_period": "现任"},

    # 莫昌良 — 在张以东领导下工作
    {"person_a": 3, "person_b": 2,
     "type": "上下级",
     "context": "莫昌良（常务副县长）在张以东（县长）领导下工作",
     "overlap_org": "锦屏县人民政府", "overlap_period": "现任"},

    # 谢枝清 — 在唐标领导下工作
    {"person_a": 4, "person_b": 1,
     "type": "上下级",
     "context": "谢枝清（县委常委、副县长）在唐标（县委书记）领导下工作",
     "overlap_org": "中共锦屏县委员会", "overlap_period": "现任"},

    # 谢枝清 — 在张以东领导下工作
    {"person_a": 4, "person_b": 2,
     "type": "上下级",
     "context": "谢枝清（副县长）在张以东（县长）领导下工作",
     "overlap_org": "锦屏县人民政府", "overlap_period": "现任"},

    # 卢秋米 — 在张以东领导下工作
    {"person_a": 5, "person_b": 2,
     "type": "上下级",
     "context": "卢秋米（副县长）在张以东（县长）领导下工作",
     "overlap_org": "锦屏县人民政府", "overlap_period": "现任"},

    # 李作维 — 在张以东领导下工作
    {"person_a": 6, "person_b": 2,
     "type": "上下级",
     "context": "李作维（副县长）在张以东（县长）领导下工作",
     "overlap_org": "锦屏县人民政府", "overlap_period": "现任"},

    # 黄万辉 — 在张以东领导下工作
    {"person_a": 7, "person_b": 2,
     "type": "上下级",
     "context": "黄万辉（副县长）在张以东（县长）领导下工作",
     "overlap_org": "锦屏县人民政府", "overlap_period": "现任"},

    # 林少丛 — 在张以东领导下工作
    {"person_a": 8, "person_b": 2,
     "type": "上下级",
     "context": "林少丛（副县长）在张以东（县长）领导下工作",
     "overlap_org": "锦屏县人民政府", "overlap_period": "现任"},
]


# =========================================================================
# Person JSON helpers
# =========================================================================

def make_person_json_tangbiao():
    """Create person JSON for 唐标 (current 锦屏县委书记)."""
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "贵州省",
            "city": "黔东南苗族侗族自治州",
            "region": "锦屏县",
            "job": "锦屏县委书记",
            "task_id": "guizhou_锦屏县",
            "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": "jinping_唐标",
            "name": "唐标",
            "aliases": [],
            "gender": "男",
            "ethnicity": "",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "唐标_",
                "name_birthplace": "唐标_",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": "锦屏县委书记",
            "current_org": "中共锦屏县委员会",
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": [
            {
                "start": "", "end": "",
                "org": "锦屏县人民政府",
                "title": "锦屏县长",
                "level": "县级", "location": "贵州省锦屏县",
                "system": "government", "rank": "正处级",
                "is_key_promotion": True,
                "notes": "此前曾任锦屏县长，具体任期待查",
                "confidence": "plausible",
                "source_ids": ["S001"]
            },
            {
                "start": "", "end": "present",
                "org": "中共锦屏县委员会",
                "title": "锦屏县委书记",
                "level": "县级", "location": "贵州省锦屏县",
                "system": "party", "rank": "正处级",
                "is_key_promotion": True,
                "notes": "现任锦屏县委书记。2026年5-7月多次出席领导活动（调研、汇报对接、慰问等）",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"]
            }
        ],
        "organizations": [],
        "relationships": [
            {
                "person": "张以东", "person_id": "jinping_张以东",
                "relationship_type": "overlap",
                "strength": "strong",
                "evidence": "唐标（县委书记）与张以东（县长）为锦屏县党政主要领导搭档",
                "overlap_org": "锦屏县党政领导班子",
                "overlap_period": "现任",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"]
            },
            {
                "person": "莫昌良", "person_id": "jinping_莫昌良",
                "relationship_type": "superior_subordinate",
                "strength": "medium",
                "evidence": "莫昌良（县委常委、常务副县长）在唐标领导下工作",
                "overlap_org": "中共锦屏县委员会",
                "overlap_period": "现任",
                "direction": "other_to_person",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "person": "谢枝清", "person_id": "jinping_谢枝清",
                "relationship_type": "superior_subordinate",
                "strength": "medium",
                "evidence": "谢枝清（县委常委、副县长）在唐标领导下工作",
                "overlap_org": "中共锦屏县委员会",
                "overlap_period": "现任",
                "direction": "other_to_person",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "governance_record": [
            {
                "period": "2026-07",
                "domain": "economic_development",
                "achievement_or_event": "带队到中国农业发展银行、国家体育总局汇报对接工作",
                "role_in_event": "县委书记（带队）",
                "measurable_outcome": "向上争取政策和资金支持",
                "location": "北京",
                "confidence": "confirmed",
                "source_ids": ["S002"]
            },
            {
                "period": "2026-06",
                "domain": "industry",
                "achievement_or_event": "到锦屏经济开发区调研走访服务企业",
                "role_in_event": "县委书记",
                "measurable_outcome": "调研企业发展状况",
                "location": "锦屏经济开发区",
                "confidence": "confirmed",
                "source_ids": ["S002"]
            },
            {
                "period": "2026-05",
                "domain": "discipline",
                "achievement_or_event": "督导调研群众身边不正之风和腐败问题集中整治工作",
                "role_in_event": "县委书记",
                "measurable_outcome": "推动整治工作落实",
                "location": "锦屏县",
                "confidence": "confirmed",
                "source_ids": ["S002"]
            },
            {
                "period": "2026-05",
                "domain": "public_security",
                "achievement_or_event": "督导调研防汛备汛、基层党建等工作，到三江镇督导地质灾害防治工作",
                "role_in_event": "县委书记",
                "measurable_outcome": "部署防汛和地质灾害防治",
                "location": "锦屏县平秋镇、彦洞乡、三江镇",
                "confidence": "confirmed",
                "source_ids": ["S002"]
            }
        ],
        "professional_profile": {
            "primary_specializations": ["县域治理", "产业发展", "党风廉政"],
            "secondary_specializations": ["经济开发区建设"],
            "career_pattern": "unknown",
            "systems_experience": ["government", "party"],
            "geographic_pattern": ["锦屏县"],
            "promotion_velocity": {
                "summary": "从县长晋升为县委书记，属于县内晋升的常规路径，具体晋升时间待查",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "grassroots_oriented",
                    "evidence": "多次赴乡镇督导调研基层党建、防汛备汛、地质灾害防治等工作",
                    "confidence": "plausible",
                    "source_ids": ["S002"]
                },
                {
                    "trait": "discipline_oriented",
                    "evidence": "督导调研群众身边不正之风和腐败问题集中整治工作",
                    "confidence": "plausible",
                    "source_ids": ["S002"]
                }
            ],
            "speech_themes": [],
            "management_signals": [
                "带队赴北京向上级汇报对接工作",
                "重视经济开发区发展",
                "关注基层党建和安全生产",
                "亲自督导防汛备汛和地质灾害防治"
            ],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "No risk signals found through available public sources",
            "date": "",
            "confidence": "unverified",
            "source_ids": []
        }],
        "source_register": [
            {
                "id": "S001",
                "title": "锦屏县人民政府 — 政务公开·领导之窗",
                "url": "https://www.jinping.gov.cn/zwgk/",
                "publisher": "锦屏县人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "确认张以东为县长，县政府领导班子名单。领导之窗页面仅展示政府口领导"
            },
            {
                "id": "S002",
                "title": "锦屏县人民政府 — 领导活动栏目",
                "url": "https://www.jinping.gov.cn/xwzx/ldhd/",
                "publisher": "锦屏县人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "确认唐标出席多项重要领导活动，身份为全县最高领导。2026年5-7月活动记录"
            }
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "high",
            "biggest_gap": "Full identity (birth year, birthplace, education, party join date, entry to public service, complete career timeline) all unknown"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "What is 唐标's full identity (birth year, birthplace, ethnicity, education, party join date, work start date)?",
                "why_it_matters": "Needed for deduplication and timeline completeness",
                "suggested_queries": ["唐标 简历 锦屏", "唐标 锦屏县委书记 简历", "唐标 黔东南"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": "When did 唐标 assume the role of 锦屏县委书记?",
                "why_it_matters": "Critical for establishing the leadership timeline",
                "suggested_queries": ["唐标 任锦屏县委书记", "锦屏县 县委书记 任命 唐标"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": "When exactly did 唐标 serve as 锦屏县长 and when was he promoted?",
                "why_it_matters": "Reveals the promotion timeline within Jinping county",
                "suggested_queries": ["唐标 锦屏县长 任职时间"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": "Who preceded 唐标 as 锦屏县委书记?",
                "why_it_matters": "Establishes the leadership turnover pattern",
                "suggested_queries": ["锦屏县 前任县委书记", "锦屏县 历届县委书记"],
                "last_attempted": AS_OF
            }
        ]
    }


def make_person_json_zhangyidong():
    """Create person JSON for 张以东 (current 锦屏县长)."""
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "贵州省",
            "city": "黔东南苗族侗族自治州",
            "region": "锦屏县",
            "job": "锦屏县委副书记、县长",
            "task_id": "guizhou_锦屏县",
            "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": "jinping_张以东",
            "name": "张以东",
            "aliases": [],
            "gender": "男",
            "ethnicity": "",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "张以东_",
                "name_birthplace": "张以东_",
                "official_profile_url": "https://www.jinping.gov.cn/zwgk/"
            }
        },
        "current_status": {
            "current_post": "锦屏县委副书记、县长",
            "current_org": "锦屏县人民政府",
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": [
            {
                "start": "", "end": "present",
                "org": "锦屏县人民政府",
                "title": "锦屏县委副书记、县长",
                "level": "县级", "location": "贵州省锦屏县",
                "system": "government", "rank": "正处级",
                "is_key_promotion": True,
                "notes": "现任锦屏县委副书记、县长。全面领导县人民政府和贵州锦屏经济开发区管委会工作，分管财政局、审计局。2026年6-7月出席多项活动（调研防溺水、水毁重建、高考备考、招商考察等）",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"]
            },
            {
                "start": "", "end": "present",
                "org": "贵州锦屏经济开发区管委会",
                "title": "贵州锦屏经济开发区管委会主任（兼）",
                "level": "县级", "location": "贵州省锦屏县",
                "system": "government", "rank": "正处级",
                "is_key_promotion": False,
                "notes": "兼任经开区管委会主任",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "organizations": [],
        "relationships": [
            {
                "person": "唐标", "person_id": "jinping_唐标",
                "relationship_type": "overlap",
                "strength": "strong",
                "evidence": "张以东（县长）与唐标（县委书记）为锦屏县党政主要领导搭档",
                "overlap_org": "锦屏县党政领导班子",
                "overlap_period": "现任",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"]
            },
            {
                "person": "莫昌良", "person_id": "jinping_莫昌良",
                "relationship_type": "superior_subordinate",
                "strength": "medium",
                "evidence": "莫昌良（常务副县长）在张以东（县长）领导下作为副手工作",
                "overlap_org": "锦屏县人民政府",
                "overlap_period": "现任",
                "direction": "other_to_person",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "person": "谢枝清", "person_id": "jinping_谢枝清",
                "relationship_type": "superior_subordinate",
                "strength": "medium",
                "evidence": "谢枝清（副县长）在张以东（县长）领导下工作",
                "overlap_org": "锦屏县人民政府",
                "overlap_period": "现任",
                "direction": "other_to_person",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "person": "卢秋米", "person_id": "jinping_卢秋米",
                "relationship_type": "superior_subordinate",
                "strength": "medium",
                "evidence": "卢秋米（副县长）在张以东（县长）领导下工作",
                "overlap_org": "锦屏县人民政府",
                "overlap_period": "现任",
                "direction": "other_to_person",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "person": "李作维", "person_id": "jinping_李作维",
                "relationship_type": "superior_subordinate",
                "strength": "medium",
                "evidence": "李作维（副县长）在张以东（县长）领导下工作",
                "overlap_org": "锦屏县人民政府",
                "overlap_period": "现任",
                "direction": "other_to_person",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "person": "黄万辉", "person_id": "jinping_黄万辉",
                "relationship_type": "superior_subordinate",
                "strength": "medium",
                "evidence": "黄万辉（副县长）在张以东（县长）领导下工作",
                "overlap_org": "锦屏县人民政府",
                "overlap_period": "现任",
                "direction": "other_to_person",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "person": "林少丛", "person_id": "jinping_林少丛",
                "relationship_type": "superior_subordinate",
                "strength": "medium",
                "evidence": "林少丛（副县长）在张以东（县长）领导下工作",
                "overlap_org": "锦屏县人民政府",
                "overlap_period": "现任",
                "direction": "other_to_person",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "governance_record": [
            {
                "period": "2026-07",
                "domain": "public_security",
                "achievement_or_event": "调研防溺水及水毁重建工作",
                "role_in_event": "县长（带队调研）",
                "measurable_outcome": "部署汛期安全和灾后重建",
                "location": "锦屏县",
                "confidence": "confirmed",
                "source_ids": ["S002"]
            },
            {
                "period": "2026-06",
                "domain": "education",
                "achievement_or_event": "到锦屏县中等职业学校讲授思想政治理论课",
                "role_in_event": "县长",
                "measurable_outcome": "推动学校思政教育",
                "location": "锦屏县中等职业学校",
                "confidence": "confirmed",
                "source_ids": ["S002"]
            },
            {
                "period": "2026-06",
                "domain": "other",
                "achievement_or_event": "到县政务服务中心调研",
                "role_in_event": "县长",
                "measurable_outcome": "推动政务服务质量提升",
                "location": "锦屏县政务服务中心",
                "confidence": "confirmed",
                "source_ids": ["S002"]
            },
            {
                "period": "2026-05",
                "domain": "education",
                "achievement_or_event": "调研督导高考备考工作",
                "role_in_event": "县长",
                "measurable_outcome": "检查高考备考准备工作",
                "location": "锦屏县",
                "confidence": "confirmed",
                "source_ids": ["S002"]
            },
            {
                "period": "2026-05",
                "domain": "economic_development",
                "achievement_or_event": "率队赴福建、江西、湖南等地开展招商考察活动",
                "role_in_event": "县长（率队）",
                "measurable_outcome": "推进招商引资工作",
                "location": "福建、江西、湖南",
                "confidence": "confirmed",
                "source_ids": ["S002"]
            }
        ],
        "professional_profile": {
            "primary_specializations": ["县域经济发展", "招商引资", "教育管理"],
            "secondary_specializations": ["政务服务"],
            "career_pattern": "unknown",
            "systems_experience": ["government", "party"],
            "geographic_pattern": ["锦屏县"],
            "promotion_velocity": {
                "summary": "现任锦屏县长，兼任经开区主任，具体晋升路径待查",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "pragmatic",
                    "evidence": "调研防溺水及水毁重建、督导高考备考、赴外省招商——工作聚焦实际事务",
                    "confidence": "plausible",
                    "source_ids": ["S002"]
                },
                {
                    "trait": "grassroots_oriented",
                    "evidence": "到政务服务中心、中等职业学校等一线单位调研",
                    "confidence": "plausible",
                    "source_ids": ["S002"]
                }
            ],
            "speech_themes": [],
            "management_signals": [
                "亲自率队赴多省招商考察",
                "关注高考备考和基础教育",
                "重视政务服务水平",
                "关心汛期安全和灾后重建"
            ],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "No risk signals found through available public sources",
            "date": "",
            "confidence": "unverified",
            "source_ids": []
        }],
        "source_register": [
            {
                "id": "S001",
                "title": "锦屏县人民政府 — 政务公开·领导之窗",
                "url": "https://www.jinping.gov.cn/zwgk/",
                "publisher": "锦屏县人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "确认张以东为锦屏县委副书记、县长，附领导分工"
            },
            {
                "id": "S002",
                "title": "锦屏县人民政府 — 领导活动栏目",
                "url": "https://www.jinping.gov.cn/xwzx/ldhd/",
                "publisher": "锦屏县人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "2026年5-7月张以东出席多项领导活动记录"
            }
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "high",
            "biggest_gap": "Full identity (birth year, birthplace, education, party join date, entry to public service, complete career timeline) all unknown"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "What is 张以东's full identity (birth year, birthplace, ethnicity, education, party join date, work start date)?",
                "why_it_matters": "Needed for deduplication and timeline completeness",
                "suggested_queries": ["张以东 简历 锦屏", "张以东 锦屏县长 个人简历"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": "When did 张以东 assume the role of 锦屏县长?",
                "why_it_matters": "Critical for establishing the leadership timeline",
                "suggested_queries": ["张以东 任锦屏县长", "锦屏县 县长 任命 张以东"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": "What was 张以东's position before becoming 锦屏县长?",
                "why_it_matters": "Reveals the career progression path",
                "suggested_queries": ["张以东 曾任", "张以东 黔东南"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": "Who preceded 张以东 as 锦屏县长?",
                "why_it_matters": "Establishes the leadership turnover pattern",
                "suggested_queries": ["锦屏县 前任县长", "锦屏县 县长 任免"],
                "last_attempted": AS_OF
            }
        ]
    }


def make_minimal_person_json(p, role_label):
    """Create a minimal person JSON for non-core leaders (deputy county mayors etc)."""
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "贵州省",
            "city": "黔东南苗族侗族自治州",
            "region": "锦屏县",
            "job": p["current_post"],
            "task_id": "guizhou_锦屏县",
            "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": f"jinping_{p['name']}",
            "name": p["name"],
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
                "name_birth": f"{p['name']}_",
                "name_birthplace": f"{p['name']}_",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p.get("current_org", ""),
            "administrative_rank": "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": [
            {
                "start": "", "end": "present",
                "org": p.get("current_org", ""),
                "title": p["current_post"],
                "level": "县级",
                "location": "贵州省锦屏县",
                "system": "government",
                "rank": "副处级",
                "is_key_promotion": False,
                "notes": f"现任{p['current_post']}，姓名通过县政府官网确认，具体履历待查",
                "confidence": "confirmed",
                "source_ids": ["S001"]
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
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "No risk signals found — limited public information",
            "date": "",
            "confidence": "unverified",
            "source_ids": []
        }],
        "source_register": [
            {
                "id": "S001",
                "title": "锦屏县人民政府 — 政务公开·领导之窗",
                "url": "https://www.jinping.gov.cn/zwgk/",
                "publisher": "锦屏县人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": f"确认{p['name']}职务为{p['current_post']}"
            }
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": f"Complete identity (birth, birthplace, education, career timeline) unknown for {p['name']}"
        },
        "open_questions": [
            {
                "priority": "high",
                "question": f"What is {p['name']}'s full identity (birth year, birthplace, education, party join date, career timeline)?",
                "why_it_matters": "Needed for deduplication and relationship analysis",
                "suggested_queries": [f"{p['name']} 锦屏县 简历"],
                "last_attempted": AS_OF
            }
        ]
    }


# =========================================================================
# BUILD
# =========================================================================

def build():
    print(f"=== Building 锦屏县 data ===")
    print(f"Staging dir: {STAGING_DIR}")
    print(f"AS_OF: {AS_OF}")
    print()

    # 1. Database + GEXF via gov_relation.runner
    run_build(
        slug="锦屏县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    # 2. Person JSONs
    person_jsons = []

    # 唐标 (县委书记)
    pj_tb = make_person_json_tangbiao()
    fname_tb = f"20260723-贵州省-黔东南苗族侗族自治州-县委书记-唐标.json"
    fpath_tb = os.path.join(PERSONS_DIR, fname_tb)
    with open(fpath_tb, "w", encoding="utf-8") as f:
        json.dump(pj_tb, f, ensure_ascii=False, indent=2)
    person_jsons.append(fpath_tb)
    print(f"Person JSON written: {fpath_tb}")

    # 张以东 (县长)
    pj_zyd = make_person_json_zhangyidong()
    fname_zyd = f"20260723-贵州省-黔东南苗族侗族自治州-县长-张以东.json"
    fpath_zyd = os.path.join(PERSONS_DIR, fname_zyd)
    with open(fpath_zyd, "w", encoding="utf-8") as f:
        json.dump(pj_zyd, f, ensure_ascii=False, indent=2)
    person_jsons.append(fpath_zyd)
    print(f"Person JSON written: {fpath_zyd}")

    # Other government team members (minimal person JSONs)
    deputy_names = {
        "莫昌良": "副县长-莫昌良",
        "谢枝清": "副县长-谢枝清",
        "卢秋米": "副县长-卢秋米",
        "李作维": "副县长-李作维",
        "黄万辉": "副县长-黄万辉",
        "林少丛": "副县长-林少丛",
    }
    for p in persons[2:]:  # skip 唐标 and 张以东
        label = deputy_names.get(p["name"], f"副职-{p['name']}")
        pj_min = make_minimal_person_json(p, label)
        fname_min = f"20260723-贵州省-黔东南苗族侗族自治州-{label}.json"
        fpath_min = os.path.join(PERSONS_DIR, fname_min)
        with open(fpath_min, "w", encoding="utf-8") as f:
            json.dump(pj_min, f, ensure_ascii=False, indent=2)
        person_jsons.append(fpath_min)
        print(f"Person JSON written: {fpath_min}")

    print()
    print("Build complete.")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
    print(f"  JSONs: {len(person_jsons)} files")


if __name__ == "__main__":
    build()
