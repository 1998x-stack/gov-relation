#!/usr/bin/env python3
"""
杜尔伯特蒙古族自治县（黑龙江省大庆市）领导班子工作关系网络 — 2026-07-24
Build script for Dorbod Mongol Autonomous County, Daqing City, Heilongjiang Province.

Data sources:
- 杜尔伯特蒙古族自治县人民政府官网 http://www.dorbod.gov.cn/ — inaccessible due to network restrictions
- 大庆市人民政府官网 http://www.daqing.gov.cn/ — cross-county references
- News reports and appointment notices (2026)

TASK: heilongjiang_杜尔伯特蒙古族自治县

NOTE: This investigation operates under partial-evidence mode. The Dorbod county
government website (www.dorbod.gov.cn) was unreachable. Leadership data is based on
available news reports and limited web evidence. All claims are marked with confidence
levels. Biographical details remain incomplete and are explicitly flagged as gaps.
"""

import json
import os
import sqlite3  # noqa: used via gov_relation.runner
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

TODAY = "2026-07-24"
AS_OF = TODAY

# ── STAGING DIRECTORIES ──
STAGING = Path(__file__).resolve().parent
DB_PATH = STAGING / "杜尔伯特蒙古族自治县_network.db"
GEXF_PATH = STAGING / "杜尔伯特蒙古族自治县_network.gexf"
PERSONS_DIR = STAGING

# ── DATA ──

# Integer IDs
PERSON_ID_MAP = {
    # 县委书记 — TODO: confirm name from official source
    "县委书记（待确认姓名）": 1,
    # 县长 — TODO: confirm name from official source
    "县长（待确认姓名）": 2,
    "县委副书记（待确认姓名）": 3,
    "常务副县长（待确认姓名）": 4,
    "纪委书记（待确认姓名）": 5,
    "组织部长（待确认姓名）": 6,
    "宣传部长（待确认姓名）": 7,
    "政法委书记（待确认姓名）": 8,
    "统战部长（待确认姓名）": 9,
    "副县长（待确认姓名）": 10,
    "人大主任（待确认姓名）": 11,
    "政协主席（待确认姓名）": 12,
}

ORG_ID_MAP = {
    "中共杜尔伯特蒙古族自治县委员会": 1,
    "杜尔伯特蒙古族自治县人民政府": 2,
    "杜尔伯特蒙古族自治县人大常委会": 3,
    "杜尔伯特蒙古族自治县政协": 4,
    "杜尔伯特蒙古族自治县纪委监委": 5,
    "杜尔伯特蒙古族自治县委组织部": 6,
    "杜尔伯特蒙古族自治县委宣传部": 7,
    "杜尔伯特蒙古族自治县委统战部": 8,
    "杜尔伯特蒙古族自治县委政法委": 9,
}

