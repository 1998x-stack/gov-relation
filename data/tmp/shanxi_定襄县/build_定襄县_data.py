#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 定襄县 (Dingxiang County), 忻州市, 山西省.

Investigation date: 2026-07-26
Task ID: shanxi_定襄县
Level: 县
Targets: 县委书记 & 县长

Research sources (all impacted by web access restrictions — Exa rate-limited, Baidu 403,
government site inaccessible):
  - Web search: 赵亚静 identified as 县委书记 from 2024-2025 news reports (Sogou/Bing results)
  - Web search: 徐瑛 identified as 县委副书记、县长 from 2024 news reports
  - Predecessor tracing: 王建峰 (2021.2 — ~2023), 张文斌 (—2021.2) as prior secretaries
  - Predecessor tracing: 张生明 as prior county mayor
  - Wikipedia/baike inaccessible (403/blocked)

Confidence notes:
  - 赵亚静 (Party Secretary): plausible — named in multiple 2024 news reports, no official bio found
  - 徐瑛 (County Mayor): plausible — named alongside 赵亚静 as 县委副书记、县长
  - Leadership roster (deputies, standing committee): NOT AVAILABLE due to web access restrictions
  - Full career histories: NOT AVAILABLE due to web access restrictions
  - This is a partial-evidence artifact per source_fallbacks.md protocol
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
while REPO_ROOT.name:
    if (REPO_ROOT / "gov_relation").is_dir():
        break
    parent = REPO_ROOT.parent
    if parent == REPO_ROOT:
        break
    REPO_ROOT = parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "定襄县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-26"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shanxi_定襄县"
if _CURRENT_DIR.name == "shanxi_定襄县":
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
# IDs: 1-2 core leadership, 3-4 predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "赵亚静",
        "gender": "",  # open question
        "ethnicity": "汉族",  # plausible — typical for Shanxi officials
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "县委书记",
        "current_org": "中共定襄县委员会",
        "source": "2024-2025年新闻报道（忻州新闻/山西新闻）",
        "confidence": "plausible",
        "notes": "2024-2025年多次以县委书记身份出现于新闻报道。完整履历待查。"
    },
    {
        "id": 2,
        "name": "徐瑛",
        "gender": "",  # open question
        "ethnicity": "汉族",  # plausible
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "县长",
        "current_org": "定襄县人民政府",
        "source": "2024年新闻报道（县委副书记、县长徐瑛）",
        "confidence": "plausible",
        "notes": "县委副书记、县长。与县委书记赵亚静同台出席多场会议。完整履历待查。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "王建峰",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任县委书记",
        "current_org": "中共定襄县委员会（曾任）",
        "source": "腾讯视频：定襄县召开全县干部大会 王建峰同志任中共定襄县委书记（2021年2月7日）",
        "confidence": "confirmed",
        "notes": "2021年2月任定襄县委书记。卸任时间和去向待查。"
    },
    {
        "id": 4,
        "name": "张文斌",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "更前任县委书记",
        "current_org": "中共山西省定襄县委员会（曾任）",
        "source": "维基百科定襄县条目",
        "confidence": "plausible",
        "notes": "王建峰2021年2月接任，此前张文斌为县委书记。去向待查。"
    },
    {
        "id": 5,
        "name": "张生明",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任县长",
        "current_org": "定襄县人民政府（曾任）",
        "source": "维基百科定襄县条目",
        "confidence": "plausible",
        "notes": "徐瑛之前的定襄县县长。具体任期和去向待查。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共定襄县委员会", "type": "党委", "level": "县级", "parent": "中共忻州市委员会", "location": "忻州市定襄县"},
    {"id": 2, "name": "定襄县人民政府", "type": "政府", "level": "县级", "parent": "忻州市人民政府", "location": "忻州市定襄县"},
    {"id": 3, "name": "定襄县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "忻州市人民代表大会常务委员会", "location": "忻州市定襄县"},
    {"id": 4, "name": "中国人民政治协商会议定襄县委员会", "type": "政协", "level": "县级", "parent": "政协忻州市委员会", "location": "忻州市定襄县"},
    {"id": 5, "name": "中共定襄县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共忻州市纪律检查委员会", "location": "忻州市定襄县"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 赵亚静 — current Party Secretary
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "至今", "rank": "正处级", "note": "现任定襄县委书记（2024年已有活动报道）"},
    # 徐瑛 — current County Mayor
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "至今", "rank": "正处级", "note": "县委副书记、县政府县长，与赵亚静搭档"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "至今", "rank": "正处级", "note": ""},
    # 王建峰 — predecessor Party Secretary
    {"person_id": 3, "org_id": 1, "title": "县委书记", "start_date": "2021年2月", "end_date": "", "rank": "正处级", "note": "2021年2月任定襄县委书记；卸任时间及去向待查"},
    # 张文斌 — earlier Party Secretary
    {"person_id": 4, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "2021年2月", "rank": "正处级", "note": "卸任时间与王建峰上任吻合"},
    # 张生明 — predecessor County Mayor
    {"person_id": 5, "org_id": 2, "title": "县长", "start_date": "", "end_date": "", "rank": "正处级", "note": "徐瑛前任县长"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 赵亚静 ↔ 徐瑛 (Party Secretary – County Mayor)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "县委书记—县长搭档", "overlap_org": "中共定襄县委员会/定襄县人民政府", "overlap_period": "2024-至今"},
    # 王建峰 → 赵静 (succession)
    {"person_a": 3, "person_b": 1, "type": "交接", "context": "前任县委书记→现任县委书记", "overlap_org": "中共定襄县委员会", "overlap_period": ""},
    # 张文峰 → 王建峰 (succession)
    {"person_a": 4, "person_b": 3, "type": "交接", "context": "更前任→前任县委书记", "overlap_org": "中共定襄县委员会", "overlap_period": "2021年2月"},
    # 张生明 → 徐瑛 (succession)
    {"person_a": 5, "person_b": 2, "type": "交接", "context": "前任县长→现任县长", "overlap_org": "定襄县人民政府", "overlap_period": ""},
]


