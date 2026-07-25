#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
兴海县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 青海省
Parent City: 海南藏族自治州
Region: 兴海县
Targets: 县委书记 & 县长

Task ID: qinghai_兴海县
Research Date: 2026-07-25

Research Sources:
- 百度百科 baike.baidu.com (兴海县词条) — 2026年7月访问，确认闫海峰当选县委书记
- 兴海县人民政府网站 (www.xinghai.gov.cn) — 访问返回403，不可用
- 百度搜索/必应搜索 — 被限流或超时，搜索结果不相关

Confidence Notes:
  All web search tools (Exa, Baidu, Bing, Google, Jina Reader) were rate-limited,
  blocked, or timed out during research. Government site www.xinghai.gov.cn returns 403.
  Baidu Baike page for 兴海县 was accessible and confirmed two leadership figures.

  This is a partial-evidence build per source_fallbacks.md artifact mode. Missing
  biographical details and the specific identity of the 县长 (county magistrate)
  are the primary gaps.

Current Status (as of 2026-07-25):
- 县委书记: 闫海峰 (confirmed — elected 2026-07-22 at 17th CPC Xinghai County Committee 1st Plenary)
- 县委副书记: 安娜 (confirmed — listed in 兴海县 Baike page "政治" section)
- 县长: 待确认 (possibly 安娜 if she concurrently serves as 县长, but not explicitly confirmed)
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
_REPO_ROOT = (_STAGING_DIR / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "兴海县"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-07-25"
TODAY = "20260725"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "闫海峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴海县委书记",
        "current_org": "中共兴海县委员会",
        "source": "百度百科兴海县词条（2026年7月访问）：2026年7月22日，中国共产党兴海县第十七届委员会第一次全体会议选举闫海峰为县委书记。confidence=confirmed"
    },
    {
        "id": 2,
        "name": "安娜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "兴海县委副书记",
        "current_org": "中共兴海县委员会",
        "source": "百度百科兴海县词条（2026年7月访问）：现任领导栏目显示安娜为县委副书记。confidence=confirmed"
    },
    # ════════════════════════════════════════
    # Potential Deputy Leaders (unverified)
    # ════════════════════════════════════════
    # The following are plausible based on standard county governance structure,
    # but specific names could not be confirmed. They are excluded from the graph
    # until verified.
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 101,
        "name": "中共兴海县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共海南藏族自治州委员会",
        "location": "青海省海南藏族自治州兴海县"
    },
    {
        "id": 102,
        "name": "兴海县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "海南藏族自治州人民政府",
        "location": "青海省海南藏族自治州兴海县"
    },
    {
        "id": 103,
        "name": "兴海县人民代表大会常务委员会",
        "type": "人大",
        "level": "县",
        "parent": "海南藏族自治州人民代表大会常务委员会",
        "location": "青海省海南藏族自治州兴海县"
    },
    {
        "id": 104,
        "name": "中国人民政治协商会议兴海县委员会",
        "type": "政协",
        "level": "县",
        "parent": "中国人民政治协商会议海南藏族自治州委员会",
        "location": "青海省海南藏族自治州兴海县"
    },
    {
        "id": 105,
        "name": "中共兴海县纪律检查委员会",
        "type": "纪委",
        "level": "县",
        "parent": "中共海南藏族自治州纪律检查委员会",
        "location": "青海省海南藏族自治州兴海县"
    },
    {
        "id": 106,
        "name": "中共兴海县委组织部",
        "type": "党委",
        "level": "县",
        "parent": "中共兴海县委员会",
        "location": "青海省海南藏族自治州兴海县"
    },
    {
        "id": 107,
        "name": "中共兴海县委宣传部",
        "type": "党委",
        "level": "县",
        "parent": "中共兴海县委员会",
        "location": "青海省海南藏族自治州兴海县"
    },
    {
        "id": 108,
        "name": "中共兴海县委政法委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共兴海县委员会",
        "location": "青海省海南藏族自治州兴海县"
    },
    {
        "id": 109,
        "name": "子科滩镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "兴海县人民政府",
        "location": "青海省海南藏族自治州兴海县子科滩镇"
    },
    {
        "id": 110,
        "name": "河卡镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "兴海县人民政府",
        "location": "青海省海南藏族自治州兴海县河卡镇"
    },
    {
        "id": 111,
        "name": "曲什安镇",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "兴海县人民政府",
        "location": "青海省海南藏族自治州兴海县曲什安镇"
    },
    {
        "id": 112,
        "name": "温泉乡",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "兴海县人民政府",
        "location": "青海省海南藏族自治州兴海县温泉乡"
    },
    {
        "id": 113,
        "name": "龙藏乡",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "兴海县人民政府",
        "location": "青海省海南藏族自治州兴海县龙藏乡"
    },
    {
        "id": 114,
        "name": "中铁乡",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "兴海县人民政府",
        "location": "青海省海南藏族自治州兴海县中铁乡"
    },
    {
        "id": 115,
        "name": "唐乃亥乡",
        "type": "乡镇/街道",
        "level": "乡镇",
        "parent": "兴海县人民政府",
        "location": "青海省海南藏族自治州兴海县唐乃亥乡"
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 闫海峰 — 县委书记
    {
        "person_id": 1,
        "org_id": 101,
        "title": "兴海县委书记",
        "start_date": "2026-07-22",
        "end_date": "",
        "rank": "正处级",
        "note": "2026年7月22日当选第十七届兴海县委书记"
    },
    # 安娜 — 县委副书记
    {
        "person_id": 2,
        "org_id": 101,
        "title": "兴海县委副书记",
        "start_date": "",
        "end_date": "",
        "rank": "副处级",
        "note": "现任兴海县委副书记，具体任职日期待确认"
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "共事",
        "context": "闫海峰（县委书记）与安娜（县委副书记）在兴海县第十七届县委班子中共同任职",
        "overlap_org": "中共兴海县委员会",
        "overlap_period": "2026-07-22至今"
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSON DATA (inline for generation)
# ══════════════════════════════════════════════════════════════════════════════

PERSON_JSONS = {
    "闫海峰": {
        "identity": {
            "person_id": "qinghai_xinghai_county_yanhaifeng",
            "name": "闫海峰",
            "aliases": [],
            "gender": "",
            "ethnicity": "",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "闫海峰_",
                "name_birthplace": "闫海峰_",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": "兴海县委书记",
            "current_org": "中共兴海县委员会",
            "administrative_rank": "正处级",
            "as_of": "2026-07-25",
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": [
            {
                "start": "2026-07-22",
                "end": "present",
                "org": "中共兴海县委员会",
                "title": "兴海县委书记",
                "level": "县",
                "location": "青海省海南藏族自治州兴海县",
                "system": "party",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "2026年7月22日在中国共产党兴海县第十七届委员会第一次全体会议上当选县委书记",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "",
                "notes": "公开资料未找到2026年7月之前的履历信息",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "organizations": [],
        "relationships": [
            {
                "person": "安娜",
                "person_id": "qinghai_xinghai_county_anna",
                "relationship_type": "overlap",
                "strength": "strong",
                "evidence": "闫海峰（县委书记）与安娜（县委副书记）在兴海县第十七届县委领导班子中共同任职",
                "overlap_org": "中共兴海县委员会",
                "overlap_period": "2026-07-22至今",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "信息不足，无法评估",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "unknown",
                    "evidence": "缺乏公开资料",
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至2026年7月，未发现闫海峰的纪律处分、审计问题或负面报道",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "兴海县 - 百度百科",
                "url": "https://baike.baidu.com/item/%E5%85%B4%E6%B5%B7%E5%8E%BF/3851763",
                "publisher": "百度百科",
                "published_at": "",
                "accessed_at": "2026-07-25",
                "source_type": "encyclopedia",
                "reliability": "medium",
                "notes": "百科页面'政治'栏目列出县委书记和县委副书记。最新新闻条目确认闫海峰当选。"
            }
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "闫海峰的完整履历（出生年月、籍贯、学历、曾任职务等）均未有公开来源确认"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "闫海峰就任兴海县委书记前的职务是什么？",
                "why_it_matters": "需要了解其职业路径和可能的跨县/跨系统交流背景",
                "suggested_queries": ["闫海峰 简历 兴海", "闫海峰 海南州 任职", "闫海峰 任前公示"],
                "last_attempted": "2026-07-25"
            },
            {
                "priority": "critical",
                "question": "闫海峰的出生年月、籍贯、学历、民族是什么？",
                "why_it_matters": "基础身份信息，用于人员去重和人物画像",
                "suggested_queries": ["闫海峰 出生", "闫海峰 籍贯"],
                "last_attempted": "2026-07-25"
            },
            {
                "priority": "high",
                "question": "闫海峰的前任（上一任兴海县委书记）是谁？",
                "why_it_matters": "县委书记的更替路径是关系网络的关键节点",
                "suggested_queries": ["兴海县 前任 县委书记", "兴海县委 换届 2026"],
                "last_attempted": "2026-07-25"
            }
        ]
    },
    "安娜": {
        "identity": {
            "person_id": "qinghai_xinghai_county_anna",
            "name": "安娜",
            "aliases": [],
            "gender": "",
            "ethnicity": "",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "安娜_",
                "name_birthplace": "安娜_",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": "兴海县委副书记",
            "current_org": "中共兴海县委员会",
            "administrative_rank": "副处级",
            "as_of": "2026-07-25",
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": [
            {
                "start": "",
                "end": "present",
                "org": "中共兴海县委员会",
                "title": "兴海县委副书记",
                "level": "县",
                "location": "青海省海南藏族自治州兴海县",
                "system": "party",
                "rank": "副处级",
                "is_key_promotion": False,
                "notes": "现任兴海县委副书记，具体任职起始时间待确认",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "",
                "notes": "公开资料未找到安娜任兴海县委副书记前的履历信息",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "organizations": [],
        "relationships": [
            {
                "person": "闫海峰",
                "person_id": "qinghai_xinghai_county_yanhaifeng",
                "relationship_type": "overlap",
                "strength": "strong",
                "evidence": "安娜（县委副书记）与闫海峰（县委书记）在兴海县第十七届县委领导班子中共同任职",
                "overlap_org": "中共兴海县委员会",
                "overlap_period": "2026-07-22至今",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "信息不足，无法评估",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "unknown",
                    "evidence": "缺乏公开资料",
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至2026年7月，未发现安娜的纪律处分、审计问题或负面报道",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "兴海县 - 百度百科",
                "url": "https://baike.baidu.com/item/%E5%85%B4%E6%B5%B7%E5%8E%BF/3851763",
                "publisher": "百度百科",
                "published_at": "",
                "accessed_at": "2026-07-25",
                "source_type": "encyclopedia",
                "reliability": "medium",
                "notes": "百科页面'政治'栏目列出安娜为县委副书记"
            }
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "安娜的完整履历（出生年月、籍贯、学历、曾任职务等）均未有公开来源确认"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": "安娜是否同时担任兴海县县长？",
                "why_it_matters": "在县级政治中，县委副书记通常兼任县长。如果安娜不是县长，则县长身份未知，是重大空缺。",
                "suggested_queries": ["兴海县 县长 安娜", "兴海县 第十七届 人民代表大会 县长 选举"],
                "last_attempted": "2026-07-25"
            },
            {
                "priority": "critical",
                "question": "安娜就任兴海县委副书记前的职务是什么？",
                "why_it_matters": "需要了解其职业路径和可能的跨县/跨系统交流背景",
                "suggested_queries": ["安娜 兴海县 任职", "安娜 海南州 简历"],
                "last_attempted": "2026-07-25"
            },
            {
                "priority": "critical",
                "question": "安娜的出生年月、籍贯、民族是什么？",
                "why_it_matters": "基础身份信息，用于人员去重和人物画像",
                "suggested_queries": ["安娜 兴海县 出生", "安娜 青海 简历"],
                "last_attempted": "2026-07-25"
            }
        ]
    }
}


# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════

def write_person_json(name: str, data: dict) -> None:
    """Write a single person JSON file to the staging directory."""
    job = data["current_status"]["current_post"]
    filename = f"{TODAY}-青海省-海南藏族自治州-{job}-{name}.json"
    path = PERSONS_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump({
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "青海省",
                "city": "海南藏族自治州",
                "region": "兴海县",
                "job": job,
                "task_id": "qinghai_兴海县",
                "time_focus": "2026年至今"
            },
            **data
        }, f, ensure_ascii=False, indent=2)
    print(f"  ✅ Person JSON: {filename}")


if __name__ == "__main__":
    print(f"Building {SLUG} leadership network...")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

    # Build SQLite DB and GEXF
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

    # Write person JSONs
    for name, data in PERSON_JSONS.items():
        write_person_json(name, data)

    print(f"\nDone! {len(persons)} persons, {len(organizations)} orgs, "
          f"{len(positions)} positions, {len(relationships)} relationships.")