persons = [
    {
        "id": 1,
        "name": "县委书记（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "杜尔伯特蒙古族自治县委书记",
        "current_org": "中共杜尔伯特蒙古族自治县委员会",
        "source": "待确认。杜尔伯特蒙古族自治县官网（www.dorbod.gov.cn）当前无法访问，需通过大庆市委组织部或县官网领导之窗页面确认现任县委书记姓名。",
    },
    {
        "id": 2,
        "name": "县长（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "杜尔伯特蒙古族自治县委副书记、县长",
        "current_org": "杜尔伯特蒙古族自治县人民政府",
        "source": "待确认。杜尔伯特蒙古族自治县官网当前无法访问，需通过大庆市政府或县官网确认现任县长姓名。",
    },
    {
        "id": 3,
        "name": "县委副书记（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "杜尔伯特蒙古族自治县委副书记",
        "current_org": "中共杜尔伯特蒙古族自治县委员会",
        "source": "待确认。",
    },
    {
        "id": 4,
        "name": "常务副县长（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "杜尔伯特蒙古族自治县委常委、常务副县长",
        "current_org": "杜尔伯特蒙古族自治县人民政府",
        "source": "待确认。",
    },
    {
        "id": 5,
        "name": "纪委书记（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "杜尔伯特蒙古族自治县委常委、纪委书记、监委主任",
        "current_org": "杜尔伯特蒙古族自治县纪委监委",
        "source": "待确认。",
    },
    {
        "id": 6,
        "name": "组织部长（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "杜尔伯特蒙古族自治县委常委、组织部长",
        "current_org": "杜尔伯特蒙古族自治县委组织部",
        "source": "待确认。",
    },
    {
        "id": 7,
        "name": "宣传部长（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "杜尔伯特蒙古族自治县委常委、宣传部长",
        "current_org": "杜尔伯特蒙古族自治县委宣传部",
        "source": "待确认。",
    },
    {
        "id": 8,
        "name": "政法委书记（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "杜尔伯特蒙古族自治县委常委、政法委书记",
        "current_org": "杜尔伯特蒙古族自治县委政法委",
        "source": "待确认。",
    },
    {
        "id": 9,
        "name": "统战部长（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "杜尔伯特蒙古族自治县委常委、统战部长",
        "current_org": "杜尔伯特蒙古族自治县委统战部",
        "source": "待确认。",
    },
    {
        "id": 10,
        "name": "副县长（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "杜尔伯特蒙古族自治县副县长",
        "current_org": "杜尔伯特蒙古族自治县人民政府",
        "source": "待确认。",
    },
    {
        "id": 11,
        "name": "人大主任（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "杜尔伯特蒙古族自治县人大常委会主任",
        "current_org": "杜尔伯特蒙古族自治县人大常委会",
        "source": "待确认。",
    },
    {
        "id": 12,
        "name": "政协主席（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "杜尔伯特蒙古族自治县政协主席",
        "current_org": "杜尔伯特蒙古族自治县政协",
        "source": "待确认。",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共杜尔伯特蒙古族自治县委员会",
        "type": "党委",
        "level": "县处级",
        "location": "黑龙江省大庆市杜尔伯特蒙古族自治县",
    },
    {
        "id": 2,
        "name": "杜尔伯特蒙古族自治县人民政府",
        "type": "政府",
        "level": "县处级",
        "location": "黑龙江省大庆市杜尔伯特蒙古族自治县",
    },
    {
        "id": 3,
        "name": "杜尔伯特蒙古族自治县人大常委会",
        "type": "人大",
        "level": "县处级",
        "location": "黑龙江省大庆市杜尔伯特蒙古族自治县",
    },
    {
        "id": 4,
        "name": "杜尔伯特蒙古族自治县政协",
        "type": "政协",
        "level": "县处级",
        "location": "黑龙江省大庆市杜尔伯特蒙古族自治县",
    },
    {
        "id": 5,
        "name": "杜尔伯特蒙古族自治县纪委监委",
        "type": "纪委",
        "level": "县处级",
        "location": "黑龙江省大庆市杜尔伯特蒙古族自治县",
    },
    {
        "id": 6,
        "name": "杜尔伯特蒙古族自治县委组织部",
        "type": "党委部门",
        "level": "县处级",
        "location": "黑龙江省大庆市杜尔伯特蒙古族自治县",
    },
    {
        "id": 7,
        "name": "杜尔伯特蒙古族自治县委宣传部",
        "type": "党委部门",
        "level": "县处级",
        "location": "黑龙江省大庆市杜尔伯特蒙古族自治县",
    },
    {
        "id": 8,
        "name": "杜尔伯特蒙古族自治县委统战部",
        "type": "党委部门",
        "level": "县处级",
        "location": "黑龙江省大庆市杜尔伯特蒙古族自治县",
    },
    {
        "id": 9,
        "name": "杜尔伯特蒙古族自治县委政法委",
        "type": "党委部门",
        "level": "县处级",
        "location": "黑龙江省大庆市杜尔伯特蒙古族自治县",
    },
]

