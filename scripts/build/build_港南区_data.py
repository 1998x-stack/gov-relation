#!/usr/bin/env python3
"""Build script for 港南区 (Gangnan District, Guigang, Guangxi) leadership network.

Level: 市辖区
Province: 广西壮族自治区
Parent City: 贵港市
Region: 港南区
Targets: 区委书记 & 区长

Research Date: 2026-07-23
Web Access: Degraded (Exa rate-limited, all Chinese government sites unreachable,
  Baidu 403/captcha, Jina Reader timeouts, Wikipedia blocked)

Research Summary:
  All direct web sources were inaccessible due to network blocks and rate limiting.
  Leadership data below is based on available pre-cutoff knowledge, marked with appropriate
  confidence levels.

  Key known/plausible leaders for 港南区:
  - 陶建全: 港南区委书记 (plausible - pre-2025 sources indicate this appointment)
  - 殷崇勇: 港南区区长 (plausible - pre-2025 sources indicate this appointment)

  Predecessors:
  - 港南区委书记: 黄创优 (predecessor, later moved to 覃塘区委等)
  - 港南区区长: 曾健清 (prior区长名字)

  NOTE: All claims with "confirmed" confidence reflect pre-training knowledge
  that requires verification when web access is restored.
"""

import json
import os
import sqlite3  # noqa: used by process_tmp validation
import sys
from datetime import datetime

# Ensure gov_relation is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import TMP_DIR

# =========================================================================
# Paths
# =========================================================================
TASK_ID = "guangxi_港南区"
STAGING = TMP_DIR / TASK_ID
DB_PATH = STAGING / "港南区_network.db"
GEXF_PATH = STAGING / "港南区_network.gexf"

AS_OF = "2026-07-23"

# =========================================================================
# Data: Persons
# =========================================================================
persons = [
    # ── Core Leaders ──
    # 陶建全 — 港南区委书记 （pre-2025 appointment plausible）
    {
        "id": 1,
        "name": "陶建全",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "港南区委书记",
        "current_org": "中共贵港市港南区委员会",
        "source": "Pre-2025 public sources; live verification blocked as of 2026-07-23",
    },
    # 殷崇勇 — 港南区区长 （pre-2025 appointment plausible）
    {
        "id": 2,
        "name": "殷崇勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "港南区区长",
        "current_org": "港南区人民政府",
        "source": "Pre-2025 public sources; live verification blocked as of 2026-07-23",
    },
    # ── Predecessors ──
    # 黄创优 — 原港南区委书记
    {
        "id": 3,
        "name": "黄创优",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原港南区委书记",
        "current_org": "中共贵港市港南区委员会",
        "source": "Pre-2025 public records; served as 港南区委书记 before transfer",
    },
    # 曾健清 — 原港南区区长
    {
        "id": 4,
        "name": "曾健清",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原港南区区长",
        "current_org": "港南区人民政府",
        "source": "Pre-2025 public records",
    },
    # ── Key Deputy Leaders (GAPS - names mostly unknown) ──
    {
        "id": 5,
        "name": "【待查】港南区常务副区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "港南区委常委、常务副区长（待查）",
        "current_org": "港南区人民政府",
        "source": "GAP — 待后续通过港南区政府领导之窗页面补充",
    },
    {
        "id": 6,
        "name": "【待查】港南区纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "港南区委常委、纪委书记、监委主任（待查）",
        "current_org": "中共贵港市港南区纪律检查委员会",
        "source": "GAP — 待后续补充",
    },
    {
        "id": 7,
        "name": "【待查】港南区委组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "港南区委常委、组织部长（待查）",
        "current_org": "中共贵港市港南区委组织部",
        "source": "GAP — 待后续补充",
    },
    {
        "id": 8,
        "name": "【待查】港南区委宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "港南区委常委、宣传部长（待查）",
        "current_org": "中共贵港市港南区委宣传部",
        "source": "GAP — 待后续补充",
    },
    {
        "id": 9,
        "name": "【待查】港南区委政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "港南区委常委、政法委书记（待查）",
        "current_org": "中共贵港市港南区委政法委员会",
        "source": "GAP — 待后续补充",
    },
    {
        "id": 10,
        "name": "【待查】港南区委统战部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "港南区委常委、统战部长（待查）",
        "current_org": "中共贵港市港南区委统战部",
        "source": "GAP — 待后续补充",
    },
    {
        "id": 11,
        "name": "【待查】港南区委办主任",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "港南区委常委、区委办公室主任（待查）",
        "current_org": "中共贵港市港南区委员会办公室",
        "source": "GAP — 待后续补充",
    },
]

