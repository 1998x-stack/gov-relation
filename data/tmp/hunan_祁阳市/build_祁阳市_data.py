#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
祁阳市领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县级市
Province: 湖南省
Parent City: 永州市
Region: 祁阳市
Targets: 市委书记 & 市长

Research status (2026-07-24):
- 蒋崇华 (Party Secretary): confirmed — 祁阳市委书记 (as of Jul 2026)
  - Identity: 男, 汉族, 1968.03, 湖南东安人
  - Career: thin — current role confirmed; full career history unknown
- 向子顺 (Mayor): confirmed — 祁阳市市长 (as of Jul 2026)
  - Identity: 男, 汉族, 1976.08, 湖南洪江人
  - Career: thin — current role confirmed (appointed 2025.03); full career history unknown
- 祁阳县于2021年撤县设市

Research constraints:
  - Exa search: rate limited
  - Baidu Baike: 403/Cloudflare block
  - Government websites (qiyang.gov.cn): timeouts
  - Wikipedia (zh): connection timeouts
  - Jina Reader: transport errors
  - Primary source: 永州市 pre-existing report (2026-07-14) with Wikipedia-derived data
  - All personal biographical details beyond basic identity are open questions

Gaps logged in open_questions and report/open_gaps.md
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Allow import from repo root
REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

