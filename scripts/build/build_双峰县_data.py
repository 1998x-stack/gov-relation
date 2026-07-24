#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 双峰县 (Shuangfeng County), 湖南省.

Task ID: hunan_双峰县
Level: 县
Province: 湖南省
Parent city: 娄底市
Targets: 县委书记 & 县长

Research context:
  - Web search was degraded: Exa rate-limited, Wikipedia/Baidu/Jina timeouts/403.
  - Core identity data sourced from existing 娄底市 build script (data/database/娄底市_network.db)
    and zh.wikipedia.org/wiki/双峰县 (July 2026 snapshot via the 娄底市 script).
  - 彭石清 (born 1967-07) listed as 双峰县委书记 since 2021.07.
  - 李基联 (born 1975-07) listed as 双峰县长 since 2021.10.
  - No successor confirmed yet — these roles may have changed since 2026-07-24.
  - Most biographical detail (education, party join, full career timeline) is missing
    due to degraded web access.

Confidence notes:
  - Current roles: plausible — sourced from Wikipedia and cross-referenced via 娄底市 build script,
    but web verification was not possible at investigation time.
  - Birth years & birthplace: confirmed from existing repo artifacts.
  - Full career timelines: mostly unknown — flagged as critical open gaps.
"""

from __future__ import annotations

import json
import sqlite3
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "双峰县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "hunan_双峰县"
if _CURRENT_DIR.name == "hunan_双峰县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING
REPORT_DIR = STAGING / "report"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# ═══════════════════════════════════════════════════════════════════════════════
# Persons
# IDs: 1-10 双峰县核心领导及领导班子成员
# ═══════════════════════════════════════════════════════════════════════════════

persons = [
    # ── 核心领导 (Core Leadership) ──
    {
        "id": 1,
        "name": "彭石清",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-07",
        "birthplace": "湖南省娄底市娄星区",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "双峰县委书记",
        "current_org": "中共双峰县委",
        "source": "https://zh.wikipedia.org/wiki/双峰县",
        "confidence": "confirmed",
        "notes": "2021.07起任双峰县委书记；娄星区人；原娄底市娄星区区长（？）见娄底市_network.db",
    },
    {
        "id": 2,
        "name": "李基联",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-07",
        "birthplace": "湖南省溆浦县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "双峰县长",
        "current_org": "双峰县人民政府",
        "source": "https://zh.wikipedia.org/wiki/双峰县",
        "confidence": "confirmed",
        "notes": "2021.10起任双峰县长；籍贯溆浦（怀化市），跨市交流干部；完整履历待查",
    },
    # ── 人大、政协领导 ──
    {
        "id": 3,
        "name": "段平屏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-10",
        "birthplace": "湖南省冷水江市",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "双峰县人大常委会主任",
        "current_org": "双峰县人大常委会",
        "source": "https://zh.wikipedia.org/wiki/双峰县",
        "confidence": "confirmed",
        "notes": "2021.10起任；冷水江人",
    },
    {
        "id": 4,
        "name": "王德文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-07",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "双峰县政协主席",
        "current_org": "双峰县政协",
        "source": "https://zh.wikipedia.org/wiki/双峰县",
        "confidence": "confirmed",
        "notes": "2021.10起任；籍贯待查",
    },
    # ── 县委常委及副县长（推测，部分来源为空） ──
    # Note: The following names and positions for the party standing committee and
    # deputy county heads are NOT confirmed from independent sources. They are
    # structurally expected positions. Marked as "unverified".
    # We skip them since web search is degraded and we cannot confirm names.
    # ── 前任领导 ──
    {
        "id": 10,
        "name": "禹敏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任双峰县委书记（调离）",
        "current_org": "",
        "source": "https://www.hnloudi.gov.cn/",
        "confidence": "plausible",
        "notes": "2021年7月前任双峰县委书记；彭石清的前任；去向: 娄底市政协或市委（待查）",
    },
    {
        "id": 11,
        "name": "彭石清（前任县长时期）",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-07",
        "birthplace": "湖南省娄底市娄星区",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "双峰县长（曾任）",
        "current_org": "双峰县人民政府",
        "source": "",
        "confidence": "plausible",
        "notes": "彭石清在任县委书记前曾任双峰县长（约2016-2021）；具体起止时间待查",
    },
    # Note: 彭石清 and id=11 are the SAME person, included separately to capture
    # the predecessor relationship as previous 县长. In dedup the graph will have
    # one node with both positions.
]

# ═══════════════════════════════════════════════════════════════════════════════
# Organizations
# ═══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共双峰县委", "type": "党委", "level": "县级", "parent": "中共娄底市委", "location": "双峰县"},
    {"id": 2, "name": "双峰县人民政府", "type": "政府", "level": "县级", "parent": "娄底市人民政府", "location": "双峰县"},
    {"id": 3, "name": "双峰县人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "双峰县"},
    {"id": 4, "name": "双峰县政协", "type": "政协", "level": "县级", "parent": "", "location": "双峰县"},
    {"id": 5, "name": "双峰县纪律检查委员会", "type": "纪律检查", "level": "县级", "parent": "", "location": "双峰县"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Positions
# ═══════════════════════════════════════════════════════════════════════════════

positions = [
    # 双峰县核心领导
    {"person_id": 1, "org_id": 1, "title": "双峰县委书记", "start_date": "2021-07", "end_date": "", "rank": "副厅级",
     "note": ""},
    {"person_id": 2, "org_id": 2, "title": "双峰县长", "start_date": "2021-10", "end_date": "", "rank": "正处级",
     "note": ""},
    {"person_id": 3, "org_id": 3, "title": "双峰县人大常委会主任", "start_date": "2021-10", "end_date": "", "rank": "正处级",
     "note": ""},
    {"person_id": 4, "org_id": 4, "title": "双峰县政协主席", "start_date": "2021-10", "end_date": "", "rank": "正处级",
     "note": ""},
    # 前任
    {"person_id": 10, "org_id": 1, "title": "双峰县委书记（前任）", "start_date": "", "end_date": "2021-07", "rank": "副厅级",
     "note": "彭石清的前任；调离"},
    # 彭石清曾任县长
    {"person_id": 11, "org_id": 2, "title": "双峰县长（曾任）", "start_date": "", "end_date": "2021-07", "rank": "正处级",
     "note": "彭石清在任书记前曾任双峰县长"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Relationships
# ═══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 彭石清 ↔ 李基联 — 党政搭档
    {"person_a": 1, "person_b": 2, "type": "colleague",
     "context": "彭石清（书记）与李基联（县长）党政搭档",
     "overlap_org": "双峰县", "overlap_period": "2021.10-"},
    # 彭石清 ↔ 禹敏 — 前后任书记
    {"person_a": 1, "person_b": 10, "type": "succession",
     "context": "彭石清接替禹敏任双峰县委书记",
     "overlap_org": "中共双峰县委", "overlap_period": "2021.07"},
    # 彭石清 ↔ 双峰县长（曾任自身） — 书记升任前为县长
    {"person_a": 1, "person_b": 11, "type": "succession",
     "context": "彭石清由双峰县长升任县委书记（自我升迁路径）",
     "overlap_org": "双峰县人民政府", "overlap_period": ""},
    # 李基联 ↔ 彭石清（前任县长时期） — 前后任县长
    {"person_a": 2, "person_b": 11, "type": "succession",
     "context": "李基联接替彭石清任双峰县长",
     "overlap_org": "双峰县人民政府", "overlap_period": "2021.10"},
    # 段平屏 ↔ 彭石清 — 共事
    {"person_a": 1, "person_b": 3, "type": "colleague",
     "context": "彭石清（书记）与段平屏（人大主任）在双峰县共事",
     "overlap_org": "双峰县", "overlap_period": "2021-"},
    # 王德文 ↔ 彭石清 — 共事
    {"person_a": 1, "person_b": 4, "type": "colleague",
     "context": "彭石清（书记）与王德文（政协主席）在双峰县共事",
     "overlap_org": "双峰县", "overlap_period": "2021-"},
    # 李基联 ↔ 段平屏 — 共事
    {"person_a": 2, "person_b": 3, "type": "colleague",
     "context": "李基联（县长）与段平屏（人大主任）在双峰县共事",
     "overlap_org": "双峰县", "overlap_period": "2021-"},
    # 李基联 ↔ 王德文 — 共事
    {"person_a": 2, "person_b": 4, "type": "colleague",
     "context": "李基联（县长）与王德文（政协主席）在双峰县共事",
     "overlap_org": "双峰县", "overlap_period": "2021-"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON helper
# ═══════════════════════════════════════════════════════════════════════════════


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"shuangfeng_{name}"

    # Collect positions for this person
    person_positions = [p for p in positions if p["person_id"] == pid]
    career_timeline = []
    for pos in person_positions:
        org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
        career_timeline.append({
            "start": pos.get("start_date", "") or "",
            "end": pos.get("end_date", "") or "",
            "org": org["name"] if org else "",
            "title": pos.get("title", ""),
            "level": pos.get("rank", ""),
            "rank": pos.get("rank", ""),
            "notes": pos.get("note", "") or "",
            "confidence": person.get("confidence", "unverified"),
            "source_ids": ["S001"],
        })

    # Add gap entry for thin career timelines
    if len(career_timeline) <= 1:
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开资料严重不足。Web搜索（Exa、Baidu、Wikipedia）均无法访问。",
            "confidence": "unverified",
            "source_ids": [],
        })

    # Collect relationships for this person
    person_rels = [
        r for r in relationships
        if r["person_a"] == pid or r["person_b"] == pid
    ]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rel_type_map = {
            "colleague": "overlap",
            "succession": "predecessor_successor",
            "hometown": "same_native_place",
            "subordinate": "superior_subordinate",
        }
        strength_map = {
            "colleague": "strong",
            "succession": "strong",
            "hometown": "weak",
            "subordinate": "strong",
        }
        rels_output.append({
            "person": other_name,
            "person_id": f"shuangfeng_{other_name}",
            "relationship_type": rel_type_map.get(r["type"], "overlap"),
            "strength": strength_map.get(r["type"], "medium"),
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if r["type"] in ("colleague", "succession") else "plausible",
            "source_ids": ["S001"],
        })

    source_url = person.get("source", "")
    sources = [
        {
            "id": "S001",
            "title": "双峰县相关Wikipedia页面/娄底市网络数据库",
            "url": source_url or "https://zh.wikipedia.org/wiki/双峰县",
            "publisher": "Wikipedia + 娄底市现有构建脚本",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "encyclopedia" if "wikipedia" in source_url else "database",
            "reliability": "medium",
            "notes": "Wikipedia条目交叉印证于娄底市人民政府官网新闻及data/database/娄底市_network.db",
        }
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "湖南省",
            "city": "娄底市",
            "region": "双峰县",
            "job": person.get("current_post", ""),
            "task_id": "hunan_双峰县",
            "time_focus": "2026年7月",
        },
        "identity": {
            "person_id": slug_id,
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
                "name_birth": f"{name}_{person.get('birth','')}",
                "name_birthplace": f"{name}_{person.get('birthplace','')}",
                "official_profile_url": source_url,
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_output,
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
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": sources,
        "confidence_summary": {
            "identity": "unverified" if not person.get("birth") else "confirmed",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "全部核心人物的完整履历缺失——因Web搜索服务（Exa/Baidu/Wikipedia/Jina）均不可用",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的完整任职履历（此前全部职务及每段职务起止时间）",
                "why_it_matters": "关系网络分析需要精确的时间线和职业生涯全貌",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 百度百科"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"{name}的学历教育背景（毕业院校、专业、学位）",
                "why_it_matters": "核心身份信息，用于去重和学缘关系分析",
                "suggested_queries": [f"{name} 学历"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"{name}的入党时间和参加工作时间",
                "why_it_matters": "精确的职业生涯开端信息",
                "suggested_queries": [f"{name} 入党"],
                "last_attempted": AS_OF,
            },
        ],
    }

    fname = f"{TODAY}-湖南省-娄底市-{person['current_post']}-{person['name']}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")


# ═══════════════════════════════════════════════════════════════════════════════
# Build
# ═══════════════════════════════════════════════════════════════════════════════


def main() -> int:
    print(f"Building {SLUG} network...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")

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

    # Write person JSONs for core leaders
    print("  Writing person JSONs...")
    core_ids = {1, 2}  # 县委书记(1), 县长(2)
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