positions = [
    # 县委书记 → 县委
    {"person_id": 1, "org_id": 1, "title": "杜尔伯特蒙古族自治县委书记", "start": "待查", "end": "至今", "rank": "县处级正职", "note": "现任县委书记，姓名待确认"},
    # 县长 → 县政府
    {"person_id": 2, "org_id": 2, "title": "杜尔伯特蒙古族自治县委副书记、县长", "start": "待查", "end": "至今", "rank": "县处级正职", "note": "现任县长，姓名待确认"},
    # 县委副书记 → 县委
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "待查", "end": "至今", "rank": "县处级副职", "note": "姓名待确认"},
    # 常务副县长 → 县政府
    {"person_id": 4, "org_id": 2, "title": "县委常委、常务副县长", "start": "待查", "end": "至今", "rank": "县处级副职", "note": "姓名待确认"},
    # 纪委书记 → 纪委
    {"person_id": 5, "org_id": 5, "title": "县委常委、纪委书记、监委主任", "start": "待查", "end": "至今", "rank": "县处级副职", "note": "姓名待确认"},
    # 组织部长 → 组织部
    {"person_id": 6, "org_id": 6, "title": "县委常委、组织部长", "start": "待查", "end": "至今", "rank": "县处级副职", "note": "姓名待确认"},
    # 宣传部长 → 宣传部
    {"person_id": 7, "org_id": 7, "title": "县委常委、宣传部长", "start": "待查", "end": "至今", "rank": "县处级副职", "note": "姓名待确认"},
    # 政法委书记 → 政法委
    {"person_id": 8, "org_id": 9, "title": "县委常委、政法委书记", "start": "待查", "end": "至今", "rank": "县处级副职", "note": "姓名待确认"},
    # 统战部长 → 统战部
    {"person_id": 9, "org_id": 8, "title": "县委常委、统战部长", "start": "待查", "end": "至今", "rank": "县处级副职", "note": "姓名待确认"},
    # 副县长 → 县政府
    {"person_id": 10, "org_id": 2, "title": "副县长", "start": "待查", "end": "至今", "rank": "县处级副职", "note": "姓名待确认"},
    # 人大主任 → 人大
    {"person_id": 11, "org_id": 3, "title": "县人大常委会主任", "start": "待查", "end": "至今", "rank": "县处级正职", "note": "姓名待确认"},
    # 政协主席 → 政协
    {"person_id": 12, "org_id": 4, "title": "县政协主席", "start": "待查", "end": "至今", "rank": "县处级正职", "note": "姓名待确认"},
]

# ── RELATIONSHIPS ──
# Note: With names unknown, only structural/organizational relationships are recorded.
# Once individual names are confirmed, person-to-person relationships should be added.

relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长：党委和政府主要领导搭档关系",
        "overlap_org": "中共杜尔伯特蒙古族自治县委员会 / 杜尔伯特蒙古族自治县人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记与县委副书记：党委班子核心成员",
        "overlap_org": "中共杜尔伯特蒙古族自治县委员会",
        "overlap_period": "至今",
    },
    {
        "person_a": 2,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "县长与常务副县长：政府班子正副职",
        "overlap_org": "杜尔伯特蒙古族自治县人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "县委书记与纪委书记：党委与纪委监督关系",
        "overlap_org": "中共杜尔伯特蒙古族自治县委员会",
        "overlap_period": "至今",
    },
    {
        "person_a": 1,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "县委书记与组织部长：党委核心人事关系",
        "overlap_org": "中共杜尔伯特蒙古族自治县委员会",
        "overlap_period": "至今",
    },
    {
        "person_a": 1,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "县委书记与宣传部长：党委宣传工作关系",
        "overlap_org": "中共杜尔伯特蒙古族自治县委员会",
        "overlap_period": "至今",
    },
    {
        "person_a": 1,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "县委书记与政法委书记：党委政法工作关系",
        "overlap_org": "中共杜尔伯特蒙古族自治县委员会",
        "overlap_period": "至今",
    },
    {
        "person_a": 2,
        "person_b": 10,
        "type": "superior_subordinate",
        "context": "县长与副县长：政府班子内部关系",
        "overlap_org": "杜尔伯特蒙古族自治县人民政府",
        "overlap_period": "至今",
    },
]

# ══════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════


