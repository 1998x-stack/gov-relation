#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 滨州市 (Binzhou City), 山东省.

Investigation date: 2026-07-25
Task ID: shandong_滨州市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - zh.wikipedia.org/wiki/滨州市 — Chinese Wikipedia (primary, current leadership as of July 2026)
  - www.binzhou.gov.cn — 滨州市人民政府官方网站 (timeout/unreachable during research)
  - Web search was degraded: Exa rate-limited, Baidu Baike 403, Jina Reader timeouts

Confidence notes:
  - Current roles (李春田): confirmed via Wikipedia (encyclopedia source)
  - Note: 李春田 is listed as both 市委书记 (since April 2026) and 市长 (since January 2022)
    — Wikipedia shows both roles held concurrently by the same person
  - 范连生 (政协主席): confirmed, born Oct 1967, Shandong native
  - 人大常委会主任: listed as "空缺" on Wikipedia
  - Biographical details (birth exact date, education, early career): mostly unverified due to web access limitations
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
SLUG = "滨州市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shandong_滨州市"
if _CURRENT_DIR.name == "shandong_滨州市":
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
# IDs: 1-9 current party/government leaders, 10-19 standing committee, 20-29 deputy govt, 30+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "李春田",
        "gender": "男",
        "ethnicity": "汉族",  # plausible — from Wikipedia
        "birth": "1972年3月",  # from Wikipedia infobox
        "birthplace": "山东省莱阳市",  # from Wikipedia infobox
        "education": "",  # open question — unverified
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "市委书记",
        "current_org": "中共滨州市委员会",
        "source": "https://zh.wikipedia.org/wiki/%E6%BB%A8%E5%B7%9E%E5%B8%82",
        "confidence": "confirmed",
        "notes": "1972年3月出生，山东莱阳人。此前曾任市长；2026年4月任市委书记。Wikipedia同时列出为市长（2022年1月起）。"
    },
    {
        "id": 2,
        "name": "李春田",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年3月",
        "birthplace": "山东省莱阳市",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "滨州市人民政府",
        "source": "https://zh.wikipedia.org/wiki/%E6%BB%A8%E5%B7%9E%E5%B8%82",
        "confidence": "confirmed",
        "notes": "李春田同时兼任市委书记和市长（截至2026年7月Wikipedia数据）。市长就任日期：2022年1月。市人大常委会主任空缺。"
    },
    {
        "id": 3,
        "name": "范连生",
        "gender": "男",
        "ethnicity": "汉族",  # plausible
        "birth": "1967年10月",  # from Wikipedia infobox
        "birthplace": "山东省滨州市",  # from Wikipedia — 籍贯 listed as 山东滨州
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议滨州市委员会",
        "source": "https://zh.wikipedia.org/wiki/%E6%BB%A8%E5%B7%9E%E5%B8%82",
        "confidence": "confirmed",
        "notes": "1967年10月出生，山东滨州人。2022年2月就任市政协主席。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Standing Committee Members (市委常委) — names from Wikipedia leadership table
    # Note: Wikipedia only shows the top 4 leaders. Full roster is unknown.
    # ══════════════════════════════════════════════════════════════════════
    # 市人大常委会主任 — listed as "空缺" on Wikipedia; no person recorded

    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "宋永祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # open question
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "中共滨州市委员会",
        "source": "公开报道/Wikipedia",
        "confidence": "plausible",
        "notes": "前任市委书记（约2021-2026年任职）。李春田的前任。具体去向待查。"
    },
    {
        "id": 31,
        "name": "李春田",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年3月",
        "birthplace": "山东省莱阳市",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市长",
        "current_org": "滨州市人民政府",
        "source": "Wikipedia",
        "confidence": "confirmed",
        "notes": "李春田2022年1月任市长，2026年4月起兼任市委书记。前任市长信息（宋永祥之前）待查。"
    },
    {
        "id": 32,
        "name": "张光峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "中共滨州市委员会",
        "source": "EN Wikipedia (outdated listing)",
        "confidence": "plausible",
        "notes": "EN Wikipedia页面仍列出张光峰为市委书记，表明其曾长期任职，约2010年代初—2020年代。"
    },
    {
        "id": 33,
        "name": "崔洪刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市长",
        "current_org": "滨州市人民政府",
        "source": "EN Wikipedia (outdated listing)",
        "confidence": "plausible",
        "notes": "EN Wikipedia页面列出崔洪刚为市长（2010年代末期数据），显示其为张光峰时期的搭档。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共滨州市委员会", "type": "党委", "level": "地级市", "parent": "中共山东省委员会", "location": "滨州市"},
    {"id": 2, "name": "滨州市人民政府", "type": "政府", "level": "地级市", "parent": "山东省人民政府", "location": "滨州市"},
    {"id": 3, "name": "中国人民政治协商会议滨州市委员会", "type": "政协", "level": "地级市", "parent": "政协山东省委员会", "location": "滨州市"},
    {"id": 4, "name": "滨州市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "山东省人大常委会", "location": "滨州市"},
    {"id": 5, "name": "中共滨州市纪律检查委员会", "type": "党委", "level": "地级市", "parent": "中共山东省纪律检查委员会", "location": "滨州市"},
    {"id": 6, "name": "滨州市监察委员会", "type": "政府", "level": "地级市", "parent": "山东省监察委员会", "location": "滨州市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 李春田 — current Party Secretary & Mayor (dual role)
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2026-04", "end_date": "", "rank": "正厅级", "note": "现任市委书记，2026年4月起任职"},
    {"person_id": 1, "org_id": 2, "title": "市长", "start_date": "2022-01", "end_date": "", "rank": "正厅级", "note": "兼任市长，2022年1月起任职"},
    # 李春田 (person 2 is the same person as mayor role)
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "2022-01", "end_date": "", "rank": "正厅级", "note": "2022年1月起任市长"},
    # 范连生 — CPPCC Chair
    {"person_id": 3, "org_id": 3, "title": "市政协主席", "start_date": "2022-02", "end_date": "", "rank": "正厅级", "note": "2022年2月起任职"},
    # 宋永祥 — predecessor Party Secretary
    {"person_id": 30, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "2026-04", "rank": "正厅级", "note": "前任市委书记，约2021-2026年任职"},
    # 李春田 (predecessor mayor - same person, prior role)
    {"person_id": 31, "org_id": 2, "title": "市长", "start_date": "", "end_date": "", "rank": "正厅级", "note": "前任市长时期的数据"},
    # 张光峰 — earlier predecessor Party Secretary
    {"person_id": 32, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "前任市委书记，EN Wikipedia不再更新数据"},
    # 崔洪刚 — earlier predecessor Mayor
    {"person_id": 33, "org_id": 2, "title": "市长", "start_date": "", "end_date": "", "rank": "正厅级", "note": "前任市长"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 李春田 ↔ 范连生 (Party Secretary – CPPCC Chair)
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "市委书记—政协主席同届领导班子", "overlap_org": "中共滨州市委员会", "overlap_period": "2022-2026"},
    # 宋永祥 → 李春田 (predecessor-successor Party Secretary)
    {"person_a": 30, "person_b": 1, "type": "交接", "context": "前任市委书记—现任市委书记", "overlap_org": "中共滨州市委员会", "overlap_period": "2026"},
    # 张光峰 → 宋永祥 (predecessor-successor Party Secretary chain)
    {"person_a": 32, "person_b": 30, "type": "交接", "context": "前任市委书记—接任者", "overlap_org": "中共滨州市委员会", "overlap_period": ""},
    # 张光峰 ↔ 崔洪刚 (former Party Secretary – Mayor pair)
    {"person_a": 32, "person_b": 33, "type": "共事", "context": "前任搭档（市委书记—市长）", "overlap_org": "中共滨州市委员会", "overlap_period": ""},
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
    if not person.get("notes", ""):
        questions.append("完整任职履历未确认")
    return questions


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"binzhou_{name}"

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
    if len(career_timeline) <= 1 and not person.get("birth"):
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开资料不足，完整履历待查。滨州市政府网站超时无法访问，百度百科403禁止访问。",
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
        rel_type = "predecessor_successor" if r["type"] == "交接" else "overlap"
        rels_output.append({
            "person": other_name,
            "person_id": f"binzhou_{other_name}",
            "relationship_type": rel_type,
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
            "title": "维基百科 - 滨州市",
            "url": source_url,
            "publisher": "维基百科",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "encyclopedia",
            "reliability": "medium",
            "notes": "2026年7月Wikipedia数据，含现任领导信息。依赖Wikipedia作为主要来源是由于滨州市政府网站不可访问。",
        }
    ]

    # Build education list if any
    education_list = []
    if person.get("education"):
        education_list.append({
            "period": "",
            "institution": person["education"],
            "major": "",
            "degree": "",
            "study_type": "unknown",
            "source_ids": [],
        })

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "山东省",
            "city": "滨州市",
            "region": "滨州市",
            "job": person.get("current_post", ""),
            "task_id": "shandong_滨州市",
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
            "native_place": person.get("birthplace", ""),  # same as birthplace from Wikipedia
            "education": education_list,
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
            "identity": "partial" if person.get("birth") else "unverified",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "完整任职履历、学历教育背景、早期职业经历（政府网站超时，百度百科403）",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的完整任职履历（每段职务的起止时间）",
                "why_it_matters": "关系网络分析需要精确的时间线",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 百度百科"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{name}的学历教育背景和参加工作年份",
                "why_it_matters": "身份去重和职业轨迹分析",
                "suggested_queries": [f"{name} 教育背景", f"{name} 毕业院校"],
                "last_attempted": AS_OF,
            },
        ],
    }

    # Add education-specific question if empty
    if not person.get("education"):
        record["open_questions"].append({
            "priority": "high",
            "question": f"{name}的学历和专业背景",
            "why_it_matters": "专业分工分析",
            "suggested_queries": [f"{name} 学历", f"{name} 毕业"],
            "last_attempted": AS_OF,
        })

    fname = f"{TODAY}-山东省-滨州市-{person['current_post']}-{person['name']}.json"
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
    # Core leaders: 李春田(书记), 李春田(市长), 范连生, 宋永祥, 张光峰
    core_ids = {1, 2, 3, 30, 32, 33}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
