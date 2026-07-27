#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 吉县, 临汾市, 山西省.

Investigation date: 2026-07-26
Task ID: shanxi_吉县
Level: 县
Targets: 县委书记 & 县长

Current Status (as of 2026-07-26):
  - 县委书记: 待确认 (all government sites unreachable, all search engines blocked)
  - 县长: 待确认 (same access limitations)

Research notes:
  - www.jixian.gov.cn — timed out (unreachable)
  - baike.baidu.com — 403/blocked
  - Exa search — rate limited
  - Jina Reader — timed out
  - lin fen gov sites — all timed out
  - Google — inaccessible
  - All Chinese government websites unreachable
  - All Chinese search engines blocked

Confidence notes:
  - ALL person data is unverified — complete web blockade for Chinese government content
  - 吉县 is a county (县) under 临汾市, 山西省
  - Even officeholder names and basic demographic info are unverified in this session
  - Artifacts created in partial evidence mode with explicit uncertainty markers
"""

from __future__ import annotations

import json
import os
import sqlite3  # noqa: used by gov_relation.runner internally
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve()
for _ in range(10):
    if (REPO_ROOT / "gov_relation").is_dir():
        break
    REPO_ROOT = REPO_ROOT.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "吉县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-26"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shanxi_吉县"
if _CURRENT_DIR.name == "shanxi_吉县":
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
# IDs: 1-2 core leadership (unknown names), 3-8 typical standing committee positions
# All data is UNVERIFIED — web access completely blocked for Chinese government sites

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership — NAMES UNVERIFIED
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "待确认_县委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "吉县县委书记",
        "current_org": "中国共产党吉县委员会",
        "source": "无法访问 — 吉县政府网站(www.jixian.gov.cn)超时, 百度百科403禁止, 所有中文搜索引擎不可达",
        "confidence": "unverified",
        "notes": "因运行环境存在严重的对外网络访问限制, 2026年7月吉县县委书记姓名无法确认。山西县级书记通常3-5年轮换, 按县级惯例推测为某位正处级干部。前任可查信息见下述。"
    },
    {
        "id": 2,
        "name": "待确认_县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "吉县人民政府县长",
        "current_org": "吉县人民政府",
        "source": "无法访问 — 所有官方通道封锁",
        "confidence": "unverified",
        "notes": "2026年吉县县长姓名因网络封锁无法确认。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy/Standing Committee — ALL UNVERIFIED
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "待确认_县委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "吉县县委副书记（待确认）",
        "current_org": "中国共产党吉县委员会",
        "source": "无法访问",
        "confidence": "unverified",
        "notes": "县委副书记通常同时兼任县长或专职副书记。因网络封锁无法确认姓名和分工。"
    },
    {
        "id": 4,
        "name": "待确认_常务副县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "吉县县委常委、常务副县长（待确认）",
        "current_org": "吉县人民政府",
        "source": "无法访问",
        "confidence": "unverified",
        "notes": "常务副县长为县政府排名第二的领导, 通常同时任县委常委。"
    },
    {
        "id": 5,
        "name": "待确认_纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "吉县县委常委、纪委书记、监委主任（待确认）",
        "current_org": "中国共产党吉县纪律检查委员会",
        "source": "无法访问",
        "confidence": "unverified",
    },
    {
        "id": 6,
        "name": "待确认_组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "吉县县委常委、组织部部长（待确认）",
        "current_org": "中国共产党吉县委员会组织部",
        "source": "无法访问",
        "confidence": "unverified",
    },
    {
        "id": 7,
        "name": "待确认_宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "吉县县委常委、宣传部部长（待确认）",
        "current_org": "中国共产党吉县委员会宣传部",
        "source": "无法访问",
        "confidence": "unverified",
    },
    {
        "id": 8,
        "name": "待确认_政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "吉县县委常委、政法委书记（待确认）",
        "current_org": "中国共产党吉县委员会政法委员会",
        "source": "无法访问",
        "confidence": "unverified",
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessor figures (historical knowledge, unverifiable in session)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 101,
        "name": "待确认_前任县委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前吉县县委书记（待确认）",
        "current_org": "",
        "source": "无法访问 — 历史数据不可达",
        "confidence": "unverified",
        "notes": "吉县前任县委书记姓名、去向因网络封锁无法确认。山西县级主要领导通常任期约3-5年后进行轮换/提拔。"
    },
    {
        "id": 102,
        "name": "待确认_前任县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前吉县人民政府县长（待确认）",
        "current_org": "",
        "source": "无法访问",
        "confidence": "unverified",
        "notes": "吉县前任县长姓名无法确认。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中国共产党吉县委员会",           "type": "党委", "level": "县级", "parent": "中共临汾市委员会", "location": "山西省临汾市吉县"},
    {"id": 2, "name": "吉县人民政府",                   "type": "政府", "level": "县级", "parent": "临汾市人民政府", "location": "山西省临汾市吉县"},
    {"id": 3, "name": "吉县纪律检查委员会",             "type": "纪委", "level": "县级", "parent": "中共临汾市纪律检查委员会", "location": "山西省临汾市吉县"},
    {"id": 4, "name": "吉县人大常委会",                 "type": "人大", "level": "县级", "parent": "临汾市人大常委会", "location": "山西省临汾市吉县"},
    {"id": 5, "name": "吉县政协",                       "type": "政协", "level": "县级", "parent": "政协临汾市委员会", "location": "山西省临汾市吉县"},
    {"id": 6, "name": "中共吉县县委组织部",             "type": "党委", "level": "县级", "parent": "中共临汾市委组织部", "location": "山西省临汾市吉县"},
    {"id": 7, "name": "中共吉县县委宣传部",             "type": "党委", "level": "县级", "parent": "中共临汾市委宣传部", "location": "山西省临汾市吉县"},
    {"id": 8, "name": "中共吉县县委政法委员会",         "type": "党委", "level": "县级", "parent": "中共临汾市委政法委员会", "location": "山西省临汾市吉县"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # Current leadership (all unverified names)
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "姓名及任期因网络封锁无法确认"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "", "rank": "正处级", "note": "姓名及任期因网络封锁无法确认"},
    {"person_id": 3, "org_id": 1, "title": "县委副书记(推定)", "start_date": "", "end_date": "", "rank": "副处级", "note": "推定职位, 姓名未确认"},
    {"person_id": 4, "org_id": 2, "title": "常务副县长(推定)", "start_date": "", "end_date": "", "rank": "副处级", "note": "推定职位, 姓名未确认"},
    {"person_id": 5, "org_id": 3, "title": "纪委书记(推定)", "start_date": "", "end_date": "", "rank": "副处级", "note": "推定职位, 姓名未确认"},
    {"person_id": 6, "org_id": 6, "title": "组织部部长(推定)", "start_date": "", "end_date": "", "rank": "副处级", "note": "推定职位, 姓名未确认"},
    {"person_id": 7, "org_id": 7, "title": "宣传部部长(推定)", "start_date": "", "end_date": "", "rank": "副处级", "note": "推定职位, 姓名未确认"},
    {"person_id": 8, "org_id": 8, "title": "政法委书记(推定)", "start_date": "", "end_date": "", "rank": "副处级", "note": "推定职位, 姓名未确认"},
    # Predecessors
    {"person_id": 101, "org_id": 1, "title": "前任县委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "姓名及任期均无法确认"},
    {"person_id": 102, "org_id": 2, "title": "前任县长", "start_date": "", "end_date": "", "rank": "正处级", "note": "姓名及任期均无法确认"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # Core party-government partnership (structural — exists regardless of names)
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "吉县县委书记与县长党政搭档关系(结构推定)", "overlap_org": "吉县", "overlap_period": ""},
    {"person_a": 1, "person_b": 3, "type": "同事", "context": "县委常委会成员(结构推定)", "overlap_org": "吉县县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "县委书记与常务副县长(结构推定)", "overlap_org": "吉县", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "县委与纪委领导关系(结构推定)", "overlap_org": "吉县县委", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "县长与常务副县长(结构推定)", "overlap_org": "吉县政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 101, "type": "前后任", "context": "现任与前任县委书记(结构推定)", "overlap_org": "吉县县委", "overlap_period": ""},
    {"person_a": 2, "person_b": 102, "type": "前后任", "context": "现任与前任县长(结构推定)", "overlap_org": "吉县政府", "overlap_period": ""},
]


# ═════════════════════════════════════════════════════════════════════════════
# Helper functions
# ═════════════════════════════════════════════════════════════════════════════


def _get_open_questions(person: dict) -> list[dict]:
    """Generate open questions for a person record."""
    name_display = person["name"]
    questions = [
        {
            "priority": "critical",
            "question": f"{name_display}（吉县）的法定代表人姓名",
            "why_it_matters": "这是本次调查的核心目标——连最基本的信息都因网络封锁缺失",
            "suggested_queries": ["吉县 县委书记 2026", "吉县 县长 2026", "www.jixian.gov.cn 领导信息"],
            "last_attempted": AS_OF,
        },
        {
            "priority": "critical",
            "question": f"{name_display}的出生年月",
            "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
            "suggested_queries": [f"吉县 {name_display} 出生", f"吉县 {name_display} 简历"],
        },
    ]
    if not person.get("birthplace"):
        questions.append({
            "priority": "high",
            "question": f"吉县{person.get('current_post','领导')}的籍贯",
            "why_it_matters": "籍贯信息用于关联分析和去重",
            "suggested_queries": [f"吉县 县委书记 籍贯"],
        })
    return questions


def _make_person_id(name: str) -> str:
    return f"jixian_{name}"


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file."""
    pid = person["id"]
    name = person["name"]

    person_positions = [p for p in positions if p["person_id"] == pid]

    career_timeline = []
    for pos in person_positions:
        org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
        career_timeline.append({
            "start": pos.get("start_date", ""),
            "end": pos.get("end_date", ""),
            "org": org["name"] if org else "",
            "title": pos.get("title", ""),
            "level": pos.get("rank", ""),
            "location": "",
            "system": "party" if org and "中共" in org["name"] else "government",
            "rank": pos.get("rank", ""),
            "is_key_promotion": pid in (1, 2),
            "notes": pos.get("note", ""),
            "confidence": person.get("confidence", "unverified"),
            "source_ids": ["S001"],
        })

    # Gap for missing career
    career_timeline.insert(0, {
        "start": "未知",
        "end": "未知",
        "org": "履历缺口",
        "title": "",
        "notes": f"因网络封锁完全无法获取{name}的公开履历",
        "confidence": "unverified",
        "source_ids": [],
    })

    person_rels = [
        r for r in relationships if r["person_a"] == pid or r["person_b"] == pid
    ]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rels_output.append({
            "person": other_name,
            "person_id": _make_person_id(other_name),
            "relationship_type": "overlap",
            "strength": "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "unverified",
            "source_ids": ["S001"],
        })

    sources = [
        {
            "id": "S001",
            "title": "吉县政府网站 — 无法访问(超时)",
            "url": "https://www.jixian.gov.cn/",
            "publisher": "吉县人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "low",
            "notes": "www.jixian.gov.cn — 连接超时。百度百科 403。搜狗/百度搜索不可达。Jina Reader 超时。本会话无法获取任何中文政府网站内容。",
        },
    ]

    current_post = person.get("current_post", "")
    current_org_val = person.get("current_org", "")
    is_core = pid in (1, 2)
    admin_rank = "正处级" if is_core or "正处级" in current_post else "副处级"

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "山西省",
            "city": "临汾市",
            "region": "吉县",
            "job": current_post,
            "task_id": "shanxi_吉县",
            "time_focus": "2026年7月",
        },
        "identity": {
            "person_id": _make_person_id(name),
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
                "official_profile_url": person.get("source", ""),
            },
        },
        "current_status": {
            "current_post": current_post,
            "current_org": current_org_val,
            "administrative_rank": admin_rank,
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_output,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": ["党政管理(推定)"],
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
            "caveat": "因网络封锁无法获取任何公开信息来推断工作风格。",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": sources,
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "所有信息 — 全部对外网络访问被封锁",
        },
        "open_questions": _get_open_questions(person) + [
            {
                "priority": "critical",
                "question": "吉县2026年县委书记和县长姓名",
                "why_it_matters": "这是最基本的调查目标，但完全无法通过网络获取",
                "suggested_queries": ["吉县 领导之窗", "吉县 县委", "吉县 县政府"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "吉县县委常委会全体成员名单",
                "why_it_matters": "全面的领导班子信息",
                "suggested_queries": ["吉县 县委常委会排名", "吉县 常委分工"],
                "last_attempted": AS_OF,
            },
        ],
    }

    # Build filename using the displayed name
    safe_post = current_post.replace('/', '_').replace('（', '(').replace('）', ')')
    fname = f"{TODAY}-山西省-临汾市-{safe_post}-{person['name']}.json"
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

    # Write person JSONs for core targets (id=1,2 = 县委书记 & 县长)
    print("  Writing person JSONs...")
    core_ids = {1, 2}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())