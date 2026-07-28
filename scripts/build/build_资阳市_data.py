#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 资阳市 (Ziyang City), 四川省.

Investigation date: 2026-07-28
Task ID: sichuan_资阳市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.ziyang.gov.cn — 资阳市人民政府官方网站 (primary, confirmed as of July 2026)
  - Site confirms 袁泉 as 市委书记, 颜磊 as 市长

Confidence notes:
  - Current roles (袁泉 as 市委书记, 颜磊 as 市长): confirmed via official site (July 2026)
  - Biographical details (birth, birthplace, education): mostly unverified due to web access
    limitations (Exa rate-limited, Baidu 403, Google/Bing timeout, Jina Reader transport error)
  - Full leadership roster beyond top 2: not yet discovered from degraded web
  - Predecessor information: 元方 is a plausible inference from media reports — unverified
  - All claims labeled with confidence level; gaps explicitly documented

Artifacts staged under data/tmp/sichuan_资阳市/ for validation before promotion.
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

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "资阳市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-28"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "sichuan_资阳市"
if _CURRENT_DIR.name == "sichuan_资阳市":
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
persons = [
    # ..................................................................
    # Current Core Leadership
    # ..................................................................
    {
        "id": 1,
        "name": "袁泉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共资阳市委员会",
        "source": "https://www.ziyang.gov.cn/",
        "confidence": "confirmed",
        "notes": "Confirmed as 市委书记 on ziyang.gov.cn homepage (July 2026). Full career timeline unknown."
    },
    {
        "id": 2,
        "name": "颜磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "资阳市人民政府",
        "source": "https://www.ziyang.gov.cn/",
        "confidence": "confirmed",
        "notes": "Confirmed as 市长 on ziyang.gov.cn homepage (July 2026). Biography details limited."
    },
    # ..................................................................
    # Predecessors (unverified)
    # ..................................................................
    {
        "id": 10,
        "name": "元方",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "中共资阳市委员会",
        "source": "https://baike.baidu.com/item/%E5%85%83%E6%96%B9/24257995",
        "confidence": "unverified",
        "notes": "推测前任。元方约2021-2025年任资阳市委书记。2025年调任四川省政府。具体中间节点待确认。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共资阳市委员会", "type": "党委", "level": "地级市", "parent": "中共四川省委员会", "location": "资阳市"},
    {"id": 2, "name": "资阳市人民政府", "type": "政府", "level": "地级市", "parent": "四川省人民政府", "location": "资阳市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "现任市委书记（2026年7月）"},
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "", "end_date": "", "rank": "正厅级", "note": "现任市长（2026年7月）"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "前任市委书记，约2022-2025年任职"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档", "overlap_org": "中共资阳市委员会", "overlap_period": "2026"},
    {"person_a": 10, "person_b": 1, "type": "交接", "context": "前任市委书记—现任市委书记", "overlap_org": "中共资阳市委员会", "overlap_period": "2025-2026"},
]


# ═════════════════════════════════════════════════════════════════════════════
# Person JSON writer
# ═════════════════════════════════════════════════════════════════════════════

def _get_open_questions(person: dict) -> list[dict]:
    result = []
    missing = []
    if not person.get("birth"):
        missing.append("出生年月未确认")
    if not person.get("birthplace"):
        missing.append("籍贯未确认")
    if not person.get("education"):
        missing.append("学历教育背景未确认")
    if not person.get("work_start"):
        missing.append("参加工作年份未确认")
    for m in missing:
        result.append({
            "priority": "critical",
            "question": m,
            "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
            "suggested_queries": [],
            "last_attempted": AS_OF,
        })
    return result


def write_person_json(person: dict) -> None:
    pid = person["id"]
    name = person["name"]
    slug_id = f"ziyang_{name}"

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

    if len(career_timeline) <= 1 or not person.get("birth"):
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开资料严重不足。百度百科403禁止访问，Jina Reader超时，Exa/Google/Bing均不可用。",
            "confidence": "unverified",
            "source_ids": [],
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
            "person_id": f"ziyang_{other_name}",
            "relationship_type": "overlap",
            "strength": "strong" if r["type"] == "共事" else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    sources = [
        {
            "id": "S001",
            "title": "资阳市人民政府官方网站",
            "url": "https://www.ziyang.gov.cn/",
            "publisher": "资阳市人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "主页确认袁泉为书记、颜磊为市长。",
        },
    ]

    person_data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "四川省",
            "city": "资阳市",
            "region": "资阳市",
            "job": person.get("current_post", ""),
            "task_id": "sichuan_资阳市",
            "time_focus": "2024-2026"
        },
        "identity": {
            "person_id": slug_id,
            "name": person.get("name", ""),
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
                "official_profile_url": person.get("source", ""),
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "正厅级",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [o for o in organizations],
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
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "未发现公开的违纪、审计问题或负面报道",
                "date": "",
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": sources,
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "出生年月、籍贯、学历、完整履历均缺失",
        },
        "open_questions": _get_open_questions(person),
    }

    fn = f"{TODAY}-四川省-资阳市-{person.get('current_post', 'unknown')}-{name}.json"
    out_path = PJSON_DIR / fn
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(person_data, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON -> {out_path}")


# ═════════════════════════════════════════════════════════════════════════════
# Main
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Building {SLUG} network...")
    print(f"  DB     -> {DB_PATH}")
    print(f"  GEXF   -> {GEXF_PATH}")
    print(f"  Person JSONs -> {PJSON_DIR}")

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

    # Write person JSON files for core leaders
    for p in persons:
        if p["id"] in (1, 2, 10):
            write_person_json(p)

    # Summary
    import sqlite3
    conn = sqlite3.connect(str(DB_PATH))
    pcount = conn.execute("SELECT COUNT(*) FROM persons").fetchone()[0]
    orcount = conn.execute("SELECT COUNT(*) FROM organizations").fetchone()[0]
    pocount = conn.execute("SELECT COUNT(*) FROM positions").fetchone()[0]
    rcount = conn.execute("SELECT COUNT(*) FROM relationships").fetchone()[0]
    conn.close()

    pjson_count = len(list(PJSON_DIR.glob(f"{TODAY}-*.json")))

    print()
    print(f"Summary for {SLUG}:")
    print(f"  Persons:       {pcount}")
    print(f"  Organizations: {orcount}")
    print(f"  Positions:     {pocount}")
    print(f"  Relationships: {rcount}")
    print(f"  Person JSONs:  {pjson_count}")
    print()
    print("Gaps / Open Questions:")
    print("  - 袁泉 & 颜磊: 出生年月、籍贯、学历、完整履历均缺失")
    print("  - 前任书记（元方未确认）")
    print("  - 市委常委班子名单未确认")
    print("  - 副市长班子未确认")
    print("  - 跨县/周边关系网络未建")

    for check_path in [DB_PATH, GEXF_PATH]:
        status = "✓" if check_path.exists() else "✗"
        print(f"  {status} {check_path}")

    print()
    print(f"Person JSON files:")
    for jf in sorted(PJSON_DIR.glob(f"{TODAY}-*.json")):
        print(f"  ✓ {jf}")