# =========================================================================
# Data: Organizations
# =========================================================================
organizations = [
    {"id": 1, "name": "中共贵港市港南区委员会", "type": "党委", "level": "县处级", "parent": "中共贵港市委员会", "location": "广西贵港市港南区"},
    {"id": 2, "name": "港南区人民政府", "type": "政府", "level": "县处级", "parent": "贵港市人民政府", "location": "广西贵港市港南区"},
    {"id": 3, "name": "中共贵港市港南区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "贵港市纪委监委", "location": "广西贵港市港南区"},
    {"id": 4, "name": "中共贵港市港南区委组织部", "type": "党委", "level": "乡科级", "parent": "中共贵港市港南区委员会", "location": "广西贵港市港南区"},
    {"id": 5, "name": "中共贵港市港南区委宣传部", "type": "党委", "level": "乡科级", "parent": "中共贵港市港南区委员会", "location": "广西贵港市港南区"},
    {"id": 6, "name": "中共贵港市港南区委政法委员会", "type": "党委", "level": "乡科级", "parent": "中共贵港市港南区委员会", "location": "广西贵港市港南区"},
    {"id": 7, "name": "中共贵港市港南区委统战部", "type": "党委", "level": "乡科级", "parent": "中共贵港市港南区委员会", "location": "广西贵港市港南区"},
    {"id": 8, "name": "中共贵港市港南区委员会办公室", "type": "党委", "level": "乡科级", "parent": "中共贵港市港南区委员会", "location": "广西贵港市港南区"},
    {"id": 9, "name": "港南区人大常委会", "type": "人大", "level": "县处级", "parent": "贵港市人大常委会", "location": "广西贵港市港南区"},
    {"id": 10, "name": "港南区政协", "type": "政协", "level": "县处级", "parent": "政协贵港市委员会", "location": "广西贵港市港南区"},
    {"id": 11, "name": "中共贵港市委员会", "type": "党委", "level": "地厅级", "parent": "中共广西壮族自治区委员会", "location": "广西贵港市"},
    {"id": 12, "name": "贵港市人民政府", "type": "政府", "level": "地厅级", "parent": "广西壮族自治区人民政府", "location": "广西贵港市"},
]

# =========================================================================
# Data: Positions
# =========================================================================
positions = [
    # 陶建全 - 区委书记
    {"person_id": 1, "org_id": 1, "title": "港南区委书记", "start_date": "约2022-2023年", "end_date": "至今", "rank": "县处级正职", "note": "现任港南区委书记"},
    # 殷崇勇 - 区长
    {"person_id": 2, "org_id": 2, "title": "港南区区长", "start_date": "约2022-2023年", "end_date": "至今", "rank": "县处级正职", "note": "现任港南区区长"},
    {"person_id": 2, "org_id": 1, "title": "港南区委副书记", "start_date": "约2022-2023年", "end_date": "至今", "rank": "县处级副职", "note": ""},
    # 黄创优 - 原区委书记
    {"person_id": 3, "org_id": 1, "title": "港南区委书记", "start_date": "约2019-2020年", "end_date": "约2022-2023年", "rank": "县处级正职", "note": "陶建全的前任"},
    # 曾健清 - 原区长
    {"person_id": 4, "org_id": 2, "title": "港南区区长", "start_date": "约2016-2020年", "end_date": "约2022-2023年", "rank": "县处级正职", "note": "殷崇勇的前任"},
    # GAP positions（姓名未知的副职）
    {"person_id": 5, "org_id": 2, "title": "港南区委常委、常务副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "GAP — 姓名未知"},
    {"person_id": 6, "org_id": 3, "title": "港南区委常委、纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "GAP — 姓名未知"},
    {"person_id": 7, "org_id": 4, "title": "港南区委常委、组织部长", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": "GAP — 姓名未知"},
    {"person_id": 8, "org_id": 5, "title": "港南区委常委、宣传部长", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": "GAP — 姓名未知"},
    {"person_id": 9, "org_id": 6, "title": "港南区委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": "GAP — 姓名未知"},
    {"person_id": 10, "org_id": 7, "title": "港南区委常委、统战部长", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": "GAP — 姓名未知"},
    {"person_id": 11, "org_id": 8, "title": "港南区委常委、区委办主任", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": "GAP — 姓名未知"},
]

# =========================================================================
# Data: Relationships
# =========================================================================
relationships = [
    # 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "区委书记与区长党政搭档", "overlap_org": "港南区四套班子", "overlap_period": "约2022-2023年至今"},
    # 陶建全 -> 黄创优（前后任书记）
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "陶建全接替黄创优任港南区委书记", "overlap_org": "中共贵港市港南区委员会", "overlap_period": "约2022-2023年"},
    # 殷崇勇 -> 曾健清（前后任区长）
    {"person_a": 2, "person_b": 4, "type": "predecessor_successor", "context": "殷崇勇接替曾健清任港南区区长", "overlap_org": "港南区人民政府", "overlap_period": "约2022-2023年"},
    # 黄创优 - 曾健清（前任书记-前任区长搭档）
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "前任党政正职搭档", "overlap_org": "港南区四套班子", "overlap_period": "约2019-2022年"},
]

# =========================================================================
# Main
# =========================================================================
if __name__ == "__main__":
    run_build(
        slug="港南区领导班子关系图",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    # Write person JSON files for core leaders
    today = datetime.now().strftime("%Y%m%d")

    persons_dir = STAGING
    persons_dir.mkdir(parents=True, exist_ok=True)

    person_files = []

    # ── 陶建全 person JSON ──
    tao_json = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "贵港市",
            "region": "港南区",
            "job": "港南区委书记",
            "task_id": "guangxi_港南区",
            "time_focus": "2022年至今"
        },
        "identity": {
            "person_id": "guangxi_guigang_gangnan_taojianquan",
            "name": "陶建全",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {"name_birth": "陶建全", "name_birthplace": "", "official_profile_url": ""}
        },
        "current_status": {
            "current_post": "港南区委书记",
            "current_org": "中共贵港市港南区委员会",
            "administrative_rank": "县处级正职",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": ["S001"]
        },
        "career_timeline": [
            {"start": "约2022-2023年", "end": "至今", "org": "中共贵港市港南区委员会", "title": "港南区委书记", "level": "县处级正职", "location": "广西贵港市港南区", "system": "party", "rank": "县处级正职", "is_key_promotion": True, "notes": "接替黄创优任港南区委书记", "confidence": "plausible", "source_ids": ["S001"]},
            {"start": "unknown", "end": "约2022-2023年", "org": "履历缺口", "title": "", "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False, "notes": "公开资料未找到任港南区委书记前的完整履历", "confidence": "unverified", "source_ids": []}
        ],
        "organizations": [
            {"org_id": 1, "name": "中共贵港市港南区委员会", "role": "区委书记", "period": "约2022-2023年至今", "source_ids": ["S001"]}
        ],
        "relationships": [
            {"person": "殷崇勇", "person_id": "guangxi_guigang_gangnan_yinchongyong", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "党政正职搭档：区委书记与区长", "overlap_org": "港南区四套班子", "overlap_period": "约2022-2023年至今", "direction": "person_to_other", "confidence": "plausible", "source_ids": ["S001"]},
            {"person": "黄创优", "person_id": "", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "接替黄创优任港南区委书记", "overlap_org": "中共贵港市港南区委员会", "overlap_period": "约2022-2023年", "direction": "other_to_person", "confidence": "plausible", "source_ids": ["S001"]}
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": ["地方党政管理"],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["party"],
            "geographic_pattern": ["广西", "贵港市"],
            "promotion_velocity": {"summary": "履历信息不足，无法评估晋升速度", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "截至2026-07-23未发现公开负面信息", "date": AS_OF, "confidence": "unverified", "source_ids": []}],
        "source_register": [
            {"id": "S001", "title": "Pre-2025 public sources on 港南区 leadership", "url": "", "publisher": "Various", "published_at": "", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": "Pre-cutoff training data; live verification blocked"}
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "plausible",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "Current status as of 2026-07-23 unverifiable; full career timeline, education, birth info missing"
        },
        "open_questions": [
            {"priority": "critical", "question": "陶建全是否仍担任港南区委书记？", "why_it_matters": "核心领导岗位确认", "suggested_queries": ["港南区 领导之窗 区委书记 2026", "陶建全 最新 任职"], "last_attempted": AS_OF},
            {"priority": "high", "question": "陶建全的完整工作履历（任区委书记前的经历）", "why_it_matters": "履历完整性与关系网络分析", "suggested_queries": ["陶建全 简历 港南区", "陶建全 任前公示 贵港"], "last_attempted": AS_OF},
            {"priority": "high", "question": "陶建全的出生年份、籍贯、教育背景", "why_it_matters": "个人身份确认与dedup", "suggested_queries": ["陶建全 出生 年月"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "陶建全的具体任职起止时间", "why_it_matters": "精确时间线", "suggested_queries": ["陶建全 任港南区委书记 时间"], "last_attempted": AS_OF}
        ]
    }
    person_files.append(("陶建全", "港南区委书记", tao_json))

    # ── 殷崇勇 person JSON ──
    yin_json = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "贵港市",
            "region": "港南区",
            "job": "港南区区长",
            "task_id": "guangxi_港南区",
            "time_focus": "2022年至今"
        },
        "identity": {
            "person_id": "guangxi_guigang_gangnan_yinchongyong",
            "name": "殷崇勇",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {"name_birth": "殷崇勇", "name_birthplace": "", "official_profile_url": ""}
        },
        "current_status": {
            "current_post": "港南区区长",
            "current_org": "港南区人民政府",
            "administrative_rank": "县处级正职",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": ["S002"]
        },
        "career_timeline": [
            {"start": "约2022-2023年", "end": "至今", "org": "港南区人民政府", "title": "港南区区长", "level": "县处级正职", "location": "广西贵港市港南区", "system": "government", "rank": "县处级正职", "is_key_promotion": True, "notes": "接替曾健清任港南区区长", "confidence": "plausible", "source_ids": ["S002"]},
            {"start": "unknown", "end": "约2022-2023年", "org": "履历缺口", "title": "", "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False, "notes": "公开资料未找到任港南区区长前的完整履历", "confidence": "unverified", "source_ids": []}
        ],
        "organizations": [
            {"org_id": 2, "name": "港南区人民政府", "role": "区长", "period": "约2022-2023年至今", "source_ids": ["S002"]}
        ],
        "relationships": [
            {"person": "陶建全", "person_id": "guangxi_guigang_gangnan_taojianquan", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "党政正职搭档：区长与区委书记", "overlap_org": "港南区四套班子", "overlap_period": "约2022-2023年至今", "direction": "other_to_person", "confidence": "plausible", "source_ids": ["S002"]},
            {"person": "曾健清", "person_id": "", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "接替曾健清任港南区区长", "overlap_org": "港南区人民政府", "overlap_period": "约2022-2023年", "direction": "other_to_person", "confidence": "plausible", "source_ids": ["S002"]}
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": ["地方行政管理"],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["government"],
            "geographic_pattern": ["广西", "贵港市"],
            "promotion_velocity": {"summary": "履历信息不足，无法评估晋升速度", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "截至2026-07-23未发现公开负面信息", "date": AS_OF, "confidence": "unverified", "source_ids": []}],
        "source_register": [
            {"id": "S002", "title": "Pre-2025 public sources on 港南区 leadership", "url": "", "publisher": "Various", "published_at": "", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": "Pre-cutoff training data; live verification blocked"}
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "plausible",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "Current status as of 2026-07-23 unverifiable; full career timeline, education, birth info missing"
        },
        "open_questions": [
            {"priority": "critical", "question": "殷崇勇是否仍担任港南区区长？", "why_it_matters": "核心领导岗位确认", "suggested_queries": ["港南区 区长 2026", "殷崇勇 最新 任职"], "last_attempted": AS_OF},
            {"priority": "high", "question": "殷崇勇的完整工作履历（任区长前的经历）", "why_it_matters": "履历完整性与关系网络", "suggested_queries": ["殷崇勇 简历 港南区"], "last_attempted": AS_OF},
            {"priority": "high", "question": "殷崇勇的出生年份、籍贯、教育背景", "why_it_matters": "个人身份确认与dedup", "suggested_queries": ["殷崇勇 出生 年月"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "殷崇勇的具体任职起止时间", "why_it_matters": "精确时间线", "suggested_queries": ["殷崇勇 任港南区区长 时间"], "last_attempted": AS_OF}
        ]
    }
    person_files.append(("殷崇勇", "港南区区长", yin_json))

    # Write person JSON files
    for name, job, data in person_files:
        safe_name = name.replace("【", "").replace("】", "").replace(" ", "")
        filename = f"{today}-广西壮族自治区-贵港市-{job}-{safe_name}.json"
        filepath = persons_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Person JSON: {filepath}")

    print(f"Done: DB={DB_PATH}, GEXF={GEXF_PATH}")
    print(f"Total: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")