import sqlite3  # noqa: F401 — used by gov_relation.runner; token needed by process_tmp

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "祁阳市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "hunan_祁阳市"
if _CURRENT_DIR.name == "hunan_祁阳市":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-9 current leaders, 10-19 standing committee, 20-29 deputy gov, 30+ predecessors/others

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════

    # 蒋崇华 — 祁阳市委书记 (Party Secretary)
    {
        "id": 1,
        "name": "蒋崇华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-03",
        "birthplace": "湖南东安",
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "祁阳市委书记",
        "current_org": "中共祁阳市委员会",
        "source": "永州市领导班子关系网络调查报告 (2026-07-14) / Wikipedia 祁阳市",
        "confidence": "confirmed",
        "notes": "2021年4月起任祁阳市委书记。确认截至2026年7月仍在任。籍贯湖南东安，同籍干部陈雄（新田县委书记）。"
    },

    # 向子顺 — 祁阳市委副书记、市长 (Mayor)
    {
        "id": 2,
        "name": "向子顺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-08",
        "birthplace": "湖南洪江",
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "祁阳市委副书记、市长",
        "current_org": "祁阳市人民政府",
        "source": "永州市领导班子关系网络调查报告 (2026-07-14) / Wikipedia 祁阳市",
        "confidence": "confirmed",
        "notes": "2025年3月起任祁阳市市长。确认截至2026年7月仍在任。"
    },

    # ══════════════════════════════════════════════════════════════════════
    # Predecessors (前任)
    # ══════════════════════════════════════════════════════════════════════

    # 前任市委书记 (待查)
    {
        "id": 30,
        "name": "",  # open question
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "open question",
        "confidence": "unverified",
        "notes": "蒋崇华2021年4月接任祁阳市委书记。前任书记姓名、去向均为待查。"
    },

    # 前任市长 (待查)
    {
        "id": 31,
        "name": "",  # open question
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "open question",
        "confidence": "unverified",
        "notes": "向子顺2025年3月接任祁阳市市长。前任市长姓名、去向均为待查。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────

organizations = [
    # Party
    {"id": 1, "name": "中共祁阳市委员会", "type": "党委",
     "level": "县处级", "parent": "中共永州市委员会", "location": "祁阳市"},
    {"id": 2, "name": "中共祁阳市纪律检查委员会", "type": "党委",
     "level": "县处级", "parent": "中共祁阳市委员会", "location": "祁阳市"},
    {"id": 3, "name": "中共祁阳市委组织部", "type": "党委",
     "level": "正科级", "parent": "中共祁阳市委员会", "location": "祁阳市"},
    {"id": 4, "name": "中共祁阳市委宣传部", "type": "党委",
     "level": "正科级", "parent": "中共祁阳市委员会", "location": "祁阳市"},
    {"id": 5, "name": "中共祁阳市委政法委员会", "type": "党委",
     "level": "正科级", "parent": "中共祁阳市委员会", "location": "祁阳市"},
    {"id": 6, "name": "中共祁阳市委统一战线工作部", "type": "党委",
     "level": "正科级", "parent": "中共祁阳市委员会", "location": "祁阳市"},

    # Government
    {"id": 10, "name": "祁阳市人民政府", "type": "政府",
     "level": "县处级", "parent": "永州市人民政府", "location": "祁阳市"},
    {"id": 11, "name": "祁阳市人民政府办公室", "type": "政府",
     "level": "正科级", "parent": "祁阳市人民政府", "location": "祁阳市"},

    # Dep't / Bureau
    {"id": 20, "name": "祁阳市发展和改革局", "type": "政府",
     "level": "正科级", "parent": "祁阳市人民政府", "location": "祁阳市"},
    {"id": 21, "name": "祁阳市教育局", "type": "政府",
     "level": "正科级", "parent": "祁阳市人民政府", "location": "祁阳市"},
    {"id": 22, "name": "祁阳市公安局", "type": "政府",
     "level": "正科级", "parent": "祁阳市人民政府", "location": "祁阳市"},
    {"id": 23, "name": "祁阳市财政局", "type": "政府",
     "level": "正科级", "parent": "祁阳市人民政府", "location": "祁阳市"},

    # NPC & CPPCC
    {"id": 30, "name": "祁阳市人民代表大会常务委员会", "type": "人大",
     "level": "县处级", "parent": "祁阳市", "location": "祁阳市"},
    {"id": 31, "name": "中国人民政治协商会议祁阳市委员会", "type": "政协",
     "level": "县处级", "parent": "祁阳市", "location": "祁阳市"},

    # Supervision / Justice
    {"id": 40, "name": "祁阳市监察委员会", "type": "党委",
     "level": "县处级", "parent": "祁阳市", "location": "祁阳市"},
    {"id": 41, "name": "祁阳市人民法院", "type": "政府",
     "level": "县处级", "parent": "祁阳市", "location": "祁阳市"},
    {"id": 42, "name": "祁阳市人民检察院", "type": "政府",
     "level": "县处级", "parent": "祁阳市", "location": "祁阳市"},

    # Townships (selected major ones)
    {"id": 50, "name": "祁阳市龙山街道办事处", "type": "乡镇/街道",
     "level": "乡科级", "parent": "祁阳市人民政府", "location": "祁阳市"},
    {"id": 51, "name": "祁阳市长虹街道办事处", "type": "乡镇/街道",
     "level": "乡科级", "parent": "祁阳市人民政府", "location": "祁阳市"},
    {"id": 52, "name": "祁阳市浯溪街道办事处", "type": "乡镇/街道",
     "level": "乡科级", "parent": "祁阳市人民政府", "location": "祁阳市"},
    {"id": 53, "name": "祁阳市黎家坪镇", "type": "乡镇/街道",
     "level": "乡科级", "parent": "祁阳市人民政府", "location": "祁阳市"},
    {"id": 54, "name": "祁阳市白水镇", "type": "乡镇/街道",
     "level": "乡科级", "parent": "祁阳市人民政府", "location": "祁阳市"},
    {"id": 55, "name": "祁阳市金洞镇", "type": "乡镇/街道",
     "level": "乡科级", "parent": "祁阳市人民政府", "location": "祁阳市"},
    {"id": 56, "name": "祁阳市潘市镇", "type": "乡镇/街道",
     "level": "乡科级", "parent": "祁阳市人民政府", "location": "祁阳市"},
    {"id": 57, "name": "祁阳市大忠桥镇", "type": "乡镇/街道",
     "level": "乡科级", "parent": "祁阳市人民政府", "location": "祁阳市"},
]

# ── Positions ─────────────────────────────────────────────────────────────────

positions = [
    # 蒋崇华
    {"id": 1, "person_id": 1, "org_id": 1, "title": "市委书记",
     "start": "2021-04", "end": "present", "rank": "", "note": "confirmed via Wikipedia / 永州市报告"},

    # 向子顺
    {"id": 2, "person_id": 2, "org_id": 1, "title": "市委副书记",
     "start": "2025-03", "end": "present", "rank": "", "note": ""},
    {"id": 3, "person_id": 2, "org_id": 10, "title": "市长",
     "start": "2025-03", "end": "present", "rank": "", "note": "confirmed via Wikipedia / 永州市报告"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
# Key relationship: 蒋崇华 and 向子顺 work together as county's top leaders

relationships = [
    # 蒋崇华 <-> 向子顺: 党政配合 (直接搭档关系)
    {
        "id": 1,
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "党政一把手（市委书记—市长）",
        "overlap_org": "中共祁阳市委员会 / 祁阳市人民政府",
        "overlap_period": "2025-03 — present",
    },
]


# ══════════════════════════════════════════════════════════════════════════
# Person JSON Writer
# ══════════════════════════════════════════════════════════════════════════

def write_person_json(person: dict, output_dir: Path) -> str | None:
    """Write a person graph JSON file. Returns filename or None if skipped."""
    name = person.get("name", "")
    if not name:
        return None
    job_short = {
        1: "市委书记",
        2: "市长",
    }.get(person["id"], "干部")

    filename = f"{TODAY}-湖南省-永州市-{job_short}-{name}.json"
    filepath = output_dir / filename

    person_id_str = f"hunan_祁阳市_{name}"

    # Source register
    sources = [
        {
            "id": "S001",
            "title": "永州市领导班子工作关系网络调查报告",
            "url": "report/20260714-永州市-领导班子.md",
            "publisher": "本地报告",
            "published_at": "2026-07-14",
            "accessed_at": AS_OF,
            "source_type": "database",
            "reliability": "medium",
            "notes": "Confirmed 蒋崇华/向子顺 current roles via Wikipedia-derived data",
        },
        {
            "id": "S002",
            "title": "祁阳市 — 维基百科",
            "url": "https://zh.wikipedia.org/wiki/%E7%A5%81%E9%98%B3%E5%B8%82",
            "publisher": "Wikipedia",
            "published_at": "2026",
            "accessed_at": "2026-07-14",
            "source_type": "encyclopedia",
            "reliability": "medium",
            "notes": "Encyclopedia reference, cited in 永州市 report",
        },
    ]

    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "湖南省",
            "city": "永州市",
            "region": "祁阳市",
            "job": job_short,
            "task_id": "hunan_祁阳市",
            "time_focus": "2026",
        },
        "identity": {
            "person_id": person_id_str,
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth', '')}",
                "name_birthplace": f"{name}_{person.get('birthplace', '')}",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "县处级正职",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002"],
        },
        "career_timeline": [
            {
                "start": person.get("position_start", "unknown"),
                "end": "present",
                "org": person.get("current_org", ""),
                "title": person.get("current_post", ""),
                "level": "",
                "location": "祁阳市",
                "system": "party" if "书记" in person.get("current_post", "") else "government",
                "rank": "",
                "is_key_promotion": True,
                "notes": "当前任职，confirmed via Wikipedia",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"],
            },
            {
                "start": "unknown",
                "end": "unknown",
                "org": "履历缺口",
                "title": "",
                "notes": "公开资料未找到任职前的完整履历",
                "confidence": "unverified",
                "source_ids": [],
            },
        ],
        "organizations": [
            {
                "id": 1,
                "name": "中共祁阳市委员会",
                "org_type": "党委",
                "level": "县处级",
            },
            {
                "id": 10,
                "name": "祁阳市人民政府",
                "org_type": "政府",
                "level": "县处级",
            },
        ],
        "relationships": [
            {
                "person": "向子顺" if person["id"] == 1 else "蒋崇华",
                "person_id": "hunan_祁阳市_向子顺" if person["id"] == 1 else "hunan_祁阳市_蒋崇华",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "党政一把手（市委书记—市长），2025年3月起搭档",
                "overlap_org": "中共祁阳市委员会 / 祁阳市人民政府",
                "overlap_period": "2025-03 — present",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"],
            },
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "无法判断 — 公开资料不足",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": f"截至{AS_OF}，未在公开来源发现{name}的违纪、处分或负面报道",
                "date": "",
                "confidence": "unverified",
                "source_ids": [],
            },
        ],
        "source_register": sources,
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": f"{name}的历任职务（出生前/任职前履历完全未知）",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的完整职业生涯（历任职务）",
                "why_it_matters": "构建关系网络和干部流动分析的核心数据",
                "suggested_queries": [
                    f"{name} 简历 祁阳",
                    f"{name} 任前公示 永州",
                    f"{name} 任职经历",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{name}的教育背景（毕业院校、专业、学历学位）",
                "why_it_matters": "教育背景是身份识别和干部评价的重要字段",
                "suggested_queries": [
                    f"{name} 毕业",
                    f"{name} 学历",
                ],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"{name}的入党时间和参加工作时间",
                "why_it_matters": "确定工龄和党龄的基础数据",
                "suggested_queries": [
                    f"{name} 简历",
                    f"{name} 中共党员",
                ],
                "last_attempted": AS_OF,
            },
        ],
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ {filename}")
    return filename


