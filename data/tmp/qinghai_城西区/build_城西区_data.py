#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 城西区 (Chengxi District), 西宁市, 青海省.

Level: 市辖区
Province: 青海省
Parent city: 西宁市
Targets: 区委书记 (Party Secretary) & 区长 (District Mayor)
Task ID: qinghai_城西区

Research date: 2026-07-25
Official source: https://www.xnchengxi.gov.cn/ (西宁市城西区人民政府 - site unreachable during research)

Current status (as of 2026-07-25):
- 区委书记: 待查 — official site (xnchengxi.gov.cn) was unreachable throughout the investigation period
- 区长: 待查 — same source constraint

Web access status during investigation:
  - xnchengxi.gov.cn: TCP connection timeout (both HTTP and HTTPS)
  - Jina Reader (r.jina.ai): timed out for all Chinese government targets
  - Baidu Baike: HTTP 403 (blocked)
  - Exa API: rate-limited (MCP free tier exceeded)
  - Google/Bing search results via webfetch: mostly inaccessible or timed out
  - Wikipedia (both zh and en): timed out
  - Baidu search (m.baidu.com): captcha challenge

All external search was degraded; this artifact is built in "partial evidence" mode
with explicit uncertainty labels.

Confidence notes:
  - Current officeholders: UNVERIFIED — all web search attempts failed; open questions documented
  - Person identities: unknown — unable to confirm 区委书记 and 区长 names from any source
  - District metadata (location, level): confirmed from general geographic knowledge
  - Organization structure: standard 市辖区 pattern, confirmed from administrative knowledge
  - All claims labeled with confidence level; gaps explicitly documented in open_gaps.md
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
# Try to find repo root
_REPO_ROOT = None
for parent_count in range(2, 8):
    candidate = _STAGING_DIR.parents[parent_count - 1] if parent_count > 1 else _STAGING_DIR
    if (candidate / "gov_relation").is_dir() or (candidate / "scripts").is_dir():
        _REPO_ROOT = candidate
        break
if _REPO_ROOT is None:
    _REPO_ROOT = Path(__file__).resolve().parents[4]  # fallback
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "城西区"
AS_OF = "2026-07-25"
TODAY = "20260725"

