#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 文圣区, 辽阳市, 辽宁省.

Investigation date: 2026-07-25
Task ID: liaoning_文圣区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - Web search (Exa, Baidu, Google, Bing): all rate-limited or blocked (403/timeout)
  - Official website www.lywensheng.gov.cn: unreachable (connection timeout)
  - Parent city site www.liaoyang.gov.cn: unreachable
  - Jina Reader: timeouts on all Chinese government and encyclopedia URLs

Key findings:
  - 文圣区 is a district under Liaoyang City, Liaoning Province
  - Current officeholders COULD NOT BE CONFIRMED via live web due to total web access failure
  - No existing artifacts found in local repo for 文圣区
  - Neighboring district build scripts (白塔区, 弓长岭区) exist and provided pattern
  - All fields based on pre-training knowledge, marked as unverified

Confidence notes:
  - All identity fields marked as unverified — no live source could confirm current officeholders
  - Current posts and names may be outdated; explicit gap entries created
  - Person JSON files created with open_questions for future web-based verification
  - Build script structurally valid but data content requires web verification
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "文圣区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "liaoning_文圣区"
if _CURRENT_DIR.name == "liaoning_文圣区":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1xxx = party committee, 2xxx = government, 3xxx = predecessor
# NOTE: All names are based on pre-training knowledge (latest ~early 2025) and
# COULD NOT BE VERIFIED via live web. Mark all as unverified.

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current — UNVERIFIED)
    # ══════════════════════════════════════════════════════════════════════
    # 1. 郑海涛 — 区委书记
    {
        "id": 1001,
        "name": "郑海涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "文圣区委书记",
        "current_org": "中共辽阳市文圣区委员会",
        "source": "unverified — web search unavailable during investigation",
    },
    # 2. 郭振峰 — 区政府党组书记、区长
    {
        "id": 2001,
        "name": "郭振峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "文圣区委副书记、区长",
        "current_org": "文圣区人民政府",
        "source": "unverified — web search unavailable during investigation",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {
        "id": 10,
        "name": "中共辽阳市文圣区委员会",
        "type": "party",
        "level": "district",
        "parent": "中共辽阳市委员会",
        "location": "文圣区",
    },
    {
        "id": 11,
        "name": "文圣区人民政府",
        "type": "government",
        "level": "district",
        "parent": "辽阳市人民政府",
        "location": "文圣区",
    },
    {
        "id": 12,
        "name": "辽阳市文圣区人民代表大会常务委员会",
        "type": "npc",
        "level": "district",
        "parent": "辽阳市人民代表大会常务委员会",
        "location": "文圣区",
    },
    {
        "id": 13,
        "name": "中国人民政治协商会议辽阳市文圣区委员会",
        "type": "cppcc",
        "level": "district",
        "parent": "政协辽阳市委员会",
        "location": "文圣区",
    },
    {
        "id": 14,
        "name": "中共辽阳市文圣区纪律检查委员会",
        "type": "party_discipline",
        "level": "district",
        "parent": "中共辽阳市纪律检查委员会",
        "location": "文圣区",
    },
]

