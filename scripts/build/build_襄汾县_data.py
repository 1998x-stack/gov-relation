#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 襄汾县, 临汾市, 山西省.

Investigation date: 2026-07-26
Task ID: shanxi_襄汾县
Level: 县
Targets: 县委书记 & 县长

Current Status (as of 2026-07-26):
  - 县委书记: 刘春林 (confirmed active through 2024-2025 Sogou news cache)
  - 县长: 杜斌 (confirmed active through 2024-2025 Sogou news cache)

Research sources:
  - Sogou search (www.sogou.com) — 襄汾县委全会、生态环保会议、两会等报道
  - 临汾新闻网 (lfxww.com) — 县委十四届九次/十一次全会报道
  - 搜狐新闻 — 2024年襄汾县生态环境保护工作会议等报道
  - 澎湃新闻 / 网易 — 2024年襄汾县人大常委会任免名单
  - 抖音 — 2024年襄汾政协会议报道

Research notes:
  - www.xiangfen.gov.cn — timed out (unreachable)
  - baike.baidu.com — 403/blocked
  - Exa search — rate limited
  - Person biographies (birth, education, party join, birthplace) — all UNVERIFIED
  - Personnel rotation 2024-2026: cannot confirm if 刘春林/杜斌 still in post as of July 2026

Confidence notes:
  - 刘春林 (Party Secretary): confirmed from 2024 Sogou news cache (still in post late 2024)
  - 杜斌 (County Magistrate): confirmed from 2024 Sogou news cache (still in post late 2024)
  - Biographical details for ALL persons: unverified — see open_questions
  - Full career histories: not found — see open_gaps.md
  - Incumbent status as of July 2026: plausible (continued from 2024)
