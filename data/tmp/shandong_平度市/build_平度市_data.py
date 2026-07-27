#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 平度市, 青岛市, 山东省.

Investigation date: 2026-07-25
Task ID: shandong_平度市
Level: 县级市 (县级)
Targets: 市委书记 & 市长

Key findings:
- 前任市长 张宏业 (1978年11月生) 于 2026年2月调任即墨区长
- 张宏业 2023年3月-2026年2月任平度市委副书记、市长
- 张宏业此前在胶州市工作多年
- 现任市委书记和接任市长信息待查（公开网络访问受限）

Research sources:
- 即墨区调查记录 (confirmed 张宏业 tenure)
- 即墨区调查记录 (confirmed 张宏业 biography)
- 百度百科 — 张宏业 (出生于1978年11月, 省委党校研究生, 工学学士)

Confidence notes:
- 张宏业平度市长任期已确认 (来自即墨区调查)
- 张宏业基本个人信息已确认 (出生年月, 学历)
- 平度市委书记信息待查 — 公开网络访问受限
- 接任市长信息待查 — 公开网络访问受限
- 领导班子其他成员信息待查 — 公开网络访问受限
"""

import json
import os
import sqlite3  # noqa: F401
import sys
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from gov_relation.runner import run_build

SLUG = "平度市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

STAGING_DIR = Path(BASE)
DB_PATH = str(STAGING_DIR / f"{SLUG}_network.db")
GEXF_PATH = str(STAGING_DIR / f"{SLUG}_network.gexf")

# ═══════════════════════════════════════════════════════════════════════════════
# Data
# ═══════════════════════════════════════════════════════════════════════════════

# Person ID convention: pingdu_{pinyin_name}
# Person IDs: 1-19 for personnel, 20+ for predecessors/others

persons_data = [
    # ══════════════════════════════════════════════════════════════════════════
    # Former Leaders (confirmed)
    # ══════════════════════════════════════════════════════════════════════════

    # 张宏业 — 原平度市委副书记、市长 (2023.3-2026.2), 调任即墨区长
    {
        "id": 1,
        "name": "张宏业",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年11月",
        "birthplace": "",
        "education": "省委党校研究生，工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原平度市长（现任即墨区长）",
        "current_org": "即墨区人民政府",
        "source": "即墨区调查记录, 百度百科",
        "notes": "2023年3月-2026年2月任平度市委副书记、市长；2026年2月调任即墨区委副书记、区长。此前在胶州市工作多年。"
    },
]

organizations_data = [
    {
        "id": 1,
        "name": "中共平度市委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共青岛市委员会",
        "location": "青岛市平度市"
    },
    {
        "id": 2,
        "name": "平度市人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "青岛市人民政府",
        "location": "青岛市平度市"
    },
    {
        "id": 3,
        "name": "平度市人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "青岛市人民代表大会常务委员会",
        "location": "青岛市平度市"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议平度市委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协青岛市委员会",
        "location": "青岛市平度市"
    },
    {
        "id": 5,
        "name": "中共平度市纪律检查委员会 / 平度市监察委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共青岛市纪律检查委员会",
        "location": "青岛市平度市"
    },
    {
        "id": 6,
        "name": "中共青岛市委员会",
        "type": "党委",
        "level": "副省级",
        "parent": "中共山东省委员会",
        "location": "青岛市"
    },
    {
        "id": 7,
        "name": "青岛市人民政府",
        "type": "政府",
        "level": "副省级",
        "parent": "山东省人民政府",
        "location": "青岛市"
    },
    {
        "id": 8,
        "name": "中共胶州市委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共青岛市委员会",
        "location": "青岛市胶州市"
    },
    {
        "id": 9,
        "name": "胶州市人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "青岛市人民政府",
        "location": "青岛市胶州市"
    },
    {
        "id": 10,
        "name": "即墨区人民政府",
        "type": "政府",
        "level": "地厅级",
        "parent": "青岛市人民政府",
        "location": "青岛市即墨区"
    },
    {
        "id": 11,
        "name": "中共青岛市即墨区委员会",
        "type": "党委",
        "level": "地厅级",
        "parent": "中共青岛市委员会",
        "location": "青岛市即墨区"
    },
]

positions_data = [
    # 张宏业 (id=1)
    {"person_id": 1, "org_id": 9, "title": "胶州市副市长等职", "start_date": "unknown", "end_date": "unknown", "rank": "副处级", "note": "在胶州市工作多年，历任多职；精确时间待查"},
    {"person_id": 1, "org_id": 1, "title": "平度市委副书记", "start_date": "2023-03", "end_date": "2026-02", "rank": "副厅级", "note": "confirmed from 即墨区调查"},
    {"person_id": 1, "org_id": 2, "title": "平度市市长", "start_date": "2023-03", "end_date": "2026-02", "rank": "正处级", "note": "2023年3月-2026年2月任平度市长"},
    {"person_id": 1, "org_id": 10, "title": "即墨区委副书记、区政府党组书记、区长", "start_date": "2026-02-13", "end_date": "present", "rank": "正厅级", "note": "2026年2月13日正式当选即墨区长"},
    {"person_id": 1, "org_id": 11, "title": "即墨区委副书记", "start_date": "2026-02", "end_date": "present", "rank": "副厅级", "note": "兼任"},
]

relationships_data = [
]

# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON generation
# ═══════════════════════════════════════════════════════════════════════════════

PERSON_JSON_TEMPLATE = {
    "张宏业": {
        "filename": f"{TODAY}-山东省-青岛市-市长-张宏业.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "山东省",
                "city": "青岛市",
                "region": "平度市",
                "job": "市长",
                "task_id": "shandong_平度市",
                "time_focus": "2023-2026"
            },
            "identity": {
                "person_id": "pingdu_zhang_hongye",
                "name": "张宏业",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "1978年11月",
                "birthplace": "",
                "native_place": "",
                "education": [
                    {
                        "period": "unknown",
                        "institution": "山东省委党校",
                        "major": "",
                        "degree": "研究生",
                        "study_type": "party_school",
                        "source_ids": ["S001"]
                    },
                    {
                        "period": "unknown",
                        "institution": "unknown",
                        "major": "",
                        "degree": "工学学士",
                        "study_type": "unknown",
                        "source_ids": ["S001"]
                    }
                ],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {
                    "name_birth": "张宏业_1978年11月",
                    "name_birthplace": "张宏业_unknown",
                    "official_profile_url": ""
                }
            },
            "current_status": {
                "current_post": "即墨区委副书记、区政府党组书记、区长兼青岛蓝谷管理局党委副书记、局长",
                "current_org": "即墨区人民政府",
                "administrative_rank": "正厅级（即墨区长）",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S002"]
            },
            "career_timeline": [
                {
                    "start": "unknown",
                    "end": "unknown",
                    "org": "胶州市",
                    "title": "历任职务（含副市长等）",
                    "level": "",
                    "location": "山东青岛胶州",
                    "system": "government",
                    "rank": "",
                    "is_key_promotion": False,
                    "notes": "在胶州市工作多年，具体职务和时间待查",
                    "confidence": "plausible",
                    "source_ids": ["S002"]
                },
                {
                    "start": "2023-03",
                    "end": "2026-02",
                    "org": "中共平度市委员会/平度市人民政府",
                    "title": "平度市委副书记、市长",
                    "level": "县处级",
                    "location": "山东青岛平度",
                    "system": "government",
                    "rank": "正处级",
                    "is_key_promotion": True,
                    "notes": "2023年3月至2026年2月任职平度市长",
                    "confidence": "confirmed",
                    "source_ids": ["S002"]
                },
                {
                    "start": "2026-02-13",
                    "end": "present",
                    "org": "即墨区人民政府",
                    "title": "即墨区委副书记、区长",
                    "level": "地厅级",
                    "location": "山东青岛即墨",
                    "system": "government",
                    "rank": "正厅级",
                    "is_key_promotion": True,
                    "notes": "2026年2月13日当选即墨区长；职务属副省级城市辖区，行政级别高于平度",
                    "confidence": "confirmed",
                    "source_ids": ["S001", "S002"]
                }
            ],
            "organizations": [
                {"org_name": "胶州市", "org_type": "政府", "role": "历任县级领导职务"},
                {"org_name": "中共平度市委员会", "org_type": "党委", "role": "市委副书记"},
                {"org_name": "平度市人民政府", "org_type": "政府", "role": "市长"},
                {"org_name": "即墨区人民政府", "org_type": "政府", "role": "区长"},
                {"org_name": "中共青岛市即墨区委员会", "org_type": "党委", "role": "区委副书记"}
            ],
            "relationships": [
                {
                    "person": "孙杰（即墨区委书记）",
                    "person_id": "jimo_sun_jie",
                    "relationship_type": "党政搭档",
                    "strength": "strong",
                    "evidence": "张宏业接替孙杰之前的即墨区长职务，孙杰转任区委书记，二人为当前即墨区党政主要搭档",
                    "overlap_org": "即墨区人民政府",
                    "overlap_period": "2026-02-present",
                    "direction": "person_to_other",
                    "confidence": "confirmed",
                    "source_ids": ["S001"]
                }
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": ["地方政府治理"],
                "secondary_specializations": [],
                "career_pattern": "跨区调任型",
                "systems_experience": ["government"],
                "geographic_pattern": ["胶州→平度→即墨"],
                "promotion_velocity": {
                    "summary": "从平度市长（县级市）调任即墨区长（副省级城市辖区），属于重用提拔",
                    "notable_fast_promotions": []
                }
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style assessment requires more public records"
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "未发现公开的纪律处分、审计问题或负面报道",
                    "date": "",
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "source_register": [
                {
                    "id": "S001",
                    "title": "即墨区调查记录 — 张宏业 biography",
                    "url": "",
                    "publisher": "Gov-Relation Research",
                    "published_at": "2026-07-25",
                    "accessed_at": "2026-07-25",
                    "source_type": "database",
                    "reliability": "high",
                    "notes": "来自即墨区调查的 confirmed 数据"
                },
                {
                    "id": "S002",
                    "title": "即墨区调查记录 — build_即墨区_data.py",
                    "url": "",
                    "publisher": "Gov-Relation Research",
                    "published_at": "2026-07-25",
                    "accessed_at": "2026-07-25",
                    "source_type": "database",
                    "reliability": "high",
                    "notes": "confirmed 张宏业平度市长任期和基本个人信息"
                }
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "partial",
                "relationship_confidence": "low",
                "biggest_gap": "早期履历（胶州市时期的具体职务和时间）完全未知"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": "张宏业在胶州市的具体职务和时间线是什么？",
                    "why_it_matters": "缺少完整的职业履历，无法构建完整的工作关系网络",
                    "suggested_queries": ["张宏业 胶州 副市长 简历", "张宏业 胶州 任职 时间"],
                    "last_attempted": "2026-07-25"
                },
                {
                    "priority": "critical",
                    "question": "张宏业的出生地和教育背景细节是什么？",
                    "why_it_matters": "出生地和教育背景是人员去重和关系分析的重要字段",
                    "suggested_queries": ["张宏业 出生 哪里", "张宏业 工学学士 专业"],
                    "last_attempted": "2026-07-25"
                }
            ]
        }
    }
}


# ═══════════════════════════════════════════════════════════════════════════════
# Build
# ═══════════════════════════════════════════════════════════════════════════════

def build():
    """Run database + GEXF build."""
    run_build(
        slug=SLUG,
        persons=persons_data,
        organizations=organizations_data,
        positions=positions_data,
        relationships=relationships_data,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # ── Person JSONs ──────────────────────────────────────────────────────
    for name, template in PERSON_JSON_TEMPLATE.items():
        path = STAGING_DIR / template["filename"]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(template["data"], f, ensure_ascii=False, indent=2)
        print(f"✅ Person JSON: {path}")

    # ── Summary ──────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"平度市 Network Build Complete")
    print(f"{'='*60}")
    print(f"Persons:     {len(persons_data)}")
    print(f"Orgs:        {len(organizations_data)}")
    print(f"Positions:   {len(positions_data)}")
    print(f"Relationships: {len(relationships_data)}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")
    print(f"\n⚠️  NOTE: Research incomplete due to degraded web access.")
    print(f"   Current 市委书记 and new mayor information could not be obtained.")
    print(f"   See report/open_gaps.md for detailed gap tracking.")


if __name__ == "__main__":
    build()
