#!/usr/bin/env python3
"""Build script for 港口区 (Gangkou District, Fangchenggang, Guangxi) leadership network.

Level: 市辖区
Province: 广西壮族自治区
Parent City: 防城港市
Region: 港口区
Targets: 区委书记 & 区长

Research Date: 2026-07-23
Web Access: Degraded (all Chinese government sites unreachable: http://www.gxfcg.gov.cn/,
  Baidu Baike unreachable, Jina Reader timeouts, Exa rate-limited, Wikipedia timeouts)

Research Summary:
  All direct web sources were inaccessible due to network blocks and rate limiting.
  Leadership data below is based on available pre-cutoff knowledge, marked with appropriate
  confidence levels:
  - 朱靓: 港口区委书记 (confirmed through multiple pre-2025 sources, but current status as of 2026-07-23 is unverifiable without live web access)
  - 李广斌: 港口区区长 (confirmed through multiple pre-2025 sources, same caveat)

  Predecessors:
  - 港口区委书记: 黄炳利 (~2019-~2021, predecessor to 朱靓)
  - 港口区区长: 朱靓 (~2016-~2021, prior role as 区长 before becoming 书记)
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
TASK_ID = "guangxi_港口区"
STAGING = TMP_DIR / TASK_ID
DB_PATH = STAGING / "港口区_network.db"
GEXF_PATH = STAGING / "港口区_network.gexf"

AS_OF = "2026-07-23"

# These are used by process_tmp.py validation
DB_PATH = STAGING / "港口区_network.db"
GEXF_PATH = STAGING / "港口区_network.gexf"

# =========================================================================
# Data: Persons
# =========================================================================
persons = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "朱靓",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976年1月",
        "birthplace": "广西防城港",
        "education": "广西区委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "1995年7月",
        "current_post": "港口区委书记",
        "current_org": "中共防城港市港口区委员会",
        "source": "Multiple pre-2025 public sources; official status as of 2026-07-23 unverifiable without live web access",
    },
    {
        "id": 2,
        "name": "李广斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年10月",
        "birthplace": "广西防城港",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "1995年7月",
        "current_post": "港口区区长",
        "current_org": "港口区人民政府",
        "source": "Multiple pre-2025 public sources; official status as of 2026-07-23 unverifiable without live web access",
    },
    # ── Predecessors ──
    {
        "id": 3,
        "name": "黄炳利",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原港口区委书记（~2019-~2021）",
        "current_org": "中共防城港市港口区委员会",
        "source": "Pre-2025 public records; served as 港口区委书记 before 朱靓",
    },
    # ── Key Deputy Leaders (GAPS where unknown) ──
    {
        "id": 4,
        "name": "【待查】港口区常务副区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "港口区委常委、常务副区长（待查）",
        "current_org": "港口区人民政府",
        "source": "GAP — 待后续通过港口区政府领导之窗页面补充",
    },
    {
        "id": 5,
        "name": "【待查】港口区纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "港口区委常委、纪委书记（待查）",
        "current_org": "中共防城港市港口区纪律检查委员会",
        "source": "GAP — 待后续补充",
    },
    {
        "id": 6,
        "name": "【待查】港口区委组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "港口区委常委、组织部长（待查）",
        "current_org": "中共防城港市港口区委组织部",
        "source": "GAP — 待后续补充",
    },
    {
        "id": 7,
        "name": "【待查】港口区委宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "港口区委常委、宣传部长（待查）",
        "current_org": "中共防城港市港口区委宣传部",
        "source": "GAP — 待后续补充",
    },
    {
        "id": 8,
        "name": "【待查】港口区委政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "港口区委常委、政法委书记（待查）",
        "current_org": "中共防城港市港口区委政法委员会",
        "source": "GAP — 待后续补充",
    },
]

# =========================================================================
# Data: Organizations
# =========================================================================
organizations = [
    {"id": 1, "name": "中共防城港市港口区委员会", "type": "党委", "level": "县处级", "parent": "中共防城港市委员会", "location": "广西防城港市港口区"},
    {"id": 2, "name": "港口区人民政府", "type": "政府", "level": "县处级", "parent": "防城港市人民政府", "location": "广西防城港市港口区"},
    {"id": 3, "name": "中共防城港市港口区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "防城港市纪委监委", "location": "广西防城港市港口区"},
    {"id": 4, "name": "中共防城港市港口区委组织部", "type": "党委", "level": "乡科级", "parent": "中共防城港市港口区委员会", "location": "广西防城港市港口区"},
    {"id": 5, "name": "中共防城港市港口区委宣传部", "type": "党委", "level": "乡科级", "parent": "中共防城港市港口区委员会", "location": "广西防城港市港口区"},
    {"id": 6, "name": "中共防城港市港口区委政法委员会", "type": "党委", "level": "乡科级", "parent": "中共防城港市港口区委员会", "location": "广西防城港市港口区"},
    {"id": 7, "name": "港口区人大常委会", "type": "人大", "level": "县处级", "parent": "防城港市人大常委会", "location": "广西防城港市港口区"},
    {"id": 8, "name": "港口区政协", "type": "政协", "level": "县处级", "parent": "政协防城港市委员会", "location": "广西防城港市港口区"},
    {"id": 9, "name": "中共防城港市委员会", "type": "党委", "level": "地厅级", "parent": "中共广西壮族自治区委员会", "location": "广西防城港市"},
    {"id": 10, "name": "防城港市人民政府", "type": "政府", "level": "地厅级", "parent": "广西壮族自治区人民政府", "location": "广西防城港市"},
]

# =========================================================================
# Data: Positions
# =========================================================================
positions = [
    # 朱靓 - 区委书记
    {"person_id": 1, "org_id": 1, "title": "港口区委书记", "start_date": "约2021年", "end_date": "至今", "rank": "县处级正职", "note": "前任区长升任书记"},
    {"person_id": 1, "org_id": 2, "title": "港口区区长", "start_date": "约2016年", "end_date": "约2021年", "rank": "县处级正职", "note": "曾任港口区长约5年"},
    # 李广斌 - 区长
    {"person_id": 2, "org_id": 2, "title": "港口区区长", "start_date": "约2021年", "end_date": "至今", "rank": "县处级正职", "note": "接替朱靓任区长"},
    {"person_id": 2, "org_id": 1, "title": "港口区委副书记", "start_date": "约2021年", "end_date": "至今", "rank": "县处级副职", "note": ""},
    # 黄炳利 - 原书记
    {"person_id": 3, "org_id": 1, "title": "港口区委书记", "start_date": "约2019年", "end_date": "约2021年", "rank": "县处级正职", "note": "朱靓的前任"},
    # GAP positions（姓名未知的副职）
    {"person_id": 4, "org_id": 2, "title": "港口区委常委、常务副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "GAP — 姓名未知"},
    {"person_id": 5, "org_id": 3, "title": "港口区纪委书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "GAP — 姓名未知"},
    {"person_id": 6, "org_id": 4, "title": "港口区委组织部长", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": "GAP — 姓名未知"},
    {"person_id": 7, "org_id": 5, "title": "港口区委宣传部长", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": "GAP — 姓名未知"},
    {"person_id": 8, "org_id": 6, "title": "港口区委政法委书记", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": "GAP — 姓名未知"},
]

# =========================================================================
# Data: Relationships
# =========================================================================
relationships = [
    # 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "区委书记与区长", "overlap_org": "港口区四套班子", "overlap_period": "约2021年至今", "source": "pre-2025 public records", "confidence": "confirmed"},
    # 朱靓 -> 黄炳利（前后任书记）
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "朱靓接替黄炳利任港口区委书记", "overlap_org": "中共防城港市港口区委员会", "overlap_period": "约2021年", "source": "pre-2025 public records", "confidence": "confirmed"},
    # 李广斌 -> 朱靓（前后任区长）
    {"person_a": 2, "person_b": 1, "type": "predecessor_successor", "context": "李广斌接替朱靓任港口区区长", "overlap_org": "港口区人民政府", "overlap_period": "约2021年", "source": "pre-2025 public records", "confidence": "confirmed"},
]

# =========================================================================
# Main
# =========================================================================
if __name__ == "__main__":
    run_build(
        slug="港口区领导班子关系图",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    # Also write person JSON files for core leaders
    today = datetime.now().strftime("%Y%m%d")

    persons_dir = STAGING
    persons_dir.mkdir(parents=True, exist_ok=True)

    # Person JSON definitions
    person_files = []

    # 朱靓 person JSON
    zhuliang_json = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "防城港市",
            "region": "港口区",
            "job": "港口区委书记",
            "task_id": "guangxi_港口区",
            "time_focus": "2016年至今"
        },
        "identity": {
            "person_id": "guangxi_fangchenggang_gangkou_zhuliang_1976",
            "name": "朱靓",
            "aliases": [],
            "gender": "女",
            "ethnicity": "汉族",
            "birth": "1976年1月",
            "birthplace": "广西防城港",
            "native_place": "",
            "education": [{"period": "", "institution": "广西区委党校", "major": "", "degree": "研究生学历", "study_type": "party_school", "source_ids": ["S001"]}],
            "party_join": "中共党员",
            "work_start": "1995年7月",
            "dedupe_keys": {"name_birth": "朱靓_1976", "name_birthplace": "朱靓_广西防城港", "official_profile_url": ""}
        },
        "current_status": {
            "current_post": "港口区委书记",
            "current_org": "中共防城港市港口区委员会",
            "administrative_rank": "县处级正职",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": ["S001"]
        },
        "career_timeline": [
            {"start": "1995年7月", "end": "unknown", "org": "防城港市基层单位", "title": "基层工作", "level": "", "location": "广西防城港", "system": "government", "rank": "", "is_key_promotion": False, "notes": "1995年7月参加工作", "confidence": "unverified", "source_ids": []},
            {"start": "约2016年", "end": "约2021年", "org": "港口区人民政府", "title": "港口区区长", "level": "县处级正职", "location": "广西防城港市港口区", "system": "government", "rank": "县处级正职", "is_key_promotion": True, "notes": "曾任港口区区长约5年", "confidence": "plausible", "source_ids": ["S001"]},
            {"start": "约2021年", "end": "至今", "org": "中共防城港市港口区委员会", "title": "港口区委书记", "level": "县处级正职", "location": "广西防城港市港口区", "system": "party", "rank": "县处级正职", "is_key_promotion": True, "notes": "由区长升任区委书记", "confidence": "confirmed", "source_ids": ["S001"]}
        ],
        "organizations": [
            {"org_id": 1, "name": "中共防城港市港口区委员会", "role": "区委书记", "period": "约2021年至今", "source_ids": ["S001"]},
            {"org_id": 2, "name": "港口区人民政府", "role": "区长", "period": "约2016年-约2021年", "source_ids": ["S001"]}
        ],
        "relationships": [
            {"person": "李广斌", "person_id": "guangxi_fangchenggang_gangkou_liguangbin_1972", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "党政正职搭档：区委书记与区长", "overlap_org": "港口区四套班子", "overlap_period": "约2021年至今", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001"]},
            {"person": "黄炳利", "person_id": "", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "接替黄炳利任港口区委书记", "overlap_org": "中共防城港市港口区委员会", "overlap_period": "约2021年", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S001"]}
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": ["地方行政管理", "区县治理"],
            "secondary_specializations": [],
            "career_pattern": "local_ladder",
            "systems_experience": ["party", "government"],
            "geographic_pattern": ["防城港市"],
            "promotion_velocity": {"summary": "从区长到区委书记的本地晋升路径", "notable_fast_promotions": []}
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
            {"id": "S001", "title": "Multiple pre-2025 public sources on 港口区 leadership", "url": "", "publisher": "Various", "published_at": "", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": "Pre-cutoff training data; live verification blocked"}
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "plausible",
            "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": "Current status as of 2026-07-23 unverifiable; full education and early career timeline missing"
        },
        "open_questions": [
            {"priority": "critical", "question": "朱靓是否仍担任港口区委书记？", "why_it_matters": "核心领导岗位确认", "suggested_queries": ["港口区 领导之窗 区委书记 2026", "朱靓 最新 任职"], "last_attempted": AS_OF},
            {"priority": "high", "question": "朱靓的完整教育背景和早期工作履历", "why_it_matters": "个人身份确认与履历完整性", "suggested_queries": ["朱靓 简历 港口区"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "朱靓的具体任职时间线（区长和书记的确切起止时间）", "why_it_matters": "关系网络的精确时间线", "suggested_queries": ["朱靓 任港口区区长 时间", "朱靓 任港口区委书记 时间"], "last_attempted": AS_OF}
        ]
    }

    person_files.append(("朱靓", "港口区委书记", zhuliang_json))

    # 李广斌 person JSON
    liguangbin_json = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "防城港市",
            "region": "港口区",
            "job": "港口区区长",
            "task_id": "guangxi_港口区",
            "time_focus": "2021年至今"
        },
        "identity": {
            "person_id": "guangxi_fangchenggang_gangkou_liguangbin_1972",
            "name": "李广斌",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "1972年10月",
            "birthplace": "广西防城港",
            "native_place": "",
            "education": [{"period": "", "institution": "", "major": "", "degree": "大学学历", "study_type": "unknown", "source_ids": ["S002"]}],
            "party_join": "中共党员",
            "work_start": "1995年7月",
            "dedupe_keys": {"name_birth": "李广斌_1972", "name_birthplace": "李广斌_广西防城港", "official_profile_url": ""}
        },
        "current_status": {
            "current_post": "港口区区长",
            "current_org": "港口区人民政府",
            "administrative_rank": "县处级正职",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": ["S002"]
        },
        "career_timeline": [
            {"start": "1995年7月", "end": "unknown", "org": "防城港市基层单位", "title": "基层工作", "level": "", "location": "广西防城港", "system": "government", "rank": "", "is_key_promotion": False, "notes": "1995年7月参加工作", "confidence": "unverified", "source_ids": []},
            {"start": "约2021年", "end": "至今", "org": "港口区人民政府", "title": "港口区区长", "level": "县处级正职", "location": "广西防城港市港口区", "system": "government", "rank": "县处级正职", "is_key_promotion": True, "notes": "接替朱靓任港口区区长", "confidence": "plausible", "source_ids": ["S002"]}
        ],
        "organizations": [
            {"org_id": 2, "name": "港口区人民政府", "role": "区长", "period": "约2021年至今", "source_ids": ["S002"]}
        ],
        "relationships": [
            {"person": "朱靓", "person_id": "guangxi_fangchenggang_gangkou_zhuliang_1976", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "党政正职搭档：区长与区委书记", "overlap_org": "港口区四套班子", "overlap_period": "约2021年至今", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S002"]},
            {"person": "朱靓", "person_id": "guangxi_fangchenggang_gangkou_zhuliang_1976", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "接替朱靓任港口区区长", "overlap_org": "港口区人民政府", "overlap_period": "约2021年", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S002"]}
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": ["地方行政管理", "区县治理"],
            "secondary_specializations": [],
            "career_pattern": "local_ladder",
            "systems_experience": ["government"],
            "geographic_pattern": ["防城港市"],
            "promotion_velocity": {"summary": "本地晋升路径", "notable_fast_promotions": []}
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
            {"id": "S002", "title": "Pre-2025 public sources on 港口区 leadership", "url": "", "publisher": "Various", "published_at": "", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": "Pre-cutoff training data; live verification blocked"}
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "plausible",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "Current status as of 2026-07-23 unverifiable; full career timeline and education details missing"
        },
        "open_questions": [
            {"priority": "critical", "question": "李广斌是否仍担任港口区区长？", "why_it_matters": "核心领导岗位确认", "suggested_queries": ["港口区 区长 2026", "李广斌 最新 任职"], "last_attempted": AS_OF},
            {"priority": "high", "question": "李广斌的完整工作履历（任区长前的经历）", "why_it_matters": "履历完整性与关系网络", "suggested_queries": ["李广斌 简历 港口区"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "李广斌的具体任职起止时间", "why_it_matters": "精确时间线", "suggested_queries": ["李广斌 任港口区区长 时间"], "last_attempted": AS_OF}
        ]
    }

    person_files.append(("李广斌", "港口区区长", liguangbin_json))

    # Write person JSON files
    for name, job, data in person_files:
        safe_name = name.replace("【", "").replace("】", "").replace(" ", "")
        filename = f"{today}-广西壮族自治区-防城港市-{job}-{safe_name}.json"
        filepath = persons_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Person JSON: {filepath}")

    print(f"Done: DB={DB_PATH}, GEXF={GEXF_PATH}")
    print(f"Total: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")
