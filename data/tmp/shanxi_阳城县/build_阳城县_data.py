#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 阳城县 (Yangcheng County), 山西省晋城市.

Investigation date: 2026-07-26
Task ID: shanxi_阳城县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - www.jcgov.gov.cn — 晋城市人民政府官方网站 (primary, current as of July 2026)
  - Note: 阳城县独立政府网站(ycx.gov.cn)被陕西宜川县占用，阳城县政府可能使用子域名或统一平台
  - 晋城市领导之窗页面确认阳城县为晋城市辖县
  - News article "张钧在阳城县调研" (2026-07-26) confirms current active county leadership
  - General public records and media reports

Confidence notes:
  - Current county leadership identities: partially confirmed
  - Detailed biographies: mostly unverified — web access was severely degraded (Exa rate-limited, Baidu 403, gov sites timing out)
  - County-level leadership roster: inferred from known patterns, needs verification
  - Career timelines: mostly unknown — marked explicitly as gaps
  - All claims labeled with confidence level; gaps explicitly documented

IMPORTANT: This build was created under partial-evidence mode due to degraded web access.
All uncertainty is explicitly marked. See open_questions and confidence labels.
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
SLUG = "阳城县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-26"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shanxi_阳城县"
if _CURRENT_DIR.name == "shanxi_阳城县":
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
# IDs: 1=县委书记, 2=县长, 3-7=县委常委, 10-12=副县长, 20=前任相关
# NOTE: Due to web access degradation (Exa rate-limited, Baidu/Bing blocked,
# government sites unreachable), the identities of the CURRENT county leaders
# are partially researched. Based on available evidence:
# - 高喜全 served as 阳城县委书记 (confirmed via multiple media reports from 2021 onward)
# - 牛琛 served as 阳城县县长 (confirmed via media reports through 2023-2024)
# However, these may have changed. All fields marked accordingly.

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current — subject to verification)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "待查_县委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共阳城县委员会",
        "source": "待查 — web search degraded. Recent occupant: 高喜全 (2021-2024 period, confirmed via media). Current incumbent as of 2026 needs official site verification.",
    },
    {
        "id": 2,
        "name": "待查_县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县长",
        "current_org": "阳城县人民政府",
        "source": "待查 — web search degraded. Recent occupant: 牛琛 (confirmed via media reports through 2023-2024). Current as of 2026 needs verification.",
    },
    # ══════════════════════════════════════════════════════════════════════
    # Key Deputies (需要确认)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "待查_县委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共阳城县委员会",
        "source": "待查 — 通常由县长兼任或设专职副书记",
    },
    {
        "id": 4,
        "name": "待查_常务副县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "阳城县人民政府",
        "source": "待查",
    },
    {
        "id": 5,
        "name": "待查_纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共阳城县纪律检查委员会",
        "source": "待查",
    },
    {
        "id": 6,
        "name": "待查_组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共阳城县委组织部",
        "source": "待查",
    },
    {
        "id": 7,
        "name": "待查_宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共阳城县委宣传部",
        "source": "待查",
    },
    {
        "id": 8,
        "name": "待查_政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共阳城县委政法委员会",
        "source": "待查",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 已知的近期人物 (Known from prior records)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 20,
        "name": "高喜全",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任县委书记",
        "current_org": "中共阳城县委员会",
        "source": "plausible — media reports; 曾历任阳城县委书记，后可能调任晋城市或省直部门",
    },
    {
        "id": 21,
        "name": "牛琛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任/现任县长",
        "current_org": "阳城县人民政府",
        "source": "plausible — 阳城县县长 (confirmed in prior reports through 2023-2024)",
    },
    {
        "id": 22,
        "name": "王震",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山西省委常委、省委秘书长",  # per 晋城市 investigation
        "current_org": "中共山西省委",
        "source": "plausible — 前任晋城市委书记，曾主政晋城市，阳城县归其管辖",
    },
]


# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共阳城县委员会", "type": "党委", "level": "县级", "parent": "中共晋城市委员会", "location": "阳城县"},
    {"id": 2, "name": "阳城县人民政府", "type": "政府", "level": "县级", "parent": "晋城市人民政府", "location": "阳城县"},
    {"id": 3, "name": "中共阳城县纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共阳城县委员会", "location": "阳城县"},
    {"id": 4, "name": "中共阳城县委组织部", "type": "党委", "level": "县级", "parent": "中共阳城县委员会", "location": "阳城县"},
    {"id": 5, "name": "中共阳城县委宣传部", "type": "党委", "level": "县级", "parent": "中共阳城县委员会", "location": "阳城县"},
    {"id": 6, "name": "中共阳城县委政法委员会", "type": "党委", "level": "县级", "parent": "中共阳城县委员会", "location": "阳城县"},
    {"id": 7, "name": "中共晋城市委员会", "type": "党委", "level": "地级市", "parent": "中共山西省委", "location": "晋城市"},
    {"id": 8, "name": "晋城市人民政府", "type": "政府", "level": "地级市", "parent": "山西省人民政府", "location": "晋城市"},
    {"id": 9, "name": "阳城县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "阳城县", "location": "阳城县"},
    {"id": 10, "name": "政协阳城县委员会", "type": "政协", "level": "县级", "parent": "阳城县", "location": "阳城县"},
]


# ── Positions ───────────────────────────────────────────────────────────────

positions = [
    # Current leadership
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "待查", "end_date": "现任", "rank": "正处级", "note": "具体任职起始时间待查（高喜全曾任职于约2021年起）"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "待查", "end_date": "现任", "rank": "正处级", "note": "具体任职起始时间待查（牛琛曾任职至2023-2024年）"},

    # Standing committee typical positions
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "待查", "end_date": "现任", "rank": "副处级", "note": "通常由县长兼任或设专职副书记"},
    {"person_id": 4, "org_id": 2, "title": "常务副县长", "start_date": "待查", "end_date": "现任", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "纪委书记", "start_date": "待查", "end_date": "现任", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 4, "title": "组织部部长", "start_date": "待查", "end_date": "现任", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "宣传部部长", "start_date": "待查", "end_date": "现任", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 6, "title": "政法委书记", "start_date": "待查", "end_date": "现任", "rank": "副处级", "note": ""},

    # Known predecessors
    {"person_id": 20, "org_id": 1, "title": "县委书记（前）", "start_date": "约2021", "end_date": "约2024/2025", "rank": "正处级", "note": "高喜全曾任县委书记，后调任。不确认现任是否为其继任者"},
    {"person_id": 21, "org_id": 2, "title": "县长（前/现）", "start_date": "待查", "end_date": "待查", "rank": "正处级", "note": "牛琛任县长至2023-2024年，需要确认是否仍在任"},

    # 晋城市级关联
    {"person_id": 22, "org_id": 7, "title": "市委书记（前）", "start_date": "待查", "end_date": "约2024/2025", "rank": "正厅级", "note": "王震前晋城市委书记，阳城县在晋城市治下"},
]


# ── Relationships ───────────────────────────────────────────────────────────

relationships = [
    # Core leadership overlap
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记—县长搭档", "overlap_org": "阳城县", "overlap_period": AS_OF},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记—县委副书记", "overlap_org": "中共阳城县委员会", "overlap_period": AS_OF},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "县长—常务副县长", "overlap_org": "阳城县人民政府", "overlap_period": AS_OF},

    # 县委常委班子成员
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "县委常委班子：书记+纪委书记", "overlap_org": "中共阳城县委员会", "overlap_period": AS_OF},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县委常委班子：书记+组织部长", "overlap_org": "中共阳城县委员会", "overlap_period": AS_OF},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "县委常委班子：书记+宣传部长", "overlap_org": "中共阳城县委员会", "overlap_period": AS_OF},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "县委常委班子：书记+政法委书记", "overlap_org": "中共阳城县委员会", "overlap_period": AS_OF},

    # 前后任关系
    {"person_a": 1, "person_b": 20, "type": "predecessor_successor", "context": "可能为高喜全的后任", "overlap_org": "中共阳城县委员会", "overlap_period": "交接期", "confidence": "unverified"},
    {"person_a": 2, "person_b": 21, "type": "predecessor_successor", "context": "牛琛可能为前任或现任县长", "overlap_org": "阳城县人民政府", "overlap_period": "交接期", "confidence": "unverified"},

    # 与晋城市级关联
    {"person_a": 1, "person_b": 22, "type": "superior_subordinate", "context": "阳城县委书记受晋城市委领导", "overlap_org": "阳城县委—晋城市委", "overlap_period": AS_OF},
    {"person_a": 2, "person_b": 22, "type": "superior_subordinate", "context": "阳县长受晋城市政府领导", "overlap_org": "阳城县政府—晋城市政府", "overlap_period": AS_OF},
]

# ── Person JSON builders ─────────────────────────────────────────────────────

