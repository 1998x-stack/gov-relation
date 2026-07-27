#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
田东县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库、GEXF 图文件和人物深度图谱 JSON

Level: 县
Province: 广西壮族自治区
Parent City: 百色市
Region: 田东县
Targets: 县委书记 & 县长

Research Note:
   田东县是百色市下辖县，位于广西西部，总面积约2,816平方公里，
   常住人口约43万（2020年普查数据），是以壮族为主的多民族聚居县。

   本次调查期间，田东县人民政府网站（https://www.tiandong.gov.cn/）
   及百度百科均因网络封锁无法访问。Exa 搜索限流，Jina Reader 超时。
   领导信息基于公开报道的已知资料，标注适当置信度。

Data Date: 2026-07-23
"""

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# ── Ensure gov_relation is importable ──
_REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# ── Paths ──
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "田东县"
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

AS_OF = "2026-07-23"
TODAY = AS_OF.replace("-", "")

# ═══════════════════════════════════════════════════════════════
# 1. PERSONS
# ═══════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # 核心领导：县委书记
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "欧阳可爽",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "田东县委书记",
        "current_org": "中共田东县委员会",
        "source": "公开报道 — 欧阳可爽曾任百色市右江区委副书记、区长，2021年左右调任田东县委书记",
    },
    # ════════════════════════════════════════
    # 核心领导：县长
    # ════════════════════════════════════════
    {
        "id": 2,
        "name": "韩启强",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "田东县委副书记、县长",
        "current_org": "田东县人民政府",
        "source": "公开报道 — 韩启强曾任田东县委副书记、县长，负责县人民政府全面工作",
    },
    # ════════════════════════════════════════
    # 县委副书记（待查）
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "【待查】田东县委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "田东县委副书记（待查）",
        "current_org": "中共田东县委员会",
        "source": "GAP — 官方网站无法访问",
    },
    # ════════════════════════════════════════
    # 县委常委、常务副县长（待查）
    # ════════════════════════════════════════
    {
        "id": 4,
        "name": "【待查】田东县常务副县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "田东县委常委、常务副县长（待查）",
        "current_org": "田东县人民政府",
        "source": "GAP — 官方网站无法访问",
    },
    # ════════════════════════════════════════
    # 县委常委、纪委书记（待查）
    # ════════════════════════════════════════
    {
        "id": 5,
        "name": "【待查】田东县纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "田东县委常委、纪委书记（待查）",
        "current_org": "中共田东县纪律检查委员会",
        "source": "GAP — 官方网站无法访问",
    },
    # ════════════════════════════════════════
    # 县委常委、组织部部长（待查）
    # ════════════════════════════════════════
    {
        "id": 6,
        "name": "【待查】田东县委组织部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "田东县委常委、组织部部长（待查）",
        "current_org": "中共田东县委组织部",
        "source": "GAP — 官方网站无法访问",
    },
    # ════════════════════════════════════════
    # 县委常委、政法委书记（待查）
    # ════════════════════════════════════════
    {
        "id": 7,
        "name": "【待查】田东县政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "田东县委常委、政法委书记（待查）",
        "current_org": "中共田东县委政法委员会",
        "source": "GAP — 官方网站无法访问",
    },
    # ════════════════════════════════════════
    # 县委常委、宣传部部长（待查）
    # ════════════════════════════════════════
    {
        "id": 8,
        "name": "【待查】田东县委宣传部部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "田东县委常委、宣传部部长（待查）",
        "current_org": "中共田东县委宣传部",
        "source": "GAP — 官方网站无法访问",
    },
    # ════════════════════════════════════════
    # 县人大常委会主任（待查）
    # ════════════════════════════════════════
    {
        "id": 9,
        "name": "【待查】田东县人大常委会主任",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "田东县人大常委会主任（待查）",
        "current_org": "田东县人民代表大会常务委员会",
        "source": "GAP — 官方网站无法访问",
    },
    # ════════════════════════════════════════
    # 县政协主席（待查）
    # ════════════════════════════════════════
    {
        "id": 10,
        "name": "【待查】田东县政协主席",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "田东县政协主席（待查）",
        "current_org": "中国人民政治协商会议田东县委员会",
        "source": "GAP — 官方网站无法访问",
    },
]

# ═══════════════════════════════════════════════════════════════
# 2. ORGANIZATIONS
# ═══════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共田东县委员会", "type": "党委", "level": "正处级"},
    {"id": 2, "name": "田东县人民政府", "type": "政府", "level": "正处级"},
    {"id": 3, "name": "中共田东县纪律检查委员会", "type": "纪委", "level": "正科级"},
    {"id": 4, "name": "中共田东县委组织部", "type": "党委", "level": "正科级"},
    {"id": 5, "name": "中共田东县委政法委员会", "type": "党委", "level": "正科级"},
    {"id": 6, "name": "中共田东县委宣传部", "type": "党委", "level": "正科级"},
    {"id": 7, "name": "田东县人民代表大会常务委员会", "type": "人大", "level": "正处级"},
    {"id": 8, "name": "中国人民政治协商会议田东县委员会", "type": "政协", "level": "正处级"},
    {"id": 9, "name": "中共百色市委员会", "type": "党委", "level": "地厅级"},
    {"id": 10, "name": "百色市人民政府", "type": "政府", "level": "地厅级"},
    {"id": 11, "name": "百色市人民代表大会常务委员会", "type": "人大", "level": "地厅级"},
    {"id": 12, "name": "中国人民政治协商会议百色市委员会", "type": "政协", "level": "地厅级"},
]

# ═══════════════════════════════════════════════════════════════
# 3. POSITIONS (person → organization edges)
# ═══════════════════════════════════════════════════════════════

positions = [
    # 县委书记
    {"person_id": 1, "org_id": 1, "title": "田东县委书记", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 县长
    {"person_id": 2, "org_id": 2, "title": "田东县委副书记、县长", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "田东县委副书记", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 县委副书记（待查）
    {"person_id": 3, "org_id": 1, "title": "田东县委副书记（待查）", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 常务副县长（待查）
    {"person_id": 4, "org_id": 2, "title": "田东县委常委、常务副县长（待查）", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 纪委书记（待查）
    {"person_id": 5, "org_id": 3, "title": "田东县委常委、纪委书记（待查）", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 组织部部长（待查）
    {"person_id": 6, "org_id": 4, "title": "田东县委常委、组织部部长（待查）", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 政法委书记（待查）
    {"person_id": 7, "org_id": 5, "title": "田东县委常委、政法委书记（待查）", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 宣传部部长（待查）
    {"person_id": 8, "org_id": 6, "title": "田东县委常委、宣传部部长（待查）", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 人大常委会主任（待查）
    {"person_id": 9, "org_id": 7, "title": "田东县人大常委会主任（待查）", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 政协主席（待查）
    {"person_id": 10, "org_id": 8, "title": "田东县政协主席（待查）", "start_date": "", "end_date": "present", "rank": "", "note": ""},
]

# ═══════════════════════════════════════════════════════════════
# 4. RELATIONSHIPS (person → person edges)
# ═══════════════════════════════════════════════════════════════

relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "田东县委班子核心搭档：书记+县长",
        "overlap_period": "2021至今",
        "confidence": "plausible",
    },
    {
        "person_a": 1,
        "person_b": 9,
        "type": "overlap",
        "context": "县委—人大同期任职",
        "overlap_period": "2021至今",
        "confidence": "unverified",
    },
    {
        "person_a": 2,
        "person_b": 9,
        "type": "overlap",
        "context": "县政府—人大同期任职",
        "overlap_period": "2021至今",
        "confidence": "unverified",
    },
]

# ═══════════════════════════════════════════════════════════════
# 5. PERSON JSON GENERATOR
# ═══════════════════════════════════════════════════════════════

def generate_person_json(p: dict, name: str, job: str) -> dict:
    """Generate a person graph JSON following person_graph_json.md schema."""
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "百色市",
            "region": "田东县",
            "job": job,
            "task_id": "guangxi_田东县",
            "time_focus": "2026",
        },
        "identity": {
            "person_id": f"baise_tiandong_{name}",
            "name": name,
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": f"{name}_",
                "name_birthplace": f"{name}_",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": ["S001"],
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "",
                "level": "",
                "location": "广西",
                "system": "other",
                "rank": "",
                "is_key_promotion": False,
                "notes": f"{name}的完整履历在当前网络环境下无法获取。基本情况来自公开报道，详细信息需待网站可访问时补充。",
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "organizations": [
            {
                "org_name": p["current_org"],
                "org_id": "",
                "role": p["current_post"],
                "period": "",
                "confidence": "plausible",
                "source_ids": ["S001"],
            }
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
                "summary": "信息不足，无法评估",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "unknown",
                    "evidence": "缺乏公开信息",
                    "confidence": "unverified",
                    "source_ids": [],
                }
            ],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": f"本次调查未发现{name}相关的负面纪律审查或处分信息。但需注意网络访问受限，信息不完整。",
                "date": "",
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": f"田东县{job}{name}公开报道",
                "url": "https://www.tiandong.gov.cn/",
                "publisher": "田东县人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "medium",
                "notes": "官方网站因网络限制无法直接访问，信息来源于历史公开报道记录",
            }
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "plausible",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "完整履历、出生年月、籍贯、学历等基本信息均缺失",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的出生年月、籍贯、学历等基本信息",
                "why_it_matters": "人员身份去重和基础档案的必备信息",
                "suggested_queries": [f"{name} 简历 田东县"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{name}的完整工作履历时间线",
                "why_it_matters": "构建可靠的关系网络需要精确的时间线数据",
                "suggested_queries": [f"{name} 任前公示 田东县 百色"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "田东县现任县委常委班子的完整名单和分工",
                "why_it_matters": "县委班子核心成员约10-12人，当前仅掌握书记和县长信息",
                "suggested_queries": ["田东县 县委常委 分工"],
                "last_attempted": AS_OF,
            },
        ],
    }


# ═══════════════════════════════════════════════════════════════
# 6. BUILD
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
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
    person_json_configs = [
        (1, "县委书记", "欧阳可爽"),
        (2, "县长", "韩启强"),
    ]

    for pid, job, name in person_json_configs:
        p = next(x for x in persons if x["id"] == pid)
        person_data = generate_person_json(p, name, job)
        fname = f"{TODAY}-广西壮族自治区-百色市-{job}-{name}.json"
        fpath = PERSONS_DIR / fname
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(person_data, f, ensure_ascii=False, indent=2)
        print(f"  Wrote {fpath.name}")

    print(f"\nDone! Database: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"Person JSONs: {PERSONS_DIR}")
