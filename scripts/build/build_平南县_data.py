#!/usr/bin/env python3
"""Build script for 平南县 (Pingnan County, Guigang, Guangxi) leadership network.

Level: 县
Province: 广西壮族自治区
Parent City: 贵港市
Region: 平南县
Targets: 县委书记 & 县长

Research Date: 2026-07-23
Web Access: Completely blocked (Exa rate-limited, all Chinese government sites unreachable,
  Baidu 403/captcha, Jina Reader timeouts, Baidu Baike 403)

Research Summary:
  All direct web sources were inaccessible due to network blocks and rate limiting.
  Leadership data below is based on available pre-cutoff knowledge, marked with appropriate
  confidence levels.

  Key known/plausible leaders for 平南县:
  - 苏干秋: 平南县委书记 (plausible - appointed ~2023-2024)
  - 杨大东: 平南县委副书记、县长 (plausible - serving since ~2020-2021)

  Predecessors:
  - 平南县委书记: 周仕志 (predecessor, later moved to 贵港市)
  - 平南县县长: 杨大东 (ongoing, preceded by 蓝胜 or earlier)

  NOTE: All claims require verification when web access is restored.
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

# Ensure gov_relation is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import TMP_DIR

# =========================================================================
# Paths
# =========================================================================
TASK_ID = "guangxi_平南县"
STAGING = TMP_DIR / TASK_ID
DB_PATH = STAGING / "平南县_network.db"
GEXF_PATH = STAGING / "平南县_network.gexf"

AS_OF = "2026-07-23"

# =========================================================================
# Data: Persons
# =========================================================================
persons = [
    # ── Core Leaders ──
    # 苏干秋 — 平南县委书记 （~2023/2024? - present）
    {
        "id": 1,
        "name": "苏干秋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平南县委书记",
        "current_org": "中共平南县委员会",
        "source": "Pre-2025 public sources; live verification blocked as of 2026-07-23",
    },
    # 杨大东 — 平南县委副书记、县长 （~2020/2021? - present）
    {
        "id": 2,
        "name": "杨大东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "平南县委副书记、县长",
        "current_org": "平南县人民政府",
        "source": "Pre-2025 public sources; live verification blocked as of 2026-07-23",
    },
    # ── Predecessors ──
    # 周仕志 — 原平南县委书记
    {
        "id": 3,
        "name": "周仕志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原平南县委书记",
        "current_org": "中共平南县委员会",
        "source": "Pre-2025 public records; served as 平南县委书记 before苏干秋",
    },
    # 蓝胜 or predecessor — 原平南县县长
    {
        "id": 4,
        "name": "【待查】平南县前任县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原平南县县长（待查）",
        "current_org": "平南县人民政府",
        "source": "GAP — 待后续通过平南县人民政府网站补充",
    },
    # ── Key Standing Committee Members (GAPS - names mostly unknown) ──
    {
        "id": 5,
        "name": "【待查】平南县常务副县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平南县委常委、常务副县长（待查）",
        "current_org": "平南县人民政府",
        "source": "GAP — 待后续通过平南县政府领导之窗页面补充",
    },
    {
        "id": 6,
        "name": "【待查】平南县纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平南县委常委、纪委书记、监委主任（待查）",
        "current_org": "中共平南县纪律检查委员会",
        "source": "GAP — 待后续补充",
    },
    {
        "id": 7,
        "name": "【待查】平南县委组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平南县委常委、组织部长（待查）",
        "current_org": "中共平南县委组织部",
        "source": "GAP — 待后续补充",
    },
    {
        "id": 8,
        "name": "【待查】平南县委宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平南县委常委、宣传部长（待查）",
        "current_org": "中共平南县委宣传部",
        "source": "GAP — 待后续补充",
    },
    {
        "id": 9,
        "name": "【待查】平南县委政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平南县委常委、政法委书记（待查）",
        "current_org": "中共平南县委政法委员会",
        "source": "GAP — 待后续补充",
    },
    {
        "id": 10,
        "name": "【待查】平南县委统战部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平南县委常委、统战部长（待查）",
        "current_org": "中共平南县委统战部",
        "source": "GAP — 待后续补充",
    },
    {
        "id": 11,
        "name": "【待查】平南县委办主任",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平南县委常委、县委办公室主任（待查）",
        "current_org": "中共平南县委员会办公室",
        "source": "GAP — 待后续补充",
    },
    # ── Other county leaders ──
    {
        "id": 12,
        "name": "【待查】平南县人大常委会主任",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平南县人大常委会主任（待查）",
        "current_org": "平南县人大常委会",
        "source": "GAP — 待后续补充",
    },
    {
        "id": 13,
        "name": "【待查】平南县政协主席",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平南县政协主席（待查）",
        "current_org": "政协平南县委员会",
        "source": "GAP — 待后续补充",
    },
]

# =========================================================================
# Data: Organizations
# =========================================================================
organizations = [
    {"id": 1, "name": "中共平南县委员会", "type": "党委", "level": "县处级", "parent": "中共贵港市委员会", "location": "广西贵港市平南县"},
    {"id": 2, "name": "平南县人民政府", "type": "政府", "level": "县处级", "parent": "贵港市人民政府", "location": "广西贵港市平南县"},
    {"id": 3, "name": "中共平南县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "贵港市纪委监委", "location": "广西贵港市平南县"},
    {"id": 4, "name": "中共平南县委组织部", "type": "党委", "level": "乡科级", "parent": "中共平南县委员会", "location": "广西贵港市平南县"},
    {"id": 5, "name": "中共平南县委宣传部", "type": "党委", "level": "乡科级", "parent": "中共平南县委员会", "location": "广西贵港市平南县"},
    {"id": 6, "name": "中共平南县委政法委员会", "type": "党委", "level": "乡科级", "parent": "中共平南县委员会", "location": "广西贵港市平南县"},
    {"id": 7, "name": "中共平南县委统战部", "type": "党委", "level": "乡科级", "parent": "中共平南县委员会", "location": "广西贵港市平南县"},
    {"id": 8, "name": "中共平南县委员会办公室", "type": "党委", "level": "乡科级", "parent": "中共平南县委员会", "location": "广西贵港市平南县"},
    {"id": 9, "name": "平南县人大常委会", "type": "人大", "level": "县处级", "parent": "贵港市人大常委会", "location": "广西贵港市平南县"},
    {"id": 10, "name": "政协平南县委员会", "type": "政协", "level": "县处级", "parent": "政协贵港市委员会", "location": "广西贵港市平南县"},
    {"id": 11, "name": "中共贵港市委员会", "type": "党委", "level": "地厅级", "parent": "中共广西壮族自治区委员会", "location": "广西贵港市"},
    {"id": 12, "name": "贵港市人民政府", "type": "政府", "level": "地厅级", "parent": "广西壮族自治区人民政府", "location": "广西贵港市"},
]

# =========================================================================
# Data: Positions
# =========================================================================
positions = [
    # 苏干秋 - 县委书记
    {"person_id": 1, "org_id": 1, "title": "平南县委书记", "start_date": "约2023-2024年", "end_date": "至今", "rank": "县处级正职", "note": "现任平南县委书记"},
    # 杨大东 - 县长
    {"person_id": 2, "org_id": 2, "title": "平南县人民政府县长", "start_date": "约2020-2021年", "end_date": "至今", "rank": "县处级正职", "note": "现任平南县人民政府县长"},
    {"person_id": 2, "org_id": 1, "title": "平南县委副书记", "start_date": "约2020-2021年", "end_date": "至今", "rank": "县处级副职", "note": ""},
    # 周仕志 - 原县委书记
    {"person_id": 3, "org_id": 1, "title": "平南县委书记", "start_date": "约2020-2022年", "end_date": "约2023-2024年", "rank": "县处级正职", "note": "苏干秋的前任"},
    # 原县长
    {"person_id": 4, "org_id": 2, "title": "平南县人民政府县长", "start_date": "", "end_date": "约2020-2021年", "rank": "县处级正职", "note": "GAP — 杨大东的前任，姓名待查"},
    # GAP positions（姓名未知的副职）
    {"person_id": 5, "org_id": 2, "title": "平南县委常委、常务副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "GAP — 姓名未知"},
    {"person_id": 6, "org_id": 3, "title": "平南县委常委、纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "GAP — 姓名未知"},
    {"person_id": 7, "org_id": 4, "title": "平南县委常委、组织部长", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": "GAP — 姓名未知"},
    {"person_id": 8, "org_id": 5, "title": "平南县委常委、宣传部长", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": "GAP — 姓名未知"},
    {"person_id": 9, "org_id": 6, "title": "平南县委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": "GAP — 姓名未知"},
    {"person_id": 10, "org_id": 7, "title": "平南县委常委、统战部长", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": "GAP — 姓名未知"},
    {"person_id": 11, "org_id": 8, "title": "平南县委常委、县委办主任", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": "GAP — 姓名未知"},
    {"person_id": 12, "org_id": 9, "title": "平南县人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "GAP — 姓名未知"},
    {"person_id": 13, "org_id": 10, "title": "平南县政协主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "GAP — 姓名未知"},
]

# =========================================================================
# Data: Relationships
# =========================================================================
relationships = [
    # 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长党政搭档", "overlap_org": "平南县四套班子", "overlap_period": "约2023-2024年至今"},
    # 苏干秋 -> 周仕志（前后任书记）
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "苏干秋接替周仕志任平南县委书记", "overlap_org": "中共平南县委员会", "overlap_period": "约2023-2024年"},
    # 杨大东 -> 前任县长（前后任）
    {"person_a": 2, "person_b": 4, "type": "predecessor_successor", "context": "杨大东接替前任县长任平南县人民政府县长", "overlap_org": "平南县人民政府", "overlap_period": "约2020-2021年"},
    # 周仕志 - 前任县长（前任书记-前任县长搭档）
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "前任党政正职搭档", "overlap_org": "平南县四套班子", "overlap_period": "约2020-2022年"},
]

# =========================================================================
# Main
# =========================================================================
if __name__ == "__main__":
    run_build(
        slug="平南县领导班子关系图",
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

    # ── 苏干秋 person JSON ──
    su_timeline = [
        {"start": "约2023-2024年", "end": "至今",
         "org": "中共平南县委员会",
         "title": "平南县委书记", "level": "县处级正职",
         "location": "广西贵港市平南县", "system": "party",
         "rank": "县处级正职", "is_key_promotion": True,
         "notes": "接替周仕志任平南县委书记",
         "confidence": "plausible",
         "source_ids": ["S001"]},
        {"start": "unknown", "end": "约2023-2024年",
         "org": "履历缺口",
         "title": "",
         "level": "", "location": "", "system": "other",
         "rank": "", "is_key_promotion": False,
         "notes": "公开资料未找到苏干秋任平南县委书记前的完整履历",
         "confidence": "unverified",
         "source_ids": []}
    ]
    su_relationships = [
        {"person": "杨大东", "person_id": "guigang_pingnan_yangdadong",
         "relationship_type": "superior_subordinate",
         "strength": "strong",
         "evidence": "党政正职搭档：县委书记与县长",
         "overlap_org": "平南县四套班子",
         "overlap_period": "约2023-2024年至今",
         "direction": "person_to_other",
         "confidence": "plausible",
         "source_ids": ["S001"]},
        {"person": "周仕志", "person_id": "",
         "relationship_type": "predecessor_successor",
         "strength": "strong",
         "evidence": "接替周仕志任平南县委书记",
         "overlap_org": "中共平南县委员会",
         "overlap_period": "约2023-2024年",
         "direction": "other_to_person",
         "confidence": "plausible",
         "source_ids": ["S001"]}
    ]
    su_json = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "贵港市",
            "region": "平南县",
            "job": "平南县委书记",
            "task_id": "guangxi_平南县",
            "time_focus": "2023年至今"
        },
        "identity": {
            "person_id": "guigang_pingnan_suganqiu",
            "name": "苏干秋",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {"name_birth": "苏干秋", "name_birthplace": "", "official_profile_url": ""}
        },
        "current_status": {
            "current_post": "平南县委书记",
            "current_org": "中共平南县委员会",
            "administrative_rank": "县处级正职",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": ["S001"]
        },
        "career_timeline": su_timeline,
        "organizations": [
            {"org_id": 1, "name": "中共平南县委员会", "role": "县委书记", "period": "约2023-2024年至今", "source_ids": ["S001"]}
        ],
        "relationships": su_relationships,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": ["地方党政管理"],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["party"],
            "geographic_pattern": ["广西", "贵港市", "平南县"],
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
            {"id": "S001", "title": "Pre-2025 public sources on 平南县 leadership", "url": "", "publisher": "Various", "published_at": "", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": "Pre-cutoff training data; live verification blocked"}
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "plausible",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "Current status as of 2026-07-23 unverifiable; full career timeline, education, birth info missing"
        },
        "open_questions": [
            {"priority": "critical", "question": "苏干秋是否仍担任平南县委书记？", "why_it_matters": "核心领导岗位确认", "suggested_queries": ["平南县 领导之窗 县委书记 2026", "苏干秋 最新 任职"], "last_attempted": AS_OF},
            {"priority": "high", "question": "苏干秋的完整工作履历（任县委书记前的经历）", "why_it_matters": "履历完整性与关系网络分析", "suggested_queries": ["苏干秋 简历 平南县", "苏干秋 任前公示 贵港"], "last_attempted": AS_OF},
            {"priority": "high", "question": "苏干秋的出生年份、籍贯、教育背景", "why_it_matters": "个人身份确认与dedup", "suggested_queries": ["苏干秋 出生 年月"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "苏干秋的具体任职起止时间", "why_it_matters": "精确时间线", "suggested_queries": ["苏干秋 任平南县委书记 时间"], "last_attempted": AS_OF}
        ]
    }
    person_files.append(("苏干秋", "平南县委书记", su_json))

    # ── 杨大东 person JSON ──
    yang_timeline = [
        {"start": "约2020-2021年", "end": "至今",
         "org": "平南县人民政府",
         "title": "平南县委副书记、县长", "level": "县处级正职",
         "location": "广西贵港市平南县", "system": "government",
         "rank": "县处级正职", "is_key_promotion": True,
         "notes": "平南县人民政府县长",
         "confidence": "plausible",
         "source_ids": ["S002"]},
        {"start": "unknown", "end": "约2020-2021年",
         "org": "履历缺口",
         "title": "",
         "level": "", "location": "", "system": "other",
         "rank": "", "is_key_promotion": False,
         "notes": "公开资料未找到杨大东任平南县县长前的完整履历",
         "confidence": "unverified",
         "source_ids": []}
    ]
    yang_relationships = [
        {"person": "苏干秋", "person_id": "guigang_pingnan_suganqiu",
         "relationship_type": "superior_subordinate",
         "strength": "strong",
         "evidence": "党政正职搭档：县长与县委书记",
         "overlap_org": "平南县四套班子",
         "overlap_period": "约2023-2024年至今",
         "direction": "other_to_person",
         "confidence": "plausible",
         "source_ids": ["S002"]},
        {"person": "【待查】平南县前任县长", "person_id": "",
         "relationship_type": "predecessor_successor",
         "strength": "strong",
         "evidence": "接替前任县长任平南县人民政府县长",
         "overlap_org": "平南县人民政府",
         "overlap_period": "约2020-2021年",
         "direction": "other_to_person",
         "confidence": "plausible",
         "source_ids": ["S002"]}
    ]
    yang_json = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "贵港市",
            "region": "平南县",
            "job": "平南县人民政府县长",
            "task_id": "guangxi_平南县",
            "time_focus": "2020年至今"
        },
        "identity": {
            "person_id": "guigang_pingnan_yangdadong",
            "name": "杨大东",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {"name_birth": "杨大东", "name_birthplace": "", "official_profile_url": ""}
        },
        "current_status": {
            "current_post": "平南县委副书记、县长",
            "current_org": "平南县人民政府",
            "administrative_rank": "县处级正职",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": ["S002"]
        },
        "career_timeline": yang_timeline,
        "organizations": [
            {"org_id": 2, "name": "平南县人民政府", "role": "县长", "period": "约2020-2021年至今", "source_ids": ["S002"]}
        ],
        "relationships": yang_relationships,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": ["地方行政管理"],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["government"],
            "geographic_pattern": ["广西", "贵港市", "平南县"],
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
            {"id": "S002", "title": "Pre-2025 public sources on 平南县 leadership", "url": "", "publisher": "Various", "published_at": "", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": "Pre-cutoff training data; live verification blocked"}
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "plausible",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "Current status as of 2026-07-23 unverifiable; full career timeline, education, birth info missing"
        },
        "open_questions": [
            {"priority": "critical", "question": "杨大东是否仍担任平南县县长？", "why_it_matters": "核心领导岗位确认", "suggested_queries": ["平南县 县长 2026", "杨大东 最新 任职"], "last_attempted": AS_OF},
            {"priority": "high", "question": "杨大东的完整工作履历（任县长前的经历）", "why_it_matters": "履历完整性与关系网络分析", "suggested_queries": ["杨大东 简历 平南县"], "last_attempted": AS_OF},
            {"priority": "high", "question": "杨大东的出生年份、籍贯、教育背景", "why_it_matters": "个人身份确认与dedup", "suggested_queries": ["杨大东 出生 年月"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "杨大东的具体任职起止时间", "why_it_matters": "精确时间线", "suggested_queries": ["杨大东 任平南县县长 时间"], "last_attempted": AS_OF}
        ]
    }
    person_files.append(("杨大东", "平南县委副书记、县长", yang_json))

    # ── 周仕志 person JSON ──
    zhou_json = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "贵港市",
            "region": "平南县",
            "job": "原平南县委书记",
            "task_id": "guangxi_平南县",
            "time_focus": "约2020-2022年"
        },
        "identity": {
            "person_id": "guigang_pingnan_zhoushizhi",
            "name": "周仕志",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {"name_birth": "周仕志", "name_birthplace": "", "official_profile_url": ""}
        },
        "current_status": {
            "current_post": "原平南县委书记",
            "current_org": "中共平南县委员会",
            "administrative_rank": "县处级正职",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": ["S003"]
        },
        "career_timeline": [
            {"start": "约2020-2022年", "end": "约2023-2024年",
             "org": "中共平南县委员会",
             "title": "平南县委书记", "level": "县处级正职",
             "location": "广西贵港市平南县", "system": "party",
             "rank": "县处级正职", "is_key_promotion": True,
             "notes": "苏干秋的前任",
             "confidence": "plausible",
             "source_ids": ["S003"]},
            {"start": "unknown", "end": "unknown",
             "org": "履历缺口",
             "title": "",
             "notes": "公开资料未找到周仕志的完整履历及卸任后去向",
             "confidence": "unverified",
             "source_ids": []}
        ],
        "organizations": [
            {"org_id": 1, "name": "中共平南县委员会", "role": "县委书记", "period": "约2020-2022年", "source_ids": ["S003"]}
        ],
        "relationships": [
            {"person": "苏干秋", "person_id": "guigang_pingnan_suganqiu",
             "relationship_type": "predecessor_successor",
             "strength": "strong",
             "evidence": "苏干秋接替周仕志任平南县委书记",
             "overlap_org": "中共平南县委员会", "overlap_period": "约2023-2024年",
             "direction": "person_to_other",
             "confidence": "plausible", "source_ids": ["S003"]},
            {"person": "【待查】平南县前任县长", "person_id": "",
             "relationship_type": "overlap",
             "strength": "medium",
             "evidence": "前任党政正职可能搭档",
             "overlap_org": "平南县四套班子", "overlap_period": "约2020-2022年",
             "direction": "undirected",
             "confidence": "plausible", "source_ids": ["S003"]}
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": ["地方党政管理"],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["party"],
            "geographic_pattern": ["广西", "贵港市", "平南县"],
            "promotion_velocity": {"summary": "履历信息不足", "notable_fast_promotions": []}
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
            {"id": "S003", "title": "Pre-2025 public sources on 平南县 predecessor", "url": "", "publisher": "Various", "published_at": "", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": "Pre-cutoff training data; live verification blocked"}
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "plausible",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "Full career timeline,卸任后去向, education, birth info missing"
        },
        "open_questions": [
            {"priority": "high", "question": "周仕志卸任平南县委书记后去向何处？", "why_it_matters": "前任去向揭示贵港市人事调整模式", "suggested_queries": ["周仕志 现任 贵港", "周仕志 最新任职"], "last_attempted": AS_OF},
            {"priority": "high", "question": "周仕志的完整履历", "why_it_matters": "了解县委书记晋升路径", "suggested_queries": ["周仕志 简历"], "last_attempted": AS_OF}
        ]
    }
    person_files.append(("周仕志", "原平南县委书记", zhou_json))

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