STAGING_DIR = _STAGING_DIR
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING_DIR

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════
#
# NOTE: All person data is unverified due to complete web access degradation.
# The current 区委书记 and 区长 of 城西区 could not be confirmed from any source.
# Names, identities, and career histories are all open questions.
# See open_gaps.md for prioritized research gaps.
#
# This build script creates the data structure with placeholder entries for the
# known leadership positions, which should be filled once web access is restored.
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership — UNVERIFIED
    # ════════════════════════════════════════

    # 1. 区委书记 (party secretary) — Name unknown
    {
        "id": 1,
        "name": "待查_区委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共西宁市城西区委员会",
        "source": "https://www.xnchengxi.gov.cn/ (site unreachable)",
        "confidence": "unverified",
        "notes": "⚠ 姓名待查 — 因政府网站无法访问，未能确认现任区委书记姓名",
    },
    # 2. 区长 (district mayor) — Name unknown
    {
        "id": 2,
        "name": "待查_区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区长",
        "current_org": "城西区人民政府",
        "source": "https://www.xnchengxi.gov.cn/ (site unreachable)",
        "confidence": "unverified",
        "notes": "⚠ 姓名待查 — 因政府网站无法访问，未能确认现任区长姓名",
    },
    # 3. 区委副书记 (typically兼任区长 or专职副书记) — Name unknown
    {
        "id": 3,
        "name": "待查_区委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共西宁市城西区委员会",
        "source": "待查",
        "confidence": "unverified",
        "notes": "⚠ 姓名待查 — 通常由区长兼任或设专职副书记",
    },
    # 4. 区人大常委会主任 — Name unknown
    {
        "id": 4,
        "name": "待查_人大常委会主任",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "西宁市城西区人民代表大会常务委员会",
        "source": "待查",
        "confidence": "unverified",
        "notes": "⚠ 姓名待查",
    },
    # 5. 区政协主席 — Name unknown
    {
        "id": 5,
        "name": "待查_政协主席",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议西宁市城西区委员会",
        "source": "待查",
        "confidence": "unverified",
        "notes": "⚠ 姓名待查",
    },
    # 6. 区纪委书记、监委主任 — Name unknown
    {
        "id": 6,
        "name": "待查_纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、区纪委书记、区监委主任",
        "current_org": "中共西宁市城西区纪律检查委员会",
        "source": "待查",
        "confidence": "unverified",
        "notes": "⚠ 姓名待查",
    },
    # 7. 常务副区长 — Name unknown
    {
        "id": 7,
        "name": "待查_常务副区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "城西区人民政府",
        "source": "待查",
        "confidence": "unverified",
        "notes": "⚠ 姓名待查",
    },
    # 8. 区委组织部部长 — Name unknown
    {
        "id": 8,
        "name": "待查_组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共西宁市城西区委员会组织部",
        "source": "待查",
        "confidence": "unverified",
        "notes": "⚠ 姓名待查",
    },
    # 9. 区委宣传部部长 — Name unknown
    {
        "id": 9,
        "name": "待查_宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、宣传部部长",
        "current_org": "中共西宁市城西区委员会宣传部",
        "source": "待查",
        "confidence": "unverified",
        "notes": "⚠ 姓名待查",
    },
    # 10. 区委政法委书记 — Name unknown
    {
        "id": 10,
        "name": "待查_政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、政法委书记",
        "current_org": "中共西宁市城西区委员会政法委员会",
        "source": "待查",
        "confidence": "unverified",
        "notes": "⚠ 姓名待查",
    },
    # 11-15. 副区长 (deputy mayors) — Names unknown
    *[
        {
            "id": 10 + i,
            "name": f"待查_副区长{i}",
            "gender": "",
            "ethnicity": "",
            "birth": "",
            "birthplace": "",
            "education": "",
            "party_join": "",
            "work_start": "",
            "current_post": "副区长",
            "current_org": "城西区人民政府",
            "source": "待查",
            "confidence": "unverified",
            "notes": f"⚠ 第{i}位副区长姓名待查",
        }
        for i in range(1, 6)
    ],

    # 20. 前任区委书记 (predecessor) — Name unknown
    {
        "id": 20,
        "name": "待查_前任区委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任区委书记（已离任）",
        "current_org": "中共西宁市城西区委员会（已离任）",
        "source": "待查",
        "confidence": "unverified",
        "notes": "⚠ 姓名待查 — 无法确认前任区委书记姓名及去向",
    },
    # 21. 前任区长 (predecessor) — Name unknown
    {
        "id": 21,
        "name": "待查_前任区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任区长（已离任）",
        "current_org": "城西区人民政府（已离任）",
        "source": "待查",
        "confidence": "unverified",
        "notes": "⚠ 姓名待查 — 无法确认前任区长姓名及去向",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    # 党委系统
    {"id": 1, "name": "中共西宁市城西区委员会", "type": "党委", "level": "县处级", "parent": "中共西宁市委", "location": "青海省西宁市城西区"},
    {"id": 2, "name": "中共西宁市城西区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共西宁市城西区委员会", "location": "青海省西宁市城西区"},
    {"id": 3, "name": "中共西宁市城西区委员会组织部", "type": "党委", "level": "县处级", "parent": "中共西宁市城西区委员会", "location": "青海省西宁市城西区"},
    {"id": 4, "name": "中共西宁市城西区委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共西宁市城西区委员会", "location": "青海省西宁市城西区"},
    {"id": 5, "name": "中共西宁市城西区委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共西宁市城西区委员会", "location": "青海省西宁市城西区"},
    {"id": 6, "name": "中共西宁市城西区委员会统战部", "type": "党委", "level": "县处级", "parent": "中共西宁市城西区委员会", "location": "青海省西宁市城西区"},

    # 政府系统
    {"id": 10, "name": "城西区人民政府", "type": "政府", "level": "县处级", "parent": "西宁市人民政府", "location": "青海省西宁市城西区"},

    # 人大、政协
    {"id": 20, "name": "西宁市城西区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "西宁市人民代表大会常务委员会", "location": "青海省西宁市城西区"},
    {"id": 21, "name": "中国人民政治协商会议西宁市城西区委员会", "type": "政协", "level": "县处级", "parent": "中国人民政治协商会议西宁市委员会", "location": "青海省西宁市城西区"},
    {"id": 22, "name": "西宁市城西区监察委员会", "type": "政府", "level": "县处级", "parent": "中共西宁市城西区委员会", "location": "青海省西宁市城西区"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS (standard 市辖区 leadership structure)
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # Core leadership — current
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "待查", "end_date": "现任", "rank": "县处级正职", "note": ""},
    {"person_id": 2, "org_id": 10, "title": "区长", "start_date": "待查", "end_date": "现任", "rank": "县处级正职", "note": "通常兼任区委副书记"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "待查", "end_date": "现任", "rank": "县处级正职", "note": "区长一般兼任区委副书记"},
    {"person_id": 3, "org_id": 1, "title": "区委副书记（专职）", "start_date": "待查", "end_date": "现任", "rank": "县处级副职", "note": "如区长不兼任，则设专职副书记"},
    {"person_id": 4, "org_id": 20, "title": "区人大常委会主任", "start_date": "待查", "end_date": "现任", "rank": "县处级正职", "note": ""},
    {"person_id": 5, "org_id": 21, "title": "区政协主席", "start_date": "待查", "end_date": "现任", "rank": "县处级正职", "note": ""},

    # 区委常委
    {"person_id": 6, "org_id": 2, "title": "区委常委、区纪委书记、区监委主任", "start_date": "待查", "end_date": "现任", "rank": "县处级副职", "note": "兼任区监委主任"},
    {"person_id": 7, "org_id": 10, "title": "区委常委、常务副区长", "start_date": "待查", "end_date": "现任", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 3, "title": "区委常委、组织部部长", "start_date": "待查", "end_date": "现任", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 4, "title": "区委常委、宣传部部长", "start_date": "待查", "end_date": "现任", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 5, "title": "区委常委、政法委书记", "start_date": "待查", "end_date": "现任", "rank": "县处级副职", "note": ""},

    # 副区长
    {"person_id": 11, "org_id": 10, "title": "副区长", "start_date": "待查", "end_date": "现任", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 10, "title": "副区长", "start_date": "待查", "end_date": "现任", "rank": "县处级副职", "note": ""},
    {"person_id": 13, "org_id": 10, "title": "副区长", "start_date": "待查", "end_date": "现任", "rank": "县处级副职", "note": ""},
    {"person_id": 14, "org_id": 10, "title": "副区长", "start_date": "待查", "end_date": "现任", "rank": "县处级副职", "note": ""},
    {"person_id": 15, "org_id": 10, "title": "副区长", "start_date": "待查", "end_date": "现任", "rank": "县处级副职", "note": ""},

    # 前任
    {"person_id": 20, "org_id": 1, "title": "前任区委书记", "start_date": "待查", "end_date": "待查", "rank": "县处级正职", "note": "已离任"},
    {"person_id": 21, "org_id": 10, "title": "前任区长", "start_date": "待查", "end_date": "待查", "rank": "县处级正职", "note": "已离任"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════
# NOTE: No confirmed relationships. These are inferred structural relationships
# that are typical for a 市辖区 leadership team.
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # Inferred structural relationships (confidence: unverified)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "区委书记与区长党政搭档", "overlap_org": "中共西宁市城西区委员会 / 城西区人民政府", "overlap_period": "待查"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "区委书记与区委副书记", "overlap_org": "中共西宁市城西区委员会", "overlap_period": "待查"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "区长与常务副区长工作搭档", "overlap_org": "城西区人民政府", "overlap_period": "待查"},
    {"person_a": 6, "person_b": 22, "type": "overlap", "context": "纪委书记兼任监委主任", "overlap_org": "西宁市城西区监察委员会", "overlap_period": "待查"},
]

# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSON HELPER
# ══════════════════════════════════════════════════════════════════════════════

def make_person_json(person_id: int, confidence_level: str = "unverified") -> dict:
    """Generate a person graph JSON for a given person ID."""
    p = next(x for x in persons if x["id"] == person_id)
    name_for_file = p["current_post"].replace("、", "_").replace("，", "_").replace(" ", "_")
    return {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "青海省",
            "city": "西宁市",
            "region": "城西区",
            "job": p["current_post"],
            "task_id": "qinghai_城西区",
            "time_focus": "2025-2026",
        },
        "identity": {
            "person_id": f"chengxi_{name_for_file}",
            "name": p["name"],
            "aliases": [],
            "gender": p["gender"],
            "ethnicity": p["ethnicity"],
            "birth": p["birth"],
            "birthplace": p["birthplace"],
            "native_place": "",
            "education": [],
            "party_join": p["party_join"],
            "work_start": p["work_start"],
            "dedupe_keys": {
                "name_birth": "",
                "name_birthplace": "",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": "县处级正职" if person_id in (1, 2, 4, 5) else "县处级副职",
            "as_of": AS_OF,
            "is_current_confirmed": False,
            "source_ids": [],
        },
        "career_timeline": [],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "未知 — 所有网络搜索均无法访问",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "因政府网站不可达，无法获取公开信息",
        },
        "network_metrics": {
            "direct_reports": [],
            "peers": [],
            "superiors": [],
            "reported_associations_count": 0,
        },
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "因政府网站不可达，未搜索到任何风险信号",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "西宁市城西区人民政府官方网站",
                "url": "https://www.xnchengxi.gov.cn/",
                "publisher": "城西区人民政府",
                "published_at": "",
                "accessed_at": AS_OF,
                "source_type": "official",
                "reliability": "high",
                "notes": "站点在研究期间无法访问（TCP 连接超时）",
            }
        ],
        "confidence_summary": {
            "identity": confidence_level,
            "current_role": confidence_level,
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "完全无法访问政府网站，所有现任领导姓名未知",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"现任{p['current_post']}的真实姓名？",
                "why_it_matters": "这是本次调研的核心目标",
                "suggested_queries": [
                    f"西宁市城西区 {p['current_post']}",
                    f"城西区 {p['current_post']} 简历",
                    "site:xnchengxi.gov.cn 领导之窗",
                    "西宁市城西区 领导分工 2025 2026",
                ],
                "last_attempted": AS_OF,
            }
        ],
    }