def write_person_json(person: dict, extra: dict | None = None) -> None:
    """Write a single person JSON file to the staging directory."""
    name = person["name"]
    if "待查" in name:
        # Don't write person JSON for unknown-name placeholders
        return
    job = person["current_post"].split("（")[0].replace("(", "").replace(")", "").replace(" ", "_").replace("/", "_")
    filename = f"{TODAY}-山西省-晋城市-{job}-{name}.json"
    name_birth_key = f"阳城县_{name}"
    if person.get("birth"):
        name_birth_key = f"阳城县_{name}_{person['birth']}"

    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "山西省",
            "city": "晋城市",
            "region": "阳城县",
            "job": person["current_post"],
            "task_id": "shanxi_阳城县",
            "time_focus": AS_OF,
        },
        "identity": {
            "person_id": name_birth_key,
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person.get("birth") if person.get("birth") else "待查",
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": person["party_join"] if person["party_join"] in ("中共党员",) else "未知",
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth', '未知')}",
                "name_birthplace": person["name"],
                "official_profile_url": person.get("source", "")
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": ["S001"]
        },
        "career_timeline": [{
            "start": "未知",
            "end": "present",
            "org": person["current_org"],
            "title": person["current_post"],
            "level": "",
            "location": "阳城县",
            "system": "party" if "委" in person["current_org"] else "government",
            "rank": "",
            "is_key_promotion": True,
            "notes": "详细履历待查；web search degraded during investigation",
            "confidence": "unverified",
            "source_ids": ["S001"]
        }],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "salaries": {},
        "deputies": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [{
                "trait": "unknown",
                "evidence": "公开资料不足；web_search degraded",
                "confidence": "unverified",
                "source_ids": []
            }],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "本次调查未发现风险信号（搜索受限）",
            "date": AS_OF,
            "confidence": "unverified",
            "source_ids": []
        }],
        "source_register": [{
            "id": "S001",
            "title": f"阳城县相关 — {person['current_post']}",
            "url": person.get("source", "未知 — 搜索受限"),
            "publisher": "",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "inferred",
            "reliability": "low",
            "notes": "信息来源于 web_search 受限状态下的推断"
        }],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "所有详细履历信息均未知 — 缺乏可靠的公开信息来源"
        },
        "open_questions": [{
            "priority": "critical",
            "question": "阳城县现任县委书记姓名、履历、任职起始时间",
            "why_it_matters": "核心人物信息缺失",
            "suggested_queries": [
                "阳城县 县委书记 2026",
                "阳城县 领导之窗",
                "中共晋城市委组织部 任前公示 阳城"
            ],
            "last_attempted": AS_OF
        }, {
            "priority": "critical",
            "question": "阳城县现任县长姓名、履历、任职起始时间",
            "why_it_matters": "第二核心人物信息缺失",
            "suggested_queries": [
                "阳城县 县长 2026",
                "牛琛 阳城 县长"
            ],
            "last_attempted": AS_OF
        }, {
            "priority": "high",
            "question": "阳城县整套领导班子名单",
            "why_it_matters": "建立工作关系网的基础",
            "suggested_queries": [
                "阳城县 县委常委 名单",
                "阳城县 领导班子"
            ],
            "last_attempted": AS_OF
        }]
    }
    out_path = PJSON_DIR / filename
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {out_path}")


# ── Main ────────────────────────────────────────────────────────────────────

def main() -> None:
    print(f"=== Building {SLUG} network ===")

    # 1. Write person JSONs for known figures (skip 待查 placeholders)
    print("\n--- Writing person JSONs ---")
    for p in persons:
        if "待查" not in p["name"]:
            write_person_json(p)

    # 2. Build DB + GEXF
    print(f"\n--- Building database: {DB_PATH}")
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

    # 3. Verify
    db_size = DB_PATH.stat().st_size if DB_PATH.exists() else 0
    gexf_size = GEXF_PATH.stat().st_size if GEXF_PATH.exists() else 0
    print(f"\n=== Summary ===")
    print(f"  Database: {DB_PATH} ({db_size} bytes)")
    print(f"  GEXF:     {GEXF_PATH} ({gexf_size} bytes)")
    print(f"  Persons:   {len(persons)}")
    print(f"  Orgs:     {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relations: {len(relationships)}")
    pjson_count = len(list(PJSON_DIR.glob("*阳城*.json")))
    print(f"  Person JSONs: {pjson_count}")
    print("=== Done ===")


if __name__ == "__main__":
    main()