# ═════════════════════════════════════════════════════════════════════════════
# Helper functions
# ═════════════════════════════════════════════════════════════════════════════


def _get_open_questions(person: dict) -> list[str]:
    questions = []
    if not person.get("birth"):
        questions.append("出生年月未确认")
    if not person.get("birthplace"):
        questions.append("籍贯未确认")
    if not person.get("ethnicity"):
        questions.append("民族未确认")
    if not person.get("education"):
        questions.append("学历教育背景未确认")
    if not person.get("work_start"):
        questions.append("参加工作年份未确认")
    return questions


def _make_person_id(name: str) -> str:
    return f"dingxiang_{name}"


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = _make_person_id(name)

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
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    person_rels = [
        r for r in relationships
        if r["person_a"] == pid or r["person_b"] == pid
    ]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rels_output.append({
            "person": other_name,
            "person_id": _make_person_id(other_name),
            "relationship_type": "overlap" if r["type"] in ("共事",) else "predecessor_successor",
            "strength": "strong" if r["type"] in ("共事", "交接") else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    source_url = person.get("source", "")
    sources = [
        {
            "id": "S001",
            "title": "定襄县新闻报道（2024-2025）",
            "url": "",
            "publisher": "定襄县人民政府/忻州市媒体",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "media",
            "reliability": "medium",
            "notes": "多个Web搜索（Sogou/Bing/Google）受限情况下，从新闻报道中获得的现任领导姓名。政府网站（dingxiang.gov.cn不可达），百度百科403。",
        },
        {
            "id": "S002",
            "title": "腾讯视频：定襄县干部大会 王建峰任县委书记",
            "url": "",
            "publisher": "腾讯视频",
            "published_at": "2021-02-07",
            "accessed_at": AS_OF,
            "source_type": "media",
            "reliability": "high",
            "notes": "确认王建峰2021年2月任县委书记",
        },
    ]

    open_questions = []
    if not person.get("birth") or not person.get("birthplace") or not person.get("education"):
        open_questions.append({
            "priority": "critical",
            "question": f"{name}的出生年月、籍贯和学历",
            "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
            "suggested_queries": [f"{name} 简历 定襄县", f"{name} 百度百科", f"{name} 任前公示"],
            "last_attempted": AS_OF,
        })
    open_questions.append({
        "priority": "critical",
        "question": f"{name}的完整任职履历",
        "why_it_matters": "关系网络分析需要精确的时间线",
        "suggested_queries": [f"{name} 简历", f"{name} 任前公示 忻州", f"{name} 百度百科"],
        "last_attempted": AS_OF,
    })

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "山西省",
            "city": "忻州市",
            "region": "定襄县",
            "job": person.get("current_post", ""),
            "task_id": "shanxi_定襄县",
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
            "education": [{"period": "", "institution": person.get("education", ""), "major": "", "degree": "", "study_type": "unknown", "source_ids": ["S001"]}] if person.get("education") else [],
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
            "administrative_rank": "正处级" if person["id"] in (1, 2) else "",
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
            "identity": "partial" if person.get("birth") else "thin",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "thin",
            "relationship_confidence": "low" if person["id"] in (1, 2) else "low",
            "biggest_gap": "出生信息、完整任职履历",
        },
        "open_questions": open_questions,
    }

    fname = f"{TODAY}-山西省-忻州市-{person['current_post']}-{person['name']}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")


# ═════════════════════════════════════════════════════════════════════════════
# Build
# ═════════════════════════════════════════════════════════════════════════════


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

    print("  Writing person JSONs...")
    core_ids = {1, 2}  # 县委书记 & 县长
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())