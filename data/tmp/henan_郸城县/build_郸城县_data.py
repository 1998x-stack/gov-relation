#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 郸城县 (Dancheng County), 周口市, 河南省.

Level: 县
Province: 河南省
Parent city: 周口市
Targets: 县委书记 (Party Secretary), 县长 (County Mayor)
Task ID: henan_郸城县

Research date: 2026-07-24
Official site: https://www.dancheng.gov.cn/ (郸城县人民政府)

⚠️  RESEARCH LIMITATION NOTICE ⚠️
Due to persistent web access degradation (Exa rate-limited, Jina/Baidu/Google
all timed out or blocked as of 2026-07-24), the current officeholders' names
could not be confirmed from primary or secondary sources. This script contains
placeholder data for structural completeness.

The 周口市 person JSON files (from task henan_周口市) confirm:
- 周口市委书记: 黄玉国
- 周口市长: 詹鹏

But 郸城县-level leadership information could not be fetched.

**To complete this investigation, re-run with working web access and update:**
- ALL person names, birth info, career timelines
- ALL organization details
- ALL positions and dates
- ALL relationship edges
- Source registers with confirmed URLs

Per the project's partial-evidence artifact mode policy, we still produce
structurally valid artifacts with explicit uncertainty markers.

Data template based on:
- 郸城县 is a county under 周口市, 河南省
- Neighboring counties: 鹿邑县, 沈丘县, 淮阳区, 项城市, 太康县
- Official domain: dancheng.gov.cn
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Allow import from repo root
_REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "郸城县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# ── Staging paths ────────────────────────────────────────────────────────────
STAGING = Path(__file__).parent.resolve()
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 县委领导 (Party Committee)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "待查_县委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "郸城县委书记",
        "current_org": "中共周口市郸城县委员会",
        "source": "⚠️ 未确认——需通过 Baidu Baike 或 dancheng.gov.cn/ldzc/ 查询",
    },
    {
        "id": 2,
        "name": "待查_县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "郸城县县长",
        "current_org": "郸城县人民政府",
        "source": "⚠️ 未确认——需通过 Baidu Baike 或 dancheng.gov.cn 查询",
    },
    # ════════════════════════════════════════
    # 县委副书记 (Deputy Party Secretary)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "待查_县委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "郸城县委副书记",
        "current_org": "中共周口市郸城县委员会",
        "source": "⚠️ 未确认——需通过官方领导分工页面查询",
    },
    # ════════════════════════════════════════
    # 常务副县长 (Executive Deputy County Mayor)
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "待查_常务副县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "郸城县委常委、常务副县长",
        "current_org": "郸城县人民政府",
        "source": "⚠️ 未确认——需通过官方领导分工页面查询",
    },
    # ════════════════════════════════════════
    # 纪委书记 (Discipline Inspection Secretary)
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "待查_纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "郸城县委常委、纪委书记、监委主任",
        "current_org": "中共周口市郸城县纪律检查委员会",
        "source": "⚠️ 未确认——需通过官方页面查询",
    },
    # ════════════════════════════════════════
    # 组织部长 (Organization Department Head)
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "待查_组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "郸城县委常委、组织部部长",
        "current_org": "中共周口市郸城县委组织部",
        "source": "⚠️ 未确认——需通过官方页面查询",
    },
    # ════════════════════════════════════════
    # 宣传部长 (Propaganda Department Head)
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "待查_宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "郸城县委常委、宣传部部长",
        "current_org": "中共周口市郸城县委宣传部",
        "source": "⚠️ 未确认——需通过官方页面查询",
    },
    # ════════════════════════════════════════
    # 政法委书记 (Political-Legal Affairs Secretary)
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "待查_政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "郸城县委常委、政法委书记",
        "current_org": "中共周口市郸城县委政法委员会",
        "source": "⚠️ 未确认——需通过官方页面查询",
    },
    # ════════════════════════════════════════
    # 统战部长 (United Front Secretary)
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "待查_统战部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "郸城县委常委、统战部部长",
        "current_org": "中共周口市郸城县委统战部",
        "source": "⚠️ 未确认——需通过官方页面查询",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共周口市郸城县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共周口市委员会",
        "location": "河南省周口市郸城县",
    },
    {
        "id": 2,
        "name": "郸城县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "周口市人民政府",
        "location": "河南省周口市郸城县",
    },
    {
        "id": 3,
        "name": "中共周口市郸城县纪律检查委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共周口市纪律检查委员会",
        "location": "河南省周口市郸城县",
    },
    {
        "id": 4,
        "name": "郸城县监察委员会",
        "type": "党委",
        "level": "县",
        "parent": "周口市监察委员会",
        "location": "河南省周口市郸城县",
    },
    {
        "id": 5,
        "name": "中共周口市郸城县委组织部",
        "type": "党委",
        "level": "县",
        "parent": "中共周口市郸城县委员会",
        "location": "河南省周口市郸城县",
    },
    {
        "id": 6,
        "name": "中共周口市郸城县委宣传部",
        "type": "党委",
        "level": "县",
        "parent": "中共周口市郸城县委员会",
        "location": "河南省周口市郸城县",
    },
    {
        "id": 7,
        "name": "中共周口市郸城县委政法委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共周口市郸城县委员会",
        "location": "河南省周口市郸城县",
    },
    {
        "id": 8,
        "name": "中共周口市郸城县委统战部",
        "type": "党委",
        "level": "县",
        "parent": "中共周口市郸城县委员会",
        "location": "河南省周口市郸城县",
    },
    {
        "id": 9,
        "name": "郸城县人民代表大会常务委员会",
        "type": "人大",
        "level": "县",
        "parent": "周口市人民代表大会常务委员会",
        "location": "河南省周口市郸城县",
    },
    {
        "id": 10,
        "name": "中国人民政治协商会议郸城县委员会",
        "type": "政协",
        "level": "县",
        "parent": "中国人民政治协商会议周口市委员会",
        "location": "河南省周口市郸城县",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 县委书记
    {"person_id": 1, "org_id": 1, "title": "郸城县委书记",
     "start_date": "", "end_date": "present", "rank": "正县处级", "note": "未确认具体任职起始时间"},
    # 县长
    {"person_id": 2, "org_id": 2, "title": "郸城县县长",
     "start_date": "", "end_date": "present", "rank": "正县处级", "note": "未确认具体任职起始时间"},
    # 县委副书记
    {"person_id": 3, "org_id": 1, "title": "郸城县委副书记",
     "start_date": "", "end_date": "present", "rank": "副县处级", "note": "未确认"},
    # 常务副县长
    {"person_id": 4, "org_id": 2, "title": "郸城县委常委、常务副县长",
     "start_date": "", "end_date": "present", "rank": "副县处级", "note": "未确认"},
    # 纪委书记
    {"person_id": 5, "org_id": 3, "title": "郸城县委常委、纪委书记、监委主任",
     "start_date": "", "end_date": "present", "rank": "副县处级", "note": "未确认"},
    # 组织部长
    {"person_id": 6, "org_id": 5, "title": "郸城县委常委、组织部部长",
     "start_date": "", "end_date": "present", "rank": "副县处级", "note": "未确认"},
    # 宣传部长
    {"person_id": 7, "org_id": 6, "title": "郸城县委常委、宣传部部长",
     "start_date": "", "end_date": "present", "rank": "副县处级", "note": "未确认"},
    # 政法委书记
    {"person_id": 8, "org_id": 7, "title": "郸城县委常委、政法委书记",
     "start_date": "", "end_date": "present", "rank": "副县处级", "note": "未确认"},
    # 统战部长
    {"person_id": 9, "org_id": 8, "title": "郸城县委常委、统战部部长",
     "start_date": "", "end_date": "present", "rank": "副县处级", "note": "未确认"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "县委书记与县长为党政正职搭档关系",
        "overlap_org": "郸城县",
        "overlap_period": "",
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "overlap",
        "context": "县委书记与县委副书记为上下级工作关系",
        "overlap_org": "中共郸城县委",
        "overlap_period": "",
    },
    {
        "person_a": 2, "person_b": 4,
        "type": "overlap",
        "context": "县长与常务副县长为政府工作搭档关系",
        "overlap_org": "郸城县人民政府",
        "overlap_period": "",
    },
    {
        "person_a": 1, "person_b": 5,
        "type": "overlap",
        "context": "县委书记与纪委书记，县委主要领导与纪检监察工作负责人",
        "overlap_org": "中共郸城县委",
        "overlap_period": "",
    },
    {
        "person_a": 1, "person_b": 6,
        "type": "overlap",
        "context": "县委书记与组织部部长，干部任免工作关系",
        "overlap_org": "中共郸城县委",
        "overlap_period": "",
    },
    {
        "person_a": 1, "person_b": 7,
        "type": "overlap",
        "context": "县委书记与宣传部部长",
        "overlap_org": "中共郸城县委",
        "overlap_period": "",
    },
    {
        "person_a": 1, "person_b": 8,
        "type": "overlap",
        "context": "县委书记与政法委书记",
        "overlap_org": "中共郸城县委",
        "overlap_period": "",
    },
    {
        "person_a": 1, "person_b": 9,
        "type": "overlap",
        "context": "县委书记与统战部部长",
        "overlap_org": "中共郸城县委",
        "overlap_period": "",
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# PERSON GRAPH JSON helpers
# ══════════════════════════════════════════════════════════════════════════════

def make_person_json(
    person: dict,
    career_timeline: list,
    relationships_list: list,
    source_register: list,
) -> dict:
    """Build a person graph JSON following the schema in person_graph_json.md."""
    return {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "河南省",
            "city": "周口市",
            "region": "郸城县",
            "job": person["current_post"],
            "task_id": "henan_郸城县",
            "time_focus": AS_OF,
        },
        "identity": {
            "person_id": f"dancheng_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": person["native_place"],
            "education": [],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}",
                "name_birthplace": f"{person['name']}_{person['birthplace']}",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正县处级" if "书记" in person["current_post"] and "副" not in person["current_post"] else "副县处级" if "副" in person["current_post"] or "常委" in person["current_post"] else "正县处级",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": [],
        },
        "career_timeline": career_timeline,
        "organizations": [],
        "relationships": relationships_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "公开资料缺失，无法评估",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "工作风格和个性特征仅基于公开记录推断，非专业心理评估。当前公开资料严重不足。",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "因网络搜索受限，未发现纪律处分或负面报道。需在恢复正常网络访问后重新核查。",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "因网络访问受限（Exa 限流、百度/Jina/Google 均超时或阻断），所有领导人姓名均未确认。需在恢复网络后从 dancheng.gov.cn 和 Baidu Baike 获取基本信息。",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "现任郸城县委书记是谁？",
                "why_it_matters": "核心目标人物",
                "suggested_queries": [
                    "郸城县 县委书记",
                    "dancheng.gov.cn 领导之窗",
                    "郸城县 县委 书记 任前公示 周口",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": "现任郸城县县长是谁？",
                "why_it_matters": "核心目标人物",
                "suggested_queries": [
                    "郸城县 县长",
                    "dancheng.gov.cn 领导分工",
                    "郸城县 县长 任免 周口人大",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "郸城县委全体常委名单？",
                "why_it_matters": "完整的领导班子上报关系网络的基础",
                "suggested_queries": [
                    "郸城县委常委 名单",
                    "郸城县 领导分工",
                    "郸城县委 领导班子",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "历任郸城县委书记和县长的任职时间及去向？",
                "why_it_matters": "理解人事变动模式和工作交接关系",
                "suggested_queries": [
                    "前任郸城县委书记",
                    "前任郸城县县长",
                    "郸城县 县委书记 卸任",
                ],
                "last_attempted": AS_OF,
            },
        ],
    }


# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════

def build() -> None:
    """Run the full build: DB, GEXF, person JSONs."""
    print(f"Building {SLUG} network data...")
    print(f"  DB path: {DB_PATH}")
    print(f"  GEXF path: {GEXF_PATH}")
    print(f"  Person JSON dir: {PJSON_DIR}")

    # ── Database + GEXF ──────────────────────────────────────────────────────
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

    # ── Person Graph JSONs ───────────────────────────────────────────────────
    source_register = [
        {
            "id": "S001",
            "title": "郸城县人民政府官方网站",
            "url": "https://www.dancheng.gov.cn/",
            "publisher": "郸城县人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "主站。因网络超时未能访问领导之窗页面。",
        },
        {
            "id": "S002",
            "title": "周口市人民政府官方网站",
            "url": "https://www.zhoukou.gov.cn/",
            "publisher": "周口市人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "因网络超时未能访问。周口市级领导信息见 henan_周口市 调研。",
        },
        {
            "id": "S003",
            "title": "百度百科 - 郸城县",
            "url": "https://baike.baidu.com/item/郸城县",
            "publisher": "百度",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "encyclopedia",
            "reliability": "medium",
            "notes": "因 Baidu 访问被阻断未能获取。",
        },
    ]

    # All persons use placeholder data for now
    from copy import deepcopy

    # Generate placeholder person JSONs
    for p in persons:
        placeholder_timeline = [
            {
                "start": "",
                "end": "",
                "org": "",
                "title": "履历缺口",
                "notes": f"网络访问受限，{p['name']} 的完整履历未找到。需恢复正常网络后从 Baidu Baike 或官方领导页面查询。",
                "confidence": "unverified",
                "source_ids": [],
            },
        ]
        p_json = make_person_json(p, placeholder_timeline, [], source_register)

        # Generate a meaningful filename even with placeholder name
        safe_name = p["name"].replace("待查_", "unknown_")
        p_path = PJSON_DIR / f"{TODAY}-河南省-周口市-{safe_name}.json"
        with open(p_path, "w", encoding="utf-8") as f:
            json.dump(p_json, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {p_path.name}")

    print(f"\n✅ {SLUG} build complete (partial-evidence mode).")
    print(f"   Database: {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
    print(f"   Person JSONs: {len(persons)} files in {PJSON_DIR}")
    print("")
    print("⚠️  ALL DATA IS PLACEHOLDER. Re-run with working web access to fill in real data.")
    print("   See report/open_gaps.md for detailed research gaps.")


if __name__ == "__main__":
    build()