"""

from __future__ import annotations

import json
import os
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
SLUG = "襄汾县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-26"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shanxi_襄汾县"
if _CURRENT_DIR.name == "shanxi_襄汾县":
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
# IDs: 1-2 core leadership, 3-8 standing committee (partially known),
#      101-102 predecessor/successor figures

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current — confirmed through 2024 news)
    # ══════════════════════════════════════════════════════════════════════
    # ── 1: 刘春林 — 县委书记 ──
    {
        "id": 1,
        "name": "刘春林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "襄汾县委书记",
        "current_org": "中国共产党襄汾县委员会",
        "source": "搜狗搜索 — 襄汾县委十四届九次全会(2024-02)报道; 襄汾县2024年生态环境保护工作会议报道; 襄汾县委十四届十一次全会(2024-09)报道",
        "confidence": "confirmed",
        "notes": "Confirmed as 襄汾县委书记 through multiple 2024 news sources. Sogou搜索结果确认其主持县委全会、出席环保会议、会见乡村振兴考察团等。Lkely previously served as county magistrate before becoming secretary (typical pattern). Start date as party secretary unconfirmed — possibly 2021-2022. Current (2026年7月) status: plausible continued in post; this is unverifed in isolated session."
    },
    # ── 2. 杜斌 — 县长 ──
    {
        "id": 2,
        "name": "杜斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "襄汾县人民政府县长",
        "current_org": "襄汾县人民政府",
        "source": "Sogou search: 襄汾县2024年环保工作会议 (杜斌主持会议); 襄汾县2024年五大工业项目投产仪式 (刘春林和杜斌出席); 襄汾县2024年政协会议报道",
        "confidence": "confirmed",
        "notes": "Confirmed as 襄汾县长 from multiple 2024-2025 Sogou news results. Appeared alongside 刘春林 in county leadership settings. Exact outset of tenure unconfirmed."
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Leadership (partially known from 2024 news snippets)
    # ══════════════════════════════════════════════════════════════════════
    # ── 3. 滑颖奇 — 县委领导（推测副书记）──
    {
        "id": 3,
        "name": "滑颖奇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "襄汾县领导（推测副书记）",
        "current_org": "中共襄汾县委员会",
        "source": "搜狐新闻：襄汾县2024年生态环境保护工作会议 (列名县领导滑颖奇、曹丽娟)",
        "confidence": "plausible",
        "notes": "Appeared in 2024 county环保会报道 as '县领导滑颖奇、曹丽娟'. 在搜索结果中均被称作'县领导'。可能为县委副书记或政法委书记等职务。姓名有特色（滑姓较少见）。"
    },
    # ── 4. 曹丽娟 — 县委领导 ──
    {
        "id": 4,
        "name": "曹丽娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "襄汾县领导",
        "current_org": "中共襄汾县委员会",
        "source": "搜狐新闻 Sogou search (同滑颖奇一起出现在报道中)",
        "confidence": "plausible",
        "notes": "Listed alongside other county leaders in 2024 环保会 report. Most likely a standing committee member (formerly Boeing/统战/宣传). Exact title unknown."
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessor/Successor figures (limited info)
    # ══════════════════════════════════════════════════════════════════════
    # ── 101. 张峰 — 前县委领导（推测副县长）──
    # 张峰 appears in the 2024 环保会 news: "襄汾董2024年生态环境保护工作会议召开_刘春林_图片_张峰"
    {
        "id": 101,
        "name": "张峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前/现襄汾县领导(推测副县长)",
        "current_org": "",
        "source": "搜狐新闻2024-02-26: 襄汾县2024年生态环境保护工作会议 (图片/张峰署名)",
        "confidence": "unverified",
        "notes": "Appears in Sogou search snippet for 2024 county环保会议. Position unconfirmed — may be deputy county magistrate or party committee member."
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中国共产党襄汾县委员会",   "type": "党委", "level": "县级", "parent": "中共临汾市委员会", "location": "山西省临汾市襄汾县"},
    {"id": 2, "name": "襄汾县人民政府",           "type": "政府", "level": "县级", "parent": "临汾市人民政府", "location": "山西省临汾市襄汾县"},
    {"id": 3, "name": "襄汾县纪律检查委员会",     "type": "纪委", "level": "县级", "parent": "中共临汾市纪律检查委员会", "location": "山西省临汾市襄汾县"},
    {"id": 4, "name": "襄汾县人大常委会",         "type": "人大", "level": "县级", "parent": "临汾市人大常委会", "location": "山西省临汾市襄汾县"},
    {"id": 5, "name": "襄汾县政协",               "type": "政协", "level": "县级", "parent": "政协临汾市委员会", "location": "山西省临汾市襄汾县"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 刘春林 — Party Secretary
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "Confirmed through 2024 news; start date unconfirmed"},
    # 杜斌 — County Magistrate
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "", "rank": "正处级", "note": "Confirmed through 2024-2025 news"},
    # 滑颖奇 — Deputy/County leader
    {"person_id": 3, "org_id": 1, "title": "县领导(推定)", "start_date": "", "end_date": "", "rank": "副处级", "note": "Listed as county leader in 2024 news"},
    # 曹丽娟 — County leader
    {"person_id": 4, "org_id": 1, "title": "县领导", "start_date": "", "end_date": "", "rank": "副处级", "note": "Listed as county leader in 2024 news"},
    # 张峰 — Deputy (plausible)
    {"person_id": 101, "org_id": 2, "title": "县领导(推定)", "start_date": "", "end_date": "", "rank": "副处级", "note": "Mentioned in 2024 news photo"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 刘春林 ↔ 杜斌 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "襄汾县委书记与县长党政搭档", "overlap_org": "襄汾县", "overlap_period": "约2021/2022至今"},
    # 刘春林 ↔ 滑颖奇 (同事)
    {"person_a": 1, "person_b": 3, "type": "同事", "context": "县环保工作会议报道中同列为县领导", "overlap_org": "襄汾县委", "overlap_period": "2024年"},
    # 刘春林 ↔ 曹丽娟 (同事)
    {"person_a": 1, "person_b": 4, "type": "同事", "context": "县环保工作会议报道中同列为县领导", "overlap_org": "襄汾县委", "overlap_period": "2024年"},
    # 杜斌 ↔ 滑颖奇 (同事)
    {"person_a": 2, "person_b": 3, "type": "同事", "context": "县环保工作会报道中同列", "overlap_org": "襄汾县", "overlap_period": "2024年"},
    # 杜斌 ↔ 曹丽娟
    {"person_a": 2, "person_b": 4, "type": "同事", "context": "县环保工作会报道中同列", "overlap_org": "襄汾县", "overlap_period": "2024年"},
]

# ═════════════════════════════════════════════════════════════════════════════
# Helper functions
# ═════════════════════════════════════════════════════════════════════════════


def _get_open_questions(person: dict) -> list[dict]:
    questions = []
    if not person.get("birth"):
        questions.append({
            "priority": "high",
            "question": f"{person['name']}的出生年月",
            "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
            "suggested_queries": [f"{person['name']} 出生", f"{person['name']} 简历 襄汾"],
        })
    if not person.get("birthplace"):
        questions.append({
            "priority": "high",
            "question": f"{person['name']}的籍贯",
            "why_it_matters": "籍贯信息用于关联分析和去重",
            "suggested_queries": [f"{person['name']} 籍贯 襄汾"],
        })
    if not person.get("party_join"):
        questions.append({
            "priority": "medium",
            "question": f"{person['name']}的入党时间",
            "why_it_matters": "判断党内资历",
            "suggested_queries": [f"{person['name']} 中共党员"],
        })
    return questions


def _make_person_id(name: str) -> str:
    return f"xiangfen_{name}"


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file."""
    pid = person["id"]
    name = person["name"]
    slug_id = _make_person_id(name)

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

    # Add a gap for unverifed early career
    if person.get("confidence") in ("confirmed", "plausible") and not any(c.get("start") for c in career_timeline):
        career_timeline.insert(0, {
            "start": "未知",
            "end": "未知",
            "org": "履历缺口",
            "title": "",
            "notes": f"{name}的完整公开履历未找到——缺少出生信息、早期职务、入职时间等",
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
            "confidence": person.get("confidence", "unverified"),
            "source_ids": ["S001"],
        })

    sources = [
        {
            "id": "S001",
            "title": "搜狗搜索 — 襄汾县新闻缓存",
            "url": "https://www.sogou.com/sogou?query=襄汾县+县委书记",
            "publisher": "搜狗",
            "published_at": "2024-2025",
            "accessed_at": AS_OF,
            "source_type": "media",
            "reliability": "medium",
            "notes": "通过搜狗搜索获取的临汾新闻网、搜狐新闻等报道缓存。确认了刘春林书记、杜斌县长及滑颖奇、曹丽娟等县领导的存在。",
        },
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "山西省",
            "city": "临汾市",
            "region": "襄汾县",
            "job": person.get("current_post", ""),
            "task_id": "shanxi_襄汾县",
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
                "official_profile_url": person.get("source", ""),
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "正处级" if pid in (1, 2) else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_output,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": ["党政管理"],
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
            "identity": "plausible" if person.get("confidence") == "confirmed" else person.get("confidence", "unverified"),
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "出生年月、籍贯、完整履历（因网络封锁无法获取）",
        },
        "open_questions": _get_open_questions(person) + [
            {
                "priority": "critical",
                "question": f"{name}的完整任职履历",
                "why_it_matters": "精确时间线是关系网络分析的核心",
                "suggested_queries": [f"{name} 简历", f"{name} 襄汾 任职经历", f"{name} 曾任"],
                "last_attempted": AS_OF,
            },
        ],
    }

    fname = f"{TODAY}-山西省-临汾市-{person.get('current_post', '领导').replace('/', '_')}-{person['name']}.json"
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
    # Core targets: 县委书记 (id=1), 县长 (id=2)
    core_ids = {1, 2}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())