def write_person_json(person: dict) -> str:
    """Write a minimal person JSON file for core figures (县委书记, 县长)."""
    post_slug = person["current_post"].replace("杜尔伯特蒙古族自治县", "").replace(" ", "")
    name_slug = person["name"].replace("（待确认）", "_daiqueren")
    filename = f"20260724-黑龙江省-大庆市-{post_slug}-{name_slug}.json"
    filepath = Path(PERSONS_DIR) / filename

    person_json = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "大庆市",
            "region": "杜尔伯特蒙古族自治县",
            "job": person["current_post"],
            "task_id": "heilongjiang_杜尔伯特蒙古族自治县",
            "time_focus": "2026年7月",
        },
        "identity": {
            "person_id": f"dorbod_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"] or "",
            "ethnicity": person["ethnicity"] or "",
            "birth": person["birth"] or "",
            "birthplace": person["birthplace"] or "",
            "native_place": "",
            "education": [],
            "party_join": "",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": f"{person['name']}_",
                "name_birthplace": f"{person['name']}_",
                "official_profile_url": "http://www.dorbod.gov.cn/ldzc/（待确认）",
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "县处级",
            "as_of": TODAY,
            "is_current_confirmed": False,
            "source_ids": [],
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": person["current_org"],
                "title": person["current_post"],
                "level": "县处级",
                "location": "黑龙江省大庆市杜尔伯特蒙古族自治县",
                "system": "party" if "书记" in person["current_post"] else "government",
                "rank": "县处级正职" if "书记" in person["current_post"] or "县长" in person["current_post"] else "待查",
                "is_key_promotion": True,
                "notes": f"现任{person['current_post']}，姓名待确认",
                "confidence": "unverified",
                "source_ids": [],
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
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "暂无公开资料。",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": [
            {
                "id": "S001",
                "title": "杜尔伯特蒙古族自治县人民政府官网",
                "url": "http://www.dorbod.gov.cn/",
                "publisher": "杜尔伯特蒙古族自治县人民政府",
                "published_at": "",
                "accessed_at": TODAY,
                "source_type": "official",
                "reliability": "high",
                "notes": "官网当前无法访问，领导信息待确认",
            }
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "姓名、出生年月、籍贯、教育背景、完整履历全部缺失",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "现任杜尔伯特蒙古族自治县委书记和县长的姓名分别是什么？",
                "why_it_matters": "核心领导人身份是整个调查的基础信息",
                "suggested_queries": [
                    "杜尔伯特蒙古族自治县 现任县委书记",
                    "杜尔伯特蒙古族自治县 县长 2026",
                    "site:dorbod.gov.cn 县委书记",
                    "大庆市 杜尔伯特 领导分工",
                ],
                "last_attempted": TODAY,
            }
        ],
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(person_json, f, ensure_ascii=False, indent=2)
    print(f"  [ok]  {filename}")
    return filename


def main():
    print("=" * 60)
    print("  杜尔伯特蒙古族自治县 — 领导班子工作关系网络")
    print(f"  Generated: {TODAY}")
    print("  Mode: partial evidence (web access degraded)")
    print("=" * 60)

    # ── Build database + GEXF ──
    print("\nBuilding database and GEXF graph...")
    run_build(
        slug="杜尔伯特蒙古族自治县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")

    # ── Write person JSONs for core leaders ──
    print("\nWriting person JSON files for core leaders...")
    core_leader_ids = [1, 2]  # 县委书记, 县长
    json_files = []
    for pid in core_leader_ids:
        person = next(p for p in persons if p["id"] == pid)
        fname = write_person_json(person)
        json_files.append(fname)

    # ── Summary ──
    print()
    print("─" * 60)
    print("  统计摘要")
    print("─" * 60)
    print(f"  人员 (persons):     {len(persons)}")
    print(f"  机构 (orgs):        {len(organizations)}")
    print(f"  任职 (positions):   {len(positions)}")
    print(f"  关系 (edges):       {len(relationships)}")
    print(f"  JSON 文件:           {len(json_files)}")
    print()
    print("  置信度说明:")
    print("    - 所有核心领导人姓名均标记为'待确认'")
    print("    - 机构结构为模板填充（基于县级标准配置）")
    print("    - 所有关系为结构关系（非实际人际证据）")
    print("    - 需补充官方领导之窗页面数据后替换")
    print()
    print("  ⚠ 开放缺口（需后续调查补充）:")
    print("    1. [CRITICAL] 现任县委书记姓名")
    print("    2. [CRITICAL] 现任县长姓名")
    print("    3. [HIGH]     全部县委常委、副县长姓名")
    print("    4. [HIGH]     核心领导人出生年月、籍贯、教育")
    print("    5. [HIGH]     县委书记和县长的完整履历")
    print("    6. [HIGH]     前任县委书记和县长的去向")
    print("    7. [MEDIUM]   杜尔伯特与周边县区（林甸、肇源、肇州等）的干部交流")
    print()
    print("=" * 60)
    print("  Build complete.")
    print("  → Run validation: python3 -m py_compile build_杜尔伯特蒙古族自治县_data.py")
    print("  → Promote:        python3 scripts/process_tmp.py data/tmp/heilongjiang_杜尔伯特蒙古族自治县 --apply")
    print("=" * 60)


if __name__ == "__main__":
    main()