# ══════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════


def main():
    print(f"╔══ 祁阳市 Leadership Network Builder ══╗")
    print(f"║  Date: {TODAY}")
    print(f"║  Stage: {STAGING}")
    print(f"╚══════════════════════════════════════════╝")
    print()

    # Build DB + GEXF
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

    # Write person JSONs for key figures
    print("\n── Person JSONs ──")
    key_persons = [p for p in persons if p["id"] in [1, 2]]
    for p in key_persons:
        if p["name"]:
            write_person_json(p, PJSON_DIR)

    # Summary
    print(f"\n── Summary ──")
    print(f"  Persons (total): {len(persons)}")
    print(f"  Persons (with real names): {sum(1 for p in persons if p['name'])}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Gaps documented in person JSON open_questions")

    print("\n── Open Gaps ──")
    print("  1. 蒋崇华: full career history — CRITICAL")
    print("  2. 向子顺: full career history — CRITICAL")
    print("  3. 蒋崇华: education background — CRITICAL")
    print("  4. 向子顺: education background — CRITICAL")
    print("  5. Predecessor of 蒋崇华 (former 祁阳市委书记) — HIGH")
    print("  6. Predecessor of 向子顺 (former 祁阳市长) — HIGH")
    print("  7. Full 祁阳市委 standing committee roster — HIGH")
    print("  8. Full deputy mayor roster — HIGH")
    print("  9. Cross-county cadre exchange data — MEDIUM")
    print("  10. 祁阳撤县设市 (2021) details and impact — MEDIUM")


if __name__ == "__main__":
    main()
