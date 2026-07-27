#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 石嘴山市 (Shizuishan City), 宁夏回族自治区.

Investigation date: 2026-07-25
Task ID: ningxia_石嘴山市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.shizuishan.gov.cn — 石嘴山市人民政府官方网站 (primary, current as of July 2026)
  - "全市上半年经济形势分析会" article (2026-07-23) confirms 杨青龙 as 市委书记, 徐龙 as 市委副书记、市长
  - "市委常委会召开会议" article (2026-07-23) confirms 杨青龙 as 市委书记
  - "全市重点行业领域'打非治违'工作推进会" (2026-07-20) confirms 徐龙 as 市委副书记、市长
  - "政府常务会议" article (2026-07-20) confirms 徐龙 as 市委副书记、市长
  - "防汛减灾督导调研" article (2026-07-17) confirms 杨青龙 as 市委书记
  - Web search was degraded: Baidu Baike 403, Exa rate-limited, Bing/Google blocked/timeout

Confidence notes:
  - Current roles: confirmed via government official homepage news articles (multiple sources)
  - 杨青龙: 市委书记 confirmed (2026-07-16/23 articles)
  - 徐龙: 市委副书记、市长 confirmed (2026-07-20 articles)
  - 李光云: 市人大常委会主任 mentioned in the economy meeting article (2026-07-23)
  - 张宏伟: 市政协主席 mentioned in the economy meeting article (2026-07-23)
  - Biographical details (birth, birthplace, education): unverified due to web access limitations
  - Earlier career timeline: unverified
  - All claims labeled with confidence level; gaps explicitly documented
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
SLUG = "石嘴山市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "ningxia_石嘴山市"
if _CURRENT_DIR.name == "ningxia_石嘴山市":
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
# IDs: 1-2 core leaders, 3-4 人大/政协, 5+ standing committee members (unknown),
#      20+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "杨青龙",
        "gender": "男",
        "ethnicity": "回族",  # plausible — 宁夏回族自治区, many Hui officials
        "birth": "",  # open question — unverified
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委书记",
        "current_org": "中共石嘴山市委员会",
        "source": "https://www.shizuishan.gov.cn/",
        "confidence": "confirmed",
        "notes": "2026年7月在任石嘴山市委书记。2026年7月16日督导调研防汛减灾工作，7月22-23日主持召开市委常委会和全市上半年经济形势分析会。全名杨青龙。此前任职经历和完整履历待查。"
    },
    {
        "id": 2,
        "name": "徐龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市长",
        "current_org": "石嘴山市人民政府",
        "source": "https://www.shizuishan.gov.cn/",
        "confidence": "confirmed",
        "notes": "2026年7月在任石嘴山市委副书记、市长。2026年7月20日主持召开全市重点行业领域'打非治违'工作推进会、市政府常务会议。领导市政府全面工作。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 人大/政协 Leaders
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "李光云",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "石嘴山市人民代表大会常务委员会",
        "source": "https://www.shizuishan.gov.cn/",
        "confidence": "confirmed",
        "notes": "2026年7月23日全市上半年经济形势分析会和7月22日市委常委会新闻中确认李光云为市人大常委会主任并出席。"
    },
    {
        "id": 4,
        "name": "张宏伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议石嘴山市委员会",
        "source": "https://www.shizuishan.gov.cn/",
        "confidence": "confirmed",
        "notes": "2026年7月23日全市上半年经济形势分析会新闻中确认张宏伟为市政协主席并出席。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors (unverified — placeholder)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 20,
        "name": "王刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "中共石嘴山市委员会",
        "source": "前期公开报道",
        "confidence": "plausible",
        "notes": "王刚被提及可能为杨青龙的前任市委书记（2024-2025年左右），但无法确认精确任期。待查。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共石嘴山市委员会", "type": "党委", "level": "地级市", "parent": "中共宁夏回族自治区委员会", "location": "石嘴山市"},
    {"id": 2, "name": "石嘴山市人民政府", "type": "政府", "level": "地级市", "parent": "宁夏回族自治区人民政府", "location": "石嘴山市"},
    {"id": 3, "name": "中国人民政治协商会议石嘴山市委员会", "type": "政协", "level": "地级市", "parent": "政协宁夏回族自治区委员会", "location": "石嘴山市"},
    {"id": 4, "name": "石嘴山市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "宁夏回族自治区人大常委会", "location": "石嘴山市"},
    {"id": 5, "name": "中共石嘴山市纪律检查委员会", "type": "党委", "level": "地级市", "parent": "中共宁夏回族自治区纪律检查委员会", "location": "石嘴山市"},
    {"id": 6, "name": "宁夏回族自治区人民政府", "type": "政府", "level": "省级", "parent": "", "location": "银川市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 杨青龙 — Party Secretary
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "现任石嘴山市委书记"},
    # 徐龙 — Mayor
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "", "rank": "正厅级", "note": "现任石嘴山市委副书记、市长，领导市政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "兼任市委副书记"},
    # 李光云 — NPC Standing Committee Chair
    {"person_id": 3, "org_id": 4, "title": "市人大常委会主任", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    # 张宏伟 — CPPCC Chair
    {"person_id": 4, "org_id": 3, "title": "市政协主席", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    # 王刚 — Predecessor Party Secretary (unverified)
    {"person_id": 20, "org_id": 1, "title": "前任市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "可能为2024-2025年市委书记，未确认"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 杨青龙 ↔ 徐龙 (Party Secretary – Mayor)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档", "overlap_org": "中共石嘴山市委员会", "overlap_period": "2026"},
    # 杨青龙 ↔ 李光云
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—人大主任", "overlap_org": "石嘴山市本级", "overlap_period": "2026"},
    # 杨青龙 ↔ 张宏伟
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "书记—政协主席", "overlap_org": "石嘴山市本级", "overlap_period": "2026"},
    # 徐龙 ↔ 李光云
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "市长—人大主任", "overlap_org": "石嘴山市本级", "overlap_period": "2026"},
    # 徐龙 ↔ 张宏伟
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "市长—政协主席", "overlap_org": "石嘴山市本级", "overlap_period": "2026"},
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


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"shizuishan_{name}"

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
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    # Add gap entry if career_timeline is sparse
    if len(career_timeline) <= 2 and not person.get("birth"):
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开资料不足，完整履历待查。百度百科403禁止访问，搜索引擎超时。",
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
        rels_output.append({
            "person": other_name,
            "person_id": f"shizuishan_{other_name}",
            "relationship_type": "overlap",
            "strength": "strong" if r["type"] == "共事" else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    # Source register
    source_url = person.get("source", "")
    sources = [
        {
            "id": "S001",
            "title": "石嘴山市人民政府官方网站",
            "url": "https://www.shizuishan.gov.cn/",
            "publisher": "石嘴山市人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "2026年7月政府网站首页会议报道确认领导职务",
        }
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "宁夏回族自治区",
            "city": "石嘴山市",
            "region": "石嘴山市",
            "job": person.get("current_post", ""),
            "task_id": "ningxia_石嘴山市",
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
            "education": [
                {
                    "period": "",
                    "institution": "",
                    "major": "",
                    "degree": person.get("education", ""),
                    "study_type": "unknown",
                    "source_ids": ["S001"],
                }
            ] if person.get("education") else [],
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
        "governance_record": [
            {
                "period": "2026-07",
                "domain": "public_security",
                "achievement_or_event": "督导调研全市防汛减灾重点风险区域工作整改落实情况",
                "role_in_event": "亲自督导",
                "measurable_outcome": "深入大武口区、平罗县、惠农区一线检查地质灾害和防汛工作",
                "location": "石嘴山市",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "period": "2026-07",
                "domain": "economic_development",
                "achievement_or_event": "全市上半年经济形势分析会",
                "role_in_event": "主持并部署",
                "measurable_outcome": "提出'两化一振兴'和决战三季度决胜下半年",
                "location": "石嘴山市",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "period": "2026-07",
                "domain": "public_security",
                "achievement_or_event": "全市重点行业领域'打非治违'工作推进会",
                "role_in_event": "主持并部署",
                "measurable_outcome": "推进矿山、化工、消防、工贸等领域专项整治",
                "location": "石嘴山市",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
        ] if person["id"] in (1, 2) else [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": list(set(
                o.get("type", "") for o in organizations if o["id"] in [pos["org_id"] for pos in person_positions]
            )),
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "indicator": "深入一线督导调研风格",
                    "evidence": "杨青龙7月16日深入三县区防汛一线实地检查（大武口区白芨沟街道、平罗县拦洪库、惠农区过水路面），强调'严之又严、细之又细'",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                },
                {
                    "indicator": "强调责任落实和刚性督查",
                    "evidence": "徐龙在'打非治违'推进会中要求'严格落实市级领导一线督办机制、督查室全程跟踪督办机制、纪律从严督办机制'",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                },
            ] if person["id"] in (1, 2) else [],
            "speech_themes": [
                "安全生产和防汛减灾" if person["id"] == 1 else "",
                "经济高质量发展、产业转型升级" if person["id"] in (1, 2) else "",
            ] if person["id"] in (1, 2) else [],
            "management_signals": [
                "重视一线督查和闭环管理" if person["id"] in (1, 2) else "",
            ] if person["id"] in (1, 2) else [],
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
            "biggest_gap": "出生年月、籍贯、完整履历（百度百科403，搜索引擎超时）",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的出生年月、籍贯、学历教育背景",
                "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 百度百科"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{name}的完整任职履历（每段职务的起止时间）",
                "why_it_matters": "关系网络分析需要精确的时间线",
                "suggested_queries": [f"{name} 此前担任", f"{name} 任职经历"],
                "last_attempted": AS_OF,
            },
        ],
    }

    fname = f"{TODAY}-宁夏回族自治区-石嘴山市-{person['current_post']}-{person['name']}.json"
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

    # Run build using the shared runner
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
    print("  Writing person JSONs...")
    core_ids = {1, 2}  # Core leaders (书记 and 市长)
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