def write_person_json(person_id: int):
    """Write person JSON to staging directory."""
    data = make_person_json(person_id)
    name = data["identity"]["name"]
    post = persons[person_id - 1]["current_post"]
    safe_post = post.replace("、", "_").replace("，", "_").replace("（", "_").replace("）", "_").replace(" ", "")
    filename = f"{TODAY}-青海省-西宁市-{safe_post}-{name}.json"
    filepath = PJSON_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {filepath}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print(f"\n{'='*60}")
    print(f"  Building {SLUG} network data")
    print(f"  Staging: {STAGING_DIR}")
    print(f"  As of:   {AS_OF}")
    print(f"{'='*60}\n")

    # Person JSONs
    print("Writing person JSONs...")
    person_ids_to_write = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for pid in person_ids_to_write:
        write_person_json(pid)

    # DB + GEXF
    print("Building database and graph...")
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

    print(f"\n{'='*60}")
    print(f"  Build complete.")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Person JSONs: {PJSON_DIR}")
    print(f"{'='*60}\n")

    # Summary
    print(f"  Summary:")
    print(f"    Persons:      {len(persons)}")
    print(f"    Orgs:         {len(organizations)}")
    print(f"    Positions:    {len(positions)}")
    print(f"    Relationships:{len(relationships)}")
    print(f"    Person JSONs: {len(person_ids_to_write)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
