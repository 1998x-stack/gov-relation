#!/usr/bin/env python3
"""Build 沈阳市和平区 (Shenyang Heping District) leadership network data.

Level: 市辖区
Province: 辽宁省
Parent city: 沈阳市
Targets: 区委书记 (Party Secretary), 区长 (Mayor)
Task ID: liaoning_和平区

Research date: 2026-07-25
Official source: http://www.syhpq.gov.cn/ (沈阳市和平区人民政府 — unreachable during research)
Staging build: data/tmp/liaoning_和平区/ → promoted by process_tmp.py

⚠️  WEB ACCESS WARNING ⚠️
- syhpq.gov.cn: DNS resolution failure (could not resolve host)
- Baidu Baike: 403 / blocked
- Jina Reader: transport errors to Chinese sites
- Exa search: rate-limited
Therefore this build uses pre-existing knowledge from training data (through late 2025)
and may not reflect post-2025 personnel changes. All claims marked with confidence levels.

Known current status (from pre-2026 training data, needs verification):
- 区委书记: 张德 (Zhang De) — previously served as 和平区区长, elevated to 区委书记 ~2021-2022
  (Alternative possibility: may have been replaced in 2025-2026 in a routine rotation)
- 区长: 彭光磊 (Peng Guanglei) — assumed office ~2022-2023
  (Alternative possibility: may have been replaced in a post-2025 adjustment)

Key deputies (inferred from pre-2025 patterns):
- 常务副区长: likely appointed
- 纪委书记: likely appointed
- 组织部部长: likely appointed
- 政法委书记: likely appointed
- 宣传部部长: likely appointed

This build creates partial artifacts with explicit uncertainty. The open_gaps.md
report identifies the specific verification steps needed.
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

SLUG = "和平区"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = datetime.now().strftime("%Y-%m-%d")
TODAY = datetime.now().strftime("%Y%m%d")

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 区委领导 (Party Committee)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "张德",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共沈阳市和平区委员会",
        "source": "unverified — training data pre-2025; syhpq.gov.cn unreachable",
    },
    {
        "id": 2,
        "name": "彭光磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区长",
        "current_org": "沈阳市和平区人民政府",
        "source": "unverified — training data pre-2025; syhpq.gov.cn unreachable",
    },
    # ════════════════════════════════════════
    # 区委常委 (Standing Committee members)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "常务副区长（待核实）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "常务副区长",
        "current_org": "沈阳市和平区人民政府",
        "source": "unverified — name unknown, role inferred from structure",
    },
    {
        "id": 4,
        "name": "纪委书记（待核实）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区纪委书记",
        "current_org": "中共沈阳市和平区纪律检查委员会",
        "source": "unverified — name unknown, role inferred from structure",
    },
    {
        "id": 5,
        "name": "组织部部长（待核实）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "组织部部长",
        "current_org": "中共沈阳市和平区委组织部",
        "source": "unverified — name unknown, role inferred from structure",
    },
    {
        "id": 6,
        "name": "政法委书记（待核实）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "政法委书记",
        "current_org": "中共沈阳市和平区委政法委员会",
        "source": "unverified — name unknown, role inferred from structure",
    },
    {
        "id": 7,
        "name": "宣传部部长（待核实）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "宣传部部长",
        "current_org": "中共沈阳市和平区委宣传部",
        "source": "unverified — name unknown, role inferred from structure",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共沈阳市和平区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共沈阳市委",
        "location": "辽宁省沈阳市和平区",
    },
    {
        "id": 2,
        "name": "沈阳市和平区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "沈阳市人民政府",
        "location": "辽宁省沈阳市和平区",
    },
    {
        "id": 3,
        "name": "中共沈阳市和平区纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共沈阳市和平区委员会",
        "location": "辽宁省沈阳市和平区",
    },
    {
        "id": 4,
        "name": "中共沈阳市和平区委组织部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共沈阳市和平区委员会",
        "location": "辽宁省沈阳市和平区",
    },
    {
        "id": 5,
        "name": "中共沈阳市和平区委政法委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共沈阳市和平区委员会",
        "location": "辽宁省沈阳市和平区",
    },
    {
        "id": 6,
        "name": "中共沈阳市和平区委宣传部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共沈阳市和平区委员会",
        "location": "辽宁省沈阳市和平区",
    },
    {
        "id": 7,
        "name": "沈阳市和平区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "沈阳市人大常委会",
        "location": "辽宁省沈阳市和平区",
    },
    {
        "id": 8,
        "name": "中国人民政治协商会议沈阳市和平区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协沈阳市委员会",
        "location": "辽宁省沈阳市和平区",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 张德
    {"person_id": 1, "org_id": 1, "title": "区委书记",
     "start_date": "2021?", "end_date": "至今", "rank": "正处级",
     "note": "履历待核实；此前曾任和平区区长"},
    # 彭光磊
    {"person_id": 2, "org_id": 2, "title": "区长",
     "start_date": "2022?", "end_date": "至今", "rank": "正处级",
     "note": "履历待核实"},
    # Key deputies (names unknown)
    {"person_id": 3, "org_id": 2, "title": "常务副区长",
     "start_date": "未知", "end_date": "至今", "rank": "副处级",
     "note": "姓名待核实"},
    {"person_id": 4, "org_id": 3, "title": "区纪委书记",
     "start_date": "未知", "end_date": "至今", "rank": "副处级",
     "note": "姓名待核实"},
    {"person_id": 5, "org_id": 4, "title": "组织部部长",
     "start_date": "未知", "end_date": "至今", "rank": "副处级",
     "note": "姓名待核实"},
    {"person_id": 6, "org_id": 5, "title": "政法委书记",
     "start_date": "未知", "end_date": "至今", "rank": "副处级",
     "note": "姓名待核实"},
    {"person_id": 7, "org_id": 6, "title": "宣传部部长",
     "start_date": "未知", "end_date": "至今", "rank": "副处级",
     "note": "姓名待核实"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 书记 — 区长
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "区委书记—区长搭班", "overlap_org": "和平区",
     "overlap_period": "2022?—至今"},
    # 书记 — 纪委书记
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "区委书记—纪委书记（双重领导）",
     "overlap_org": "中共沈阳市和平区委员会",
     "overlap_period": "待核实"},
    # 书记 — 组织部部长
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "区委书记—组织部部长",
     "overlap_org": "中共沈阳市和平区委员会",
     "overlap_period": "待核实"},
    # 区长 — 常务副区长
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "区长—常务副区长",
     "overlap_org": "和平区人民政府",
     "overlap_period": "待核实"},
]


# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSON HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def _person_json_path(name: str, title: str) -> Path:
    safe_name = name.replace("（", "_").replace("）", "").replace(" ", "")
    return PERSONS_DIR / f"{TODAY}-辽宁省-沈阳市-{title}-{safe_name}.json"


def write_person_json(person: dict, title_job: str) -> None:
    """Write a person JSON file with the deep schema from person_graph_json.md."""
    name = person["name"]
    fpath = _person_json_path(name, title_job)

    is_known = "待核实" not in name

    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "沈阳市",
            "region": "和平区",
            "job": title_job,
            "task_id": "liaoning_和平区",
            "time_focus": "2024-2025",
        },
        "identity": {
            "person_id": f"liaoning_shenyang_heping_{name}",
            "name": name if is_known else "",
            "aliases": [],
            "gender": person.get("gender", "") if is_known else "",
            "ethnicity": person.get("ethnicity", "") if is_known else "",
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": "",
                "name_birthplace": "",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if title_job in ("区委书记", "区长") else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": False if not is_known else False,
            "source_ids": [],
        },
        "career_timeline": [
            {
                "start": "未知" if is_known else "未知",
                "end": "present" if is_known else "未知",
                "org": person["current_org"],
                "title": person["current_post"],
                "level": "正处级" if title_job in ("区委书记", "区长") else "副处级",
                "location": "辽宁省沈阳市和平区",
                "system": "party" if "书记" in title_job else "government",
                "rank": "",
                "is_key_promotion": False,
                "notes": f"履历待核实。当前信息来自预训练数据，未能在研究期间通过 syhpq.gov.cn 或百度百科核实。",
                "confidence": "unverified",
                "source_ids": [],
            },
        ],
        "organizations": [
            {
                "id": person["current_org"],
                "name": person["current_org"],
                "role": person["current_post"],
                "period": "未知—至今",
            },
        ],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "无法评估——缺乏详细履历数据",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "因研究期间无法访问 syhpq.gov.cn 和百度百科，无法采集工作风格线索。",
        },
        "network_metrics": {
            "degree": 0,
            "betweenness": 0.0,
            "community": "",
        },
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": f"研究期间因无法访问公开资料，未发现{name}的纪律或风险信号。",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": [],
            },
        ],
        "source_register": [],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "plausible" if is_known else "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "无法通过官方政府网站或百度百科核实当前任职信息。syhpq.gov.cn DNS 解析失败，百度百科 403 拒绝访问。",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"截至{AS_OF}，{name}是否仍在担任{person['current_post']}？请通过 syhpq.gov.cn '领导之窗' 或沈阳市委组织部任前公示核实。",
                "why_it_matters": "这是本关系网络的核心节点。如果已离任，需要替换为接任者。",
                "suggested_queries": [
                    f"沈阳市和平区 现任领导",
                    f"沈阳市和平区 领导分工",
                    f"和平区 区委书记 最新",
                    f"和平区 区长 最新",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"{name}的完整履历（出生日期、籍贯、教育背景、历任职务）是什么？",
                "why_it_matters": "履历数据是分析职业路径、跨区交流模式和社交关系的基础。",
                "suggested_queries": [
                    f"{name} 简历 和平区",
                    f"{name} 任前公示 沈阳",
                    f"{name} 辽宁 干部",
                ],
                "last_attempted": AS_OF,
            },
        ],
    }

    fpath.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
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

    # Write person JSON files
    write_person_json(persons[0], "区委书记")
    write_person_json(persons[1], "区长")

    print(f"✅ Build complete: {DB_PATH}, {GEXF_PATH}")
    print(f"✅ Person JSON files written to {PERSONS_DIR}/")


if __name__ == "__main__":
    main()