# ── Positions ─────────────────────────────────────────────────────────────────
positions = [
    # 郑海涛 — 区委书记
    {"person_id": 1001, "org_id": 10, "title": "文圣区委书记", "start": "", "end": "present", "rank": "正县级", "note": "当前任职未通过官网验证"},
    # 郭振峰 — 区长
    {"person_id": 2001, "org_id": 11, "title": "文圣区区长", "start": "", "end": "present", "rank": "正县级", "note": "全称为区委副书记、区政府区长；当前任职未通过官网验证"},
    {"person_id": 2001, "org_id": 10, "title": "文圣区委副书记", "start": "", "end": "present", "rank": "正县级", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 郑海涛 ↔ 郭振峰 — 书记+区长搭档
    {
        "person_a": 1001,
        "person_b": 2001,
        "type": "superior_subordinate",
        "context": "区委书记与区长党政搭档关系",
        "overlap_org": "中共辽阳市文圣区委员会/文圣区人民政府",
        "overlap_period": "至今",
    },
]

# ── Person JSON helper ───────────────────────────────────────────────────────
def write_person_json(person: dict, extra: dict | None = None) -> Path:
    """Write a per-person deep profile JSON file."""
    pid = person["id"]
    name = person["name"]
    job = person.get("current_post", "")
    if "区长" in job and "副区长" not in job:
        job_short = "区长"
    elif "区委书记" in job:
        job_short = "区委书记"
    else:
        job_short = "领导"

    pjson = extra or {}
    pjson.update({
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "辽阳市",
            "region": "文圣区",
            "job": job_short,
            "task_id": "liaoning_文圣区",
            "time_focus": "2026",
        },
        "identity": {
            "person_id": f"wensheng_{name}",
            "name": name,
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": [],
        },
        "career_timeline": [],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {},
        "work_style_and_personality": {"public_style_indicators": [], "caveat": "No public evidence available for style/personality assessment."},
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": [],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "全部履历信息均未通过任何公开来源验证（调查期间所有搜索工具均受限）",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的当前职务是否仍为文圣区{job_short}？完整履历（出生、籍贯、教育、此前任职）",
                "why_it_matters": "核心人物的全部基础信息需确认",
                "suggested_queries": [
                    f"文圣区 {name} {job_short}",
                    f"{name} 简历 辽阳",
                    f"{name} 任前公示 文圣区",
                    f"www.lywensheng.gov.cn 领导之窗 {name}",
                ],
                "last_attempted": AS_OF,
            }
        ],
    })

    fname = f"{TODAY}-辽宁省-辽阳市-{job_short}-{name}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(pjson, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath}")
    return fpath


# ── Build ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Write person JSONs for core figures
    for p in persons:
        pid = p["id"]
        name = p["name"]

        # Build extra data for key figures
        extra = None
        if pid == 1001:  # 郑海涛 — 区委书记
            extra = {
                "career_timeline": [
                    {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开资料未找到郑海涛担任文圣区委书记之前的任何履历信息（调查期间所有搜索工具受限）", "confidence": "unverified"},
                    {"start": "未知", "end": "present", "org": "中共辽阳市文圣区委员会", "title": "文圣区委书记", "level": "正县级", "location": "辽阳市文圣区", "system": "party", "confidence": "unverified", "source_ids": []},
                ],
                "source_register": [
                    {"id": "S001", "title": "文圣区人民政府官方网站", "url": "https://www.lywensheng.gov.cn/", "publisher": "文圣区人民政府", "source_type": "official", "reliability": "high", "notes": "网站无法访问（连接超时），未获取到任何内容"},
                ],
            }
        elif pid == 2001:  # 郭振峰 — 区长
            extra = {
                "career_timeline": [
                    {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开资料未找到郭振峰担任文圣区区长之前的任何履历信息（调查期间所有搜索工具受限）", "confidence": "unverified"},
                    {"start": "未知", "end": "present", "org": "文圣区人民政府", "title": "文圣区区长", "level": "正县级", "location": "辽阳市文圣区", "system": "government", "notes": "全称为区委副书记、区政府区长", "confidence": "unverified", "source_ids": []},
                    {"start": "未知", "end": "present", "org": "中共辽阳市文圣区委员会", "title": "文圣区委副书记", "level": "正县级", "location": "辽阳市文圣区", "system": "party", "confidence": "unverified", "source_ids": []},
                ],
                "source_register": [
                    {"id": "S001", "title": "文圣区人民政府官方网站", "url": "https://www.lywensheng.gov.cn/", "publisher": "文圣区人民政府", "source_type": "official", "reliability": "high", "notes": "网站无法访问（连接超时），未获取到任何内容"},
                ],
            }

        write_person_json(p, extra)

    # Print summary for logging
    print(f"\n{SLUG} network build complete.")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
